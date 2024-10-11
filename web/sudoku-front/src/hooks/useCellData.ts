import { useState } from 'react';

export function useCellData(initialData: { value: number, pencilMarks: number[] }[]) {
    const [cellData, setCellData] = useState(initialData);
  
    const updateCellValue = (index: number, value: number) => {
      setCellData(prevData => {
        const newData = [...prevData];
        const currentValue = newData[index].value;
        newData[index] = { ...newData[index], value: currentValue === value ? 0 : value };
        return newData;
      });
    };
  
    const updateCellPencilMarks = (index: number, pencilMark: number) => {
      if (pencilMark === 0) {
        setCellData(prevData => {
          const newData = [...prevData];
          newData[index] = { ...newData[index], pencilMarks: [] };
          return newData;
        });
      } else {
        setCellData(prevData => {
          const newData = [...prevData];
          const newPencilMarks = [...newData[index].pencilMarks];
          if (newPencilMarks.includes(pencilMark)) {
            newPencilMarks.splice(newPencilMarks.indexOf(pencilMark), 1);
          } else {
            newPencilMarks.push(pencilMark);
          }
          newData[index] = { ...newData[index], pencilMarks: newPencilMarks };
          return newData;
        });
      }
    };
    return { cellData, setCellData, updateCellValue, updateCellPencilMarks };
}