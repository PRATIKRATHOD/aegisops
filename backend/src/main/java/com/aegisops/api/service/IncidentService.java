package com.aegisops.api.service;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

@Service
public class IncidentService {

    private static final String INCIDENT_FILE = "src/main/resources/data/incidents.json";

    // ------------------ LOAD ALL INCIDENTS ------------------
    public List<Map<String, Object>> getAllIncidents() throws Exception {
        ensureFileExists(INCIDENT_FILE);

        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(new File(INCIDENT_FILE), List.class);
    }

    // ------------------ LOAD SINGLE INCIDENT ------------------
    public Map<String, Object> getIncidentById(String id) throws Exception {
        ensureFileExists(INCIDENT_FILE);

        ObjectMapper mapper = new ObjectMapper();
        List<Map<String, Object>> incidents =
                mapper.readValue(new File(INCIDENT_FILE), List.class);

        for (Map<String, Object> incident : incidents) {
            if (incident.get("incident_id").equals(id)) {
                return incident;
            }
        }
        return null;
    }

    // ------------------ GENERIC SECTION FETCH ------------------
    public Object getIncidentSection(String incidentId, String sectionKey) {
        try {
            Map<String, Object> incident = getIncidentById(incidentId);

            if (incident == null) {
                return Map.of("error", "Incident not found");
            }

            return incident.getOrDefault(sectionKey, Map.of("message", "No data found"));

        } catch (Exception e) {
            return Map.of("error", "Failed to read incident");
        }
    }

    // ------------------ CREATE NEW INCIDENT ------------------
    public Map<String, Object> createIncident(Map<String, Object> newIncident) throws Exception {
        ensureFileExists(INCIDENT_FILE);

        ObjectMapper mapper = new ObjectMapper();
        List<Map<String, Object>> incidents =
                mapper.readValue(new File(INCIDENT_FILE), List.class);

        String id = "INC" + String.format("%07d", incidents.size() + 1);
        newIncident.put("incident_id", id);
        newIncident.put("number", id);
        newIncident.put("opened_at", java.time.LocalDateTime.now().toString());
        newIncident.put("opened_by", "api-client");

        incidents.add(newIncident);

        mapper.writeValue(new File(INCIDENT_FILE), incidents);

        return newIncident;
    }

    // ------------------ FILE ENSURE ------------------
    private void ensureFileExists(String path) throws Exception {
        File file = new File(path);
        if (!file.exists()) {
            file.getParentFile().mkdirs();
            file.createNewFile();
            new ObjectMapper().writeValue(file, new Object[]{}); // empty array
        }
    }

    // ------------------ POSTMORTEM LOADING ------------------
    public Object getPostmortem(String incidentId) throws Exception {
        Path file = Paths.get("src/main/resources/data/postmortem.json");
        if (!Files.exists(file)) return Map.of("error", "No postmortem available");

        String json = Files.readString(file);
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(json, Map.class);
    }

    // ------------------ NOTIFICATIONS ------------------
    public Object getNotifications(String incidentId) throws Exception {
        Map<String, Object> incident = getIncidentById(incidentId);
        if (incident == null) return Map.of("error", "Incident not found");

        Map<String, Object> info = new HashMap<>();
        info.put("notification_state", incident.getOrDefault("notification_state", "NONE"));
        info.put("notified_at", incident.getOrDefault("notified_at", "N/A"));

        return info;
    }
}
