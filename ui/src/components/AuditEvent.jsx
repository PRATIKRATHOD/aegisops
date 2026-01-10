import React from "react";

export default function AuditEvent({ event }) {
  const color = {
    RCA_GENERATED: "#2563EB",
    CONFIDENCE_SCORED: "#059669",
    AGENT_DECISION: "#D97706",
    EXECUTION_PREVIEW_CREATED: "#DC2626",
    ACTION_PLAN_STORED_IN_KB: "#7C3AED",
    INCIDENT_CREATED: "#1D4ED8",
  }[event.event_type] || "#6B7280";

  return (
    <div
      style={{
        borderLeft: `4px solid ${color}`,
        background: "white",
        padding: "15px 18px",
        marginBottom: "15px",
        borderRadius: "8px",
        boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ fontSize: "16px", fontWeight: 600 }}>
        {event.event_type}
      </div>

      <div style={{ color: "#6B7280", fontSize: "14px", marginTop: "4px" }}>
        {event.timestamp}
      </div>

      <pre
        style={{
          marginTop: "10px",
          padding: "12px",
          background: "#F9FAFB",
          borderRadius: "6px",
          fontSize: "13px",
          overflowX: "auto",
        }}
      >
        {JSON.stringify(event.details, null, 2)}
      </pre>
    </div>
  );
}
