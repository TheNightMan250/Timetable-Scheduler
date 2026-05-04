import json
import os
from typing import List, Optional, Dict, Any

# Handle imports for both direct execution and module import
try:
    from backend.data_models import Course, Teacher, Room, Section, ScheduleEntry, TAG_TAXONOMY
    from backend import seed_data
except ImportError:
    from data_models import Course, Teacher, Room, Section, ScheduleEntry, TAG_TAXONOMY
    import seed_data

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# In-memory storage
_courses: List[Course] = []
_teachers: List[Teacher] = []
_rooms: List[Room] = []
_sections: List[Section] = []
_schedule: List[ScheduleEntry] = []
_conflicts: List[str] = []
_curriculum: Dict[str, Any] = {}


def init_storage():
    """Initialize storage from JSON files or seed_data on startup."""
    global _courses, _teachers, _rooms, _sections, _schedule, _curriculum

    # Try to load from JSON first
    courses_data = load_courses()
    if courses_data is not None and len(courses_data) > 0:
        _courses = courses_data
    else:
        # Fall back to seed_data - load RAW_COURSES
        _courses = []
        for c in seed_data.get_seed_courses():
            _courses.append(Course(**c))
        save_courses(_courses)

    teachers_data = load_teachers()
    if teachers_data is not None:
        _teachers = teachers_data
    else:
        # Convert RAW_TEACHERS from seed_data (tuples) to Teacher objects
        _teachers = []
        for t in seed_data.get_seed_teachers():
            # RAW_TEACHERS format: (id, name, department, domain_tags)
            _teachers.append(Teacher(
                id=t[0],
                name=t[1],
                department=t[2],
                domain_tags=t[3]
            ))
        save_teachers(_teachers)

    rooms_data = load_rooms()
    if rooms_data is not None:
        _rooms = rooms_data
    else:
        # Convert ROOMS from seed_data (dicts) to Room objects
        _rooms = []
        for r in seed_data.get_seed_rooms():
            _rooms.append(Room(
                id=r["id"],
                name=r["name"],
                capacity=r["capacity"],
                room_type=r["room_type"],
                department=r["department"]
            ))
        save_rooms(_rooms)

    sections_data = load_sections()
    if sections_data is not None:
        _sections = sections_data
    else:
        # Generate sections from CURRICULUM map - never hardcode section course lists
        _sections = []
        section_dicts = seed_data.generate_sections_from_curriculum()
        for s in section_dicts:
            _sections.append(Section(**s))
        save_sections(_sections)

    schedule_data = load_schedule()
    if schedule_data is not None:
        _schedule = schedule_data
    else:
        _schedule = []

# Helper function to load JSON from file

def _load_json(filename: str):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Helper function to save JSON to file

def _save_json(filename: str, data):
    path = os.path.join(DATA_DIR, filename)
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Load all entities

def load_courses() -> Optional[List[Course]]:
    data = _load_json("courses.json")
    if data is None:
        return None
    return [Course(**item) for item in data]


def load_teachers() -> Optional[List[Teacher]]:
    data = _load_json("teachers.json")
    if data is None:
        return None
    return [Teacher(**item) for item in data]


def load_rooms() -> Optional[List[Room]]:
    data = _load_json("rooms.json")
    if data is None:
        return None
    return [Room(**item) for item in data]


def load_sections() -> Optional[List[Section]]:
    data = _load_json("sections.json")
    if data is None:
        return None
    return [Section(**item) for item in data]


def load_schedule() -> Optional[List[ScheduleEntry]]:
    data = _load_json("schedule.json")
    if data is None:
        return None
    return [ScheduleEntry(**item) for item in data]

# Save all entities

def save_courses(courses: List[Course]):
    _save_json("courses.json", [course.dict() for course in courses])


def save_teachers(teachers: List[Teacher]):
    _save_json("teachers.json", [teacher.dict() for teacher in teachers])


def save_rooms(rooms: List[Room]):
    _save_json("rooms.json", [room.dict() for room in rooms])


def save_sections(sections: List[Section]):
    _save_json("sections.json", [section.dict() for section in sections])


def save_schedule(schedule: List[ScheduleEntry]):
    _save_json("schedule.json", [entry.dict() for entry in schedule])

# ═════════════════════════════════════════════════════════════════
# In-Memory Data Access
# ═════════════════════════════════════════════════════════════════

def get_courses() -> List[Course]:
    return _courses


def get_teachers() -> List[Teacher]:
    return _teachers


def get_rooms() -> List[Room]:
    return _rooms


def get_sections() -> List[Section]:
    return _sections


