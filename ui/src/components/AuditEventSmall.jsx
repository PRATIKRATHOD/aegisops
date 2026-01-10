export default function AuditEventSmall({ event }) {
  return (
    <div
      style={{
        background: "#F9FAFB",
        padding: "12px 15px",
        borderRadius: "8px",
        marginBottom: "10px",
        border: "1px solid #E5E7EB"
      }}
    >
      <div style={{ fontWeight: 600, color: "#111827" }}>
        {event.event_type}
      </div>
      
      <div style={{ color: "#6B7280", fontSize: "13px", marginBottom: "6px" }}>
        {event.timestamp}
      </div>

      <pre
        style={{
          margin: 0,
          padding: "8px",
          background: "white",
          borderRadius: "6px",
          fontSize: "12px",
          overflowX: "auto",
          border: "1px solid #E5E7EB"
        }}
      >
        {JSON.stringify(event.details, null, 2)}
      </pre>
    </div>
  );
}
