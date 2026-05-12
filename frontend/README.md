# CampusCare — Frontend

This folder contains the frontend module for CampusCare. The frontend is implemented in Python using NiceGUI. All code is in English (identifiers and files) and the user-facing interface is in Spanish.

Installation

1. Create a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Run

Start the NiceGUI app from the `frontend` folder:

```bash
python -m app.main
```

Notes

- The frontend consumes a backend API (FastAPI) via `requests` through a simple `ApiClient`.
- Project structure follows a lightweight clean-architecture approach with layers: `pages`, `components`, `clients`, `services`, `models`.
- Code is prepared to grow; currently components and services provide minimal, working behavior and fallback data when the backend is not available.

Language and UI

- Code and identifiers: English.
- User interface: Spanish.
