"""
GIKI Timetable Scheduler - FastAPI Backend

Complete REST API for the timetable scheduling system.
"""

import threading
import csv
import io
from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Handle imports for both direct execution and module import
try:
    from backend.data_models import (
        Course, Teacher, Room, Section, ScheduleEntry,
        CourseData, TeacherData, RoomData, SectionData, ScheduleEntryData,
        TAG_TAXONOMY, DepartmentEnum, RoomTypeEnum
    )
    from backend import storage
    from backend.scheduler import generate_schedule as scheduler_generate
except ImportError:
    from data_models import (
        Course, Teacher, Room, Section, ScheduleEntry,
        CourseData, TeacherData, RoomData, SectionData, ScheduleEntryData,
        TAG_TAXONOMY, DepartmentEnum, RoomTypeEnum
    )
    import storage
    from scheduler import generate_schedule as scheduler_generate

app = FastAPI(
    title="GIKI Timetable Scheduler API",
    description="REST API for automated timetable scheduling at GIK Institute",
    version="1.0.0"
)

# Enable CORS for localhost:5173 (Vite default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═════════════════════════════════════════════════════════════════
# Startup
# ═════════════════════════════════════════════════════════════════

@app.on_event("startup")
def startup_event():
    """Initialize storage on startup."""
    storage.init_storage()


# ═════════════════════════════════════════════════════════════════
# Request/Response Models
# ═════════════════════════════════════════════════════════════════

class ScheduleGenerateRequest(BaseModel):
    iterations: int = 2000
    initial_temp: float = 100.0


class ScheduleGenerateResponse(BaseModel):
    success: bool
    entries_scheduled: int
    entries_unscheduled: int
    conflicts_detected: int
    message: str


class CurriculumEntry(BaseModel):
    program: str
    semester: int
    course_codes: List[str]


class CurriculumMap(BaseModel):
    curriculum: Dict[str, List[str]]


# ═════════════════════════════════════════════════════════════════
# Courses API
# ═════════════════════════════════════════════════════════════════

@app.get("/api/courses", response_model=List[Course])
def get_courses():
    """List all courses."""
    return storage.get_courses()


@app.post("/api/courses", response_model=dict)
def create_course(course: Course):
    """Add a new course."""
    if storage.add_course(course):
        return {"success": True, "message": f"Course {course.code} created"}
    raise HTTPException(status_code=400, detail=f"Course {course.code} already exists")


@app.put("/api/courses/{code}", response_model=dict)
def update_course(code: str, course: Course):
    """Update a course."""
    if storage.update_course(code, course):
        return {"success": True, "message": f"Course {code} updated"}
    raise HTTPException(status_code=404, detail=f"Course {code} not found")


@app.delete("/api/courses/{code}", response_model=dict)
def delete_course(code: str):
    """Delete a course."""
    if storage.delete_course(code):
        return {"success": True, "message": f"Course {code} deleted"}
    raise HTTPException(status_code=404, detail=f"Course {code} not found")


# ═════════════════════════════════════════════════════════════════
# Teachers API
# ═════════════════════════════════════════════════════════════════

@app.get("/api/teachers", response_model=List[Teacher])
def get_teachers():
    """List all teachers."""
    return storage.get_teachers()


@app.post("/api/teachers", response_model=dict)
def create_teacher(teacher: Teacher):
    """Add a new teacher."""
    if storage.add_teacher(teacher):
        return {"success": True, "message": f"Teacher {teacher.id} created"}
    raise HTTPException(status_code=400, detail=f"Teacher {teacher.id} already exists")


@app.put("/api/teachers/{id}", response_model=dict)
def update_teacher(id: str, teacher: Teacher):
    """Update a teacher."""
    if storage.update_teacher(id, teacher):
        return {"success": True, "message": f"Teacher {id} updated"}
    raise HTTPException(status_code=404, detail=f"Teacher {id} not found")


@app.delete("/api/teachers/{id}", response_model=dict)
def delete_teacher(id: str):
    """Delete a teacher."""
    if storage.delete_teacher(id):
        return {"success": True, "message": f"Teacher {id} deleted"}
    raise HTTPException(status_code=404, detail=f"Teacher {id} not found")


