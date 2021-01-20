#!/usr/bin/env python3

from typing import Dict, Tuple, List

import numpy as np
from astar import Node, add_bidirectional_edge

FREE = 255.0


class Maze:
    def __init__(self, img: np.array) -> None:
        self._node2loc: Dict[Node, Tuple[int, int]] = {}
        self._parse_img(img)

    @property
    def start(self) -> Node:
        return self._start

    @property
    def goal(self) -> Node:
        return self._start

    def dist_from_goal(self, node: Node) -> int:
        node_loc: Tuple[int, int] = self._node2loc[node]
        goal_loc: Tuple[int, int] = self._node2loc[self._goal]

        return np.sum(np.abs(np.diff([node_loc, goal_loc])))

    def _parse_img(self, img: np.array) -> None:
        node_above: List[Node] = [None] * len(img[0])

        # find start location and add to dicts
        self._start = Node()
        col = np.where(img[0] == FREE)[0][0]

        self._node2loc[self._start] = (0, col)
        node_above[col] = self._start

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
                        self._node2loc[new_node] = (rowno, colno)

                        # Check wether we have an unobstructed path to a node left of us
                        if left_node:
                            distance: int = colno - self._node2loc[left_node][1]

                            add_bidirectional_edge(left_node, new_node, distance)

                        # Check wether we have an unobstructed path to a node above us
                        if node_above[colno]:
                            above: Node = node_above[colno]
                            distance: int = rowno - self._node2loc[above][0]

                            add_bidirectional_edge(above, new_node, distance)

                        left_node = new_node
                        node_above[colno] = new_node
                else:
                    left_node = None
                    node_above[colno] = None

        # find goal location
        self._goal = Node()
        col = np.where(img[-1] == FREE)[0][0]

        self._node2loc[self._goal] = (len(img) - 1, col)

        # create connection between goal node and node directly above
        above_goal: Node = node_above[col]
        distance: int = self.dist_from_goal(above_goal)

        add_bidirectional_edge(above_goal, self._goal, distance)
