import time
#from task_system import Task, TaskSystem  # Assure-toi que le nom du fichier est correct
from maxpar import Task, TaskSystem
# Simulation de données partagées
memory = {"X": 0, "Y": 0, "Z": 0}

# Fonctions avec un petit sleep pour que parCost() montre une différence
def run_t1():
    memory["X"] = 10
    print("T1 terminé")

def run_t2():
    memory["Y"] = 20
    print("T2 terminé")

def run_t3():
    memory["Z"] = memory["X"] + memory["Y"]
    print(f"T3 terminé)")

def run_t4():
    memory["X"] += 5
    print("T4 terminé")
def run_t5():
    memory["X"] *= 2
    print("T5 terminé")
def run_t6():
    memory["Y"] *= 2
    print("T6 terminé")
def run_t7():
    memory["Z"] *= 2
    print("T7 terminé")
def run_t8():
    memory["X"] -= 3
    print("T8 terminé")

if __name__ == "__main__":
    # Définition des objets Task
    t1 = Task("T1", ["X"], [], run_t1)
    t2 = Task("T2", [], ["Y"], run_t2)
    t3 = Task("T3", ["X"], ["Z"], run_t3)
    t4 = Task("T4", ["X"], [], run_t4)
    t5 = Task("T5", ["X"], [], run_t5)
    t6 = Task("T6", ["X"], [], run_t6)
    t7 = Task("T7", ["X"], [], run_t7)
    t8 = Task("T8", ["X"], [], run_t8)
    
    tasks = [t1, t2, t3, t4, t5, t6, t7, t8]

    # Précédences minimales : on laisse Bernstein faire le reste
    precedence = {
        "T2": ["T1"],
        "T3": ["T1"],
        "T4": ["T2"],
        "T5": ["T3"],
        "T7": ["T3"],
        "T8": ["T4", "T5"]
    }

    # Initialisation du système
    sys = TaskSystem(tasks, precedence)
    #sys.temporary_draw_test()
    #sys.detTestRnd(globals(), nb_iterations=3)
    # 1. Génération du PNG dans le répertoire courant
    print("--- Génération du graphe ---")
    #sys.draw("mon_graphe_execution")
    #sys.runSeq()
    sys.detTestRnd(globals(), nb_iterations=3)

    # 2. Test des performances (Séquentiel vs Parallèle)
    print("\n--- Analyse des coûts ---")
    print("Sequential execution :")
    #print(sys.topological_sort())
    #sys.runSeq()
    #sys.run()

    #3. Vérification du résultat final
    print(f"\nÉtat final de la mémoire : {memory}")