import time
from task_system import Task, TaskSystem  # Assure-toi que le nom du fichier est correct

# Simulation de données partagées
memory = {"X": 0, "Y": 0, "Z": 0}

# Fonctions avec un petit sleep pour que parCost() montre une différence
def run_t1():
    time.sleep(0.5)
    memory["X"] = 10
    print("T1 terminé")

def run_t2():
    time.sleep(0.5)
    memory["Y"] = 20
    print("T2 terminé")

def run_t3():
    time.sleep(0.5)
    memory["Z"] = memory["X"] + memory["Y"]
    print(f"T3 terminé (Z={memory['Z']})")

def run_t4():
    time.sleep(0.5)
    memory["X"] += 5
    print("T4 terminé")

if __name__ == "__main__":
    # Définition des objets Task
    t1 = Task("T1", [], ["X"], run_t1)
    t2 = Task("T2", [], ["Y"], run_t2)
    t3 = Task("T3", ["X", "Y"], ["Z"], run_t3)
    t4 = Task("T4", ["X"], ["X"], run_t4)

    tasks = [t1, t2, t3, t4]

    # Précédences minimales : on laisse Bernstein faire le reste
    precedence = {
        "T3": ["T1", "T2"]
    }

    # Initialisation du système
    sys = TaskSystem(tasks, precedence)

    # 1. Génération du PNG dans le répertoire courant
    print("--- Génération du graphe ---")
    sys.draw("mon_graphe_execution")

    # 2. Test des performances (Séquentiel vs Parallèle)
    print("\n--- Analyse des coûts ---")
    sys.parCost()

    # 3. Vérification du résultat final
    print(f"\nÉtat final de la mémoire : {memory}")