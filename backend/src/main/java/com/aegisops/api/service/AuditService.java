package com.aegisops.api.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

import java.io.File;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class AuditService {

private static final String AUDIT_FILE = "src/main/resources/data/audit_log.json";



    public List<Map<String, Object>> getAllAuditLogs() throws Exception {
        ensureFileExists(AUDIT_FILE);   // <-- REQUIRED

        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(new File(AUDIT_FILE), List.class);
    }


    public List<Map<String, Object>> getAuditLogsByIncident(String incidentId) throws Exception {
        ensureFileExists(AUDIT_FILE);   // <-- REQUIRED

        ObjectMapper mapper = new ObjectMapper();
        List<Map<String, Object>> logs =
                mapper.readValue(new File(AUDIT_FILE), List.class);

        return logs.stream()
                .filter(log -> incidentId.equals(log.get("incident_id")))
                .collect(Collectors.toList());
    }


    private void ensureFileExists(String path) throws Exception {
        File file = new File(path);
        if (!file.exists()) {
            file.getParentFile().mkdirs();
            file.createNewFile();
            new ObjectMapper().writeValue(file, new Object[]{}); // empty array
        }
    }
}
