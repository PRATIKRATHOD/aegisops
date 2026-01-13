import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { apiGet } from "../api/apiClient";

export default function IncidentDetailsPage() {
  const { id } = useParams();
  const [incident, setIncident] = useState(null);
  const [activeTab, setActiveTab] = useState("summary");

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

  if (!incident) return <h2 style={{ padding: 20 }}>Loading incident...</h2>;

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto" }}>

      {/* HEADER */}
      <h1 style={pageTitle}>Incident #{incident.incident_id}</h1>

      {/* TABS */}
      <Tabs active={activeTab} onChange={setActiveTab} />

      {/* TAB CONTENT */}
      <div style={{ marginTop: "20px" }}>
        {activeTab === "summary" && <SummaryTab incident={incident} />}
        {activeTab === "rca" && <RCATab incident={incident} />}
        {activeTab === "action" && <ActionPlanTab incident={incident} />}
        {activeTab === "execution" && (
          <ExecutionPreviewTab incident={incident} />
        )}
        {activeTab === "self" && <SelfHealingTab incident={incident} />}
        {activeTab === "notify" && <NotificationTab incident={incident} />}
        {activeTab === "postmortem" && <PostmortemTab incident={incident} />}
      </div>
    </div>
  );
}

/* --------------------- TABS COMPONENT --------------------- */

function Tabs({ active, onChange }) {
  const tabs = [
    { key: "summary", label: "Summary" },
    { key: "rca", label: "RCA" },
    { key: "action", label: "Action Plan" },
    { key: "execution", label: "Execution Preview" },
    { key: "self", label: "Self Healing" },
    { key: "notify", label: "Notifications" },
    { key: "postmortem", label: "Postmortem" },
  ];

  return (
    <div style={tabContainer}>
      {tabs.map((tab) => (
        <div
          key={tab.key}
          onClick={() => onChange(tab.key)}
          style={active === tab.key ? activeTabStyle : tabStyle}
        >
          {tab.label}
        </div>
      ))}
    </div>
  );
}

/* --------------------- TAB CONTENTS --------------------- */

function SummaryTab({ incident }) {
  return (
    <Section title="Incident Summary">
      <KeyValue label="Short Description" value={incident.short_description} />
      <KeyValue label="Status" value={incident.status} />
      <KeyValue label="Priority" value={incident.priority} />
      <KeyValue label="Category" value={incident.category} />
      <KeyValue label="Subcategory" value={incident.subcategory} />
      <KeyValue label="Opened At" value={incident.opened_at} />
      <KeyValue label="Opened By" value={incident.opened_by} />
      <KeyValue label="Source" value={incident.source} />
      <KeyValue label="Correlation ID" value={incident.correlation_id} />

      <Section title="Work Notes">
        <pre style={preBlock}>{incident.work_notes || "—"}</pre>
      </Section>
    </Section>
  );
}

function RCATab({ incident }) {
  const rca = incident.rca;

  if (!rca) return <NoData />;

  return (
    <Section title="Root Cause Analysis">
      <KeyValue label="Root Cause Type" value={rca.root_cause_type} />
      <KeyValue label="Affected Component" value={rca.affected_component} />
      <KeyValue label="Probable Cause" value={rca.probable_cause} />
      <ListBlock label="Evidence" items={rca.evidence} />
      <KeyValue label="Impact" value={rca.impact} />

      {rca.confidence && (
        <Section title="Confidence Analysis">
          <KeyValue label="Score" value={rca.confidence.confidence_score} />
          <KeyValue
            label="Reason"
            value={rca.confidence.confidence_reason}
          />
          <KeyValue label="Risk Level" value={rca.confidence.risk_level} />
        </Section>
      )}
    </Section>
  );
}

