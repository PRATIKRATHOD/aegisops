import { Routes, Route } from "react-router-dom";

// NEW PREMIUM LAYOUT
import AppLayout from "./layout/AppLayout";

// PAGES
import IncidentsPage from "./pages/IncidentsPage";
import IncidentDetailsPage from "./pages/IncidentDetailsPage";
import AuditPage from "./pages/AuditPage";

export default function App() {
  return (
    <AppLayout>
      <Routes>
        <Route path="/" element={<IncidentsPage />} />
        <Route path="/incident/:id" element={<IncidentDetailsPage />} />
        <Route path="/audit" element={<AuditPage />} />
        <Route path="/about" element={<h2>About AegisOps</h2>} />
      </Routes>
    </AppLayout>
  );
}
