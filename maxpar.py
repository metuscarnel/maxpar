""" Le projet MaxPar a été réalisé en binôme par Métus Gbogbohoundada et Youssef Kassou
Le dépôt du projet est aussi disponible à cette adresse : https://github.com/metuscarnel/maxpar/tree/metus_version
 Il permet de suivre les différentes étapes de l'évolution du projet, et de voir les différentes versions du code ainsi que les difficultés rencontrées et les solutions apportées.
 Quelques références utilisées pour la réalisation du projet :
 - https://ecampus.paris-saclay.fr/course/view.php?id=172689
 - https://ecampus.paris-saclay.fr/pluginfile.php/4540864/mod_resource/content/17/sye.pdf
 - https://ecampus.paris-saclay.fr/pluginfile.php/4540861/mod_resource/content/2/se-04.pdf
 - https://ecampus.paris-saclay.fr/pluginfile.php/4540866/mod_resource/content/1/se-td3.pdf
 - https://realpython.com/python-dicts/
 - https://www.w3schools.com/python/gloss_python_class_init.asp
 - https://fr.wikipedia.org/wiki/Tri_topologique
 - https://www.enseignement.polytechnique.fr/profs/informatique/Eric.Goubault/Cours05html/poly.html
 - https://perso.eleves.ens-rennes.fr/people/julie.parreaux/fichiers_agreg/info_dev/TriTopologique.pdf
 - https://sites.google.com/site/pythonpasapas/methodes/next
 - https://graphviz.org/
 - https://www.geeksforgeeks.org/python/defaultdict-in-python/
 - https://docs.python.org/3/library/collections.html
 """
import itertools
import graphviz
import time
import threading
import random
from collections import defaultdict


class Task:
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run


