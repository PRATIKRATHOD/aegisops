## 🖥️ Java Backend API Layer (Spring Boot)

### Purpose
Expose AegisOps incident intelligence through clean REST APIs.

### Responsibilities
- Serve incidents and RCA data
- Provide agent decisions and action plans
- Expose audit logs
- Enforce secure and auditable access

### Endpoints (MVP)
- `GET /incidents`
- `GET /incidents/{id}`
- `GET /incidents/{id}/rca`
- `GET /incidents/{id}/decision`
- `GET /incidents/{id}/plan`
- `GET /incidents/{id}/execution-preview`
- `GET /audit`

### Tech
- Java 17
- Spring Boot 3.x
- Jackson for JSON parsing
- Simple file-based storage (incidents.json)

### Benefit
Turns AegisOps into a platform that UI, bots, and CLIs can consume.
