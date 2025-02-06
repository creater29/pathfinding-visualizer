import pygame
from settings import *
from algorithms.astar import astar
from algorithms.bfs import bfs


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * NODE_SIZE
        self.y = row * NODE_SIZE
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_path(self):
        self.color = PURPLE

    def make_open(self):
        self.color = YELLOW

    def make_closed(self):
        self.color = ORANGE

    def reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, NODE_SIZE, NODE_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Down, Up, Right, Left
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            if 0 <= self.row + dr < ROWS and 0 <= self.col + dc < COLS:
                neighbor = grid[self.row + dr][self.col + dc]
                if not neighbor.is_barrier():
                    self.neighbors.append(neighbor)


def make_grid():
    grid = []
    for row in range(ROWS):
        grid.append([])
        for col in range(COLS):
            node = Node(row, col)
            grid[row].append(node)
    return grid


def draw_grid(win):
    for row in range(ROWS):
        pygame.draw.line(win, GREY, (0, row * NODE_SIZE), (WIDTH, row * NODE_SIZE))
    for col in range(COLS):
        pygame.draw.line(win, GREY, (col * NODE_SIZE, 0), (col * NODE_SIZE, GRID_HEIGHT))


def draw(win, grid, algorithm_name):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win)

    # Algorithm display
    font = pygame.font.Font(None, 36)
    text = font.render(f"Algorithm: {algorithm_name}", True, BLACK)
    win.blit(text, (10, HEIGHT - 35))

    pygame.display.update()


def get_clicked_pos(pos):
    y, x = pos
    row = y // NODE_SIZE
    col = x // NODE_SIZE
    return row, col


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer")
    clock = pygame.time.Clock()

    grid = make_grid()
    start = None
    end = None
    algorithm = astar  # Default algorithm
    algorithm_name = "A*"

    running = True
    while running:
        clock.tick(FPS)
        draw(win, grid, algorithm_name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # Left click
                pos = pygame.mouse.get_pos()
                if pos[1] < GRID_HEIGHT:  # Prevent clicking on UI area
                    row, col = get_clicked_pos(pos)
                    node = grid[row][col]

                    if not start and node != end:
                        start = node
                        node.make_start()
                    elif not end and node != start:
                        end = node
                        node.make_end()
                    elif node != start and node != end:
                        node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right click
                pos = pygame.mouse.get_pos()
                if pos[1] < GRID_HEIGHT:
                    row, col = get_clicked_pos(pos)
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    path = algorithm(grid, start, end)

                    if path:
                        for node in path:
                            node.make_path()

                if event.key == pygame.K_a:
                    algorithm = astar
                    algorithm_name = "A*"
                if event.key == pygame.K_b:
                    algorithm = bfs
                    algorithm_name = "BFS"
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid()

                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()


if __name__ == "__main__":
    main()
