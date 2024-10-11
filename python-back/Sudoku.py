import Conditions
import numpy as np
import copy
class Sudoku:

    def __init__(self):
        self.grid = [[Cell(i, j, 0) for i in range(9)] for j in range(9)]
        self.conditions = {}
        self.setup()

    def setup(self):
        valid = True
        for row in range(9):
            for col in range(9):
                if self.grid[row][col].val != 0: 
                    self.grid[row][col].possible = [self.grid[row][col].val]
                    self.remove_possible(row, col, self.grid[row][col].val)
                    for cond in self.grid[row][col].conditions:
                        cond.assign_cell(self.grid[row][col]) # Need to add check for valid problem

                # Condition thingrow-mabobs
                elif self.grid[row][col].conditions:
                    for condition in self.grid[row][col].conditions:
                        if not condition.setup(self.grid[row][col]):
                            valid = False
        return valid
                        
    def remove_possible(self, row, col, val):
        affected_cells = set()
            # Remove possible value from the same row
        for i in range(9):
            if val in self.grid[row][i].possible and self.grid[row][i].val == 0:
                self.grid[row][i].remove_pos(val)
                affected_cells.add(self.grid[row][i])

        # Remove possible value from the same column
        for i in range(9):
            if val in self.grid[i][col].possible and self.grid[i][col].val == 0:
                self.grid[i][col].remove_pos(val)
                affected_cells.add(self.grid[i][col])
        
        # Calculate the starting row and column of the 3x3 subgrid
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        
        # Remove possible value from the 3x3 subgrid
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j].val == 0 and val in self.grid[i][j].possible:
                    self.grid[i][j].remove_pos(val)
                    affected_cells.add(self.grid[i][j])
        
        # Update conditions for affected cells
        for cell in affected_cells:
            for condition in cell.conditions:
                condition.change_possible(cell)


    def find_hidden_singles(self, cells):
        seen = {}
        for (row, col) in cells:
            if self.grid[row][col].val == 0:
                for num in self.grid[row][col].possible:
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
                hidden_singles += self.find_hidden_singles([(c, r) for r in range(br*3, br*3+3) for c in range(bc*3, bc*3+3)])
        return hidden_singles
    
    def doubles(self, positions):
        # Filter positions with only two possible numbers
        doubles = [(x, y) for x, y in positions if len(self.grid[x][y].possible) == 2]

        if len(doubles) < 2:
            return False

        changes = False
        # Check every pair of cells in any row, column, or box
        for i in range(len(doubles)):
            for j in range(i + 1, len(doubles)):
                pos1, pos2 = doubles[i], doubles[j]
                # If the two pairs have the same possible numbers
                if self.grid[pos1[0]][pos1[1]].possible == self.grid[pos2[0]][pos2[1]].possible and len(self.grid[pos1[0]][pos1[1]].possible) == 2:
                    # Eliminate these numbers from other positions in the same row, column, or box
                    common_values = self.grid[pos1[0]][pos1[1]].possible
                    for pos in positions:
                        if pos != pos1 and pos != pos2:
                            if common_values[0] in self.grid[pos[0]][pos[1]].possible:
                                self.grid[pos[0]][pos[1]].possible.remove(common_values[0])
                                changes = True
                            if common_values[1] in self.grid[pos[0]][pos[1]].possible:
                                self.grid[pos[0]][pos[1]].possible.remove(common_values[1])
                                changes = True
        return changes

    # Gets all numbers in a row, box, col, and passes through is_valid_group
    def is_valid_sudoku(self):
        for i in range(9):
            row = self.grid[i]
            if not self.is_valid_group(row):
                return False
                break
            col = [row[i] for row in self.grid]
            if not self.is_valid_group(col):
                return False
            box = [self.grid[i//3*3 + j//3][i%3*3 + j%3] for j in range(9)]
            if not self.is_valid_group(box):
                return False
        return True
        
    # Checks is all numbers in a group are unique (row, column, box)
    def is_valid_group(self, group):
        numbers = [cell.val for cell in group if cell.val != 0]
        return len(numbers) == np.unique(numbers).size
    
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
                if len(self.grid[x][y].possible) == 1 and self.grid[x][y].val == 0:
                    singletons.append((x, y, self.grid[x][y].possible[0]))
        return singletons
    
    def count_possible(self):
        count = 0
        for row in self.grid:
            for cell in row:
                count += len(cell.possible)
        return count


    def set_state(self, row, col, val):
        # Store the initial state of the entire grid
        original_state = copy.deepcopy(self)

        original_state.grid[row][col].possible = [val]
        original_state.grid[row][col].val = val

        for condition in original_state.grid[row][col].conditions:
            if not condition.assign_cell(original_state.grid[row][col]):
                return None

        affected_cells = set()
            # Remove possible value from the same row
        for i in range(9):
            if val in original_state.grid[row][i].possible and original_state.grid[row][i].val == 0:
                original_state.grid[row][i].remove_pos(val)
                affected_cells.add(original_state.grid[row][i])

        # Remove possible value from the same column
        for i in range(9):
            if val in original_state.grid[i][col].possible and original_state.grid[i][col].val == 0:
                original_state.grid[i][col].remove_pos(val)
                affected_cells.add(original_state.grid[i][col])
        
        # Calculate the starting row and column of the 3x3 subgrid
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        
        # Remove possible value from the 3x3 subgrid
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if original_state.grid[i][j].val == 0 and val in original_state.grid[i][j].possible:
                    original_state.grid[i][j].remove_pos(val)
                    affected_cells.add(original_state.grid[i][j])
        
        # Update conditions for affected cells
        for cell in affected_cells:
            for condition in cell.conditions:
                condition.change_possible(cell)


        if original_state.invalid():
            return None

        for r in range(9):
            for c in range(9):
                if original_state.grid[r][c].val == 0 and self.grid[r][c].possible != original_state.grid[r][c].possible:
                    for condition in original_state.grid[r][c].conditions:
                        if not condition.change_possible(original_state.grid[r][c]):
                            return None
        return original_state
    
    def get_grid(self):
        return self.grid

    def set_pos(self, x, y, val):
        self.grid[x][y].val = val

    def add_condition(self, condition):
        if condition not in self.conditions:
            self.conditions[condition] = []
        self.conditions[condition] += condition.cells
        for cell in condition.cells:
            cell.add_condition(condition)

    def __str__(self):
        print("\n")
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
        print("\n")
    
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

