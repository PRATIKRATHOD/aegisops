package com.aegisops.api.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

import java.io.File;
import java.util.List;
import java.util.Map;

@Service
public class IncidentService {

    private static final String INCIDENT_FILE = "../incidents/incidents.json"; // relative path

    public List<Map<String, Object>> getAllIncidents() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(new File(INCIDENT_FILE), List.class);
    }
    public Map<String, Object> getIncidentById(String id) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        List<Map<String, Object>> incidents =
                mapper.readValue(new File(INCIDENT_FILE), List.class);

        for (Map<String, Object> incident : incidents) {
            if (incident.get("incident_id").equals(id)) {
                return incident;
            }
        }

        return null; // not found
    }
    public Map<String, Object> getIncidentRca(String id) throws Exception {
        Map<String, Object> incident = getIncidentById(id);

        if (incident == null) {
            return null;
        }

        return (Map<String, Object>) incident.get("rca");
    }

    public Map<String, Object> getIncidentDecision(String id) throws Exception {
        Map<String, Object> incident = getIncidentById(id);

        if (incident == null) {
            return null;
        }

        return (Map<String, Object>) incident.get("agent_decision");
    }

    public Map<String, Object> getIncidentActionPlan(String id) throws Exception {
        Map<String, Object> incident = getIncidentById(id);

        if (incident == null) {
            return null;
        }

        return (Map<String, Object>) incident.get("action_plan");
    }

    public Map<String, Object> getIncidentExecutionPreview(String id) throws Exception {
        Map<String, Object> incident = getIncidentById(id);

        if (incident == null) {
            return null;
        }

        return (Map<String, Object>) incident.get("execution_preview");
    }

    public Map<String, Object> createIncident(Map<String, Object> newIncident) throws Exception {
    ObjectMapper mapper = new ObjectMapper();

    List<Map<String, Object>> incidents =
            mapper.readValue(new File(INCIDENT_FILE), List.class);

    // Generate new ID
    String id = "INC" + String.format("%07d", incidents.size() + 1);
    newIncident.put("incident_id", id);
    newIncident.put("number", id);
    newIncident.put("opened_at", java.time.LocalDateTime.now().toString());
    newIncident.put("opened_by", "api-client");

    // ⭐ ADD DEFAULT FIELDS (ServiceNow Style)
    newIncident.putIfAbsent("status", "OPEN");
    newIncident.putIfAbsent("incident_state", "New");
    newIncident.putIfAbsent("category", "software");
    newIncident.putIfAbsent("subcategory", "general");
    newIncident.putIfAbsent("source", "API");
    newIncident.putIfAbsent("priority", "3");
    newIncident.putIfAbsent("urgency", "3");
    newIncident.putIfAbsent("impact", "3");
    newIncident.putIfAbsent("assignment_group", "Application Support");
    newIncident.putIfAbsent("comments", "Created via API");
    newIncident.putIfAbsent("work_notes", "");

    // Add to list
    incidents.add(newIncident);

    // Save
    mapper.writeValue(new File(INCIDENT_FILE), incidents);

    return newIncident;
}



}
