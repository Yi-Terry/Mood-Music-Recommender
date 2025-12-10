import './App.css';

import React, { useState } from 'react';
import axios from "axios"

function App() {

  const [file,setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
      setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select and image!");

    const formData = new FormData();
    formData.append("file",file);

    try{
      setLoading(true);
        const response = await axios.post(
        "http://127.0.0.1:8000/detect-mood", // FastAPI endpoint
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setResult(response.data);
    }catch (err){
        console.error(err);
        alert("Error Uploading Image.")
    } finally{
      setLoading(false);
    }
  };
  return (
    <div style={{ maxWidth: "500px", margin: "50px auto", textAlign: "center" }}>
      <h1>Mood-Based Music Recommender</h1>

      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading} style={{ marginLeft: "10px" }}>
        {loading ? "Analyzing..." : "Upload"}
      </button>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h2>Detected Mood: {result.mood}</h2>

          <h3>Recommended Songs:</h3>
          {result.songs && result.songs.length > 0 ? (
            <ul>
              {result.songs.map((song, idx) => (
                <li key={idx}>{song}</li>
              ))}
            </ul>
          ) : (
            <p>No song recommendations available.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
