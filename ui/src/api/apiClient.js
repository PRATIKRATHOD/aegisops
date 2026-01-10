const API_BASE = "http://localhost:8080";
const API_KEY = "AegisOps-Secret-2026";

export async function apiGet(endpoint) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      "X-API-KEY": API_KEY
    }
  });

  if (!res.ok) {
    throw new Error(`API Error: ${res.status}`);
  }

  return res.json();
}

export async function apiGetIncidentAudit(incidentId) {
  return apiGet(`/audit/incident/${incidentId}`);
}