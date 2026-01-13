import { useState } from "react";

export default function Tabs({ tabs }) {
  const [active, setActive] = useState(0);

  return (
    <div style={container}>
      {/* TAB HEADERS */}
      <div style={tabRow}>
        {tabs.map((t, i) => (
          <div
            key={i}
            style={{
              ...tabItem,
              ...(i === active ? activeTab : {})
            }}
            onClick={() => setActive(i)}
          >
            {t.label}
          </div>
        ))}
      </div>

      {/* TAB CONTENT */}
      <div style={contentBox}>
        {tabs[active].content}
      </div>
    </div>
  );
}

/* ------------- STYLES (FUTURISTIC) ------------- */

const container = {
  width: "100%",
};

const tabRow = {
  display: "flex",
  gap: "10px",
  marginBottom: "15px",
};

const tabItem = {
  padding: "10px 18px",
  borderRadius: "10px",
  cursor: "pointer",
  background: "rgba(255,255,255,0.1)",
  backdropFilter: "blur(10px)",
  border: "1px solid rgba(255,255,255,0.15)",
  color: "#6B7280",
  fontWeight: 600,
  transition: "0.2s",
};

const activeTab = {
  background: "linear-gradient(135deg, #6EE7B7, #3B82F6)",
  color: "white",
  border: "none",
  boxShadow: "0 4px 20px rgba(0,0,0,0.15)",
};

const contentBox = {
  background: "white",
  padding: "25px",
  borderRadius: "14px",
  boxShadow: "0 4px 16px rgba(0,0,0,0.08)",
};
