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
      setresponsedata(response.data); // Updated to get the response data
    } catch (error) {
      console.error("Response was not posted", error);
    }
  };

  return (
    <div className="App">
      <h1>Link Input Form</h1>
      <input
        type="url"
        value={youtubelink}
        onChange={(e) => setyoutubelink(e.target.value)}
        placeholder="Enter your link here"
        required
      />
      <button type="button" onClick={sendlink}>Submit</button>
      {responsedata && (
        <div>
          <h2>Response Data</h2>
          <p>{JSON.stringify(responsedata, null, 2)}</p>
        </div>
      )}
    </div>
  );
}

export default App;
