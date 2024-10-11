
import { useState } from 'react';
import { arraysEqual } from '../utils';

export function useConditions(initialConditions: { type: string; cells: number[]; sum: number | undefined }[]) {
  const [conditions, setConditions] = useState(initialConditions);

  const addCondition = (type: string, cells: number[], sum: number | undefined) => {
    setConditions(prevConditions => [...prevConditions, { type, cells, sum }]);
  };

  const addKillerSum = (sum: number) => {
    setConditions(prevConditions => {
      if (prevConditions.length === 0) return prevConditions;
      const newConditions = [...prevConditions];
      newConditions[newConditions.length - 1].sum = sum;
      return newConditions;
    });
  };

  
  const removeCondition = (type: string, cells: number[]) => {
    setConditions(prevConditions => prevConditions.filter(
      condition => condition.type !== type || !arraysEqual(condition.cells, cells)
    ));
  };
  return { conditions, addCondition, addKillerSum, removeCondition };
}