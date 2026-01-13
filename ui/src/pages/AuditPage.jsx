import { useEffect, useState } from "react";
import { apiGet } from "../api/apiClient";
import AuditEvent from "../components/AuditEvent";

export default function AuditPage() {
  const [logs, setLogs] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [query, setQuery] = useState("");

  useEffect(() => {
    loadLogs();
  }, []);

  async function loadLogs() {
    try {
      const data = await apiGet("/audit");
      setLogs(data);
      setFiltered(data);
    } catch (err) {
      console.error("Failed to load audit logs:", err);
    }
  }

  function handleSearch(e) {
    const q = e.target.value.toLowerCase();
    setQuery(q);

    const f = logs.filter(
      (log) =>
        log.event_type.toLowerCase().includes(q) ||
        JSON.stringify(log.details).toLowerCase().includes(q) ||
        (log.incident_id && log.incident_id.toLowerCase().includes(q))
    );

    setFiltered(f);
  }

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto" }}>
      <h1 style={title}>Audit Logs</h1>

      {/* Search Bar */}
      <input
        type="text"
        placeholder="Search events..."
        value={query}
        onChange={handleSearch}
        style={searchBox}
      />

      {/* Timeline */}
      {filtered.map((event, index) => (
        <AuditEvent key={index} event={event} />
      ))}
    </div>
  );
}

const title = {
  fontSize: "28px",
  fontWeight: "700",
  marginBottom: "25px",
  color: "#111827",
};

const searchBox = {
  width: "100%",
  padding: "12px",
  marginBottom: "20px",
  borderRadius: "8px",
  border: "1px solid #D1D5DB",
  fontSize: "15px",
};
