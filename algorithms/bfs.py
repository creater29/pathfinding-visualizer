from collections import deque
from settings import *


def bfs(grid, start, end):
    queue = deque()
    queue.append(start)
    came_from = {}
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                if neighbor != end:
                    neighbor.make_open()

        if current != start:
            current.make_closed()

    return None
