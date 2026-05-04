# GIKI Timetable Scheduler - Frontend

React + TypeScript frontend for the GIKI automated timetable scheduling system.

## Quick Start

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`

## Prerequisites

- Backend server must be running at `http://localhost:8000`
- Node.js 18+ recommended

## Features

- **Dashboard**: Summary stats, schedule generation with SA parameters, CSV export
- **Manage**: View and manage courses, teachers, and rooms
- **Timetable**: Schedule table, weekly grid view, statistics and conflicts

## Tech Stack

- React 18
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui components (Radix UI)
- Zustand (state management)
- Axios (API client)
- Recharts (charts)
- TanStack Table (data tables)
- Sonner (toast notifications)

## Project Structure

```
src/
├── api/           # API client and endpoints
├── components/    # UI components
│   ├── layout/    # Layout components
│   └── ui/        # shadcn/ui primitives
├── lib/           # Utilities and constants
├── pages/         # Page components
├── store/         # Zustand store
└── types/         # TypeScript types
```

## Design System

- Dark theme throughout
- Department color coding:
  - FCSE: Blue
  - FEE: Yellow
  - FME: Green
  - FMCE: Purple
  - CIVIL: Orange
  - SMS: Teal
  - BASIC_SCIENCE: Gray
  - COMMON: Slate
