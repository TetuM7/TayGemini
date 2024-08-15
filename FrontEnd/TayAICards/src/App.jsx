import { useState } from 'react';
import axios from 'axios';
import './App.css';
import Flashcard from './Flashcard';

function App() {
  const [youtubelink, setyoutubelink] = useState('');
  const [responsedata, setresponsedata] = useState([]);
  const [isloading, setloading] = useState( false);

  const sendlink = async () => {
    try {
      setloading(true);
      const response = await axios.post('http://127.0.0.1:8000/analyze-video', { youtube_link: youtubelink });
      const data = response.data;
      
      if (data.key_concepts) {
        setresponsedata(data.key_concepts);
      } else {
        console.error(`No data in response object: ${data}`);
      }
      
    } catch (error) {
      console.error("Response was not posted", error);
    } finally {
      setloading(false);
    }
  };

  const discardcard = (index) => {
    const updatedData = responsedata.filter((_, i) => i !== index);
    setresponsedata(updatedData);
  };

  const downloadcard=()=>{

    //convert to strung
    const Jsonstring= JSON.stringify(responsedata,null,2)
    const jsonblob= new Blob([Jsonstring],{ type: 'application/json' })

    const link = document.createElement('a');
    link.href = URL.createObjectURL(jsonblob);
    link.download = 'TAYAIdata.json'; 
    link.click();
    
    // Clean up and remove the link element
    URL.revokeObjectURL(link.href);
    link.remove();

  }

  return (
    <div className="App">
      <div className="formcontainer">
        <div className='header'><h1>Youtube Link to Flashcards Generator</h1></div>
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
          {isloading ? (
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
        {isloading ? (<div> </div>):(
          <button onClick={downloadcard} className="download-button">Download Cards</button>
        ) }
      </div>
    </div>
  );
}

export default App;
