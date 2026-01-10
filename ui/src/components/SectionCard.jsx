export default function SectionCard({ title, children }) {
  return (
    <div style={card}>
      <h2 style={header}>{title}</h2>
      <div>{children}</div>
    </div>
  );
}

const card = {
  background: "white",
  padding: "22px",
  borderRadius: "14px",
  marginBottom: "25px",
  boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
  border: "1px solid #E5E7EB",
};

const header = {
  fontSize: "20px",
  fontWeight: "700",
  marginBottom: "15px",
  color: "#111827",
};
