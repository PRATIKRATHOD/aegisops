package com.aegisops.api.controller;

import com.aegisops.api.service.IncidentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/incidents")
@CrossOrigin(origins = "*")
public class IncidentDetailsController {

    private final IncidentService incidentService;

    @Autowired
    public IncidentDetailsController(IncidentService incidentService) {
        this.incidentService = incidentService;
    }

    // ------------------ INCIDENT SUMMARY ------------------
    @GetMapping("/{id}")
    public Object getIncident(@PathVariable String id) throws Exception {
        return incidentService.getIncidentById(id);
    }

    // ------------------ RCA ------------------
    @GetMapping("/{id}/rca")
    public Object getRca(@PathVariable String id) {
        return incidentService.getIncidentSection(id, "rca");
    }

    // ------------------ ACTION PLAN ------------------
    @GetMapping("/{id}/actions")
    public Object getActions(@PathVariable String id) {
        return incidentService.getIncidentSection(id, "action_recommendations");
    }

    // ------------------ EXECUTION PREVIEW ------------------
    @GetMapping("/{id}/execution-preview")
    public Object getExecutionPreview(@PathVariable String id) {
        return incidentService.getIncidentSection(id, "execution_preview");
    }

    // ------------------ SELF HEALING ------------------
    @GetMapping("/{id}/self-healing")
    public Object getSelfHealing(@PathVariable String id) {
        return incidentService.getIncidentSection(id, "self_healing_result");
    }

    // ------------------ POSTMORTEM ------------------
    @GetMapping("/{id}/postmortem")
    public Object getPostmortem(@PathVariable String id) throws Exception {
        Map<String, Object> incident = incidentService.getIncidentById(id);
        if (incident == null) {
            return Map.of("error", "Incident not found");
        }

        return incident.getOrDefault("postmortem", Map.of("message", "No postmortem available"));
    }

    // ------------------ NOTIFICATIONS ------------------
    @GetMapping("/{id}/notifications")
    public Object getNotifications(@PathVariable String id) throws Exception {
        return incidentService.getNotifications(id);
    }

    // ------------------ GET ALL INCIDENTS ------------------
    @GetMapping("")
    public Object getAllIncidents() throws Exception {
        return incidentService.getAllIncidents();
    }

}