class TaskSystem:
    def __init__(self, tasks=None, precedences_map=None):
        self.tasks = tasks if tasks is not None else []
        self.precedences_map = precedences_map if precedences_map is not None else {}
        for task in self.tasks:
            if task.name not in self.precedences_map:
                self.precedences_map[task.name] = []

    def check_input(self):
        if len(self.tasks) == 0:
            raise ValueError("Aucune tâche n'est définie dans le système.")
        for task in self.tasks:
            if not isinstance(task, Task):
                raise ValueError(
                    f"Tache invalide {task}. Toutes les tâches doivent être des instances de la classe Task."
                )
        for task, dependencies in self.precedences_map.items():
            task_obj = next((t for t in self.tasks if t.name == task), None)
            if task_obj is None:
                raise ValueError(
                    f"Tache {task} dans la map de précédences n'existe pas."
                )
            for dep in dependencies:
                dep_task = next((t for t in self.tasks if t.name == dep), None)
                if dep_task is None:
                    raise ValueError(
                        f"Tache {dep} dans la map de précédences n'est pas dans la liste des tâches."
                    )

    def getDependancies(self, task_name):
        dependancies = []
        for task, dependencies in self.precedences_map.items():
            if task == task_name:
                dependancies.extend(dependencies)
        return dependancies

    def _build_graph(self):
        graph = defaultdict(list)
        for task_name, dependencies in self.precedences_map.items():
            for dep in dependencies:
                graph[dep].append(task_name)
        return graph

    def topological_sort(self):
        graph = self._build_graph()
        visited = set()
        order = []

        def dfs(node):
            if node not in visited:
                visited.add(node)
                for neighbor in graph.get(node, []):
                    dfs(neighbor)
                order.append(node)

        for task_name in [t.name for t in self.tasks]:
            dfs(task_name)

        order_names = order[::-1]
        task_dict = {t.name: t for t in self.tasks}
        return [task_dict[name] for name in order_names]

    def runSeq(self):
        order = self.topological_sort()
        for task in order:
            task.run()

    @staticmethod
    def bernstein_conditions(task1, task2):
        condition1 = not set(task1.writes).intersection(set(task2.reads))
        condition2 = not set(task1.writes).intersection(set(task2.writes))
        condition3 = not set(task2.writes).intersection(set(task1.reads))
        return condition1 and condition2 and condition3

    def run(self):
        smax = self.generate_system_max()
        taches_restantes = list(smax.tasks)
        taches_terminees = set()

        while taches_restantes:
            taches_pretes = []
            for tache in taches_restantes:
                predecesseurs = smax.precedences_map.get(tache.name, [])
                if all(p in taches_terminees for p in predecesseurs):
                    taches_pretes.append(tache)

            threads = []
            for tache in taches_pretes:
                t = threading.Thread(target=tache.run)
                threads.append((tache, t))
                t.start()

            for tache, t in threads:
                t.join()
                taches_terminees.add(tache.name)
                taches_restantes.remove(tache)

    def has_path(self, graph, start, end):
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

    def is_determinated_system(self):
        dir_graph = self._build_graph()
        for task1, task2 in itertools.combinations(self.tasks, 2):
            if not self.has_path(
                dir_graph, task1.name, task2.name
            ) and not self.has_path(dir_graph, task2.name, task1.name):

                if not self.bernstein_conditions(task1, task2):
                    print(
                        f"{task1.name} et {task2.name} sont parallèles mais ne respectent pas les conditions de Bernstein. Système non déterminé."
                    )
                    return False
        return True

    def generate_system_max(self):
        if not self.is_determinated_system():
            raise ValueError(
                "Le système n'est pas déterminé. Impossible de construire le système de parallélisme maximal."
            )

        dir_graph = self._build_graph()
        smax_precedences = {task.name: [] for task in self.tasks}

        for task1, task2 in itertools.permutations(self.tasks, 2):
            if self.has_path(dir_graph, task1.name, task2.name):
                if not self.bernstein_conditions(task1, task2):
                    smax_precedences[task2.name].append(task1.name)
        smax_reduced = {k: list(v) for k, v in smax_precedences.items()}
        for task, deps in smax_precedences.items():
            for dep in deps:
                smax_reduced[task].remove(dep)
                if not self.has_path(smax_reduced, task, dep):
                    smax_reduced[task].append(dep)

        return TaskSystem(tasks=self.tasks, precedences_map=smax_reduced)

    def draw(self, filename="system_graph"):
        dot = graphviz.Digraph(comment="Graphe du système de parallélisme maximal")
        for task in self.tasks:
            dot.node(task.name)

        for task, dependencies in self.precedences_map.items():
            for dep in dependencies:
                dot.edge(dep, task)

        dot.render(filename, format="png", cleanup=True)

    def detTestRnd(self, dict_globals, nb_iterations=5):
        all_variables = set()
        for task in self.tasks:
            all_variables.update(task.reads)
            all_variables.update(task.writes)

        for i in range(nb_iterations):
            inits_values = {var: random.randint(1, 100) for var in all_variables}

            for var, value in inits_values.items():
                dict_globals[var] = value
            self.run()
            result1 = {var: dict_globals[var] for var in all_variables}

            for var, value in inits_values.items():
                dict_globals[var] = value
            self.run()
            result2 = {var: dict_globals[var] for var in all_variables}

            if result1 != result2:
                print("Le système n'est pas déterministe (Test Randomisé Échoué).")
                return False

        print("Le système est déterministe (Test Randomisé Validé).")
        return True

    def parCost(self, nb_iterations=8):
        seq_time = 0
        for _ in range(nb_iterations):
            start = time.perf_counter()
            self.runSeq()
            seq_time += time.perf_counter() - start
        moyenne_seq = seq_time / nb_iterations

        par_time = 0
        for _ in range(nb_iterations):
            start = time.perf_counter()
            self.run()
            par_time += time.perf_counter() - start
        moyenne_par = par_time / nb_iterations

        print(f"Moyenne exécution séquentielle : {moyenne_seq:.4f} secondes")
        print(f"Moyenne exécution parallèle    : {moyenne_par:.4f} secondes")

    def draw_all(self):
        self.draw("temp_graph")
        self.generate_system_max().draw("temp_graph_smax")
