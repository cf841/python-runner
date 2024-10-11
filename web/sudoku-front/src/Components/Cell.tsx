import React from 'react';
import '../index.css';

interface CellProps {
  index: number;
  isSelected: boolean;
  value: number;
  pencilMarks: number[];
  onClick: (index: number, event: React.MouseEvent<Element, MouseEvent>) => void;
  onMouseDown: (index: number, event: React.MouseEvent<Element, MouseEvent>) => void;
  onMouseEnter: (index: number, event: React.MouseEvent<Element, MouseEvent>) => void;
  onUpdateValue: (index: number, value: number) => void;
  onUpdatePencilMarks: (index: number, pencilMarks: number) => void;
}

const Cell: React.FC<CellProps> = ({ index, isSelected, value, pencilMarks, onClick, onMouseDown, onMouseEnter}) => {

  // Determine if the cell is on the right or bottom edge of a 3x3 box
  const isRightEdge = (index + 1) % 3 === 0 && (index + 1) % 9 !== 0;
  const isBottomEdge = Math.floor(index / 9) % 3 === 2 && index < 72;

  return (
    <div
      className={`cell ${isSelected ? 'cell-selected' : ''} ${isRightEdge ? 'border-right' : ''} ${isBottomEdge ? 'border-bottom' : ''}`}
      onClick={(event) => onClick(index, event)}
      onMouseDown={(event) => onMouseDown(index, event)}
      onMouseEnter={(event) => onMouseEnter(index, event)}
      data-index={index}
    >
      {value !== 0 ? (
        <span className="values">{value}</span>
      ) : (
        <div className="pencil-marks-container">
          <div className="pencil-marks-grid">
            {pencilMarks.sort().map((mark, i) => (
              <div key={i} className="pencil-mark">
                {mark}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Cell;