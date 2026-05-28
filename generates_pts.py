#!/usr/bin/env python3
"""
Génère un fichier .pts avec des points 2D aléatoires dans [0,1] x [0,1].

Usage : python generates_pts.py <nb_points> <fichier_sortie> [distance]
Exemple : python generates_pts.py 200 exemple_5.pts 0.05
"""

import os
import random
import sys


def generate_pts_file(filename: str, num_points: int, distance: float = 0.1) -> None:
    """Écrit un fichier .pts : 1re ligne = distance, puis les points."""
    with open(filename, "w") as f:
        f.write(f"{distance}\n")  # première ligne : le seuil de distance
        for _ in range(num_points):
            x = random.random()
            y = random.random()
            f.write(f"{x}, {y}\n")

    print(f"Generated: {filename} ({num_points} points, distance={distance})")


def main() -> None:
    """Lit les arguments et génère le fichier."""
    if len(sys.argv) < 3:
        print("Usage: python generates_pts.py <num_points> <output_file> [distance]")
        sys.exit(1)

    num_points = int(sys.argv[1])
    output_file = sys.argv[2]
    distance = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1

    # chemin relatif -> on le met à côté du script
    if not os.path.isabs(output_file):
        output_file = os.path.join(os.path.dirname(__file__), output_file)

    generate_pts_file(output_file, num_points, distance)


if __name__ == "__main__":
    main()
