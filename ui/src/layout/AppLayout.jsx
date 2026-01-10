import { Link, useLocation } from "react-router-dom";

export default function AppLayout({ children }) {
  const location = useLocation();

  const isActive = (path) => location.pathname.startsWith(path);

  return (
    <div style={container}>
      {/* LEFT SIDEBAR */}
      <div style={sidebar}>
        {/* LOGO / TITLE */}
        <div style={logoBox}>
          <div style={logoDot}></div>
          <h1 style={logoText}>AegisOps</h1>
        </div>

        {/* NAVIGATION MENU */}
        <nav style={navMenu}>
          <NavItem label="Incidents" to="/" active={isActive("/")} />
          <NavItem label="Audit Logs" to="/audit" active={isActive("/audit")} />
        </nav>

        {/* FOOTER */}
        <div style={footer}>
          <p style={{ fontSize: "12px", color: "#9CA3AF" }}>
            v1.0 • Agentic AI
          </p>
        </div>
      </div>

      {/* RIGHT CONTENT AREA */}
      <div style={content}>{children}</div>
    </div>
  );
}

/* ---------------- NAV ITEM ---------------- */

function NavItem({ label, to, active }) {
  return (
    <Link
      to={to}
      style={{
        ...navItemStyle,
        ...(active ? navItemActive : {}),
      }}
    >
      {label}
    </Link>
  );
}

/* ---------------- STYLES ---------------- */

const container = {
  display: "flex",
  height: "100vh",
  background: "#F9FAFB",
  overflow: "hidden",
};

const sidebar = {
  width: "240px",
  background: "#111827",
  color: "white",
  padding: "25px 20px",
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-between",
};

const logoBox = {
  display: "flex",
  alignItems: "center",
  gap: "10px",
  paddingBottom: "25px",
  borderBottom: "1px solid #1F2937",
};

const logoDot = {
  width: "12px",
  height: "12px",
  background: "#3B82F6",
  borderRadius: "50%",
};

const logoText = {
  fontSize: "22px",
  fontWeight: "700",
};

const navMenu = {
  marginTop: "30px",
  display: "flex",
  flexDirection: "column",
  gap: "12px",
};

const navItemStyle = {
  padding: "12px 14px",
  borderRadius: "8px",
  textDecoration: "none",
  color: "#D1D5DB",
  fontSize: "15px",
  fontWeight: "500",
  transition: "0.2s",
};

const navItemActive = {
  background: "#1F2937",
  color: "white",
  borderLeft: "4px solid #3B82F6",
};

const footer = {
  marginTop: "40px",
  borderTop: "1px solid #1F2937",
  paddingTop: "20px",
};

const content = {
  flex: 1,
  padding: "30px",
  overflowY: "auto",
};

