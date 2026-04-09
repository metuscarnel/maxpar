# Résumé du projet MaxPar

## Vue d'ensemble

MaxPar est un système d'**exécution parallèle de tâches** en Python. Il prend un ensemble de tâches avec des dépendances, et les exécute le plus en parallèle possible tout en garantissant la cohérence des données.

---

## Les deux classes

### `Task`
Représente une tâche unitaire avec :
- `name` : identifiant
- `reads` / `writes` : variables lues et écrites
- `run` : fonction à exécuter

### `TaskSystem`
Gère un ensemble de tâches et leurs dépendances via `precedences_map` (ex: `{"T2": ["T1"]}` = T2 dépend de T1).

---

## Les méthodes clés

| Méthode | Rôle |
|---|---|
| `check_input()` | Valide que les tâches et dépendances sont cohérentes |
| `getDependancies()` | Retourne les prédécesseurs directs d'une tâche |
| `_build_graph()` | Construit le graphe orienté (inverse la map) |
| `topological_sort()` | Trie les tâches par DFS post-ordre |
| `runSeq()` | Exécution séquentielle dans l'ordre topologique |
| `bernstein_conditions()` | Vérifie si deux tâches peuvent s'exécuter en parallèle |
| `is_determinated_system()` | Vérifie le déterminisme global du système |
| `generate_system_max()` | Construit le graphe à parallélisme maximal |
| `run()` | Exécution parallèle par vagues de threads |
| `draw()` / `draw_all()` | Visualisation Graphviz en PNG |
| `detTestRnd()` | Test probabiliste du déterminisme |
| `parCost()` | Compare les temps séquentiel vs parallèle |

---

## Les conditions de Bernstein

Deux tâches peuvent s'exécuter en parallèle **sans risque** si et seulement si :

```
W(T1) ∩ R(T2) = ∅   (T1 n'écrit pas ce que T2 lit)
W(T1) ∩ W(T2) = ∅   (elles n'écrivent pas la même variable)
W(T2) ∩ R(T1) = ∅   (T2 n'écrit pas ce que T1 lit)
```

---

## Fonctionnement de `run()` — Exécution par vagues

```
INITIALISATION
  smax = système à parallélisme maximal
  taches_restantes = toutes les tâches
  taches_terminees = {}

BOUCLE (tant qu'il reste des tâches)
  │
  ├─ 1. Trouver les tâches PRÊTES
  │      → tous leurs prédécesseurs sont dans taches_terminees
  │
  ├─ 2. Lancer un thread par tâche prête (en parallèle)
  │      → threading.Thread(target=tache.run).start()
  │
  └─ 3. Attendre la fin de tous les threads (.join())
         → ajouter à taches_terminees, retirer de taches_restantes
```

### Exemple visuel

```
Graphe : T1 → T3 → T5
         T2 → T4 ──╯

Vague 1 : [T1, T2]  lancés en parallèle (pas de prédécesseurs)
Vague 2 : [T3, T4]  lancés en parallèle (T1 et T2 terminés)
Vague 3 : [T5]      lancée seule         (T3 et T4 terminés)
```

---

## Flux global

```
TaskSystem
    │
    ├─ is_determinated_system()  →  vérifie Bernstein sur toutes les paires parallèles
    │
    ├─ generate_system_max()     →  construit le graphe minimal de dépendances
    │
    └─ run()                     →  exécute par vagues de threads parallèles
```