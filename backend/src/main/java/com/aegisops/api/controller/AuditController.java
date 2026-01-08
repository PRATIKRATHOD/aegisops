package com.aegisops.api.controller;

import com.aegisops.api.service.AuditService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
public class AuditController {

    private final AuditService auditService;

    public AuditController(AuditService auditService) {
        this.auditService = auditService;
    }

    @GetMapping("/audit")
    public List<Map<String, Object>> getAuditLog() throws Exception {
        return auditService.getAuditLog();
    }
}
