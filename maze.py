import random

class Cell:

    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self):

        return all(self.walls.values())

    def break_wall(self, other, wall):

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:

    def __init__(self, nx, ny, ix=0, iy=0):
        """Maze size is nx x ny cells
        starting at (ix, iy)
        """

        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def get_cell(self, x, y):

        return self.maze_map[x][y]

    def __str__(self):
        """Return a string representation of the maze."""

        maze_rows = ['█' * self.nx * 2]
        for y in range(self.ny):
            maze_row = ['█']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' █')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['█']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('██')
                else:
                    maze_row.append(' █')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.get_cell(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        # Total number of cells.
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.get_cell(self.ix, self.iy)
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.break_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1
            

# Maze dimensions (ncols, nrows)
nx, ny = 12, 12
# Maze entry position
ix, iy = 0, 0

maze = Maze(nx, ny, ix, iy)
maze.make_maze()

print(maze)