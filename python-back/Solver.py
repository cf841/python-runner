import Sudoku
import Conditions
import numpy as np
from collections import deque

class Solver:

    def next_cell(self, sudoku: Sudoku) -> tuple:
        grid = np.array([[cell.val for cell in row] for row in sudoku.grid])
        possible_counts = np.array([[len(cell.possible) if cell.val == 0 else 10 for cell in row] for row in sudoku.grid])
        
        min_count = np.min(possible_counts)
        if min_count == 10:
            return None
        
        pos = np.unravel_index(np.argmin(possible_counts), possible_counts.shape)
        return pos

    def solver(self, sudoku: Sudoku) -> Sudoku:
        state = self.solve(sudoku)
        return state if state is not None else None

    def solve(self, old_sudoku: Sudoku) -> Sudoku:
        singles = old_sudoku.get_singletons()
        hidden = old_sudoku.hidden_singles()
        changes = True

        while len(singles) > 0 or len(hidden) > 0 or changes:
            changes = False

            for single in singles:
                old_sudoku = old_sudoku.set_state(single[0], single[1], single[2])
                if old_sudoku is None or old_sudoku.invalid():
                    return None

            for (row, col), num in hidden:
                old_sudoku = old_sudoku.set_state(row, col, num)
                if old_sudoku is None or old_sudoku.invalid():
                    return None

            grid = np.array([[cell.val for cell in row] for row in old_sudoku.grid])
            possible_counts = np.array([[len(cell.possible) for cell in row] for row in old_sudoku.grid])

            for row in range(9):
                positions_row = np.where(possible_counts[row] == 2)[0]
                if len(positions_row) > 0:
                    if old_sudoku.doubles([(row, col) for col in positions_row]):
                        changes = True

            for col in range(9):
                positions_col = np.where(possible_counts[:, col] == 2)[0]
                if len(positions_col) > 0:
                    if old_sudoku.doubles([(row, col) for row in positions_col]):
                        changes = True

            for box_row in range(0, 9, 3):
                for box_col in range(0, 9, 3):
                    box = possible_counts[box_row:box_row+3, box_col:box_col+3]
                    positions_box = np.argwhere(box == 2)
                    if len(positions_box) > 0:
                        if old_sudoku.doubles([(row+box_row, col+box_col) for row, col in positions_box]):
                            changes = True

            singles = old_sudoku.get_singletons()
            hidden = old_sudoku.hidden_singles()

        cell_index = self.next_cell(old_sudoku)
        if cell_index is None:
            return old_sudoku
        row, col = cell_index

        values = old_sudoku.grid[row][col].possible
        for value in values:
            next_sudoku = old_sudoku.set_state(row, col, value)
            if next_sudoku is None or next_sudoku.invalid():
                continue
            result = self.solve(next_sudoku)

            if result is not None:
                return result

        return old_sudoku