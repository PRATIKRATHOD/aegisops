What is an incident?
    Whenever ther is an any ambiguity with any service/hardware there has to be one document which will track the issue thats an Incident.

Why we are creating it internally
    As we do not have access for SNOW we will be creating the Incident internally.

Why no ServiceNow
    As this is not free requires money.

Why logs are a primary incident source
    As each issue will be present in the logs

Simple Incident Structure:
    {
        "incident_id": "INC-001",
        "source": "LOG",
        "type": "MEMORY",
        "severity": "HIGH",
        "status": "OPEN",
        "evidence": "OutOfMemoryError",
        "created_at": "timestamp"
    }   

Notes:
Incidents don’t come from thin air
They come from signals
Logs are the most basic signal