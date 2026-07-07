"""
The Game of Life (GoL) module named in honour of John Conway
"""
import numpy as np
from scipy import signal, ndimage


def parse_pattern(filepath):
    """
    Parses a Plaintext (.cells) or RLE (.rle) pattern file.

    Returns:
        tuple: (width, height, list of (r, c) offsets of live cells)
    """
    with open(filepath, 'r') as f:
        raw_lines = f.readlines()

    data_lines = []
    for line in raw_lines:
        line = line.rstrip('\n').rstrip('\r')
        if line == '' or line.startswith('!') or line.startswith('#'):
            continue
        data_lines.append(line)

    if not data_lines:
        return 0, 0, []

    first = data_lines[0].strip().lower()
    if first.startswith('x'):
        header = data_lines[0]
        body = ''.join(data_lines[1:])
        return _parse_rle(header, body)

    return _parse_plaintext(data_lines)


def _parse_plaintext(lines):
    live_cells = []
    height = len(lines)
    width = max((len(line) for line in lines), default=0)
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch in ('O', 'o', '*'):
                live_cells.append((r, c))
    return width, height, live_cells


def _parse_rle(header, body):
    import re
    width_match = re.search(r'x\s*=\s*(\d+)', header)
    height_match = re.search(r'y\s*=\s*(\d+)', header)
    width = int(width_match.group(1)) if width_match else 0
    height = int(height_match.group(1)) if height_match else 0

    live_cells = []
    r, c = 0, 0
    count_str = ''
    for ch in body:
        if ch.isspace():
            continue
        if ch.isdigit():
            count_str += ch
            continue

        count = int(count_str) if count_str else 1
        count_str = ''

        if ch in ('b', 'B'):
            c += count
        elif ch in ('o', 'O'):
            for _ in range(count):
                live_cells.append((r, c))
                c += 1
        elif ch == '$':
            r += count
            c = 0
        elif ch == '!':
            break

    return width, height, live_cells


class GameOfLife:
    def __init__(self, N=256, finite=False, fastMode=True):
        self.grid = np.zeros((N, N), np.uint)
        self.neighborhood = np.ones((3, 3), np.uint)
        self.neighborhood[1, 1] = 0
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N
        self.cols = N

    def getStates(self):
        return self.grid

    def getGrid(self):
        return self.getStates()

    def update_grid_fast(self, grid):
        """
        [Part 1e - Fast Convolution]
        Uses scipy.signal.convolve2d with the 8-connected neighborhood kernel
        to count live neighbors for every cell at once, then applies the GoL
        rules with vectorized numpy operations instead of nested loops.
        """
        boundary = 'fill' if self.finite else 'wrap'
        neighbor_count = signal.convolve2d(
            grid, self.neighborhood, mode='same',
            boundary=boundary, fillvalue=self.deadValue
        )

        is_alive = grid == self.aliveValue
        survives = is_alive & ((neighbor_count == 2) | (neighbor_count == 3))
        born = (~is_alive) & (neighbor_count == 3)

        new_grid = np.where(survives | born, self.aliveValue, self.deadValue)
        return new_grid.astype(grid.dtype)

    def evolve(self):
        if self.fastMode:
            self.grid = self.update_grid_fast(self.grid)
        else:
            new_grid = np.copy(self.grid)
            for r in range(self.rows):
                for c in range(self.cols):
                    live_neighbors = 0
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            nr = r + dr
                            nc = c + dc
                            if self.finite:
                                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                    if self.grid[nr, nc] == self.aliveValue:
                                        live_neighbors += 1
                            else:
                                nr %= self.rows
                                nc %= self.cols
                                if self.grid[nr, nc] == self.aliveValue:
                                    live_neighbors += 1
                    if self.grid[r, c] == self.aliveValue:
                        if live_neighbors < 2 or live_neighbors > 3:
                            new_grid[r, c] = self.deadValue
                        else:
                            new_grid[r, c] = self.aliveValue
                    else:
                        if live_neighbors == 3:
                            new_grid[r, c] = self.aliveValue
                        else:
                            new_grid[r, c] = self.deadValue
            self.grid = new_grid

    def insertBlinker(self, index=(0, 0)):
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue

    def insertGlider(self, index=(0, 0)):
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 2, index[1]] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 2] = self.aliveValue

    def insertGliderGun(self, index=(0, 0)):
        self.grid[index[0] + 1, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 2, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 3, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 15] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 37] = self.aliveValue

        self.grid[index[0] + 4, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 37] = self.aliveValue

        self.grid[index[0] + 5, index[1] + 1 + 1] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 2 + 1] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 23] = self.aliveValue

        self.grid[index[0] + 6, index[1] + 1 + 1] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 2 + 1] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 16] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 19] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 7, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 8, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 8, index[1] + 17] = self.aliveValue

        self.grid[index[0] + 9, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 9, index[1] + 15] = self.aliveValue

    def insertFromFile(self, filename, index=((0, 0))):
        '''
        Insert cells from pattern file using parse_pattern
        '''
        width, height, live_cells = parse_pattern(filename)
        for r, c in live_cells:
            target_r = index[0] + r
            target_c = index[1] + c
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r, target_c] = self.aliveValue