from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import time
import random
from graphviz import Digraph

# --- Classe Task ---
class Task:
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run

# --- Classe TaskSystem ---
class TaskSystem:
    def __init__(self, tasks, precedence):
        self.tasks = {task.name: task for task in tasks}
        self.precedence = precedence
        self.graph = self._build_graph()
        self.add_bernstein_constraints()

    # --- Construction du graphe de dépendances ---
    def _build_graph(self):
        graph = defaultdict(list)
        for task_name, dependencies in self.precedence.items():
            for dep in dependencies:
                graph[dep].append(task_name)
        return graph

    # --- Conditions de Bernstein ---
    @staticmethod
    def bernstein_conditions(task1, task2):
        condition1 = not set(task1.writes).intersection(set(task2.reads))
        condition2 = not set(task1.writes).intersection(set(task2.writes))
        condition3 = not set(task2.writes).intersection(set(task1.reads))
        return condition1 and condition2 and condition3

    # --- Ajout des contraintes de Bernstein ---
    def add_bernstein_constraints(self):
        task_names = list(self.tasks.keys())
        for i in range(len(task_names)):
            for j in range(i + 1, len(task_names)):
                t1 = self.tasks[task_names[i]]
                t2 = self.tasks[task_names[j]]
                if not self.bernstein_conditions(t1, t2):
                    if t2.name not in self.graph.get(t1.name, []):
                        self.graph[t1.name].append(t2.name)
                    if t1.name not in self.graph.get(t2.name, []):
                        self.graph[t2.name].append(t1.name)

    # --- Tri topologique ---
    def topological_sort(self):
        visited = set()
        order = []

        def dfs(node):
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.get(node, []):
                    dfs(neighbor)
                order.append(node)

        for task_name in self.tasks:
            dfs(task_name)

        return order[::-1]

    # --- Exécution séquentielle ---
    def runSeq(self):
        order = self.topological_sort()
        for task_name in order:
            self.tasks[task_name].run()

    # --- Exécution parallèle ---
    def run(self):
        order = self.topological_sort()
        levels = self._group_by_levels(order)
        for level in levels:
            with ThreadPoolExecutor() as executor:
                for task_name in level:
                    executor.submit(self.tasks[task_name].run)

    def _group_by_levels(self, order):
        levels = []
        while order:
            current_level = []
            for task_name in order:
                dependencies = self.precedence.get(task_name, [])
                if all(dep in (current_level + [t for level in levels for t in level]) for dep in dependencies):
                    current_level.append(task_name)
            levels.append(current_level)
            order = [task for task in order if task not in current_level]
        return levels

    # --- Test de déterminisme ---
    def detTestRnd(self, globals_dict, num_tests=5):
        initial_globals = {k: globals_dict[k] for k in ['X', 'Y', 'Z'] if k in globals_dict}
        results = []
        for _ in range(num_tests):
            for var in ['X', 'Y', 'Z']:
                if var in globals_dict:
                    globals_dict[var] = random.randint(1, 100)
            self.run()
            results.append({k: globals_dict[k] for k in ['X', 'Y', 'Z'] if k in globals_dict})
        return all(result == results[0] for result in results)

    # --- Comparaison des coûts ---
    def parCost(self):
        start = time.time()
        self.runSeq()
        seq_time = time.time() - start

        start = time.time()
        self.run()
        par_time = time.time() - start

        print(f"Temps séquentiel : {seq_time:.4f} secondes")
        print(f"Temps parallèle : {par_time:.4f} secondes")

    # --- Visualisation du graphe ---
    def draw(self, filename="task_graph"):
        dot = Digraph()
        for task_name in self.tasks:
            dot.node(task_name)
            for neighbor in self.graph.get(task_name, []):
                dot.edge(task_name, neighbor)
        dot.render(filename, format="png", cleanup=True)
        print(f"Graphe enregistré sous {filename}.png")