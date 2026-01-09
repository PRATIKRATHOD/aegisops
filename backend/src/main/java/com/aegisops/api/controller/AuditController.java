package com.aegisops.api.controller;

import com.aegisops.api.service.AuditService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;
import java.util.Map;

@RestController
public class AuditController {

    private final AuditService auditService;

    public AuditController(AuditService auditService) {
        this.auditService = auditService;
    }

    // ✅ Get all audit logs
    @GetMapping("/audit")
    public List<Map<String, Object>> getAuditLogs() throws Exception {
        return auditService.getAllAuditLogs();
    }

    // ✅ Get audit logs for specific incident
    @GetMapping("/audit/incident/{id}")
    public List<Map<String, Object>> getAuditByIncident(@PathVariable String id) throws Exception {
        return auditService.getAuditLogsByIncident(id);
    }
}
