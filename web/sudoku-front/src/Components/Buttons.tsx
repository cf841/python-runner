interface ButtonsProps {
    entryMode: 'digit' | 'pencil';
    setEntryMode: (entryMode: 'digit' | 'pencil') => void;
    addconsecutiveCondition: () => void;
    addEvenCondition: () => void;
    addOddCondition: () => void;
    addPalindromeCondition: () => void;
    addThermoCondition: () => void;
    addKillerCondition: () => void;
    printGridAndConditions: () => void;
    }

const Buttons = ({ 
    entryMode, 
    setEntryMode, 
    addconsecutiveCondition, 
    addEvenCondition,
    addOddCondition,
    addPalindromeCondition,
    addThermoCondition,
    addKillerCondition,
    printGridAndConditions }: ButtonsProps) => {
  return (
    <div className="button-container">
      <button
        className={`button ${entryMode === 'digit' ? 'bg-blue-700' : ''}`}
        onClick={() => setEntryMode('digit')}
      >
        Digit Entry
      </button>
      <button
        className={`button ${entryMode === 'pencil' ? 'bg-blue-700' : ''}`}
        onClick={() => setEntryMode('pencil')}
      >
        Pencil Entry
      </button>
      <button className="button" onClick={addconsecutiveCondition}>consecutive</button>
      <button className="button" onClick={addEvenCondition}>even</button>
      <button className="button" onClick={addOddCondition}>odd</button>
      <button className="button" onClick={addPalindromeCondition}>palindrome</button>
      <button className="button" onClick={addThermoCondition}>thermo</button>
      <button className="button" onClick={addKillerCondition}>killer</button>
      <button className="button" onClick={printGridAndConditions}>Print Grid & conditions</button>
    </div>
  );
};

export default Buttons;