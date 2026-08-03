import { useState, useEffect, useRef } from "react";
import MeetingCard from "../components/MeetingCard";
import "./Dashboard.css";
import Navbar from "../components/Navbar";

export const Dashboard = () => {
  const [search, setSearch] = useState("");
  const [meetings, setMeetings] = useState([]);

  const fileInputRef = useRef(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/meetings")
      .then((res) => res.json())
      .then((data) => {
        console.log("MEETINGS FROM BACKEND:", data);
        setMeetings(data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);


  const filtered = meetings.filter((m) =>
    m.title.toLowerCase().includes(search.toLowerCase())
  );


  const handleUpload = () => {
    fileInputRef.current.click();
  };


  const handleFileChange = async (e) => {
    const file = e.target.files[0];

    if (!file) return;

    if (!file.type.startsWith("audio/")) {
      alert("Please upload an audio file.");
      return;
    }

    console.log("Uploading:", file.name);


    const formData = new FormData();
    formData.append("file", file);


    try {
      const response = await fetch(
        "http://127.0.0.1:8000/meetings/upload",
        {
          method: "POST",
          body: formData,
        }
      );


      if (!response.ok) {
        throw new Error("Upload failed");
      }


      const data = await response.json();

      console.log("UPLOAD RESPONSE:", data);


      // refresh meetings list
      const updated = await fetch(
        "http://127.0.0.1:8000/meetings"
      );

      const updatedMeetings = await updated.json();

      setMeetings(updatedMeetings);


    } catch (error) {
      console.log("Upload error:", error);
      alert("Upload failed");
    }
  };


  return (
    <div className="dashboard">

      <Navbar />

      <div className="top-bar">

        <h1 className="title">
          Meetings
        </h1>


        <input
          className="search-bar"
          placeholder="Search meetings..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

      </div>


      <div className="meeting-grid">

        {filtered.map((meeting) => (
          <MeetingCard
            key={meeting.id}
            meeting={meeting}
          />
        ))}

      </div>


      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="audio/*"
        style={{ display: "none" }}
      />


      <button
        className="fab"
        onClick={handleUpload}
      >
        +
      </button>


    </div>
  );
};