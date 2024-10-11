import numpy as np
import copy

class Sudoku:

    def __init__(self):
        self.grid = np.array([[Cell(i, j, 0) for i in range(9)] for j in range(9)])
        self.conditions = {}
        self.setup()

    def setup(self):
        valid = True
        for row in range(9):
            for col in range(9):
                cell = self.grid[row, col]
                if cell.val != 0:
                    cell.possible = [cell.val]
                    self.remove_possible(row, col, cell.val)
                    for cond in cell.conditions:
                        cond.assign_cell(cell)
                elif cell.conditions:
                    for condition in cell.conditions:
                        if not condition.setup(cell):
                            valid = False
        return valid

    def remove_possible(self, row, col, val):
        affected_cells = set()
        grid = self.grid

        # Remove possible value from the same row
        row_cells = grid[row, :]
        for cell in row_cells:
            if val in cell.possible and cell.val == 0:
                cell.remove_pos(val)
                affected_cells.add(cell)

        # Remove possible value from the same column
        col_cells = grid[:, col]
        for cell in col_cells:
            if val in cell.possible and cell.val == 0:
                cell.remove_pos(val)
                affected_cells.add(cell)

        # Remove possible value from the 3x3 subgrid
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        subgrid_cells = grid[start_row:start_row + 3, start_col:start_col + 3].flatten()
        for cell in subgrid_cells:
            if cell.val == 0 and val in cell.possible:
                cell.remove_pos(val)
                affected_cells.add(cell)

        # Update conditions for affected cells
        for cell in affected_cells:
            for condition in cell.conditions:
                condition.change_possible(cell)

    def find_hidden_singles(self, cells):
        seen = {}
        for (row, col) in cells:
            cell = self.grid[row, col]
            if cell.val == 0:
                for num in cell.possible:
                    if num in seen:
                        seen[num] = None
                    else:
                        seen[num] = (row, col)
        return [(value, key) for key, value in seen.items() if value is not None]

    def hidden_singles(self):
        hidden_singles = []
        for c in range(9):
            hidden_singles += self.find_hidden_singles([(c, r) for r in range(9)])
        for r in range(9):
            hidden_singles += self.find_hidden_singles([(c, r) for c in range(9)])
        for br in range(3):
            for bc in range(3):
                hidden_singles += self.find_hidden_singles([(c, r) for r in range(br * 3, br * 3 + 3) for c in range(bc * 3, bc * 3 + 3)])
        return hidden_singles

    def doubles(self, positions):
        grid = self.grid
        doubles = [(x, y) for x, y in positions if len(grid[x, y].possible) == 2]

        if len(doubles) < 2:
            return False

        changes = False
        for i in range(len(doubles)):
            for j in range(i + 1, len(doubles)):
                pos1, pos2 = doubles[i], doubles[j]
                if grid[pos1[0], pos1[1]].possible == grid[pos2[0], pos2[1]].possible:
                    common_values = grid[pos1[0], pos1[1]].possible
                    for pos in positions:
                        if pos != pos1 and pos != pos2:
                            cell = grid[pos[0], pos[1]]
                            if common_values[0] in cell.possible:
                                cell.possible.remove(common_values[0])
                                changes = True
                            if common_values[1] in cell.possible:
                                cell.possible.remove(common_values[1])
                                changes = True
        return changes

    def is_valid_sudoku(self):
        grid = self.grid
        for i in range(9):
            row = grid[i, :]
            if not self.is_valid_group(row):
                return False
            col = grid[:, i]
            if not self.is_valid_group(col):
                return False
            box = grid[(i // 3) * 3:(i // 3) * 3 + 3, (i % 3) * 3:(i % 3) * 3 + 3].flatten()
            if not self.is_valid_group(box):
                return False
        return True

    def is_valid_group(self, group):
        numbers = [cell.val for cell in group if cell.val != 0]
        return len(numbers) == len(np.unique(numbers))

    def invalid(self):
        for row in self.grid:
            for cell in row:
                if cell.val == 0 and len(cell.possible) == 0:
                    return True
        return False

    def get_singletons(self):
        singletons = []
        for y in range(9):
            for x in range(9):
                cell = self.grid[x, y]
                if len(cell.possible) == 1 and cell.val == 0:
                    singletons.append((x, y, cell.possible[0]))
        return singletons

    def count_possible(self):
        return sum(len(cell.possible) for row in self.grid for cell in row)

    def set_state(self, row, col, val):
        original_state = copy.deepcopy(self)
        cell = original_state.grid[row, col]
        cell.possible = [val]
        cell.val = val

        for condition in cell.conditions:
            if not condition.assign_cell(cell):
                return None

        affected_cells = set()
        grid = original_state.grid

        # Remove possible value from the same row
        row_cells = grid[row, :]
        for cell in row_cells:
            if val in cell.possible and cell.val == 0:
                cell.remove_pos(val)
                affected_cells.add(cell)

        # Remove possible value from the same column
        col_cells = grid[:, col]
        for cell in col_cells:
            if val in cell.possible and cell.val == 0:
                cell.remove_pos(val)
                affected_cells.add(cell)

        # Remove possible value from the 3x3 subgrid
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        subgrid_cells = grid[start_row:start_row + 3, start_col:start_col + 3].flatten()
        for cell in subgrid_cells:
            if cell.val == 0 and val in cell.possible:
                cell.remove_pos(val)
                affected_cells.add(cell)

        # Update conditions for affected cells
        for cell in affected_cells:
            for condition in cell.conditions:
                condition.change_possible(cell)

        if original_state.invalid():
            return None

        for r in range(9):
            for c in range(9):
                cell = original_state.grid[r, c]
                if cell.val == 0 and self.grid[r, c].possible != cell.possible:
                    for condition in cell.conditions:
                        if not condition.change_possible(cell):
                            return None
        return original_state

    def get_grid(self):
        return self.grid

    def set_pos(self, x, y, val):
        self.grid[x, y].val = val

    def add_condition(self, condition):
        if condition not in self.conditions:
            self.conditions[condition] = []
        self.conditions[condition] += condition.cells
        for cell in condition.cells:
            cell.add_condition(condition)

    def __str__(self):
        result = []
        for i, row in enumerate(self.grid):
            if i % 3 == 0 and i != 0:
                result.append("-" * 21)
            row_str = []
            for j, cell in enumerate(row):
                if j % 3 == 0 and j != 0:
                    row_str.append("|")
                row_str.append(str(cell.val) if cell.val != 0 else ".")
            result.append(" ".join(row_str))
        return "\n".join(result)

class Cell:

    def __init__(self, x, y, val=0):
        self.x = x
        self.y = y
        self.val = val
        self.adj = None
        self.possible = [i for i in range(1, 10)]
        self.conditions = []

    def add_condition(self, condition):
        self.conditions.append(condition)

    def remove_pos(self, val):
        self.possible.remove(val)