@app.get("/api/teachers/{id}/matches")
def get_teacher_matches(id: str):
    """
    Teacher matching preview endpoint.
    Returns courses this teacher would be matched to based on domain tags.
    """
    matches = storage.get_teacher_matches(id)
    return {
        "teacher_id": id,
        "matches": [
            {
                "course_code": m["course"].code,
                "course_name": m["course"].name,
                "overlap_tags": m["overlap_tags"],
                "overlap_count": m["overlap_count"],
                "score": m["score"]
            }
            for m in matches
        ],
        "total_matches": len(matches)
    }


# ═════════════════════════════════════════════════════════════════
# Rooms API
# ═════════════════════════════════════════════════════════════════

@app.get("/api/rooms", response_model=List[Room])
def get_rooms():
    """List all rooms."""
    return storage.get_rooms()


@app.post("/api/rooms", response_model=dict)
def create_room(room: Room):
    """Add a new room."""
    if storage.add_room(room):
        return {"success": True, "message": f"Room {room.id} created"}
    raise HTTPException(status_code=400, detail=f"Room {room.id} already exists")


@app.put("/api/rooms/{id}", response_model=dict)
def update_room(id: str, room: Room):
    """Update a room."""
    if storage.update_room(id, room):
        return {"success": True, "message": f"Room {id} updated"}
    raise HTTPException(status_code=404, detail=f"Room {id} not found")


@app.delete("/api/rooms/{id}", response_model=dict)
def delete_room(id: str):
    """Delete a room."""
    if storage.delete_room(id):
        return {"success": True, "message": f"Room {id} deleted"}
    raise HTTPException(status_code=404, detail=f"Room {id} not found")


# ═════════════════════════════════════════════════════════════════
# Sections API
# ═════════════════════════════════════════════════════════════════

@app.get("/api/sections", response_model=List[Section])
def get_sections():
    """List all sections."""
    return storage.get_sections()


@app.post("/api/sections", response_model=dict)
def create_section(section: Section):
    """Add a new section."""
    if storage.add_section(section):
        return {"success": True, "message": f"Section {section.id} created"}
    raise HTTPException(status_code=400, detail=f"Section {section.id} already exists")


# ═════════════════════════════════════════════════════════════════
# Tags API
# ═════════════════════════════════════════════════════════════════

@app.get("/api/tags")
def get_tags():
    """Return the full TAG_TAXONOMY dictionary."""
    return TAG_TAXONOMY


# ═════════════════════════════════════════════════════════════════
# Curriculum API
# ═════════════════════════════════════════════════════════════════

@app.get("/api/curriculum")
def get_curriculum():
    """Return the full curriculum map."""
    return storage.get_curriculum()


@app.put("/api/curriculum")
def update_curriculum(entry: CurriculumEntry):
    """Update a (program, semester) entry in the curriculum."""
    curriculum = storage.get_curriculum()
    key = f"{entry.program}_sem{entry.semester}"
    curriculum[key] = entry.course_codes
    storage.set_curriculum(curriculum)
    return {"success": True, "key": key, "course_codes": entry.course_codes}


# ═════════════════════════════════════════════════════════════════
# Schedule API
# ═════════════════════════════════════════════════════════════════

