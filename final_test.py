import time
import random
from maxpar import Task, TaskSystem # Assurez-vous que l'import est correct

# Simulation des 5 cases mémoire (M1 à M5)
memoire = {
    "M1": 1, 
    "M2": 2, 
    "M3": 0, 
    "M4": 0, 
    "M5": 0
}

# --- FONCTIONS DES TÂCHES ---
# Chaque tâche dort 0.5s pour prouver le gain de temps
def run_t1():
    time.sleep(0.5)
    memoire["M3"] = memoire["M1"] + memoire["M2"]
    print("  [T1] M3 écrit")

def run_t2():
    time.sleep(0.5)
    memoire["M4"] = memoire["M1"] * 2
    print("  [T2] M4 écrit")

def run_t3():
    time.sleep(0.5)
    memoire["M1"] = memoire["M3"] + memoire["M4"]
    print("  [T3] M1 écrit")

def run_t4():
    time.sleep(0.5)
    memoire["M5"] = memoire["M3"] * memoire["M4"]
    print("  [T4] M5 écrit")

def run_t5():
    time.sleep(0.5)
    memoire["M2"] = memoire["M4"] + 10
    print("  [T5] M2 écrit")

def run_t6():
    time.sleep(0.5)
    memoire["M5"] = memoire["M5"] + 5  # Lecture ET écriture
    print("  [T6] M5 modifié")

def run_t7():
    time.sleep(0.5)
    memoire["M4"] = memoire["M1"] + memoire["M2"] + memoire["M4"]
    print("  [T7] M4 modifié")

def run_t8():
    time.sleep(0.5)
    memoire["M5"] = memoire["M1"] + memoire["M3"]
    print("  [T8] M5 modifié")

if __name__ == "__main__":
    # nous avons utilisé le système à l page 4 du TD3 pour les tests.
    t1 = Task("T1", ["M1", "M2"], ["M3"], run_t1)
    t2 = Task("T2", ["M1"], ["M4"], run_t2)
    t3 = Task("T3", ["M3", "M4"], ["M1"], run_t3)
    t4 = Task("T4", ["M3", "M4"], ["M5"], run_t4)
    t5 = Task("T5", ["M4"], ["M2"], run_t5)
    t6 = Task("T6", ["M5"], ["M5"], run_t6)
    t7 = Task("T7", ["M1", "M2", "M4"], ["M4"], run_t7)
    t8 = Task("T8", ["M1", "M3"], ["M5"], run_t8)
    
    tasks = [t1, t2, t3, t4, t5, t6, t7, t8]

    # 2. DÉFINITION DU GRAPHE DE PRÉCÉDENCE INITIAL (S) SELON L'IMAGE
    # On liste toutes les flèches du schéma
    precedence = {
        "T1": [],
        "T2": ["T1"],
        "T3": ["T2"],
        "T4": ["T2"],
        "T5": ["T3", "T4"],
        "T6": ["T4"],
        "T7": ["T5","T6"],
        "T8": ["T7"]
    }

    sys= TaskSystem(tasks, precedence)
    sys.is_determinated_system() # Vérification que le système est déterminé
    sys.temporary_draw_test() 
    sys.parCost()# Génération du graphe de précédence initial