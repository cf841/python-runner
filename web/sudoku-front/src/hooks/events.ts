import { CellData } from '../types';
let killerSumInput = '';
export const handleCellClick = (
  index: number,
  setSelectedCells: (callback: (prevSelected: number[]) => number[]) => void,
  isDragging: boolean,
  event: React.MouseEvent<Element, MouseEvent>
) => {
  if (!isDragging) {
    if (event.shiftKey) {
      setSelectedCells((prevSelected) => {
        if (!prevSelected.includes(index)) {
          return [...prevSelected, index];
        }
        return prevSelected;
      });
    } else {
      setSelectedCells( () => [index]);
    }
  }
};

export const handleCellMouseDown = (
  index: number,
  setIsDragging: (isDragging: boolean) => void,
  setSelectedCells: (callback: (prevSelected: number[]) => number[]) => void,
  event: React.MouseEvent<Element, MouseEvent>
) => {
  setIsDragging(true);
  if (event.shiftKey) {
    setSelectedCells((prevSelected) => {
      if (!prevSelected.includes(index)) {
        return [...prevSelected, index];
      }
      return prevSelected;
    });
  } else {
    setSelectedCells(() => [index]);
  }
};

export const handleCellMouseEnter = (
  index: number,
  isDragging: boolean,
  setSelectedCells: (callback: (prevSelected: number[]) => number[]) => void,
  event: React.MouseEvent<Element, MouseEvent>
) => {
  if (isDragging) {
    if (event.shiftKey) {
      setSelectedCells((prevSelected) => {
        if (!prevSelected.includes(index)) {
          return [...prevSelected, index];
        }
        return prevSelected;
      });
    } else {
      setSelectedCells((prevSelected) => {
        if (!prevSelected.includes(index)) {
          return [...prevSelected, index];
        }
        return prevSelected;
      });
    }
  }
};

export const handleMouseUp = (setIsDragging: (isDragging: boolean) => void) => {
  setIsDragging(false);
};

export const handleDocumentClick = (
  event: MouseEvent, 
  changeKillerSum: (value: boolean) => void,
  setSelectedCells: (cells: number[]) => void
) => {
  const gridElement = document.querySelector('.grid');
  const targetElement = event.target as HTMLElement;
  
  if (gridElement && !gridElement.contains(targetElement) && targetElement.tagName !== 'BUTTON') {
    setSelectedCells([]);
    changeKillerSum(false);
  }
};

export const handleKeyPress = (
  event: KeyboardEvent, 
  selectedCells: number[],
  entryMode: 'digit' | 'pencil', 
  isKillerSum: boolean,
  cellData: CellData, 
  addKillerSum: (value: number) => void,
  updateCellValue: (index: number, value: number) => void, 
  updateCellPencilMarks: (index: number, value: number) => void,
  removeCondition: (type: string, cells: number[]) => void
) => {
  if (event.key === 'Backspace') {
    selectedCells.forEach(index => {
      updateCellValue(index, 0);
      updateCellPencilMarks(index, 0);
      removeCondition('odd', [index]);
      removeCondition('even', [index]);
      removeCondition('consecutive', selectedCells);
      removeCondition('palindrome', selectedCells);
      removeCondition('thermo', selectedCells);
      removeCondition('killer', selectedCells);
    });
  }
  
  const newValue = parseInt(event.key, 10);
  if (!isNaN(newValue) && newValue >= 0 && newValue <= 9) {
    if (isKillerSum) {
      console.log(killerSumInput);
      killerSumInput += event.key;
    } else if (newValue >= 1) {
      selectedCells.forEach(index => {
        if (entryMode === 'digit') {
          if (newValue === cellData[index].value) {
            updateCellValue(index, 0);
          } else {
            updateCellValue(index, newValue);
          }
          updateCellPencilMarks(index, 0);
        } else {
          updateCellPencilMarks(index, newValue);
        }
      });
    }
  } else if (event.key === 'Tab' && isKillerSum) {
    const sumValue = parseInt(killerSumInput, 10);
    if (!isNaN(sumValue)) {
      addKillerSum(sumValue);
      killerSumInput = '';
    }
  }

};