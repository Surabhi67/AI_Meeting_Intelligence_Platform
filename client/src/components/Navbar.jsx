// src/components/Navbar.jsx

import { useNavigate } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  const navigate = useNavigate();

  return (
    <nav className="navbar">
      <div
        className="navbar-logo"
        onClick={() => navigate("/dashboard")}
      >
        🎙️ MeetingAI
      </div>

      <div className="navbar-right">
        <button
          className="new-meeting-btn"
          onClick={() => console.log("upload")}
        >
          + New Meeting
        </button>

        <div className="profile-circle">
          S
        </div>
      </div>
    </nav>
  );
}