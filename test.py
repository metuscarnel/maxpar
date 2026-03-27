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
    print("Etat initial de la mémoire :", memoire)
    sys = TaskSystem(tasks=tasks, precedences_map=precedence)
    sys.check_input()
    sys.parCost()
    sys.draw_all()
    print("Etat final de la mémoire :", memoire)
    # ceci est un test de vérification avec l'exemple de l'exercice 4.1 du TD3
    """memoire = {
    "M1": 1, 
    "M2": 2, 
    "M3": 3, 
    "M4": 4, 
    "M5": 5
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
    memoire["M5"] = memoire["M5"] + 5 
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
    print("Etat initial de la mémoire :", memoire)
    sys.check_input()
    sys.parCost()
    sys.draw_all()
    print("Etat final de la mémoire :", memoire)"""
