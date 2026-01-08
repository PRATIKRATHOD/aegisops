package com.aegisops.api.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

import java.io.File;
import java.util.List;
import java.util.Map;

@Service
public class AuditService {

    private static final String AUDIT_FILE = "../incidents/audit_log.json";

    public List<Map<String, Object>> getAuditLog() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(new File(AUDIT_FILE), List.class);
    }
}
