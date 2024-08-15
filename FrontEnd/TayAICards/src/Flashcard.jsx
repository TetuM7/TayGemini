import './Flashcard.css';

export default function Flashcard({ concept, definition1, onsend }) {
  return (
    <div className="card">
      <h1 className="card-title">{concept}</h1>
      <p className="card-definition">{definition1}</p>
      <button onClick={onsend} className="card-button">Discard</button>
    </div>
  );
}
