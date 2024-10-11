from flask import Flask, request, jsonify
from flask_cors import CORS
from Sudoku import Sudoku, Cell
import Solver
import Conditions
import time

app = Flask(__name__)
CORS(app,  resources={r"/*": {"origins": "*"}})

def create_sudoku_from_json(json_data):
    sudoku = Sudoku()
    for y in range(9):
        for x in range(9):
            val = json_data[x][y]
            if val != 0:
                sudoku.set_pos(x, y, val)
    return sudoku

@app.route('/solve', methods=['POST'])
def solve_sudoku():
    start_time = time.time()

    json_data = request.json
    sudoku = create_sudoku_from_json(json_data['grid'])
    if 'conditions' in json_data:
        for condition in json_data['conditions']:
            cell_array = []
            for cell in condition['cells']:
                cell_array.append(sudoku.grid[cell['row']][cell['col']])
            print(condition)
            if condition['type'] == 'consecutive':
                sudoku.add_condition(Conditions.Consecutive(cell_array))
            elif condition['type'] == 'odd':
                print(cell_array)
                sudoku.add_condition(Conditions.Odd(cell_array))
            elif condition['type'] == 'even':
                sudoku.add_condition(Conditions.Even(cell_array))
            elif condition['type'] == 'palindrome':
                sudoku.add_condition(Conditions.Palindrome(cell_array))
            elif condition['type'] == 'thermo':
                sudoku.add_condition(Conditions.Thermo(cell_array))
            elif condition['type'] == 'killer':
                sudoku.add_condition(Conditions.Killer_Sum(cell_array, condition['sum']))
            # Add more condition types as needed
    # for r in range(9):
    #     for c in range(9):
    #         if sudoku.grid[r][c].val != 0:
    #             print("grid.set_pos(" + str(r) + ", " + str(c) + ", " + str(sudoku.grid[r][c].val) + ")")


    sudoku.setup()
    solver = Solver.Solver()
    output = solver.solver(sudoku)
    grid_return = [[0 for _ in range(9)] for _ in range(9)]
    for r in range(9):
        for c in range(9):
            grid_return[r][c] = output.grid[r][c].val # If go back to deepcopy, make this output
            
    for r in range(9):
        for c in range(9):
            if not sudoku.grid[r][c].possible and sudoku.grid[r][c].val == 0: 
                print(f"Cell at row {r}, column {c} has no possibilities")
    end_time = time.time()
    duration = end_time - start_time
    print(f"Solve Sudoku duration: {duration:.4f} seconds")
    print(grid_return)
    return jsonify(grid_return)

if __name__ == '__main__':
    app.run(debug=True)