def _run_scheduler(iterations: int, initial_temp: float):
    """Run scheduler in background thread."""
    # Convert Pydantic models to dataclasses for scheduler
    courses_data = [
        CourseData(
            code=c.code,
            name=c.name,
            credit_hours=c.credit_hours,
            department=c.department,
            is_lab=c.is_lab,
            sessions_per_week=c.sessions_per_week,
            semester=c.semester,
            is_elective=c.is_elective,
            domain_tags=c.domain_tags
        )
        for c in storage.get_courses()
    ]

    teachers_data = [
        TeacherData(
            id=t.id,
            name=t.name,
            department=t.department,
            domain_tags=t.domain_tags,
            max_sessions_per_week=t.max_sessions_per_week
        )
        for t in storage.get_teachers()
    ]

    rooms_data = [
        RoomData(
            id=r.id,
            name=r.name,
            capacity=r.capacity,
            room_type=r.room_type,
            department=r.department
        )
        for r in storage.get_rooms()
    ]

    sections_data = [
        SectionData(
            id=s.id,
            program=s.program,
            semester=s.semester,
            department=s.department,
            student_count=s.student_count,
            course_codes=s.course_codes
        )
        for s in storage.get_sections()
    ]

    schedule, conflicts, unscheduled = scheduler_generate(
        courses_data,
        teachers_data,
        rooms_data,
        sections_data,
        iterations=iterations,
        initial_temp=initial_temp
    )

    # Convert ScheduleEntryData back to ScheduleEntry Pydantic models
    schedule_entries = [
        ScheduleEntry(
            course_code=e.course_code,
            teacher_id=e.teacher_id,
            room_id=e.room_id,
            section_id=e.section_id,
            day=e.day,
            period=e.period,
            start_time=e.start_time,
            end_time=e.end_time
        )
        for e in schedule
    ]

    storage.set_schedule(schedule_entries, conflicts)
    return len(schedule), len(unscheduled), len(conflicts)


@app.post("/api/schedule/generate", response_model=ScheduleGenerateResponse)
def generate_schedule(request: ScheduleGenerateRequest, background_tasks: BackgroundTasks):
    """
    Generate schedule using the algorithm.
    Runs in background thread for non-blocking execution.
    """
    result_container = {}

    def run_and_store():
        scheduled, unscheduled, conflicts = _run_scheduler(
            request.iterations,
            request.initial_temp
        )
        result_container['scheduled'] = scheduled
        result_container['unscheduled'] = unscheduled
        result_container['conflicts'] = conflicts

    # Run in thread
    thread = threading.Thread(target=run_and_store)
    thread.start()
    thread.join()

    return ScheduleGenerateResponse(
        success=result_container['unscheduled'] == 0,
        entries_scheduled=result_container['scheduled'],
        entries_unscheduled=result_container['unscheduled'],
        conflicts_detected=result_container['conflicts'],
        message=f"Scheduled {result_container['scheduled']} entries, "
                f"{result_container['unscheduled']} unscheduled, "
                f"{result_container['conflicts']} conflicts"
    )


@app.get("/api/schedule/results", response_model=List[ScheduleEntry])
def get_schedule_results():
    """Return the last generated schedule."""
    return storage.get_schedule()


@app.get("/api/schedule/conflicts")
def get_schedule_conflicts():
    """Return conflicts from last schedule generation."""
    return {
        "conflicts": storage.get_conflicts(),
        "count": len(storage.get_conflicts())
    }


@app.get("/api/schedule/export/csv")
def export_schedule_csv():
    """Export schedule as CSV file."""
    schedule = storage.get_schedule()
    courses = {c.code: c for c in storage.get_courses()}
    teachers = {t.id: t for t in storage.get_teachers()}
    rooms = {r.id: r for r in storage.get_rooms()}
    sections = {s.id: s for s in storage.get_sections()}

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "Day", "Period", "Start Time", "End Time",
        "Course Code", "Course Name",
        "Section", "Teacher", "Room",
        "Type", "Department"
    ])

    # Sort by day, then period
    sorted_schedule = sorted(schedule, key=lambda e: (e.day, e.period))

    for entry in sorted_schedule:
        course = courses.get(entry.course_code)
        teacher = teachers.get(entry.teacher_id)
        room = rooms.get(entry.room_id)
        section = sections.get(entry.section_id)

        writer.writerow([
            entry.day,
            entry.period,
            entry.start_time,
            entry.end_time,
            entry.course_code,
            course.name if course else "Unknown",
            entry.section_id,
            teacher.name if teacher else entry.teacher_id,
            room.name if room else entry.room_id,
            "Lab" if (course and course.is_lab) else "Theory",
            course.department.value if course else "Unknown"
        ])

    output.seek(0)

    filename = f"giki_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
