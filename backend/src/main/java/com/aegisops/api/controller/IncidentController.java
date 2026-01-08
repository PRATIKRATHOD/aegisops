package com.aegisops.api.controller;

import com.aegisops.api.service.IncidentService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


import java.util.List;
import java.util.Map;

@RestController
public class IncidentController {

    private final IncidentService incidentService;

    public IncidentController(IncidentService incidentService) {
        this.incidentService = incidentService;
    }

    // ------------- GET ALL INCIDENTS --------------------
    @GetMapping("/incidents")
    public List<Map<String, Object>> getAllIncidents() throws Exception {
        return incidentService.getAllIncidents();
    }

    // ------------- GET INCIDENT BY ID --------------------
    @GetMapping("/incidents/{id}")
    public Map<String, Object> getIncidentById(@PathVariable String id) throws Exception {
        Map<String, Object> incident = incidentService.getIncidentById(id);

        if (incident == null) {
            throw new RuntimeException("Incident not found: " + id);
        }

        return incident;
    }

    @GetMapping("/incidents/{id}/rca")
    public Map<String, Object> getIncidentRca(@PathVariable String id) throws Exception {
        Map<String, Object> rca = incidentService.getIncidentRca(id);

        if (rca == null) {
            throw new RuntimeException("RCA not found for incident: " + id);
        }

        return rca;
    }

    @GetMapping("/incidents/{id}/decision")
    public Map<String, Object> getIncidentDecision(@PathVariable String id) throws Exception {
        Map<String, Object> decision = incidentService.getIncidentDecision(id);

        if (decision == null) {
            throw new RuntimeException("Decision not found for incident: " + id);
        }

        return decision;
    }

    @GetMapping("/incidents/{id}/plan")
    public Map<String, Object> getIncidentActionPlan(@PathVariable String id) throws Exception {
        Map<String, Object> plan = incidentService.getIncidentActionPlan(id);

        if (plan == null) {
            throw new RuntimeException("Action plan not found for incident: " + id);
        }

        return plan;
    }

    @GetMapping("/incidents/{id}/execution-preview")
    public Map<String, Object> getIncidentExecutionPreview(@PathVariable String id) throws Exception {
        Map<String, Object> preview = incidentService.getIncidentExecutionPreview(id);

        if (preview == null) {
            throw new RuntimeException("Execution preview not found for incident: " + id);
        }

        return preview;
    }

    @PostMapping("/incidents")
    public Map<String, Object> createIncident(@RequestBody Map<String, Object> body) throws Exception {
        Map<String, Object> created = incidentService.createIncident(body);

        return created;
    }




}
