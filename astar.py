#!env python3

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Tuple, Union
from numbers import Number
from priorityqueue import PriorityQueue

__all__ = ["Edge", "Node", "add_bidirectional_edge", "a_star"]


@dataclass
class Edge:
    weight: Number
    destination: Node


@dataclass
class Node:
    edges: List[Edge] = field(default_factory=list)

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)

    def __hash__(self) -> int:
        return super().__hash__()


def add_bidirectional_edge(node1: Node, node2: Node, weight: Number) -> None:
    node1.edges.append(Edge(weight, node2))
    node2.edges.append(Edge(weight, node1))


def _reconstruct_path(came_from: Dict[Node, Node], current: Node) -> List[Node]:
    total_path: List[Node] = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def a_star(
    start: Node, goal: Node, h: Callable[[Node], Number]
) -> Union[None, Tuple[Number, List[Node]]]:
    open_set = PriorityQueue()
    open_set.push(h(start), start)

    came_from: Dict[Node, Node] = {}

    g_score: Dict[Node, Number] = {start: 0.0}

    while open_set:
        _, current = open_set.pop()
        if current is goal:
            return g_score[current], _reconstruct_path(came_from, current)

        for edge in current.edges:
            tentative_g_score = g_score[current] + edge.weight
            neighbor = edge.destination

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                open_set.push(tentative_g_score + h(neighbor), neighbor)

    return None


if __name__ == "__main__":
    goal = Node()
    n2 = Node([Edge(2, goal)])
    n3 = Node([Edge(3, n2)])
    n5 = Node([Edge(1, goal)])
    n4 = Node([Edge(3, n3), Edge(1, n5)])
    start = Node([Edge(1, n4), Edge(5, n5)])

    d = {goal: "goal", n2: 2, n3: 3, n4: 4, n5: 5, start: "start"}

    path = a_star(start, goal, lambda x: 1)
    print([d[n] for n in path])
