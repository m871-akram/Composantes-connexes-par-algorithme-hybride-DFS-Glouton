# Composantes connexes par algorithme hybride DFS / Glouton

On a un ensemble de points 2D et un seuil de distance *d*. Deux points sont
connectés quand leur distance euclidienne est <= *d*. Le but du projet est de
trouver les composantes connexes (les "paquets" de points reliés entre eux) et
d'afficher la taille de chacune.

## Les deux algorithmes

### 1. DFS récursif — `dfs_connectes.py`

Un DFS récursif classique. On part d'un point non visité, on visite tous ses
voisins de proche en proche, et on obtient une composante. Simple et correct,
mais sur de grosses composantes denses on peut dépasser la limite de récursion
de Python.

### 2. DFS hybride glouton + itératif — `connectes.py`

La même idée, mais en itératif (une pile au lieu de la récursion), en deux
phases :

| Phase | Ce qu'on fait | Quand on s'arrête |
|-------|---------------|-------------------|
| Glouton | on empile les voisins en gardant la liste des indices | la composante dépasse *k* points (k = 8 par défaut) |
| DFS | on vide la pile en comptant juste la taille | la pile est vide |

À savoir :

- Les deux phases font le même parcours : le découpage est surtout pédagogique,
  la complexité reste O(n²) dans les deux cas.
- La phase de comptage ne garde qu'un compteur (pas la liste des points), donc
  moins de mémoire sur les grosses composantes.
- Comme c'est itératif, on évite la limite de récursion du DFS récursif.

> Pourquoi pas du multiprocessing ? Parce que le problème est séquentiel : il
> faut finir une composante avant de chercher la graine suivante. Si plusieurs
> processus se partageaient les graines, ils pourraient revendiquer le même
> voisin en même temps et casser une grosse composante en morceaux.

> Piste d'amélioration : pour l'instant on compare chaque point à tous les
> autres, d'où le O(n²). En rangeant les points dans une grille de cases de
> taille *d* (et en ne regardant que les 9 cases autour), on se rapprocherait du
> linéaire sur les gros jeux de données. Pas fait ici pour garder le code court.

## Structure du projet

```
.
├── connectes.py           # DFS hybride glouton + itératif
├── dfs_connectes.py       # DFS récursif (version de référence)
├── courbe_performance.py  # comparaison des temps + courbe
├── generates_pts.py       # générateur de fichiers .pts aléatoires
├── test_connectes.py      # test : hybride == récursif
├── exemple_1.pts          # 20 points  — seuil 0.15
├── exemple_2.pts          # 40 points  — seuil 0.15
├── exemple_3.pts          # 100 points — seuil 0.05
├── exemple_4.pts          # 200 points — seuil 0.10
├── requirements.txt       # dépendances (matplotlib)
├── rapport.pdf            # rapport détaillé
└── geo/                   # bibliothèque géométrique fournie
    ├── __init__.py
    ├── point.py           # Point + distance euclidienne
    ├── quadrant.py        # boîte englobante
    ├── segment.py         # segment
    └── tycat.py           # affichage SVG (Terminology)
```

## Lancer les algorithmes

DFS récursif sur un fichier :
```bash
python dfs_connectes.py exemple_1.pts
# exemple_1.pts (20 points)
[5, 4, 2, 2, 2, 2, 1, 1, 1]
```

DFS hybride sur plusieurs fichiers :
```bash
python connectes.py exemple_1.pts exemple_2.pts
# exemple_1.pts (20 points)
[5, 4, 2, 2, 2, 2, 1, 1, 1]
# exemple_2.pts (40 points)
[11, 6, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1]
```

La sortie est la liste des tailles des composantes, triée du plus grand au plus
petit.

Comparer les deux algos et tracer la courbe :
```bash
python courbe_performance.py
```
Ça trouve tous les fichiers `exemple_*.pts`, lance les deux algos sur chacun,
affiche les temps et ouvre une courbe matplotlib.

Générer un nouveau jeu de points :
```bash
# 500 points aléatoires, seuil 0.08
python generates_pts.py 500 exemple_5.pts 0.08
```
Arguments : `<nb_points> <fichier_sortie> [seuil]` (seuil = 0.1 par défaut).

Lancer le test :
```bash
python test_connectes.py   # ou : pytest
```

> Seul `courbe_performance.py` a besoin d'une dépendance externe (matplotlib) :
> `pip install -r requirements.txt`. Les deux algos tournent avec la
> bibliothèque standard.

## Format des fichiers `.pts`

```
<seuil_de_distance>
<x1>, <y1>
<x2>, <y2>
...
```

- Ligne 1 : le seuil de distance *d* (un flottant).
- Lignes suivantes : un point par ligne, deux flottants séparés par une virgule.

Exemple (début de `exemple_1.pts`) :
```
0.15
0.2252545216501013, 0.12013009489606818
0.9626018443381511, 0.2627781865717459
0.29367221887978456, 0.6844833441065136
```

## Résultats

Le détail des mesures et de la méthode est dans `rapport.pdf`.
