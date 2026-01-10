import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { apiGet } from "../api/apiClient";

export default function IncidentDetailsPage() {
  const { id } = useParams();
  const [incident, setIncident] = useState(null);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      const data = await apiGet(`/incidents/${id}`);
      setIncident(data);
    } catch (err) {
      console.error("Failed to load incident:", err);
    }
  }

  if (!incident) return <h2>Loading incident...</h2>;

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto" }}>

      {/* PAGE TITLE */}
      <h1 style={pageTitleStyle}>Incident #{incident.incident_id}</h1>

      {/* SUMMARY */}
      <Section title="Incident Summary">
        <KeyValue label="Short Description" value={incident.short_description} />
        <KeyValue label="Status" value={incident.status} />
        <KeyValue label="Priority" value={incident.priority} />
        <KeyValue label="Category" value={incident.category} />
        <KeyValue label="Opened At" value={incident.opened_at} />
        <KeyValue label="Opened By" value={incident.opened_by} />
      </Section>

      {/* RCA */}
      <Section title="Root Cause Analysis">
        {incident.rca ? (
          <>
            <KeyValue label="Root Cause Type" value={incident.rca.root_cause_type} />
            <KeyValue label="Affected Component" value={incident.rca.affected_component} />
            <KeyValue label="Probable Cause" value={incident.rca.probable_cause} />

            <ListBlock label="Evidence" items={incident.rca.evidence} />
            <KeyValue label="Impact" value={incident.rca.impact} />

            <ListBlock
              label="Recommended Next Steps"
              items={incident.rca.recommended_next_steps}
            />

            {/* Confidence */}
            {incident.rca.confidence && (
              <div style={subCard}>
                <h4 style={subHeader}>Confidence Score</h4>
                <KeyValue
                  label="Score"
                  value={`${incident.rca.confidence.confidence_score}`}
                />
                <KeyValue
                  label="Reason"
                  value={incident.rca.confidence.confidence_reason}
                />
                <KeyValue
                  label="Risk Level"
                  value={incident.rca.confidence.risk_level}
                />
              </div>
            )}
          </>
        ) : (
          <p>No RCA data available for this incident.</p>
        )}
      </Section>

      {/* ACTION RECOMMENDATIONS */}
      <Section title="Action Recommendations">
        {incident.action_recommendations ? (
          <ListBlock
            label="Actions"
            items={incident.action_recommendations.actions.map(
              (a) => `${a.description} (Risk: ${a.risk})`
            )}
          />
        ) : (
          <p>No action recommendations found.</p>
        )}
      </Section>

      {/* EXECUTION PREVIEW */}
      <Section title="Execution Preview">
        {incident.execution_preview ? (
          <>
            <KeyValue
              label="Execution Mode"
              value={incident.execution_preview.execution_mode}
            />
            <KeyValue
              label="Risk Level"
              value={incident.execution_preview.risk_level}
            />
            <KeyValue
              label="Requires Approval"
              value={
                incident.execution_preview.requires_approval ? "YES" : "NO"
              }
            />

            <ListBlock
              label="Steps"
              items={incident.execution_preview.steps.map(
                (s) => `${s.step} — ${s.status}`
              )}
            />
          </>
        ) : (
          <p>No execution preview generated.</p>
        )}
      </Section>
    </div>
  );
}

/* ---------------- REUSABLE COMPONENTS ---------------- */

function Section({ title, children }) {
  return (
    <div style={sectionStyle}>
      <div style={sectionHeader}>{title}</div>
      <div>{children}</div>
    </div>
  );
}

function KeyValue({ label, value }) {
  return (
    <div style={rowStyle}>
      <div style={labelStyle}>{label}</div>
      <div style={valueStyle}>{value ?? "—"}</div>
    </div>
  );
}

function ListBlock({ label, items }) {
  return (
    <div style={{ marginBottom: "12px" }}>
      <div style={labelStyle}>{label}</div>
      <ul style={listStyle}>
        {items?.length ? (
          items.map((item, idx) => <li key={idx}>{item}</li>)
        ) : (
          <li>—</li>
        )}
      </ul>
    </div>
  );
}

/* ------------------- STYLES ------------------- */

const pageTitleStyle = {
  fontSize: "28px",
  fontWeight: "700",
  marginBottom: "25px",
  color: "#111827"
};

const sectionStyle = {
  background: "white",
  padding: "25px",
  borderRadius: "12px",
  marginBottom: "25px",
  boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
  border: "1px solid #E5E7EB"
};

const sectionHeader = {
  fontSize: "20px",
  fontWeight: "600",
  marginBottom: "18px",
  paddingBottom: "10px",
  borderBottom: "2px solid #E5E7EB",
  color: "#1F2937"
};

const rowStyle = {
  display: "flex",
  marginBottom: "8px"
};

const labelStyle = {
  width: "220px",
  fontWeight: "600",
  color: "#374151"
};

const valueStyle = {
  flex: 1,
  color: "#111827"
};

const listStyle = {
  paddingLeft: "20px",
  marginTop: "5px",
  color: "#111827"
};

const subCard = {
  background: "#F9FAFB",
  padding: "15px",
  borderRadius: "8px",
  marginTop: "15px"
};

const subHeader = {
  margin: 0,
  marginBottom: "10px",
  fontWeight: "600",
  color: "#374151"
};
