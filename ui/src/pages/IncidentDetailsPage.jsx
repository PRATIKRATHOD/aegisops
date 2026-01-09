import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { apiGet } from "../api/apiClient";

export default function IncidentDetailsPage() {
  const { id } = useParams();
  const [incident, setIncident] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await apiGet(`/incidents/${id}`);
        setIncident(data);
      } catch (err) {
        console.error("Failed to load incident:", err);
      }
    }
    load();
  }, [id]);

  if (!incident) {
    return <h2 style={{ padding: 20 }}>Loading...</h2>;
  }

  return (
    <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
      
      <Link to="/" style={backLink}>
        ← Back to Incidents
      </Link>

      <h1 style={title}>Incident {incident.incident_id}</h1>

      {/* SUMMARY */}
      <SectionCard title="Summary">
        <table style={infoTable}>
          <tbody>
            <InfoRow label="Short Description" value={incident.short_description} />
            <InfoRow label="Priority" value={incident.priority} />
            <InfoRow label="Status" value={incident.status || "OPEN"} />
            <InfoRow label="Category" value={incident.category} />
            <InfoRow label="Subcategory" value={incident.subcategory} />
            <InfoRow label="Opened At" value={incident.opened_at} />
            <InfoRow label="Opened By" value={incident.opened_by} />
          </tbody>
        </table>
      </SectionCard>

      {/* RCA */}
      <SectionCard title="Root Cause Analysis">
        {incident.rca ? (
          <pre style={jsonBox}>{JSON.stringify(incident.rca, null, 2)}</pre>
        ) : (
          <EmptyText>No RCA available</EmptyText>
        )}
      </SectionCard>

      {/* ACTION PLAN */}
      <SectionCard title="Action Plan">
        {incident.action_plan ? (
          <pre style={jsonBox}>{JSON.stringify(incident.action_plan, null, 2)}</pre>
        ) : (
          <EmptyText>No action plan available</EmptyText>
        )}
      </SectionCard>

      {/* EXECUTION PREVIEW */}
      <SectionCard title="Execution Preview">
        {incident.execution_preview ? (
          <pre style={jsonBox}>{JSON.stringify(incident.execution_preview, null, 2)}</pre>
        ) : (
          <EmptyText>No execution preview available</EmptyText>
        )}
      </SectionCard>

      {/* AGENT DECISION */}
      <SectionCard title="Agent Decision">
        {incident.agent_decision ? (
          <pre style={jsonBox}>{JSON.stringify(incident.agent_decision, null, 2)}</pre>
        ) : (
          <EmptyText>No agent decision available</EmptyText>
        )}
      </SectionCard>

    </div>
  );
}

/* ---------- COMPONENTS ---------- */

function SectionCard({ title, children }) {
  return (
    <div style={card}>
      <h2 style={sectionTitle}>{title}</h2>
      {children}
    </div>
  );
}

function InfoRow({ label, value }) {
  return (
    <tr>
      <td style={tdLabel}>{label}</td>
      <td style={tdValue}>{value}</td>
    </tr>
  );
}

function EmptyText({ children }) {
  return <p style={noData}>{children}</p>;
}

/* ---------- STYLES ---------- */

const title = {
  marginBottom: "20px",
  color: "#111827",
};

const backLink = {
  display: "inline-block",
  marginBottom: "20px",
  color: "#2563EB",
  textDecoration: "none",
  fontSize: "15px",
};

const card = {
  background: "white",
  padding: "20px",
  borderRadius: "10px",
  marginBottom: "25px",
  boxShadow: "0 2px 10px rgba(0,0,0,0.05)",
};

const sectionTitle = {
  marginBottom: "15px",
  fontSize: "18px",
  color: "#111827",
  borderBottom: "1px solid #E5E7EB",
  paddingBottom: "8px",
};

const infoTable = {
  width: "100%",
  borderCollapse: "collapse",
};

const tdLabel = {
  width: "30%",
  padding: "10px 0",
  color: "#4B5563",
  fontWeight: "600",
};

const tdValue = {
  padding: "10px 0",
  color: "#111827",
};

const jsonBox = {
  background: "#F9FAFB",
  padding: "15px",
  borderRadius: "8px",
  border: "1px solid #E5E7EB",
  fontSize: "14px",
  whiteSpace: "pre-wrap",
  overflowX: "auto",
};

const noData = {
  color: "#6B7280",
  fontStyle: "italic",
};
