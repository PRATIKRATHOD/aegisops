import { useEffect, useState } from "react";
import { apiGet } from "../api/apiClient";

export default function AuditPage() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      const data = await apiGet("/audit");
      setLogs(data);
    } catch (err) {
      console.error("ERROR loading audit logs:", err);
    }
  }

  const card = {
    background: "white",
    padding: "20px",
    borderRadius: "12px",
    marginBottom: "20px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.05)"
  };

  const jsonBox = {
    background: "#F9FAFB",
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #E5E7EB",
    whiteSpace: "pre-wrap",
    fontSize: "14px"
  };

  return (
    <div>
      <h2 style={{ marginBottom: "20px" }}>Audit Logs</h2>

      {logs.length === 0 && <p>No audit logs found.</p>}

      {logs.map((log, i) => (
        <div key={i} style={card}>
          <h3 style={{ margin: "0 0 5px 0" }}>{log.event_type}</h3>
          <p style={{ color: "#6B7280", marginTop: 0 }}>{log.timestamp}</p>

          <div style={jsonBox}>
            {JSON.stringify(log.details, null, 2)}
          </div>
        </div>
      ))}
    </div>
  );
}
