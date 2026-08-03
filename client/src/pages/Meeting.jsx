import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./Meeting.css";

export const Meeting = () => {
  const { id } = useParams();

  const [meeting, setMeeting] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/meetings/${id}`)
      .then((res) => res.json())
      .then((data) => {
        setMeeting(data);
      })
      .catch((err) => console.log(err));


    fetch(`http://127.0.0.1:8000/meetings/${id}/audio`)
      .then((res) => res.json())
      .then((data) => {
        setAudioUrl(data.audio_url);
      })
      .catch((err) => console.log(err));

  }, [id]);


  if (!meeting) {
    return <p>Loading...</p>;
  }


  return (
    <div className="meeting-page">

      <div className="meeting-header">
        <h1>{meeting.title}</h1>

        <span className="status">
          {meeting.status}
        </span>
      </div>


      <div className="audio-card">
        <h2>🎧 Audio Recording</h2>

        {audioUrl && (
          <audio controls>
             <source src={audioUrl} type="audio/wav" />
          </audio>
        )}
      </div>


      <div className="summary-card">
        <h2>Summary</h2>

        <p>
          {meeting.summary || "No summary available"}
        </p>
      </div>


      <div className="transcript-card">
        <h2>Transcript</h2>

        <p>
          {meeting.transcript || "Transcript will appear here."}
        </p>
      </div>

    </div>
  );
};