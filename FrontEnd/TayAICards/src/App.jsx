import { useState } from 'react';
import axios from 'axios';
import './App.css';
import Flashcard from './Flashcard';

function App() {
  const [youtubelink, setyoutubelink] = useState('');
  const [responsedata, setresponsedata] = useState([]);
  const [isloading, setloading] = useState(false);
  const [isloadingerror, setloadingerror] = useState(false);
  const [iserror, seterror] = useState('');

  const sendlink = async () => {
    try {
      setloading(true);
      setloadingerror(false); // Reset any previous errors
      const response = await axios.post('http://127.0.0.1:8000/analyze-video', { youtube_link: youtubelink });
      const data = response.data;
      
      if (data.key_concepts) {
        setresponsedata(data.key_concepts);
      } else {
        console.error(`No data in response object: ${data}`);
      }
      
    } catch (error) {
      seterror(error.message || "Link not valid, please try again.");
      setloadingerror(true);
    } finally {
      setloading(false);
    }
  };

  const discardcard = (index) => {
    const updatedData = responsedata.filter((_, i) => i !== index);
    setresponsedata(updatedData);
  };

  const downloadcard = () => {
    const Jsonstring = JSON.stringify(responsedata, null, 2);
    const jsonblob = new Blob([Jsonstring], { type: 'application/json' });

    const link = document.createElement('a');
    link.href = URL.createObjectURL(jsonblob);
    link.download = 'Flashcards.json';
    link.click();

    // Clean up and remove the link element
    URL.revokeObjectURL(link.href);
    link.remove();
  };

  return (
    <div className="App">
      <div className="formcontainer">
        <div className="header">
          <h1>Youtube Link to Flashcards Generator</h1>
        </div>
        <div className="inputsec">
          <input
            type="url"
            value={youtubelink}
            onChange={(e) => setyoutubelink(e.target.value)}
            placeholder="Enter your link here"
            required
          />
          <button type="button" onClick={sendlink}>Submit</button>
        </div>
        <div className="Flashcards">
          {isloadingerror ? (
            <p className="error">{iserror}</p>
          ) : isloading ? (
            <p>Generating Flash Cards...</p>
          ) : (
            responsedata.map((term, index) => (
              <Flashcard 
                key={index} 
                concept={term.concept} 
                definition1={term.definition} 
                onsend={() => discardcard(index)} 
              />
            ))
          )}
        </div>
        {!isloading && responsedata.length > 0 && (
          <button onClick={downloadcard} className="download-button">Download Cards</button>
        )}
      </div>
    </div>
  );
}

export default App;
