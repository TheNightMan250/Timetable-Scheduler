# GIKI Timetable Scheduler - Backend

FastAPI-based REST API for the automated timetable scheduling system at GIK Institute.

## Quick Start

```bash
cd backend
pip install fastapi uvicorn pydantic
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Architecture

- **main.py**: FastAPI application with all REST endpoints
- **data_models.py**: Pydantic models and dataclasses for API and algorithm
- **seed_data.py**: 52 real GIKI rooms and 171 faculty members with domain tags
- **storage.py**: JSON persistence layer with in-memory caching
- **scheduler.py**: 5-phase scheduling algorithm engine

## API Endpoints

### Courses
- `GET /api/courses` - List all courses
- `POST /api/courses` - Add a new course
- `PUT /api/courses/{code}` - Update a course
- `DELETE /api/courses/{code}` - Delete a course

### Teachers
- `GET /api/teachers` - List all teachers
- `POST /api/teachers` - Add a new teacher
- `PUT /api/teachers/{id}` - Update a teacher
- `DELETE /api/teachers/{id}` - Delete a teacher
- `GET /api/teachers/{id}/matches` - Preview courses this teacher would match

### Rooms
- `GET /api/rooms` - List all rooms
- `POST /api/rooms` - Add a new room
- `PUT /api/rooms/{id}` - Update a room
- `DELETE /api/rooms/{id}` - Delete a room

### Sections
- `GET /api/sections` - List all sections
- `POST /api/sections` - Add a new section

### Tags
- `GET /api/tags` - Return the full TAG_TAXONOMY dictionary

### Curriculum
- `GET /api/curriculum` - Return curriculum map
- `PUT /api/curriculum` - Update a (program, semester) entry

### Schedule
- `POST /api/schedule/generate` - Run the scheduling algorithm
  - Body: `{ "iterations": 2000, "initial_temp": 100.0 }`
- `GET /api/schedule/results` - Get last generated schedule
- `GET /api/schedule/conflicts` - Get conflicts from last run
- `GET /api/schedule/export/csv` - Download schedule as CSV

## Scheduling Algorithm

The 5-phase algorithm:

1. **Teacher-Course Matching**: Domain tag overlap scoring
2. **Priority Scoring**: Determines scheduling order
3. **Greedy Assignment**: Room and timeslot scoring with backtracking
4. **Simulated Annealing**: Post-processing optimization
5. **Conflict Validation**: Final hard constraint check

## CORS

Enabled for `http://localhost:5173` (Vite default development server).

## Data Persistence

All data is stored in JSON files under `backend/data/`:
- `courses.json`
- `teachers.json`
- `rooms.json`
- `sections.json`
- `schedule.json`
- `curriculum.json`

On startup, if JSON files don't exist, data is loaded from `seed_data.py`.