def get_schedule() -> List[ScheduleEntry]:
    return _schedule


def get_conflicts() -> List[str]:
    return _conflicts


def get_curriculum() -> Dict[str, Any]:
    return _curriculum


def set_schedule(schedule: List[ScheduleEntry], conflicts: List[str]):
    global _schedule, _conflicts
    _schedule = schedule
    _conflicts = conflicts
    save_schedule(_schedule)


def set_curriculum(curriculum: Dict[str, Any]):
    global _curriculum
    _curriculum = curriculum
    _save_json("curriculum.json", _curriculum)


# ═════════════════════════════════════════════════════════════════
# CRUD Operations for Courses
# ═════════════════════════════════════════════════════════════════

def add_course(course: Course) -> bool:
    # Check for duplicate code
    for c in _courses:
        if c.code == course.code:
            return False
    _courses.append(course)
    save_courses(_courses)
    return True


def update_course(code: str, updated_course: Course) -> bool:
    for i, c in enumerate(_courses):
        if c.code == code:
            _courses[i] = updated_course
            save_courses(_courses)
            return True
    return False


def delete_course(code: str) -> bool:
    for i, c in enumerate(_courses):
        if c.code == code:
            del _courses[i]
            save_courses(_courses)
            return True
    return False


# ═════════════════════════════════════════════════════════════════
# CRUD Operations for Teachers
# ═════════════════════════════════════════════════════════════════

def add_teacher(teacher: Teacher) -> bool:
    # Check for duplicate ID
    for t in _teachers:
        if t.id == teacher.id:
            return False
    _teachers.append(teacher)
    save_teachers(_teachers)
    return True


def update_teacher(id: str, updated_teacher: Teacher) -> bool:
    for i, t in enumerate(_teachers):
        if t.id == id:
            _teachers[i] = updated_teacher
            save_teachers(_teachers)
            return True
    return False


def delete_teacher(id: str) -> bool:
    for i, t in enumerate(_teachers):
        if t.id == id:
            del _teachers[i]
            save_teachers(_teachers)
            return True
    return False


# ═════════════════════════════════════════════════════════════════
# CRUD Operations for Rooms
# ═════════════════════════════════════════════════════════════════

def add_room(room: Room) -> bool:
    # Check for duplicate ID
    for r in _rooms:
        if r.id == room.id:
            return False
    _rooms.append(room)
    save_rooms(_rooms)
    return True


def update_room(id: str, updated_room: Room) -> bool:
    for i, r in enumerate(_rooms):
        if r.id == id:
            _rooms[i] = updated_room
            save_rooms(_rooms)
            return True
    return False


def delete_room(id: str) -> bool:
    for i, r in enumerate(_rooms):
        if r.id == id:
            del _rooms[i]
            save_rooms(_rooms)
            return True
    return False


# ═════════════════════════════════════════════════════════════════
# CRUD Operations for Sections
# ═════════════════════════════════════════════════════════════════

def add_section(section: Section) -> bool:
    # Check for duplicate ID
    for s in _sections:
        if s.id == section.id:
            return False
    _sections.append(section)
    save_sections(_sections)
    return True


def update_section(id: str, updated_section: Section) -> bool:
    for i, s in enumerate(_sections):
        if s.id == id:
            _sections[i] = updated_section
            save_sections(_sections)
            return True
    return False


def delete_section(id: str) -> bool:
    for i, s in enumerate(_sections):
        if s.id == id:
            del _sections[i]
            save_sections(_sections)
            return True
    return False


# ═════════════════════════════════════════════════════════════════
# Teacher-Course Matching
# ═════════════════════════════════════════════════════════════════

def get_teacher_matches(teacher_id: str) -> List[dict]:
    """Get courses that match a teacher's domain tags."""
    teacher = None
    for t in _teachers:
        if t.id == teacher_id:
            teacher = t
            break

    if not teacher:
        return []

    matches = []
    teacher_tags = set(teacher.domain_tags)

    for course in _courses:
        course_tags = set(course.domain_tags)
        overlap = teacher_tags & course_tags
        overlap_count = len(overlap)

        if overlap_count > 0:
            # Department bonus
            dept_bonus = 0
            if teacher.department == course.department:
                dept_bonus = 3
            elif teacher.department.value in ["COMMON", "BASIC_SCIENCE"]:
                dept_bonus = 2

            score = (overlap_count * 10) + dept_bonus

            matches.append({
                "course": course,
                "overlap_tags": list(overlap),
                "overlap_count": overlap_count,
                "score": score
            })

    # Sort by score descending
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches

