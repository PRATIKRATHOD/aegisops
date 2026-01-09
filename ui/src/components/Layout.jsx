import { Link } from "react-router-dom";

export default function Layout({ children }) {
  return (
    <div style={{ display: "flex", minHeight: "100vh", fontFamily: "Inter, Arial" }}>
      
      {/* Sidebar */}
      <div
        style={{
          width: "240px",
          background: "#111827",  // dark slate
          color: "white",
          padding: "25px 20px",
          display: "flex",
          flexDirection: "column",
          gap: "20px",
        }}
      >
        <h1 style={{ margin: "0 0 20px 0", fontSize: "22px" }}>AegisOps</h1>

        <NavItem to="/" label="Incidents" />
        <NavItem to="/audit" label="Audit Logs" />
        <NavItem to="/about" label="About" />
      </div>

      {/* Main Content Area */}
      <div style={{ flex: 1, background: "#F3F4F6" }}>
        
        {/* Top Header */}
        <div
          style={{
            background: "white",
            padding: "15px 25px",
            borderBottom: "1px solid #E5E7EB",
            marginBottom: "20px",
          }}
        >
          <h2 style={{ margin: 0, fontSize: "20px", color: "#111827" }}>
            AegisOps Dashboard
          </h2>
        </div>

        {/* Page Content */}
        <div style={{ padding: "25px" }}>
          {children}
        </div>

      </div>
    </div>
  );
}

function NavItem({ to, label }) {
  return (
    <Link
      to={to}
      style={{
        padding: "10px 14px",
        borderRadius: "6px",
        background: "#1F2937",
        color: "white",
        textDecoration: "none",
        fontSize: "15px",
      }}
    >
      {label}
    </Link>
  );
}
