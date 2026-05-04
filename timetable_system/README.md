# GIKI Automated Timetable Scheduling System

CS378 — Design and Analysis of Algorithms | GIKI Spring 2026

A production-grade automated timetable scheduler for GIK Institute, implementing a 5-phase optimization algorithm with simulated annealing and constraint satisfaction.

---

## Quick Start

### Backend

```bash
cd backend
pip install fastapi uvicorn pydantic
python main.py
```

→ Runs on http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

→ Runs on http://localhost:5173

---

## Architecture

| File | Role |
|------|------|
| `backend/main.py` | FastAPI server, REST endpoints, CORS, CSV export |
| `backend/scheduler.py` | 5-phase scheduling algorithm (see Complexity Analysis below) |
| `backend/data_models.py` | Pydantic models, TAG_TAXONOMY, DepartmentEnum |
| `backend/storage.py` | JSON persistence layer with CRUD operations |
| `backend/seed_data.py` | CURRICULUM map, RAW_TEACHERS, RAW_ROOMS |
| `frontend/src/App.tsx` | React entry with data loading |
| `frontend/src/store/index.ts` | Zustand global state |
| `frontend/src/api/index.ts` | Axios client with typed API functions |
| `frontend/src/pages/Dashboard.tsx` | Schedule generation UI, export |
| `frontend/src/pages/Manage.tsx` | CRUD for courses/teachers/rooms |
| `frontend/src/pages/Timetable.tsx` | Schedule table, weekly grid, statistics |

---

## Algorithm Overview

### 5-Phase Scheduling Algorithm

**Phase 1: Teacher-Course Matching** (O(C × T × D))
- Matches teachers to courses via domain tag overlap
- NO hardcoded teacher-to-course assignments — only TAG_TAXONOMY matching

**Phase 2: Priority Scoring** (O(1) per course)
- Fewer available teachers → higher priority
- Core courses before electives
- Higher semester courses first

**Phase 3: Greedy Assignment** (O(N × R × S)) — **DOMINANT**
- N = scheduling tasks, R = rooms, S = timeslots (40 = 5 days × 8 periods)
- Slot scoring with faculty building alignment (Lab=-4, Lecture=-2 for cross-building)
- Backtracking for hard cases

**Phase 4: Simulated Annealing** (O(I × N))
- I = iterations (runtime parameter from UI)
- Random swaps to escape local optima
- Temperature cooling: temp *= 0.995 per iteration

**Phase 5: Conflict Detection** (O(N))
- Validates all constraints AFTER SA completes
- Teacher double-booking, room conflicts, section collisions, capacity violations

### Overall Complexity: O(N × R × S)

---

## Critical Constraints (Verified)

1. ✓ **No hardcoded teacher assignments** — domain tags only
2. ✓ **CURRICULUM-driven sections** — section course lists derived from curriculum map
3. ✓ **JSON persistence** — seed data is initial state only
4. ✓ **TAG_TAXONOMY only** — no free-text tags anywhere
5. ✓ **Faculty building alignment** — room scoring includes building penalties
6. ✓ **Runtime-adjustable SA** — iterations and initial_temp from UI/API
7. ✓ **Threading** — schedule generation runs in background thread
8. ✓ **Conflict detection post-SA** — runs after optimization, not before

---

## Adding Data

Room and faculty data is pre-populated from the real GIKI Spring 2026 timetable.

### To add rooms/teachers/courses:

**Option 1: Use the UI**
- Navigate to the Manage tab
- Use the Courses/Teachers/Rooms tabs to add/edit/delete

**Option 2: Edit seed data** (affects fresh install only)
- Edit `RAW_ROOMS` / `RAW_TEACHERS` in `backend/seed_data.py`
- Edit `CURRICULUM` map to define section course lists
- Delete `backend/data/*.json` and restart to re-seed

### Domain Tags

All tags MUST come from `TAG_TAXONOMY` in `data_models.py`:
- Mathematics: calculus, linear_algebra, discrete_math, ...
- CS Core: algorithms, data_structures, operating_systems, ...
- AI & Data: machine_learning, deep_learning, nlp, ...
- Security: cyber_security, cryptography, ...
- ... (see full list in data_models.py)

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/courses` | GET/POST | List/add courses |
| `/api/teachers` | GET/POST | List/add teachers |
| `/api/rooms` | GET/POST | List/add rooms |
| `/api/sections` | GET/POST | List/add sections |
| `/api/schedule/generate` | POST | Run scheduler with SA params |
| `/api/schedule/results` | GET | Get generated schedule |
| `/api/schedule/conflicts` | GET | Get conflict list |
| `/api/schedule/export` | GET | Export CSV |
| `/api/teachers/{id}/matches` | GET | Preview teacher-course matches |
| `/api/curriculum` | GET/PUT | Curriculum map CRUD |

---

## Project Structure

```
timetable_system/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── scheduler.py         # Scheduling algorithm
│   ├── data_models.py       # Pydantic models, TAG_TAXONOMY
│   ├── storage.py           # JSON persistence
│   ├── seed_data.py         # CURRICULUM, RAW_TEACHERS, RAW_ROOMS
│   └── README.md            # Backend docs
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main React app
│   │   ├── store/           # Zustand state
│   │   ├── api/             # Axios client
│   │   ├── pages/           # Dashboard, Manage, Timetable
│   │   └── components/ui/   # shadcn/ui components
│   ├── package.json
│   └── README.md            # Frontend docs
└── README.md                # This file
```

---

## Tech Stack

**Backend:**
- Python 3.10+
- FastAPI + Uvicorn
- Pydantic v2
- Threading for background tasks

**Frontend:**
- React 18 + TypeScript
- Vite
- Tailwind CSS + shadcn/ui
- Zustand (state management)
- Axios (API client)

---

## Design Decisions

1. **JSON over SQLite**: Simple file-based persistence for easier debugging and git tracking
2. **Domain tags over hardcoding**: Flexible teacher-course matching without brittle mappings
3. **CURRICULUM map**: Single source of truth for section course requirements
4. **Threading**: Prevents UI freezing during 2000+ iteration SA runs
5. **Dark theme UI**: Modern shadcn/ui with Tailwind for GIKI branding

---

## Authors

CS378 Project Team | GIKI Spring 2026
