# CampusCare

CampusCare is an academic backend project for managing and prioritizing university campus incidents. This first backend block provides the initial FastAPI structure, clean layers, Pydantic schemas, and base incident endpoints.

## Technologies

- Python
- FastAPI
- Pydantic
- Uvicorn

## Integrante 1 Scope

This implementation corresponds only to Integrante 1. It creates the initial backend architecture and placeholder-ready services without database integration, authentication, frontend code, or advanced data structures.

## Project Structure

```text
campuscare/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── incident_routes.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── schemas/
│   │   │   └── incident_schema.py
│   │   ├── services/
│   │   │   └── incident_service.py
│   │   └── repositories/
│   │       └── incident_repository.py
│   └── requirements.txt
├── README.md
└── .gitignore
```

## Setup on Windows PowerShell

From Visual Studio Code, open a PowerShell terminal and run:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Swagger

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

## Initial Endpoints

- `GET /`
- `GET /health`
- `POST /api/incidents/`
- `GET /api/incidents/`
- `GET /api/incidents/{incident_id}`
- `PATCH /api/incidents/{incident_id}/status`
- `PATCH /api/incidents/{incident_id}/assign`
- `GET /api/incidents/queue/next`

## Notes for Next Integrantes

- The repository is currently in memory and can later be replaced by a database implementation.
- `get_next_incident` currently returns the first open incident found.
- A TODO is included in the service to integrate the future `PriorityQueueManager` from Integrante 2.
- The service and repository layers are separated so additional business rules can be added without changing the API routes directly.