function ActionPlanTab({ incident }) {
  const actionBlock = incident.action_recommendations;

  if (!actionBlock) return <NoData />;

  return (
    <Section title="Recommended Actions">
      <ListBlock
        items={actionBlock.actions.map(
          (a) => `${a.description} (Risk: ${a.risk})`
        )}
      />
    </Section>
  );
}

function ExecutionPreviewTab({ incident }) {
  const ex = incident.execution_preview;
  if (!ex) return <NoData />;

  return (
    <Section title="Execution Preview">
      <KeyValue label="Mode" value={ex.execution_mode} />
      <KeyValue label="Requires Approval" value={ex.requires_approval ? "YES" : "NO"} />
      <KeyValue label="Risk Level" value={ex.risk_level} />

      <ListBlock
        label="Steps"
        items={ex.steps.map((s) => `${s.step} — ${s.status}`)}
      />
    </Section>
  );
}

function SelfHealingTab({ incident }) {
  const heal = incident.self_healing;
  if (!heal) return <NoData />;

  return (
    <Section title="Self Healing">
      <ListBlock items={heal.steps} />
    </Section>
  );
}

function NotificationTab({ incident }) {
  const notify = incident.notification;
  if (!notify) return <NoData />;

  return (
    <Section title="Incident Notifications">
      <ListBlock items={notify.messages} />
    </Section>
  );
}

function PostmortemTab({ incident }) {
  const pm = incident.postmortem;
  if (!pm) return <NoData />;

  return (
    <Section title="Postmortem Report">
      <pre style={preBlock}>{JSON.stringify(pm, null, 2)}</pre>
    </Section>
  );
}

/* --------------------- REUSABLE ELEMENTS --------------------- */

function Section({ title, children }) {
  return (
    <div style={sectionStyle}>
      <h2 style={sectionTitle}>{title}</h2>
      <div>{children}</div>
    </div>
  );
}

function KeyValue({ label, value }) {
  return (
    <div style={row}>
      <div style={labelStyle}>{label}</div>
      <div style={valueStyle}>{value ?? "—"}</div>
    </div>
  );
}

function ListBlock({ label, items }) {
  return (
    <div style={{ marginBottom: "12px" }}>
      {label && <div style={labelStyle}>{label}</div>}
      <ul style={ulStyle}>
        {items?.length ? (
          items.map((i, idx) => <li key={idx}>{i}</li>)
        ) : (
          <li>—</li>
        )}
      </ul>
    </div>
  );
}

function NoData() {
  return <p style={{ padding: "20px", color: "#6B7280" }}>No data available</p>;
}

/* --------------------- STYLES --------------------- */

const pageTitle = {
  fontSize: "28px",
  fontWeight: "700",
  marginBottom: "25px",
  color: "#111827",
};

const tabContainer = {
  display: "flex",
  gap: "12px",
  borderBottom: "2px solid #E5E7EB",
};

const tabStyle = {
  padding: "10px 16px",
  cursor: "pointer",
  color: "#6B7280",
  fontWeight: "500",
};

const activeTabStyle = {
  ...tabStyle,
  color: "#111827",
  borderBottom: "3px solid #2563EB",
};

const sectionStyle = {
  background: "white",
  padding: "25px",
  borderRadius: "12px",
  marginBottom: "25px",
  boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
  border: "1px solid #E5E7EB",
};

const sectionTitle = {
  marginBottom: "15px",
  fontSize: "20px",
  fontWeight: "600",
  color: "#1F2937",
  borderBottom: "2px solid #E5E7EB",
  paddingBottom: "8px",
};

const row = { display: "flex", marginBottom: "8px" };
const labelStyle = { width: "220px", color: "#374151", fontWeight: "600" };
const valueStyle = { flex: 1, color: "#111827" };
const ulStyle = { paddingLeft: "20px", marginTop: "5px" };
const preBlock = {
  background: "#F3F4F6",
  padding: "12px",
  borderRadius: "8px",
  whiteSpace: "pre-wrap",
  fontSize: "14px",
};

