class Task:
    name ="" #nom de la tâche
    reads=[] # domaine de lecture de la tâche
    writes=[] # domaine d'écriture de la tâche
    run=None # la fonction qui déterminera le comportement de la tâche



class TaskSystem:
    tasks= [Task()] # liste des tâches à exécuter
    precedences_map = {
    }
    def getDependancies(self, task_name):
        return self.precedences_map[task_name]
    def runSeq(self):
        for task in self.tasks:
            if self.precedences_map[task.name] is not None:
                for dep in self.precedences_map[task.name]:
                    dep.run()
            task.run()
    def run(self):
        print("Not implemented yet")
    def check_input(self):
        if len(self.tasks) == 0:
            raise ValueError("No tasks to execute.")
        for task in self.tasks:
            if not isinstance(task, Task):
                raise ValueError(f"Invalid task: {task}. All tasks must be instances of Task class.")
        for task, dependencies in self.precedences_map.items():
            if task not in self.tasks: #la tâche doit être dans la liste des tâches
                raise ValueError(f"Task {task} in precedence map is not in tasks list.")
            for dep in dependencies: #les dépendances doivent être dans la liste des tâches
                if dep not in self.tasks:
                    raise ValueError(f"Dependency {dep} for task {task} is not in tasks list.")
                if dep == task: #une tâche ne peut pas dépendre d'elle-même
                    raise ValueError(f"Task {task} cannot depend on itself.")
                
    def draw(self):
        print("Not implemented yet")
    def detTestRnd(self, globals):
        print("Not implemented yet")
    def parCost(self):
        print("Not implemented yet")