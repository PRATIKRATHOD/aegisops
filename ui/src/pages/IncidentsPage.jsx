import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiGet } from "../api/apiClient";

export default function IncidentsPage() {
  const [incidents, setIncidents] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    async function load() {
      try {
        const data = await apiGet("/incidents");
        setIncidents(data);
      } catch (err) {
        console.error("Failed to load incidents:", err);
      }
    }
    load();
  }, []);

  return (
    <div>
      <h1 style={{ marginBottom: "20px", color: "#111827" }}>
        Incidents
      </h1>

      <div style={card}>
        <table style={table}>
          <thead>
            <tr>
              <th style={th}>ID</th>
              <th style={th}>Short Description</th>
              <th style={th}>Priority</th>
              <th style={th}>Status</th>
            </tr>
          </thead>

          <tbody>
            {incidents.map((inc) => (
              <tr
                key={inc.incident_id}
                onClick={() => navigate(`/incident/${inc.incident_id}`)}
                style={row}
              >
                <td style={td}>{inc.incident_id}</td>
                <td style={td}>{inc.short_description}</td>
                <td style={td}>{inc.priority || "-"}</td>
                <td style={td}>{inc.status || "OPEN"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ---------- Styles ---------- */

const card = {
  background: "white",
  padding: "20px",
  borderRadius: "10px",
  boxShadow: "0 2px 10px rgba(0,0,0,0.05)",
};

const table = {
  width: "100%",
  borderCollapse: "collapse",
};

const th = {
  textAlign: "left",
  padding: "12px",
  fontWeight: "600",
  background: "#F3F4F6",
  borderBottom: "1px solid #E5E7EB",
  color: "#374151",
};

const td = {
  padding: "10px",
  borderBottom: "1px solid #E5E7EB",
  color: "#374151",
};

const row = {
  cursor: "pointer",
  transition: "background 0.2s",
};
