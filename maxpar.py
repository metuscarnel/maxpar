class Task:
    name ="" #nom de la tâche
    reads=[] # domaine de lecture de la tâche
    writes=[] # domaine d'écriture de la tâche
    run=None # la fonction qui déterminera le comportement de la tâche



class TaskSystem:
    tasks= [Task()] # liste des tâches à exécuter
    precedences_map = {
        task.name: None for task in tasks
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
        print("Not implemented yet")
    def draw(self):
        print("Not implemented yet")
    def detTestRnd(self, globals):
        print("Not implemented yet")
    def parCost(self):
        print("Not implemented yet")