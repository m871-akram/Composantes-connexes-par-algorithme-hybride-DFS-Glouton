#!/usr/bin/env python3
"""
Composantes connexes par DFS hybride (glouton + DFS itératif).

On part de chaque point non visité et on explore ses voisins (distance <= seuil).
Phase 1 (glouton) : on garde la liste des indices jusqu'à k points.
Phase 2 (DFS) : on continue en comptant juste la taille (moins de mémoire).
Le découpage en deux phases ne change pas la complexité O(n^2), mais la version
itérative évite la limite de récursion de Python.
"""

from sys import argv
from typing import List, Tuple

from geo.point import Point


def load_instance(filename: str) -> Tuple[float, List[Point]]:
    """Lit un fichier .pts (1re ligne = distance, puis un point par ligne)."""
    with open(filename, "r") as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines).strip())
        points = [
            Point([float(f) for f in line.split(",")])
            for line in lines
            if line.strip()
        ]

    return distance, points


def compute_cluster(
    start_index: int,
    distance: float,
    points: List[Point],
    visited: List[bool],
    k: int = 8,
) -> int:
    """Taille de la composante connexe qui contient le point start_index."""
    n = len(points)

    # normalement déjà non visité, mais on vérifie quand même
    if visited[start_index]:
        return 0

    visited[start_index] = True
    component: List[int] = [start_index]  # indices trouvés (phase 1)
    stack: List[int] = [start_index]

    # Phase 1 : glouton, on garde la liste des indices
    while stack:
        if len(component) > k:
            break  # composante assez grosse, on passe au DFS
        current = stack.pop()
        for neighbour in range(n):
            if (
                not visited[neighbour]
                and points[current].distance_to(points[neighbour]) <= distance
            ):
                visited[neighbour] = True
                component.append(neighbour)
                stack.append(neighbour)

    # Phase 2 : DFS, on compte seulement la taille
    component_size = len(component)
    while stack:
        current = stack.pop()
        for neighbour in range(n):
            if (
                not visited[neighbour]
                and points[current].distance_to(points[neighbour]) <= distance
            ):
                visited[neighbour] = True
                component_size += 1
                stack.append(neighbour)

    return component_size


def print_components_sizes(
    distance: float,
    points: List[Point],
    k: int = 8,
    verbose: bool = True,
) -> List[int]:
    """Trouve toutes les composantes et affiche leurs tailles (ordre décroissant).

    On traite les graines une par une : il faut finir une composante avant de
    chercher la suivante, sinon on ne sait pas si un point est une vraie graine.
    """
    n = len(points)
    if n == 0:
        return []

    visited: List[bool] = [False] * n

    sizes: List[int] = []
    for i in range(n):
        if not visited[i]:
            size = compute_cluster(i, distance, points, visited, k)
            if size > 0:
                sizes.append(size)

    sizes.sort(reverse=True)

    if verbose:
        print("[" + ", ".join(map(str, sizes)) + "]")

    return sizes


def main() -> None:
    """Traite les fichiers .pts passés en argument."""
    instances = argv[1:]
    if not instances:
        print("Usage: python connectes.py file1.pts file2.pts ...")
        return

    for filename in instances:
        try:
            distance, points = load_instance(filename)
            print(f"# {filename} ({len(points)} points)")
            print_components_sizes(distance, points)
        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    main()
