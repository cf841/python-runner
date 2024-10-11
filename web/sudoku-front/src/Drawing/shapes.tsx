import { Conditions } from '../Conditions'; // Adjust the import path as necessary
import { Condition } from '../types'; // Adjust the import path as necessary
import '../index.css';

export const renderConsecutiveCircles = (conditions: Condition[]) => {
    const cellSize = 80; // Assuming each cell is 40x40 pixels
    const offset = cellSize / 2;

    return conditions.filter(condition => condition.type === Conditions.CONSECUTIVE).map(condition => {
      const [cell1, cell2] = condition.cells;
      const row1 = Math.floor(cell1 / 9);
      const col1 = cell1 % 9;
      const row2 = Math.floor(cell2 / 9);
      const col2 = cell2 % 9;

      const x1 = col1 * cellSize + offset;
      const y1 = row1 * cellSize + offset;
      const x2 = col2 * cellSize + offset;
      const y2 = row2 * cellSize + offset;

      const cx = (x1 + x2) / 2;
      const cy = (y1 + y2) / 2;

      return <circle key={`${cell1}-${cell2}`} cx={cx} cy={cy} r={5} fill="red" />;
    });
};

export const renderShapes = (conditions: Condition[]) => {
  const cellSize = 80; // Assuming each cell is 80x80 pixels
  const offset = cellSize / 2;
  const shapeSize = cellSize * 0.8; // Fill 80% of the cell
  const shapeOffset = shapeSize / 2;

  return conditions.map(condition => {
      const [cell] = condition.cells;
      const row = Math.floor(cell / 9);
      const col = cell % 9;

      const x = col * cellSize + offset;
      const y = row * cellSize + offset;

      if (condition.type === Conditions.EVEN) {
          return (
              <rect className="shape" key={cell+100} x={x - shapeOffset} y={y - shapeOffset} width={shapeSize} height={shapeSize} fill="lightgrey" />
          );
      } else if (condition.type === Conditions.ODD) {
          return (
              <circle className="shape" key={cell+200} cx={x} cy={y} r={shapeSize / 2} fill="lightgrey" />
          );
      } else {
          return null;
      }
  });
};

export const renderKillerCage = (conditions: Condition[]) => {
    const cellSize = 80; // Assuming each cell is 80x80 pixels
    const padding = 4; // Padding to be just inside the border

    const killerConditions = conditions.filter(condition => condition.type === Conditions.KILLER);

    return killerConditions.map(condition => {
        const cells = condition.cells;
        const positions = cells.map(cell => {
            const row = Math.floor(cell / 9);
            const col = cell % 9;
            return { x: col * cellSize, y: row * cellSize };
        });

        // Create a set of all cell positions for quick lookup
        const positionSet = new Set(positions.map(pos => `${pos.x},${pos.y}`));

        // Function to check if a cell exists at a given position
        const cellExists = (x, y) => positionSet.has(`${x},${y}`);

        // Determine the path that outlines the cells
        let pathData = '';
        positions.forEach(pos => {
            const x = pos.x + padding;
            const y = pos.y + padding;
            const right = x + cellSize - 2 * padding;
            const bottom = y + cellSize - 2 * padding;

            // Top edge
            if (!cellExists(pos.x, pos.y - cellSize)) {
                pathData += `M${x},${y} L${right},${y} `;
            }
            // Right edge
            if (!cellExists(pos.x + cellSize, pos.y)) {
                pathData += `M${right},${y} L${right},${bottom} `;
            }
            // Bottom edge
            if (!cellExists(pos.x, pos.y + cellSize)) {
                pathData += `M${right},${bottom} L${x},${bottom} `;
            }
            // Left edge
            if (!cellExists(pos.x - cellSize, pos.y)) {
                pathData += `M${x},${bottom} L${x},${y} `;
            }
        });

        const topLeftCell = positions.reduce((minPos, pos) => {
            if (pos.y < minPos.y || (pos.y === minPos.y && pos.x < minPos.x)) {
                return pos;
            }
            return minPos;
        }, positions[0]);

        return (
            <>
            <path
                key={cells.join('-')}
                d={pathData}
                fill="none"
                stroke="black"
                strokeWidth="2"
                strokeDasharray="4"
            />
            <text
                    x={topLeftCell.x + padding + 10}
                    y={topLeftCell.y + padding + 20} // Adjust y position to fit within the cell
                    fill="lightgrey"
                    fontSize="14"
                    fontFamily="Arial"
                >
                    {condition.sum}
                </text>
            </>
        );
    });
};

export const renderConditions = (conditions: Condition[]) => {
    const cellSize = 80; // Assuming each cell is 80x80 pixels
    const offset = cellSize / 2;

    const renderPalindromeCondition = conditions.filter(condition => condition.type === Conditions.PALINDROME).map(condition => {
        const cells = condition.cells;
        const positions = cells.map(cell => {
            const row = Math.floor(cell / 9);
            const col = cell % 9;
            return { x: col * cellSize + offset, y: row * cellSize + offset };
        });

        const points = positions.map(pos => `${pos.x},${pos.y}`).join(' ');

        return <polyline key={cells.join('-')} points={points} stroke="lightgrey" strokeWidth="5" fill="none" />;
    });

    const renderThermoCondition = conditions.filter(condition => condition.type === Conditions.THERMO).map(condition => {
        const cells = condition.cells;
        const positions = cells.map(cell => {
            const row = Math.floor(cell / 9);
            const col = cell % 9;
            return { x: col * cellSize + offset, y: row * cellSize + offset };
        });

        const points = positions.map(pos => `${pos.x},${pos.y}`).join(' ');

        return (
            <g key={cells.join('-')}>
                <circle cx={positions[0].x} cy={positions[0].y} r={cellSize / 4} fill="lightgrey" />
                <polyline points={points} stroke="lightgrey" strokeWidth="5" fill="none" />
            </g>
        );
    });

    const renderKillerCageCondition = renderKillerCage(conditions);

    return (
        <>
            {renderPalindromeCondition}
            {renderThermoCondition}
            {renderKillerCageCondition}
        </>
    );
};