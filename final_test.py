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

def run_t1():
    time.sleep(0.5)
    memoire["M3"] = memoire["M1"] + memoire["M2"]
    print("[T1] écrit dans M3 et lit dans M1, M2")

def run_t2():
    time.sleep(0.5)
    memoire["M4"] = memoire["M1"] * 2
    print("[T2] écrit dans M4 et lit dans M1")

def run_t3():
    time.sleep(0.5)
    memoire["M1"] = memoire["M3"] + memoire["M4"]
    print("[T3] écrit dans M1 et lit dans M3, M4")

def run_t4():
    time.sleep(0.5)
    memoire["M5"] = memoire["M3"] * memoire["M4"]
    print("[T4] écrit dans M5 et lit dans M3, M4")

def run_t5():
    time.sleep(0.5)
    memoire["M2"] = memoire["M4"] + 10
    print("[T5] écrit dans M2 et lit dans M4")

def run_t6():
    time.sleep(0.5)
    memoire["M5"] = memoire["M5"] + 5  # Lecture ET écriture
    print("[T6] écrit dans M5 et lit dans M5")

def run_t7():
    time.sleep(0.5)
    memoire["M4"] = memoire["M1"] + memoire["M2"] + memoire["M4"]
    print("[T7] écrit dans M4 et lit dans M1, M2, M4")

def run_t8():
    time.sleep(0.5)
    memoire["M5"] = memoire["M1"] + memoire["M3"]
    print("[T8] écrit dans M5 et lit dans M1, M3")

if __name__ == "__main__":
    t1 = Task("T1", ["M1", "M2"], ["M3"], run_t1)
    t2 = Task("T2", ["M1"], ["M4"], run_t2)
    t3 = Task("T3", ["M3", "M4"], ["M1"], run_t3)
    t4 = Task("T4", ["M3", "M4"], ["M5"], run_t4)
    t5 = Task("T5", ["M4"], ["M2"], run_t5)
    t6 = Task("T6", ["M5"], ["M5"], run_t6)
    t7 = Task("T7", ["M1", "M2", "M4"], ["M4"], run_t7)
    t8 = Task("T8", ["M1", "M3"], ["M5"], run_t8)
    
    tasks = [t1, t2, t3, t4, t5, t6, t7, t8]

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
    #sys.runSeq() # Exécution du système de tâches