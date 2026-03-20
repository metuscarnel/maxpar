import itertools


class Task:
    name = ""  # nom de la tâche
    reads = []  # domaine de lecture de la tâche
    writes = []  # domaine d'écriture de la tâche
    run = None  # la fonction qui déterminera le comportement de la tâche


class TaskSystem:
    def __init__(self, tasks=None, precedences_map=None):
        self.tasks = tasks if tasks is not None else []
        self.precedences_map = precedences_map if precedences_map is not None else {}

    tasks = []  # liste des tâches à exécuter
    precedences_map = {}

    def getDependancies(self, task_name):
        return self.precedences_map[task_name]

    def runSeq(self):
        for task in self.tasks:
            if self.precedences_map[task.name] is not None:
                for dep in self.precedences_map[task.name]:
                    dep.run()
            task.run()

    # conditions de bersntein :
    @staticmethod
    def bernstein_conditions(task1, task2):
        condition1 = not set(task1.writes).intersection(set(task2.reads))
        condition2 = not set(task1.writes).intersection(set(task2.writes))
        condition3 = not set(task2.writes).intersection(set(task1.reads))
        return condition1 and condition2 and condition3

    def run(self):
        print("Not implemented yet")

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

    def determinated_system(self):
        for task1, task2 in itertools.combinations(self.tasks, 2):
            if not self.bernstein_conditions(task1, task2):
                print(
                    f"Tasks {task1.name} and {task2.name} are not independent. The system is not determinate."
                )
                return False
        print("The system is determinate.")
        return True

    def generate_system_max(self):
        smax_precedences_map = {task.name: [] for task in self.tasks}
        for task1, task2 in itertools.permutations(self.tasks, 2):
            if self.has_path(
                self.precedences_map, task1.name, task2.name
            ) or self.has_path(self.precedences_map, task2.name, task1.name):
                if not self.bernstein_conditions(task1, task2):
                    smax_precedences_map[task1.name].append(task2.name)
        smax_precedecences_reduced_map = {
            k: list(v) for k, v in smax_precedences_map.items()
        }
        for task in smax_precedences_map:
            for dep in smax_precedences_map[task]:
                smax_precedecences_reduced_map[task].remove(dep)
                if not self.has_path(smax_precedences_map, task, dep):
                    smax_precedecences_reduced_map[task].append(dep)

        Smax = TaskSystem()
        Smax.tasks = self.tasks
        Smax.precedences_map = smax_precedecences_reduced_map
        return Smax

    def check_input(self):
        if len(self.tasks) == 0:
            raise ValueError("No tasks to execute.")
        for task in self.tasks:
            if not isinstance(task, Task):
                raise ValueError(
                    f"Invalid task: {task}. All tasks must be instances of Task class."
                )
        for task, dependencies in self.precedences_map.items():
            if task not in self.tasks:  # la tâche doit être dans la liste des tâches
                raise ValueError(f"Task {task} in precedence map is not in tasks list.")
            for (
                dep
            ) in dependencies:  # les dépendances doivent être dans la liste des tâches
                if dep not in self.tasks:
                    raise ValueError(
                        f"Dependency {dep} for task {task} is not in tasks list."
                    )
                if dep == task:  # une tâche ne peut pas dépendre d'elle-même
                    raise ValueError(f"Task {task} cannot depend on itself.")

    def draw(self):
        print("Not implemented yet")

    def detTestRnd(self, globals):
        print("Not implemented yet")

    def parCost(self):
        print("Not implemented yet")
