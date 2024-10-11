import Cell from './Cell'; // Assuming Cell is another component
import { CellData, Condition } from '../types'; // Assuming these types are defined elsewhere
import  { renderConsecutiveCircles, renderShapes, renderConditions }  from '../Drawing/shapes';

interface GridProps {
  cellData: CellData;
  selectedCells: number[];
  handleCellClick: (index: number, event: React.MouseEvent<Element, MouseEvent>) => void;
  handleCellMouseDown: (index: number, event: React.MouseEvent<Element, MouseEvent>) => void;
  handleCellMouseEnter: (index: number, event: React.MouseEvent<Element, MouseEvent>) => void;
  updateCellValue: (index: number, value: number) => void;
  updateCellPencilMarks: (index: number, value: number) => void;
  conditions: Condition[];
}

const Grid = ({ 
  cellData, 
  selectedCells, 
  handleCellClick, 
  handleCellMouseDown, 
  handleCellMouseEnter, 
  updateCellValue, 
  updateCellPencilMarks, 
  conditions 
}: GridProps) => {
  return (
    
    <div className="relative">
      
      <div className="grid grid-cols-9">
        {Array.from({ length: 81 }).map((_, index) => (
          <Cell
            key={index}
            index={index}
            isSelected={selectedCells.includes(index)}
            value={cellData[index].value}
            pencilMarks={cellData[index].pencilMarks}
            onClick={handleCellClick}
            onMouseDown={handleCellMouseDown}
            onMouseEnter={handleCellMouseEnter}
            onUpdateValue={updateCellValue}
            onUpdatePencilMarks={updateCellPencilMarks}
          />
        ))}
      </div>
      <svg className="absolute top-0 left-0 w-full h-full pointer-events-none">
        {renderConsecutiveCircles(conditions)}
        {renderShapes(conditions)}
        {renderConditions(conditions)}
      </svg>
    </div>
  );
};

export default Grid;