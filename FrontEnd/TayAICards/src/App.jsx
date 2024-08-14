import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [youtubelink, setyoutubelink] = useState('');
  const [responsedata, setresponsedata] = useState('');
  const [count, setCount] = useState(0);

  const sendlink = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/analyze-video', { youtube_link: youtubelink });
      const data= response.data;
      console.log({data})
      if (data.key_concepts)
          {const keyconceptsarray = Array.isArray(responsedata);
         setresponsedata(keyconceptsarray);
         console.log({keyconceptsarray});}

      else{
        console.log.error(`no data in response object:${data}`)

      }





    } catch (error) {
      console.error("Response was not posted", error);
    }


  };

  return (
    <div className="App">
      <div className="formcontainer">
     <div className='header'><h1>Youtube Link to Flashcards Generator</h1></div> 
     <div className="inputsec"><input
        type="url" 
        value={youtubelink}
        onChange={(e) => setyoutubelink(e.target.value)}
        placeholder="Enter your link here"
        required
      />
      <button type="button" onClick={sendlink}>Submit</button></div>
      <div className="Flashcards"> 
      {responsedata && (
        <div>
          <h2>Response Data</h2>
          <p>{JSON.stringify(responsedata, null, 2)}</p>
        </div>
      )}
    </div></div></div>
  );
}

export default App;
