import { Conditions } from './Conditions';
import { sendJsonToBackend } from './api/Transfer';
import { CellData, Condition } from './types';

export const addconsecutiveCondition = (
    selectedCells: number[], 
    conditions: Condition[], 
    addCondition: (type: string, cells: number[], sum: number|undefined) => void,
    removeCondition: (type: string, cells: number[]) => void
) => {
  if (selectedCells.length === 2) {
    const existingCondition = conditions.find(condition => 
      condition.type === Conditions.CONSECUTIVE && arraysEqual(condition.cells, selectedCells)
    );

    if (existingCondition) {
      removeCondition(Conditions.CONSECUTIVE, selectedCells);
    } else {
      addCondition(Conditions.CONSECUTIVE, selectedCells, undefined);
    }
  }
};

const findCondition = (conditions: Condition[], type: string, cell: number) => {
  const result = conditions.find(condition => {
    return condition.type === type && condition.cells[0] === cell;
  });
  return result;
};

export const addEvenCondition = (
    selectedCells: number[], 
    conditions: Condition[], 
    addCondition: (type: string, cells: number[], sum: number|undefined) => void,
    removeCondition: (type: string, cells: number[]) => void
) => {
  if (selectedCells.length === 1) {
    const cell = selectedCells[0];
    const existingEvenCondition = findCondition(conditions, Conditions.EVEN, cell);

    if (existingEvenCondition) {
      removeCondition(Conditions.EVEN, selectedCells);
    } else {
      removeCondition(Conditions.ODD, selectedCells);
      addCondition(Conditions.EVEN, selectedCells, undefined);
    }
  }
};

export const addOddCondition = (
  selectedCells: number[], 
  conditions: Condition[], 
  addCondition: (type: string, cells: number[], sum: number|undefined) => void,
  removeCondition: (type: string, cells: number[]) => void
) => {
if (selectedCells.length === 1) {
  const cell = selectedCells[0];
  const existingOddCondition = findCondition(conditions, Conditions.ODD, cell);

  if (existingOddCondition) {
    removeCondition(Conditions.ODD, selectedCells);
  } else {
    removeCondition(Conditions.EVEN, selectedCells);
    addCondition(Conditions.ODD, selectedCells, undefined);
  }
}
};

export const addPalindromeCondition = (
  selectedCells: number[], 
  conditions: Condition[], 
  addCondition: (type: string, cells: number[], sum: number|undefined) => void,
  removeCondition: (type: string, cells: number[]) => void
) => {
  if (selectedCells.length >= 2) {
    const existingCondition = conditions.find(condition => 
      condition.type === Conditions.PALINDROME && arraysEqual(condition.cells, selectedCells)
    );

    if (existingCondition) {
      removeCondition(Conditions.PALINDROME, selectedCells);
    } else {
      addCondition(Conditions.PALINDROME, selectedCells, undefined);
    }
  }
};

export const addThermoCondition = (
  selectedCells: number[], 
  conditions: Condition[], 
  addCondition: (type: string, cells: number[], sum: number|undefined) => void,
  removeCondition: (type: string, cells: number[]) => void
) => {
  if (selectedCells.length >= 2) {
    const existingCondition = conditions.find(condition => 
      condition.type === Conditions.THERMO && arraysEqual(condition.cells, selectedCells)
    );

    if (existingCondition) {
      removeCondition(Conditions.THERMO, selectedCells);
    } else {
      addCondition(Conditions.THERMO, selectedCells, undefined);
    }
  }
};

export const addKillerCondition = (
  selectedCells: number[], 
  conditions: Condition[], 
  addCondition: (type: string, cells: number[], sum: number|undefined) => void,
  removeCondition: (type: string, cells: number[]) => void,
  changeKillerSum: (value: boolean) => void
) => {
  changeKillerSum(true);
  if (selectedCells.length >= 2) {
    const existingCondition = conditions.find(condition => 
      condition.type === Conditions.KILLER && arraysEqual(condition.cells, selectedCells)
    );

    if (existingCondition) {
      removeCondition(Conditions.KILLER, selectedCells);
    } else {
      addCondition(Conditions.KILLER, selectedCells, 0);
    }
  }
};

export const printGridAndConditions = async (
  cellData: CellData, 
  conditions: Condition[], 
  setCellData: (data: CellData) => void
) => {
const gridValues = Array.from({ length: 9 }, (_, rowIndex) => 
  cellData.slice(rowIndex * 9, rowIndex * 9 + 9).map(cell => cell.value)
);

const conditions2D = conditions.map(({ type, cells, sum }) => ({
  type,
  cells: cells.map(cellIndex => ({
    row: Math.floor(cellIndex / 9),
    col: cellIndex % 9
  })),
  sum
}));

const output = {
  grid: gridValues,
  conditions: conditions2D
};

const solved_grid: number[][] = await sendJsonToBackend(output);
if (solved_grid.length === 0) {
  return;
}
const updatedCellData = solved_grid.flat().map((value: number) => ({ value, pencilMarks: [] }));
setCellData(updatedCellData);
};

export function arraysEqual(arr1: number[], arr2: number[]): boolean {
    if (arr1.length !== arr2.length) return false;
    const sortedArr1 = [...arr1].sort();
    const sortedArr2 = [...arr2].sort();
    for (let i = 0; i < sortedArr1.length; i++) {
      if (sortedArr1[i] !== sortedArr2[i]) return false;
    }
    return true;
}