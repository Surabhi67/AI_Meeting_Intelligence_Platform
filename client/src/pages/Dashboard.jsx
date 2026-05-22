import { useState } from "react";
import MeetingCard from "../components/MeetingCard";
import { mockMeetings } from "../mockdata";
import "./Dashboard.css";
import Navbar from "../components/Navbar";
import { useRef } from "react";

export const Dashboard = () => {
  const [search, setSearch] = useState("");

  const filtered = mockMeetings.filter((m) =>
    m.title.toLowerCase().includes(search.toLowerCase())
  );

  const fileinputRef = useRef(null);

  const handleUpload = () => {
    fileinputRef.current.click();
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if(!file)
        return;
    if(!file.type.startsWith("audio/")){
        alert("Please upload an audio file.");
    }
    else
    {
        console.log("uploading audio..");
    }
  };

  return (
    <div className="dashboard">
      <Navbar/>
      {/* Header */}
      <div className="top-bar">
        <h1 className="title">Meetings</h1>

        <input
          className="search-bar"
          placeholder="Search meetings..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Cards */}
      <div className="meeting-grid">
        {filtered.map((meeting) => (
          <MeetingCard key={meeting.id} meeting={meeting} />
        ))}
      </div>
        <input
        type="file"
        ref={fileinputRef}
        onChange={handleFileChange}
        accept="audio/*"
        style={{ display: "none" }}
        />
      {/* Floating Upload Button */}
      <button className="fab" 
      onClick = {handleUpload}
      >+
      </button>
    </div>
  );
}