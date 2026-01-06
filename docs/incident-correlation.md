# Incident Creation & Correlation – AegisOps

## Overview
This document describes how AegisOps creates production incidents
from log signals and applies correlation logic to prevent duplicate
incident creation, following real-world ITSM practices.

This step focuses only on:
- Incident detection
- Incident creation
- Incident correlation (duplicate suppression)

No AI reasoning or automation actions are involved at this stage.

---

## Why Incident Correlation Is Required

In production environments, monitoring systems run continuously.
The same error can appear multiple times within a short duration.

Without correlation:
- Multiple duplicate incidents are created
- Alert fatigue increases
- Support teams lose focus

AegisOps introduces correlation logic to:
- Identify repeated occurrences of the same issue
- Update an existing incident instead of creating duplicates
- Reduce noise while maintaining traceability

---

## Incident Creation Flow

1. Application logs are read from the monitored log file
2. A detection rule scans for known error patterns
3. When a match is found, an incident candidate is created
4. The system checks if a related OPEN incident already exists
5. Based on correlation result:
   - Update existing incident
   - OR create a new incident

---

## Incident Detection Logic

Currently, incidents are detected using log-based rules.

Example detection condition:
- Presence of `OutOfMemoryError` in application logs

This approach simulates real-world monitoring tools where:
- Logs act as primary signals
- Rules can later be replaced or enhanced with AI

---

## Incident Schema (ServiceNow-Aligned)

Each incident follows a ServiceNow-style structure, including:

- `incident_id` / `number` – Unique incident identifier
- `status` – OPEN, IN_PROGRESS, or RESOLVED
- `incident_state` – Human-readable lifecycle state
- `category`, `subcategory` – Classification
- `impact`, `urgency`, `priority` – Severity indicators
- `assignment_group` – Responsible support team
- `work_notes` – Internal investigation notes
- `comments` – User-facing comments
- `correlation_id` – Error signature used for correlation
- `opened_at`, `sys_updated_on` – Audit timestamps

This schema ensures ITSM compatibility without dependency on ServiceNow.

---

## Incident Number Generation

Incident numbers are generated dynamically to mimic ServiceNow behavior.

Logic:
- Existing incidents are loaded from storage
- The next incident number is calculated based on count
- Format: `INC1000001`, `INC1000002`, ...

This avoids:
- Hardcoded identifiers
- Duplicate ticket numbers
- Unrealistic incident tracking

---

## Correlation Logic

Correlation is performed using the following rules:

An incident is considered correlated if:
- `correlation_id` matches
- Existing incident status is `OPEN` or `IN_PROGRESS`

If a correlated incident is found:
- No new incident is created
- `work_notes` are updated with a repeated occurrence entry
- `sys_updated_on` timestamp is refreshed

If no correlated incident exists:
- A new incident is created in `OPEN` state

---

## Lifecycle Handling (Current Scope)

At this stage:
- All newly created incidents remain in `OPEN` state
- Incidents are NOT auto-resolved
- Lifecycle transitions will be handled in later stages

This design ensures:
- Correlation works correctly
- Incident lifecycle reflects real ITSM processes
- Resolution is event-driven, not scripted

---

## Current Limitations (Intentional)

The following are intentionally out of scope for this step:
- Automatic resolution
- Incident reopening
- Time-based correlation windows
- AI-driven classification or RCA
- ServiceNow integration

These will be implemented incrementally in future steps.

---

## Key Design Principles

- Incidents are created before ticketing systems
- Correlation reduces noise, not visibility
- Lifecycle changes must be deliberate
- No hardcoded identifiers
- Vendor-agnostic ITSM design

---

## Summary

This step establishes a solid incident foundation by:
- Detecting incidents from logs
- Creating ServiceNow-aligned incidents
- Suppressing duplicate incidents using correlation logic
- Preserving auditability and traceability

This foundation enables future enhancements such as:
- AI-based RCA
- Automated remediation
- ServiceNow or ticketing integrations
