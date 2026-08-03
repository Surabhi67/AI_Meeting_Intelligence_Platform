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
        Meeting Summarizer
      </div>

      <div className="navbar-right">
        

        <div className="profile-circle">
          S
        </div>
      </div>
    </nav>
  );
}