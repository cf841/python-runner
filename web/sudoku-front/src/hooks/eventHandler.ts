import { handleDocumentClick, handleKeyPress } from './events';
import { CellData } from '../types';

import { useEffect } from 'react';

export const EventHandler = (
  selectedCells: number[], 
  setSelectedCells: (cells: number[]) => void, 
  entryMode: 'digit' | 'pencil',
  isKillerSum: boolean,
  changeKillerSum: (value: boolean) => void,
  cellData: CellData, 
  updateCellValue: (index: number, value: number) => void, 
  updateCellPencilMarks: (index: number, value: number) => void,
  removeCondition: (type: string, cells: number[]) => void,
  addKillerSum: (value: number) => void
) => {
  useEffect(() => {
    const documentClickHandler = (event: MouseEvent) => handleDocumentClick(event, changeKillerSum, setSelectedCells);
    document.addEventListener('click', documentClickHandler);
    return () => {
      document.removeEventListener('click', documentClickHandler);
    };
  }, [setSelectedCells, changeKillerSum]);

  useEffect(() => {
    const keyPressHandler = (e: KeyboardEvent) => handleKeyPress(e, selectedCells, entryMode, isKillerSum, cellData, addKillerSum, updateCellValue, updateCellPencilMarks, removeCondition);

    if (selectedCells.length > 0) {
      window.addEventListener('keydown', keyPressHandler);
    } else {
      window.removeEventListener('keydown', keyPressHandler);
    }

    return () => {
      window.removeEventListener('keydown', keyPressHandler);
    };
  }, [selectedCells, entryMode, cellData, updateCellValue, updateCellPencilMarks, removeCondition, addKillerSum, isKillerSum]);
};