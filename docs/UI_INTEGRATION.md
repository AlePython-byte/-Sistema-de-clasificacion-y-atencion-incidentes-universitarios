# UI Integration Documentation - CampusCare

This document outlines the architectural changes and additions made to the CampusCare project to integrate a professional frontend.

## 1. Project Evolution
The project was originally a headless backend (FastAPI). It has been evolved into a full-stack desktop application using CustomTkinter, while maintaining the original backend as a modular service.

## 2. New Components

### 2.1 UI Layer (`ui/`)
- **`bridge.py`**: Acts as an **Adapter/Bridge**. It decouples the UI components from the FastAPI backend. It handles:
  - Dynamic `sys.path` injection for modularity.
  - Exception mapping (translating backend errors to UI alerts).
  - Data transformation between UI forms and Pydantic models.
- **`components/`**: (Placeholder for future modularization) Intended for reusable UI widgets.

### 2.2 Entry Point (`main_ui.py`)
- Implements a modern **Dark Theme** (#1A1A1B).
- Features a **Multi-view Sidebar** (Dashboard, New Incident).
- Includes a **Technical Console** for real-time process monitoring.
- Uses **Multi-threading** to ensure the UI remains responsive during backend operations.

### 2.3 Package Structure
Added `__init__.py` files to `backend/`, `backend/app/`, and `ui/` to ensure the project complies with standard Python package requirements and improves IDE compatibility.

## 3. Communication Pattern
The UI communicates with the backend via the `BackendBridge` class.
`UI` -> `BackendBridge` -> `IncidentService` -> `IncidentRepository`

This ensures that any future changes to the backend API or database will only require updates in the Bridge layer, not the entire UI.

## 4. Environment Setup
Dependencies are managed via `requirements_ui.txt` and the original `backend/requirements.txt`.
Key libraries added: `customtkinter`, `darkdetect`, `packaging`.
