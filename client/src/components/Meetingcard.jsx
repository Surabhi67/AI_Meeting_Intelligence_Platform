import { useNavigate } from "react-router-dom";

export default function MeetingCard({ meeting }) {
  const navigate = useNavigate();

  return (
    <div
      className="meeting-card"
      onClick={() => navigate(`/meeting/${meeting.id}`)}
    >
      <h3>{meeting.title}</h3>
      <p className="date">{meeting.created_at}</p>

      {meeting.summary && (
        <p className="summary">{meeting.summary}</p>
      )}
    </div>
  );
}