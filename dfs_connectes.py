#!/usr/bin/env python3
"""
DFS récursif classique (version de référence, comparée à connectes.py).

Deux points sont connectés si leur distance euclidienne est <= au seuil du fichier.
"""

from sys import argv
from typing import Dict, List, Optional, Tuple

from geo.point import Point


def load_instance(filename: str) -> Tuple[Optional[float], List[Point]]:
    """Lit un fichier .pts. Renvoie (None, []) si le fichier est illisible."""
    try:
        with open(filename, "r") as instance_file:
            lines = iter(instance_file)
            distance = float(next(lines).strip())
            points = [
                Point([float(f) for f in line.split(",")])
                for line in lines
                if line.strip()
            ]
        return distance, points
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None, []


def compute_component_sizes_dfs(distance: float, points: List[Point]) -> List[int]:
    """Tailles des composantes avec un DFS récursif (ordre décroissant).

    Attention : sur de grosses composantes denses on peut dépasser la limite de
    récursion de Python. Dans ce cas utiliser la version itérative (connectes.py).
    """
    if not points:
        print("[]")
        return []

    components: Dict[int, List[Point]] = {}

    def _dfs(
        seed: Point,
        all_points: List[Point],
        visited: Optional[List[Point]] = None,
    ) -> List[Point]:
        # récupère récursivement tous les points reliés à seed
        if visited is None:
            visited = [seed]
        for candidate in all_points:
            # le "not in" est en O(n), mais ok pour ces tailles de données
            if seed.distance_to(candidate) <= distance and candidate not in visited:
                visited.append(candidate)
                _dfs(candidate, all_points, visited)
        return visited

    component_id = 0
    remaining = points.copy()  # copie de travail, on enlève les points trouvés
    while remaining:
        seed = remaining[0]
        components[component_id] = _dfs(seed, points)
        for point in components[component_id]:
            if point in remaining:
                remaining.remove(point)
        component_id += 1

    sizes = sorted((len(comp) for comp in components.values()), reverse=True)

    if not sizes:
        print("[]")
    else:
        print("[" + ", ".join(map(str, sizes)) + "]")

    return sizes


def main() -> None:
    """Traite les fichiers .pts passés en argument."""
    if len(argv) < 2:
        print("Usage: python dfs_connectes.py file.pts")
        return

    for filename in argv[1:]:
        distance, points = load_instance(filename)
        if distance is not None:
            print(f"# {filename} ({len(points)} points)")
            compute_component_sizes_dfs(distance, points)


if __name__ == "__main__":
    main()
