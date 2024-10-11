from itertools import combinations

class Condition:

    def _init__(self):
        self.cells = []

    # To be overriden
    def check(self):  
        pass

class Odd(Condition):

    def __init__(self, cells):
        self.cells = cells
    
    def setup(self, cell):
        cell.possible = [val for val in cell.possible if val % 2 != 0]
        if len(cell.possible) > 0:
            return True
        return False
    
    def change_possible(self, cell):
        return True
    
    def assign_cell(self, cell):
        return True
    
class Even(Condition):

    def __init__(self, cells):
        self.cells = cells
    
    def setup(self, cell):
        cell.possible = [val for val in cell.possible if val % 2 == 0]
        if len(cell.possible) > 0:
            return True
        return False
    
    def change_possible(self, cell):
        return True

    def assign_cell(self, cell):
        return True
    
class Palindrome:
    def __init__(self, cells):
        self.cells = cells  # In order they would appear in a palindrome
        self.cell_map = {cell: cells[-i - 1] for i, cell in enumerate(cells)}

    def setup(self, cell):
        return True

    def change_possible(self, cell):
        if cell in self.cell_map:
            palindrome_cell = self.cell_map[cell]
            palindrome_cell.possible = [pos for pos in palindrome_cell.possible if pos in cell.possible]
            if len(palindrome_cell.possible) == 0:
                return False
        return True

    def assign_cell(self, cell):
        if cell in self.cell_map:
            palindrome_cell = self.cell_map[cell]
            if cell.val not in palindrome_cell.possible:
                return False
            palindrome_cell.possible = [cell.val]
        return True

# ahhhdjidhbujHUJIKHBJFNKL
class Killer_Sum(Condition):

    def __init__(self, cells, target):
        self.cells = cells
        self.target = target
        self.combinations = [com for com in (combinations(range(1, 10), len(cells))) if sum(com) == target]

    def setup(self, cell):
        unique_items = set()
        for comb in self.combinations:
            for item in comb:
                unique_items.add(item)
        for cell in self.cells:
            cell.possible = [val for val in cell.possible if val in unique_items]
            if len(cell.possible) == 0:
                return False
        return True

    def change_possible(self, cell):
        return True

    def assign_cell(self, cell):
        new_val = cell.val
        for comb in self.combinations:
            if cell.val in comb:
                for cell in self.cells:
                    if cell.val == 0:
                        cell.possible = [val for val in cell.possible if val in comb and val != new_val]
                        if len(cell.possible) == 0:
                            return False
        return True

class Thermo(Condition):

    def __init__(self, cells):
        self.cells = cells # In order
    
    def setup(self, cell):
        return True

    # Might need more complicated logic later, smth to do with relative indexxing
    def change_possible(self, cell):
        index = self.cells.index(cell)
        for i in range(len(self.cells)):
            if i < index and self.cells[i].val == 0:
                self.cells[i].possible = [pos for pos in self.cells[i].possible if pos <= (max(cell.possible) - (index-i))]
            elif i > index and self.cells[i].val == 0:
                self.cells[i].possible = [pos for pos in self.cells[i].possible if pos >= (min(cell.possible) + (i-index))]
            if len(self.cells[i].possible) == 0 and self.cells[i].val == 0:
                return False
        return True
    
    def assign_cell(self, cell):
        index_of_cell = self.cells.index(cell)
        for i in range(len(self.cells)):
            if i < index_of_cell and self.cells[i].val == 0:
                self.cells[i].possible = [pos for pos in self.cells[i].possible if pos < cell.val]
                if len(self.cells[i].possible) == 0:
                    return False
            elif i > index_of_cell and self.cells[i].val == 0:
                self.cells[i].possible = [pos for pos in self.cells[i].possible if pos > cell.val]
                if len(self.cells[i].possible) == 0:
                    return False
        return True
    
class Consecutive(Condition):
    # Multiple consecutive classes, in  this case is always going to be a pair of cells.
    def __init__(self, cells):
        self.cells = cells

    def setup(self, cell):
        return True
    
    # If a cell's possible values has changed, this can affect other cells in linked condition
    def change_possible(self, cell):
        for adj_cell in self.cells:
            if adj_cell.y != cell.y or adj_cell.x != cell.x and adj_cell.val == 0:
                adj_cell.possible = [pos for pos in adj_cell.possible if pos + 1 in cell.possible or pos - 1 in cell.possible]
                if len(adj_cell.possible) == 0:
                    return False
        return True

    def assign_cell(self, cell):
        for adj_cell in self.cells:
            if adj_cell.y != cell.y or adj_cell.x != cell.x and adj_cell.val == 0:
                adj_cell.possible = [pos for pos in adj_cell.possible if pos + 1 == cell.val or pos - 1 == cell.val]
                if len(adj_cell.possible) == 0:
                    return False
        return True

            
class NonConsecutive(Condition):

    def __init__(self, cells):
        self.cells = cells

    def check(self):
        for i in range(len(self.cells) - 1):
            if abs(self.cells[i].val - self.cells[i + 1].val) == 1:
                return False
        return True
