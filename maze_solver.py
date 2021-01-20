#!/usr/bin/env python3

from typing import Dict, Tuple, List
import sys

import math
from argparse import ArgumentParser
from pathlib import Path
import imageio
import numpy as np
from astar import Edge, Node, a_star

parser = ArgumentParser(
    description="Solves the input maze and saves the solution to an output file."
    "Assumes the input maze has an entry at the top and exit at the bottom."
)
parser.add_argument(
    "FILE", type=Path, help="The maze input file. Must be an .png image."
)
parser.add_argument(
    "--output", "-o", type=Path, default="out.png", help="Output file name."
)
args = parser.parse_args()

img = imageio.imread(args.FILE, format="PNG-PIL", as_gray=True)
img = np.asarray(img)

FREE = 255.0

print("Processing image.")

node2loc: Dict[Node, Tuple[int, int]] = {}
node_above: List[Node] = [None] * len(img[0])

# find start location and add to dicts
start = Node()
col = np.where(img[0] == FREE)[0][0]

node2loc[start] = (0, col)
node_above[col] = start

# find goal location
goal = Node()
col = np.where(img[-1] == FREE)[0][0]

node2loc[goal] = (len(img) - 1, col)

# Create graph from maze
# Nodes will be created only at corners
for rowno, row in enumerate(img[1:-1], start=1):
    left_node: Node = None
    for colno, elem in enumerate(row[1:-1], start=1):
        if elem == FREE:
            up = img[rowno - 1, colno] == FREE
            do = img[rowno + 1, colno] == FREE
            le = img[rowno, colno - 1] == FREE
            ri = img[rowno, colno + 1] == FREE

            # Check wether we're at a corner
            if (up or do) and (le or ri):
                new_node = Node()
                node2loc[new_node] = (rowno, colno)

                # Check wether we have an unobstructed path to a node left of us
                if left_node:
                    distance: int = colno - node2loc[left_node][1]

                    left_node.edges.append(Edge(distance, new_node))
                    new_node.edges.append(Edge(distance, left_node))

                # Check wether we have an unobstructed path to a node above us
                if node_above[colno]:
                    above: Node = node_above[colno]
                    distance: int = rowno - node2loc[above][0]

                    above.edges.append(Edge(distance, new_node))
                    new_node.edges.append(Edge(distance, above))

                left_node = new_node
                node_above[colno] = new_node
        else:
            left_node = None
            node_above[colno] = None

goal_loc: Tuple[int, int] = node2loc[goal]
above_goal: Node = node_above[goal_loc[1]]
# get distance between goal node and node directly above
distance: int = goal_loc[0] - node2loc[above_goal][0]

above_goal.edges.append(Edge(distance, goal))
goal.edges.append(Edge(distance, above_goal))

print(f"Generated {len(node2loc)} nodes!")


def distance_heuristic(node: Node) -> int:
    node_loc: Tuple[int, int] = node2loc[node]
    goal_loc: Tuple[int, int] = node2loc[goal]

    return np.sum(np.abs(np.diff([node_loc, goal_loc])))


print("Finding shortest path")
cost, path = a_star(start, goal, distance_heuristic)

if not path:
    print("Couldn't find path to exit!")
    sys.exit()

print("Found path with cost:", cost)

print("Saving solution")
img = imageio.imread(args.FILE, format="PNG-PIL")

RED = [255, 0, 0, 255]
BLUE = [0, 0, 255, 255]

color = RED
count: int = 0

prev_loc: Tuple[int, int] = node2loc[start]
for node in path:
    loc = node2loc[node]

    iter_col = prev_loc[0] == loc[0]
    c = int(math.copysign(1, loc[iter_col] - prev_loc[iter_col]))
    for idx in range(prev_loc[iter_col], loc[iter_col], c):
        row = loc[0] if iter_col else idx
        col = loc[1] if not iter_col else idx

        p = count / cost
        color = [(1 - p) * x + p * y for x, y in zip(RED, BLUE)]
        img[row, col] = color
        count += 1

    prev_loc = loc

end_loc = node2loc[goal]
img[end_loc] = BLUE

imageio.imwrite(args.output, img)
