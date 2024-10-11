import React, { useState} from 'react';
import './index.css';
import { useCellData } from './hooks/useCellData';
import { useConditions } from './hooks/useCondition';
import { EventHandler } from './hooks/eventHandler';
import { addconsecutiveCondition, addEvenCondition, addOddCondition, addPalindromeCondition, addThermoCondition, printGridAndConditions, addKillerCondition } from './utils';
import { handleCellClick, handleCellMouseDown, handleCellMouseEnter } from './hooks/events';
import Grid from './Components/Grid';
import Buttons from './Components/Buttons';

function App() {
  const [entryMode, setEntryMode] = useState<'digit' | 'pencil'>('digit');
  const [selectedCells, setSelectedCells] = useState<number[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isKillerSum, setIsKillerSum] = useState(false);
  const initialCellData = Array.from({ length: 81 }).map(() => ({ value: 0, pencilMarks: [] }));
  const { cellData, setCellData, updateCellValue, updateCellPencilMarks } = useCellData(initialCellData);
  const { conditions, addCondition, removeCondition, addKillerSum } = useConditions([]);

  EventHandler(selectedCells, setSelectedCells, entryMode, isKillerSum, setIsKillerSum, cellData, updateCellValue, updateCellPencilMarks, removeCondition, addKillerSum);
  return (
    <div className="container" style={{userSelect: 'none'}} onMouseUp={() => setIsDragging(false)}>
      <h1 className="header">Sudoku</h1>
      <div className="flex flex-row items-center justify-center">
        <Buttons
          entryMode={entryMode}
          setEntryMode={setEntryMode}
          addconsecutiveCondition={() => addconsecutiveCondition(selectedCells, conditions, addCondition, removeCondition)}
          addEvenCondition={() => addEvenCondition(selectedCells, conditions, addCondition, removeCondition)}
          addOddCondition={() => addOddCondition(selectedCells, conditions, addCondition, removeCondition)}
          addPalindromeCondition={() => addPalindromeCondition(selectedCells, conditions, addCondition, removeCondition)}
          addThermoCondition={() => addThermoCondition(selectedCells, conditions, addCondition, removeCondition)}
          addKillerCondition={() => addKillerCondition(selectedCells, conditions, addCondition, removeCondition, setIsKillerSum)}
          printGridAndConditions={() => printGridAndConditions(cellData, conditions, setCellData)}
        />
        <Grid
          cellData={cellData}
          selectedCells={selectedCells}
          handleCellClick={(index: number, event: React.MouseEvent<Element, MouseEvent>) => handleCellClick(index, setSelectedCells, isDragging, event)}
          handleCellMouseDown={(index: number, event: React.MouseEvent<Element, MouseEvent>) => handleCellMouseDown(index, setIsDragging, setSelectedCells, event)}
          handleCellMouseEnter={(index: number, event: React.MouseEvent<Element, MouseEvent>) => handleCellMouseEnter(index, isDragging, setSelectedCells, event)}
          updateCellValue={updateCellValue}
          updateCellPencilMarks={updateCellPencilMarks}
          conditions={conditions}
        />
      </div>
    </div>
  );
}

export default App;