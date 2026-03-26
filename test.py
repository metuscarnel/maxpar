import time
from maxpar import Task, TaskSystem

# Nous testons ici le système de tâche au point 4.4 du fichier des notes de cours disponible sur Ecampus
memoire = {"M1": 0, "M2": 0, "M3": 0, "M4": 0, "M5": 0}


def run_t1():
    time.sleep(0.5)
    memoire["M4"] = memoire["M1"] + 3
    print("[T1] écrit dans M4 et lit dans M1")


def run_t2():
    time.sleep(0.5)
    memoire["M1"] = memoire["M3"] + memoire["M4"] + 2
    print("[T2] écrit dans M1 et lit dans M3, M4")


def run_t3():
    time.sleep(0.5)
    memoire["M5"] = memoire["M3"] + memoire["M4"] + 1
    print("[T3] écrit dans M5 et lit dans M3, M4")


def run_t4():
    time.sleep(0.5)
    memoire["M2"] = memoire["M4"] + 4
    print("[T4] écrit dans M2 et lit dans M4")


def run_t5():
    time.sleep(0.5)
    memoire["M5"] = memoire["M5"] + 6
    print("[T5] écrit dans M5 et lit dans M5")


def run_t6():
    time.sleep(0.5)
    memoire["M4"] = memoire["M1"] + memoire["M2"] + 3
    print("[T6] écrit dans M4 et lit dans M1, M2")


if __name__ == "__main__":

    t1 = Task("T1", reads=["M1"], writes=["M4"], run=run_t1)
    t2 = Task("T2", reads=["M3", "M4"], writes=["M1"], run=run_t2)
    t3 = Task("T3", reads=["M3", "M4"], writes=["M5"], run=run_t3)
    t4 = Task("T4", reads=["M4"], writes=["M2"], run=run_t4)
    t5 = Task("T5", reads=["M5"], writes=["M5"], run=run_t5)
    t6 = Task("T6", reads=["M1", "M2"], writes=["M4"], run=run_t6)

    tasks = [t1, t2, t3, t4, t5, t6]

    precedence = {
        "T1": [],
        "T2": ["T1"],
        "T3": ["T1"],
        "T4": ["T2"],
        "T5": ["T2", "T3"],
        "T6": ["T4", "T5"],
    }

    sys = TaskSystem(tasks=tasks, precedences_map=precedence)
    sys.check_input()
    sys.parCost()
    sys.draw_all()
