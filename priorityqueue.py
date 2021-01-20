#!/usr/bin/env python3

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple
from heapq import heappop, heappush
import heapq
from numbers import Number


@dataclass(order=True)
class PrioritizedItem:
    priority: Number
    item: Any = field(compare=False)


class PriorityQueue:
    def __init__(self) -> None:
        self._heap: List[PrioritizedItem] = []
        self._entry_finder: Dict[Any, PrioritizedItem] = {}

    def update(self, item: Any, priority: Number) -> None:
        entry = self._entry_finder[item]
        old_priority: Number = entry.priority
        entry.priority = priority

        # TODO: fix this starting from the wrong idxs (len(heap)-1, 0)
        if priority < old_priority:
            heapq._siftup(self._heap, 0)
        else:
            heapq._siftdown(self._heap, 0, len(self._heap) - 1)

    def push(self, priority: Number, item: Any) -> None:
        if item in self._entry_finder:
            return self.update(item, priority)

        entry: PrioritizedItem = PrioritizedItem(priority, item)
        self._entry_finder[item] = entry

        heappush(self._heap, entry)

    def pop(self) -> Tuple[Number, Any]:
        elem = heappop(self._heap)
        del self._entry_finder[elem.item]
        return elem.priority, elem.item

    @property
    def front(self) -> Tuple[Number, Any]:
        return self._heap[0].priority, self._heap[0].item

    def __len__(self) -> int:
        return len(self._heap)


if __name__ == "__main__":
    queue = PriorityQueue()
    queue.push(2, "1")
    queue.push(5, "5")
    queue.push(3, "3")

    print(queue.front)

    # try updating
    queue.push(1, "5")

    print(queue.front)
    while queue:
        print(queue.pop())
