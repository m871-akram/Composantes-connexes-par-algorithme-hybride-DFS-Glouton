# Composantes connexes par algorithme hybride DFS / Glouton

Un ensemble de points 2D et un seuil *d* : deux points sont connectés si leur
distance euclidienne est <= *d*. Le programme trouve les composantes connexes
(les "paquets" de points reliés) et affiche la taille de chacune, triée du plus
grand au plus petit.

## Les deux algorithmes

- **`dfs_connectes.py`** — DFS récursif classique (version de référence). Simple,
  mais peut dépasser la limite de récursion de Python sur de grosses composantes.
- **`connectes.py`** — même idée en itératif (avec une pile), en deux phases :
  phase gloutonne (on garde la liste des indices jusqu'à *k* = 8 points), puis
  phase DFS (on vide la pile en comptant juste la taille).

Le découpage en deux phases est surtout pédagogique : la complexité reste O(n²)
dans les deux cas. Le vrai intérêt de la version itérative, c'est d'éviter la
limite de récursion. Pas de multiprocessing : le problème est séquentiel, il faut
finir une composante avant de chercher la graine suivante.

## Lancer

```bash
python connectes.py exemple_1.pts exemple_2.pts
# exemple_1.pts (20 points)
[5, 4, 2, 2, 2, 2, 1, 1, 1]
# exemple_2.pts (40 points)
[11, 6, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1]

python dfs_connectes.py exemple_1.pts            # version récursive
python courbe_performance.py                     # temps + courbe (matplotlib)
python generates_pts.py 500 exemple_5.pts 0.08   # génère un jeu de points
python test_connectes.py                         # test : hybride == récursif
```

Seul `courbe_performance.py` a besoin de matplotlib : `pip install -r requirements.txt`.

## Format des fichiers `.pts`

```
<seuil>
<x1>, <y1>
<x2>, <y2>
...
```

Ligne 1 : le seuil *d*. Lignes suivantes : un point par ligne, deux flottants
séparés par une virgule.

## Notes

- `geo/` : bibliothèque géométrique fournie (Point, distance, affichage SVG).
- Amélioration possible : la recherche de voisins scanne tous les points (O(n²)) ;
  une grille spatiale de pas *d* rapprocherait du linéaire.
- Détail des mesures et de la méthode : `rapport.pdf`.
```

