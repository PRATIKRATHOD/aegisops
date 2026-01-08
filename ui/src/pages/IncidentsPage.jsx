import { useEffect, useState } from "react";
import { apiGet } from "../api/apiClient";

export default function IncidentsPage() {
  const [incidents, setIncidents] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const data = await apiGet("/incidents");
        setIncidents(data);
      } catch (err) {
        console.error(err);
      }
    }
    load();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>AegisOps — Incidents</h1>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Short Description</th>
            <th>Priority</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {incidents.map((i) => (
            <tr key={i.incident_id}>
              <td>{i.incident_id}</td>
              <td>{i.short_description}</td>
              <td>{i.priority}</td>
              <td>{i.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
