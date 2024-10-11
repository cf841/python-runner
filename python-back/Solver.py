import Sudoku
import Conditions
import numpy as np
from collections import deque

class Solver:

    def next_cell(self, sudoku):
        min_num = 10
        pos = None
        for row in range(9):
            for col in range(9):
                if sudoku.grid[row][col].val == 0:
                    num = len(sudoku.grid[row][col].possible)
                    if num == 1:
                        return (row, col)
                    if num < min_num:
                        min_num = num
                        pos = (row, col)
        return pos
    
    def solver(self, sudoku):
        state = self.solve(sudoku)
        return state if state is not None else None
    
    def solve(self, old_sudoku):
        
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

            for row in range(9):
                positionsRow = [i for i, cell in enumerate(old_sudoku.grid[row]) if len(cell.possible) == 2]
                if len(positionsRow) > 0:
                    if old_sudoku.doubles([(row, col) for col in positionsRow]):
                        changes = True

            for col in range(9):
                positionsCol = [i for i, cell in enumerate([old_sudoku.grid[r][col] for r in range(9)]) if len(cell.possible) == 2]
                if len(positionsCol) > 0:
                    if old_sudoku.doubles([(row, col) for row in positionsCol]):
                        changes = True

            for box_row in range(0, 9, 3):
                for box_col in range(0, 9, 3):
                    positionsBox = [(i, j) for i in range(3) for j in range(3) if len(old_sudoku.grid[box_row+i][box_col+j].possible    ) == 2]
                    if len(positionsBox) > 0:
                        if old_sudoku.doubles([(row+box_row, col+box_col) for row, col in positionsBox]):
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