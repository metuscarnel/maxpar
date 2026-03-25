import itertools
import graphviz
import time
import threading
import random
from collections import defaultdict


class Task:
    name = ""  # nom de la tâche
    reads = []  # domaine de lecture de la tâche
    writes = []  # domaine d'écriture de la tâche
    run = None  # la fonction qui déterminera le comportement de la tâche

    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run


class TaskSystem:
    tasks = []  # liste des tâches à exécuter
    precedences_map = {} #dictionnaire donnant les contraintes de précédences entre les tâches
 
    def __init__(self, tasks=None, precedences_map=None):
        self.tasks = tasks if tasks is not None else []
        self.precedences_map = precedences_map if precedences_map is not None else {}
        # Ensure all task names have entries in precedences_map
        for task in self.tasks:
            if task.name not in self.precedences_map:
                self.precedences_map[task.name] = []

    def getDependancies(self, task_name): #recupère les dépendances d'une tâche donnée
        dependancies = []
        for task, dependencies in self.precedences_map.items():
            if task == task_name:
                dependancies.extend(dependencies)
        return dependancies

    def _build_graph(self): #construit un graphe à partir des précédences pour faciliter le tri topologique
        graph = defaultdict(list)
        for task_name, dependencies in self.precedences_map.items():
            for dep in dependencies:
                graph[dep].append(task_name)
        return graph

    def topological_sort(self): #effectue un tri topologique sur le graphe des tâches pour déterminer un ordre total d'exécution respectant les précédences
        graph = self._build_graph()
        visited = set()
        order = []

        def dfs(node):
            if node not in visited:
                visited.add(node)
                for neighbor in graph.get(node, []):
                    dfs(neighbor)
                order.append(node)

        for task_name in self.tasks:
            dfs(task_name)

        return order[::-1]

    # le tri topologique permet d'avoir un ordre total.
    def runSeq(self): #exécute les tâches dans un ordre séquentiel respectant les précédences, se sert du tri topologique pour déterminer cet ordre
        order = self.topological_sort()
        for task in order:
            task.run()

    # conditions de bersntein :
    @staticmethod #permet de vérifier si deux tâches sont indépendantes selon les conditions de Bernstein, c'est-à-dire qu'elles n'ont pas de conflits de lecture/écriture sur les mêmes variables
    def bernstein_conditions(task1, task2):
        condition1 = not set(task1.writes).intersection(set(task2.reads))
        condition2 = not set(task1.writes).intersection(set(task2.writes))
        condition3 = not set(task2.writes).intersection(set(task1.reads))
        return condition1 and condition2 and condition3

    def run(self): # execution parallèle des tâches incluant la generatiou du graphe de parallélisation maximale Smax, la détection des tâches prêtes à s'exécuter en parallèle via de threads
        # 1. On récupère le graphe optimisé Smax
        smax = self.generate_system_max()

        taches_restantes = list(smax.tasks)
        taches_terminees = set()

        # Tant qu'il reste des tâches à exécuter...
        while taches_restantes:
            taches_pretes = []

            for tache in taches_restantes:
                predecesseurs = [
                    u.name
                    for u in smax.tasks
                    if tache.name in smax.precedences_map[u.name]
                ]

                # Si tous ses prédécesseurs sont déjà terminés, elle est prête !
                if all(p in taches_terminees for p in predecesseurs):
                    taches_pretes.append(tache)
            # lancement des tâches en parallèle
            threads = []
            for tache in taches_pretes:
                print(f"Lancement de {tache.name}...")
                t = threading.Thread(target=tache.run) 
                threads.append((tache, t))
                t.start() 

            for tache, t in threads:
                t.join()  # attend que la tâche soit terminée
                taches_terminees.add(tache.name)
                taches_restantes.remove(tache)
                print(f"[{tache.name} terminée]")

    def has_path(self, graph, start, end): #fonction utilitaire pour vérifier s'il existe un chemin entre deux tâches dans le graphe des précédences, utilisée pour construire Smax
        visited = set()
        queue = [start]
        while queue:
            current = queue.pop(0)
            if current == end:
                return True
            if current not in visited:
                visited.add(current)
                queue.extend(graph.get(current, []))
        return False

    def is_determinated_system(self):#fonction qui vérifie si le système de tâches est déterminé en vérifiant que toutes les paires de tâches respectent les conditions de Bernstein
        for task1, task2 in itertools.combinations(self.tasks, 2):
            if not self.bernstein_conditions(task1, task2):
                print(
                    f"Tasks {task1.name} and {task2.name} are not independent. The system is not determinate."
                )
                return False
        print("The system is determinate.")
        return True

    def generate_system_max(self):#generation du graphe de parallélisation maximale Smax en vérifiant les conditions de Bernstein pour chaque paire de tâches et en construisant un nouveau graphe de précédences qui inclut uniquement les dépendances nécessaires pour respecter ces conditions
        if not self.is_determinated_system():
            raise ValueError("The system is not determinate. Cannot generate Smax.")
        smax_precedences_map = {task.name: [] for task in self.tasks}
        for task1, task2 in itertools.permutations(self.tasks, 2):
            if self.has_path(self.precedences_map, task1.name, task2.name):
                if self.bernstein_conditions(task1, task2):
                    smax_precedences_map[task1.name].append(task2.name)
        smax_precedecences_reduced_map = {
            k: list(v) for k, v in smax_precedences_map.items()
        }
        for task in smax_precedences_map:
            for dep in smax_precedences_map[task]:
                smax_precedecences_reduced_map[task].remove(dep)
                if not self.has_path(smax_precedecences_reduced_map, task, dep):
                    smax_precedecences_reduced_map[task].append(dep)

        Smax = TaskSystem(
            tasks=self.tasks, precedences_map=smax_precedecences_reduced_map
        )

        return Smax

    def check_input(self): #verifier la validité des entrées du système (nom des tâches, formatage des tâches, cohérence des précédences)
        if len(self.tasks) == 0:
            raise ValueError("No tasks to execute.")
        for task in self.tasks:
            if not isinstance(task, Task):
                raise ValueError(
                    f"Invalid task: {task}. All tasks must be instances of Task class."
                )
        for task_name, dependencies_names in self.precedences_map.items():
            print("Checking task: ", task_name)
            for objet in self.tasks:
                if objet.name == task_name:
                    task = objet
                    break
            else:
                raise ValueError(
                    f"Task {task_name} in precedence map is not in tasks list."
                )
            for dep_name in dependencies_names:
                print("  Checking dependency: ", dep_name)
                for objet in self.tasks:
                    if objet.name == dep_name:
                        dep = objet
                        break
                else:
                    raise ValueError(
                        f"Dependency {dep_name} for task {task_name} is not in tasks list."
                    )
                if dep_name == task_name:
                    raise ValueError(f"Task {task_name} cannot depend on itself.")
                if dep == task:  # une tâche ne peut pas dépendre d'elle-même
                    raise ValueError(f"Task {task} cannot depend on itself.")

    def draw(self, filename="max_parallelised_system"):
        dot = graphviz.Digraph(comment="Max Parallelised System : Smax")
        for task in self.tasks:
            dot.node(task.name)
        for task, dependencies in self.precedences_map.items():
            for dep in dependencies:
                dot.edge(dep, task)
        dot.render(filename, format="png", cleanup=True)

    def detTestRnd(self, globals_vars, nb_iterations=2):
        all_variables = set()
        for task in self.tasks:
            all_variables.update(task.reads)
            all_variables.update(task.writes)
        inits_values = {}
        for _ in range(nb_iterations):
            print(f"--- Iteration {_+1} ---")
            for var in all_variables:
                inits_values[var] = random.randint(0, 10)
        print(f"Initial variable values: {inits_values}")
        print("Start determinism test...")
        for var, value in inits_values.items():
            globals_vars[var] = value

        self.run()
        result1 = {var: globals_vars[var] for var in all_variables}
        for var, value in inits_values.items():
            globals_vars[var] = value
        self.run()
        result2 = {var: globals_vars[var] for var in all_variables}
        print(f"Result of first run: {result1}")
        print(f"Result of second run: {result2}")
        if result1 != result2:
            print("The system is not deterministic.")
            return False
        else:
            print("The system is deterministic.")
            return True

    def parCost(self):
        start = time.time()
        self.runSeq()
        seq_time = time.time() - start
        start = time.time()
        self.run()
        par_time = time.time() - start
        print(f"Sequential time: {seq_time:.2f} secondes")
        print(f"Parallel time: {par_time:.2f} secondes")
        print("time_difference: {:.2f} secondes".format((seq_time - par_time)))

    def temporary_draw_test(self):
        for task in self.tasks:
            print(f"Task: {task.name}, Reads: {task.reads}, Writes: {task.writes}")
            for domain in task.reads:
                print(f"  - Reads from: {domain}")
            for domain in task.writes:
                print(f"  - Writes to: {domain}")
        for task, dependencies in self.precedences_map.items():
            for dep in dependencies:
                print(f"Task {task} depends on {dep}")

        print(self.generate_system_max().precedences_map)

        print("Initial graph:")
        self.draw("temporary_initial_graph")
        print("Smax precedences map:")
        self.generate_system_max().draw("temporary_smax_graph")
