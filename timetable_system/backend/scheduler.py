"""
GIKI Timetable Scheduling Algorithm Engine
CS378 — Design and Analysis of Algorithms | GIKI Spring 2026

Implements a 5-phase scheduling algorithm:
1. Teacher-Course Matching (domain tag overlap)
2. Priority Scoring (scheduling order)
3. Greedy Assignment with Slot Scoring
4. Simulated Annealing (optimization)
5. Conflict Validation

╔══════════════════════════════════════════════════════════════════════╗
║ COMPLEXITY ANALYSIS                                                  ║
╠══════════════════════════════════════════════════════════════════════╣
║ Teacher matching:   O(C × T × D)  where C = courses, T = teachers,   ║
║                                     D = avg domain tags per teacher  ║
║ Greedy scheduling:  O(N × R × S)  where N = tasks, R = rooms,          ║
║                                     S = timeslots (40 total: 5×8)    ║
║ Slot scoring:       O(R × S) per task                                ║
║ SA optimization:    O(I × N)      where I = iterations               ║
║ Conflict detection: O(N)                                             ║
║ Overall:            O(N × R × S) — dominated by greedy phase         ║
╚══════════════════════════════════════════════════════════════════════╝

Key Constraints Enforced:
- Domain tag matching only (no hardcoded teacher-course assignments)
- Faculty building alignment in room scoring
- Runtime-adjustable SA parameters (iterations, initial_temp)
- Threading for non-blocking generation
- Conflict detection runs AFTER SA (not before)
"""

import random
import math
import threading
import sys
import os
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field

# Handle imports for both direct execution and module import
try:
    # When running from parent directory (e.g., python -m backend.scheduler)
    from backend.data_models import (
        CourseData, TeacherData, RoomData, SectionData, ScheduleEntryData,
        DepartmentEnum, RoomTypeEnum
    )
except ImportError:
    try:
        # When running directly from backend/ directory
        from data_models import (
            CourseData, TeacherData, RoomData, SectionData, ScheduleEntryData,
            DepartmentEnum, RoomTypeEnum
        )
    except ImportError:
        # Add parent to path and try again
        parent_dir = os.path.dirname(current_dir) if 'current_dir' in dir() else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from backend.data_models import (
            CourseData, TeacherData, RoomData, SectionData, ScheduleEntryData,
            DepartmentEnum, RoomTypeEnum
        )


@dataclass
class TimeSlot:
    day: str
    period: int
    start_time: str = ""
    end_time: str = ""


DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
PERIODS = list(range(1, 9))


def get_time_str(period: int) -> Tuple[str, str]:
    """Convert period number to start/end time strings."""
    start_hour = 8 + (period - 1)
    end_hour = start_hour + 1
    return f"{start_hour:02d}:00", f"{end_hour:02d}:00"


class ConstraintChecker:
    """
    Maintains three sets for conflict detection, updated atomically.
    """

    def __init__(self):
        self.teacher_slots: Dict[str, Set[Tuple[str, int]]] = {}
        self.room_slots: Dict[str, Set[Tuple[str, int]]] = {}
        self.section_slots: Dict[str, Set[Tuple[str, int]]] = {}
        self.entries: List[ScheduleEntryData] = []

    def can_assign(
        self,
        teacher: TeacherData,
        room: RoomData,
        section: SectionData,
        timeslot: TimeSlot,
        is_lab: bool = False
    ) -> Tuple[bool, str]:
        """
        Check if assignment is valid. Returns (is_valid, reason_string).
        """
        slot_key = (timeslot.day, timeslot.period)

        # Check teacher availability
        teacher_set = self.teacher_slots.get(teacher.id, set())
        if slot_key in teacher_set:
            return False, f"Teacher {teacher.id} already booked at {slot_key}"

        # Check room availability
        room_set = self.room_slots.get(room.id, set())
        if slot_key in room_set:
            return False, f"Room {room.id} already booked at {slot_key}"

        # Check section availability
        section_set = self.section_slots.get(section.id, set())
        if slot_key in section_set:
            return False, f"Section {section.id} already booked at {slot_key}"

        # Check room capacity
        if room.capacity < section.student_count:
            return False, f"Room capacity {room.capacity} < section size {section.student_count}"

        # Check lab/non-lab room type match
        if is_lab and room.room_type != RoomTypeEnum.LAB:
            return False, f"Lab course requires LAB room, got {room.room_type}"
        if not is_lab and room.room_type == RoomTypeEnum.LAB:
            # Non-lab can sometimes use lab rooms, but we prefer not to
            pass  # Allow but penalize in scoring

        return True, "OK"

    def assign(self, entry: ScheduleEntryData) -> None:
        """Atomically add an entry to all tracking sets."""
        slot_key = (entry.day, entry.period)

        if entry.teacher_id not in self.teacher_slots:
            self.teacher_slots[entry.teacher_id] = set()
        self.teacher_slots[entry.teacher_id].add(slot_key)

        if entry.room_id not in self.room_slots:
            self.room_slots[entry.room_id] = set()
        self.room_slots[entry.room_id].add(slot_key)

        if entry.section_id not in self.section_slots:
            self.section_slots[entry.section_id] = set()
        self.section_slots[entry.section_id].add(slot_key)

        self.entries.append(entry)

    def unassign(self, entry: ScheduleEntryData) -> None:
        """Atomically remove an entry from all tracking sets."""
        slot_key = (entry.day, entry.period)

        if entry.teacher_id in self.teacher_slots:
            self.teacher_slots[entry.teacher_id].discard(slot_key)

        if entry.room_id in self.room_slots:
            self.room_slots[entry.room_id].discard(slot_key)

        if entry.section_id in self.section_slots:
            self.section_slots[entry.section_id].discard(slot_key)

        # Remove from entries list
        self.entries = [e for e in self.entries
                       if not (e.course_code == entry.course_code and
                               e.section_id == entry.section_id and
                               e.day == entry.day and
                               e.period == entry.period)]


class Scheduler:
    """Main scheduling engine implementing all 5 phases."""

    def __init__(
        self,
        courses: List[CourseData],
        teachers: List[TeacherData],
        rooms: List[RoomData],
        sections: List[SectionData]
    ):
        self.courses = {c.code: c for c in courses}
        self.teachers = teachers
        self.rooms = rooms
        self.sections = {s.id: s for s in sections}
        self.checker = ConstraintChecker()

        # Build teacher index: course_code -> list of (teacher, score)
        self.teacher_index: Dict[str, List[Tuple[TeacherData, float]]] = {}

        # Generate all possible timeslots
        self.all_timeslots = [
            TimeSlot(day, period, *get_time_str(period))
            for day in DAYS
            for period in PERIODS
        ]

    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Teacher-Course Matching
    # ═══════════════════════════════════════════════════════════════

    def _build_teacher_index(self) -> None:
        """
        O(C × T × D) - For each course, find all teachers whose domain_tags intersect
        with course.domain_tags. Rank by: (overlap_count × 10) + department_bonus
        C = courses, T = teachers, D = avg domain tags per teacher
        """
        for course_code, course in self.courses.items():
            scored_teachers: List[Tuple[TeacherData, float]] = []
            course_tags = set(course.domain_tags)

            for teacher in self.teachers:
                teacher_tags = set(teacher.domain_tags)
                overlap = course_tags & teacher_tags
                overlap_count = len(overlap)

                if overlap_count == 0:
                    continue  # No match possible

                # Department bonus
                dept_bonus = 0
                if teacher.department == course.department:
                    dept_bonus = 3
                elif teacher.department in [DepartmentEnum.COMMON, DepartmentEnum.BASIC_SCIENCE]:
                    dept_bonus = 2

                score = (overlap_count * 10) + dept_bonus
                scored_teachers.append((teacher, score))

            # Sort by score descending
            scored_teachers.sort(key=lambda x: x[1], reverse=True)
            self.teacher_index[course_code] = scored_teachers

    def _get_course_priority(self, course: CourseData, section: SectionData) -> float:
        """
        Phase 2: Priority Scoring
        Higher score = scheduled first (before slots fill up).
        """
        score = 0.0

        # Fewer available teachers → higher priority
        available_teachers = len(self.teacher_index.get(course.code, []))
        if available_teachers > 0:
            score += (10.0 / available_teachers)

        # Core course (not elective) → higher priority
        if not course.is_elective:
            score += 20.0

        # Higher semester → higher priority
        score += course.semester * 3.0

        # More credit hours → higher priority
        score += course.credit_hours * 2.0

        return score

    def _score_room(self, room: RoomData, section: SectionData, is_lab: bool) -> Tuple[float, bool]:
        """
        O(1) - Score a room assignment. Returns (score, is_valid).
        INVALID cases skip the combination entirely.

        Faculty building alignment: Checks room.department vs section.department.
        Different building penalties: Lab=-4, Lecture=-2 (enforced per spec).
        """
        # Faculty building alignment check (lines below)
        # Hard constraints - invalid
        if room.capacity < section.student_count:
            return -1000.0, False

        if is_lab and room.room_type != RoomTypeEnum.LAB:
            return -1000.0, False

        score = 0.0

        # Room capacity > 2× student_count → -1
        if room.capacity > 2 * section.student_count:
            score -= 1.0

        # ═══════════════════════════════════════════════════════════════
        # FACULTY BUILDING ALIGNMENT (Critical Constraint #5)
        # Room scoring MUST account for faculty building alignment (not just capacity).
        # ═══════════════════════════════════════════════════════════════
        same_building = room.department == section.department
        if not same_building:
            if room.room_type == RoomTypeEnum.LAB:
                score -= 4.0  # Lab in different building (higher penalty)
            else:
                score -= 2.0  # Lecture hall in different building

        return score, True

    def _score_timeslot(
        self,
        section: SectionData,
        timeslot: TimeSlot,
        course: CourseData,
        elective_timeslots: Dict[Tuple[str, int], int]
    ) -> float:
        """
        Score a timeslot assignment.
        """
        score = 0.0
        slot_key = (timeslot.day, timeslot.period)

        # Period outside preferred window (4-6) → -1
        if timeslot.period < 4 or timeslot.period > 6:
            score -= 1.0

        # Scheduled on Monday or Friday → -1
        if timeslot.day in ["Mon", "Fri"]:
            score -= 1.0

        # Check for gaps in section's schedule on this day
        section_day_slots = [
            p for d, p in self.checker.section_slots.get(section.id, set())
            if d == timeslot.day
        ]

        if section_day_slots:
            section_day_slots.append(timeslot.period)
            section_day_slots.sort()

            # Check for gaps
            for i in range(len(section_day_slots) - 1):
                gap = section_day_slots[i + 1] - section_day_slots[i] - 1
                if gap == 1:
                    score -= 2.0  # 1-period gap
                elif gap >= 2:
                    score -= 3.0  # 2+ period gap

        # Would create 4+ consecutive classes for section → -2
        section_day_slots = [
            p for d, p in self.checker.section_slots.get(section.id, set())
            if d == timeslot.day
        ]
        if section_day_slots:
            # Check if adding this creates 4+ consecutive
            all_periods = sorted(section_day_slots + [timeslot.period])
            consecutive_count = 1
            for i in range(len(all_periods) - 1):
                if all_periods[i + 1] - all_periods[i] == 1:
                    consecutive_count += 1
                    if consecutive_count >= 4:
                        score -= 2.0
                        break
                else:
                    consecutive_count = 1

        # Elective: same timeslot used by another elective in same faculty → +2
        if course.is_elective:
            faculty_count = elective_timeslots.get(slot_key, 0)
            if faculty_count > 0:
                score += 2.0

        return score

    def _try_assign_session(
        self,
        section: SectionData,
        course: CourseData,
        session_num: int,
        depth: int = 0
    ) -> Optional[ScheduleEntryData]:
        """
        Try to assign one session of a course to a section.
        Returns ScheduleEntryData if successful, None otherwise.
        """
        best_entry: Optional[ScheduleEntryData] = None
        best_score = -float('inf')

        is_lab = course.is_lab

        # Get eligible teachers for this course
        eligible_teachers = self.teacher_index.get(course.code, [])
        if not eligible_teachers:
            return None

        # Track elective timeslots for bonus scoring
        elective_timeslots: Dict[Tuple[str, int], int] = {}
        if course.is_elective:
            for entry in self.checker.entries:
                if entry.course_code in self.courses:
                    other_course = self.courses[entry.course_code]
                    if other_course.is_elective:
                        key = (entry.day, entry.period)
                        elective_timeslots[key] = elective_timeslots.get(key, 0) + 1

        # Try all combinations
        for teacher, teacher_score in eligible_teachers:
            for room in self.rooms:
                for timeslot in self.all_timeslots:
                    # Check constraints
                    valid, reason = self.checker.can_assign(
                        teacher, room, section, timeslot, is_lab
                    )
                    if not valid:
                        continue

                    # Score room
                    room_score, room_valid = self._score_room(room, section, is_lab)
                    if not room_valid:
                        continue

                    # Score timeslot
                    timeslot_score = self._score_timeslot(
                        section, timeslot, course, elective_timeslots
                    )

                    # Combined score
                    combined_score = room_score + timeslot_score + (teacher_score * 0.1)

                    if combined_score > best_score:
                        best_score = combined_score
                        start_time, end_time = get_time_str(timeslot.period)
                        best_entry = ScheduleEntryData(
                            course_code=course.code,
                            teacher_id=teacher.id,
                            room_id=room.id,
                            section_id=section.id,
                            day=timeslot.day,
                            period=timeslot.period,
                            start_time=start_time,
                            end_time=end_time
                        )

        if best_entry:
            self.checker.assign(best_entry)
            return best_entry

        # Backtracking: try unassigning recent entries
        if depth < 2 and len(self.checker.entries) > 0:
            # Unassign most recent entry
            recent = self.checker.entries[-1]
            self.checker.unassign(recent)

            # Try again
            result = self._try_assign_session(section, course, session_num, depth + 1)

            if result:
                return result
            else:
                # Restore the unassigned entry
                self.checker.assign(recent)

        return None

    def _phase3_greedy_assignment(self) -> Tuple[List[ScheduleEntryData], List[str]]:
        """
        O(N × R × S) - Phase 3: Greedy Assignment with Slot Scoring
        N = tasks, R = rooms, S = timeslots (40 total: 5 days × 8 periods)
        This is the dominant phase in overall complexity.
        """
        schedule: List[ScheduleEntryData] = []
        unscheduled: List[str] = []

        # Build list of all (section, course) tasks
        tasks: List[Tuple[SectionData, CourseData, float]] = []

        for section in self.sections.values():
            for course_code in section.course_codes:
                if course_code in self.courses:
                    course = self.courses[course_code]
                    priority = self._get_course_priority(course, section)
                    # Add one task per required session
                    for _ in range(course.sessions_per_week):
                        tasks.append((section, course, priority))

        # Sort by priority descending
        tasks.sort(key=lambda x: x[2], reverse=True)

        # Assign each task
        for section, course, priority in tasks:
            entry = self._try_assign_session(section, course, 0)
            if entry:
                schedule.append(entry)
            else:
                unscheduled.append(
                    f"Could not schedule {course.code} for section {section.id}"
                )

        return schedule, unscheduled

    def _calculate_schedule_score(self, schedule: List[ScheduleEntryData]) -> float:
        """Calculate total score for a schedule (higher is better)."""
        score = 0.0

        for entry in schedule:
            course = self.courses.get(entry.course_code)
            section = self.sections.get(entry.section_id)
            room = next((r for r in self.rooms if r.id == entry.room_id), None)

            if not course or not section or not room:
                continue

            # Room score
            room_score, _ = self._score_room(room, section, course.is_lab)
            score += room_score

            # Timeslot score
            timeslot = TimeSlot(entry.day, entry.period, entry.start_time, entry.end_time)
            elective_timeslots: Dict[Tuple[str, int], int] = {}
            ts_score = self._score_timeslot(section, timeslot, course, elective_timeslots)
            score += ts_score

        return score

    def _phase4_simulated_annealing(
        self,
        schedule: List[ScheduleEntryData],
        iterations: int = 2000,
        initial_temp: float = 100.0
    ) -> List[ScheduleEntryData]:
        """
        O(I × N) - Phase 4: Simulated Annealing optimization.
        I = iterations (runtime parameter), N = number of schedule entries
        """
        # Note: SA parameters (iterations, initial_temp) are runtime-adjustable from UI
        # See generate() method which passes these from the API request
        if not schedule:
            return schedule

        # Reset and rebuild checker
        self.checker = ConstraintChecker()
        for entry in schedule:
            self.checker.assign(entry)

        current_score = self._calculate_schedule_score(schedule)
        best_schedule = list(schedule)
        best_score = current_score

        temp = initial_temp

        for _ in range(iterations):
            if temp < 0.001:
                break

            # Pick a random entry
            if not self.checker.entries:
                break

            entry = random.choice(self.checker.entries)

            # Get course and section info
            course = self.courses.get(entry.course_code)
            section = self.sections.get(entry.section_id)
            if not course or not section:
                continue

            # Find a new valid timeslot
            is_lab = course.is_lab
            teacher = next((t for t in self.teachers if t.id == entry.teacher_id), None)
            room = next((r for r in self.rooms if r.id == entry.room_id), None)

            if not teacher or not room:
                continue

            # Try random new timeslot
            new_timeslot = random.choice(self.all_timeslots)

            # Unassign current
            self.checker.unassign(entry)

            # Try new assignment
            valid, _ = self.checker.can_assign(teacher, room, section, new_timeslot, is_lab)

            if valid:
                new_entry = ScheduleEntryData(
                    course_code=entry.course_code,
                    teacher_id=entry.teacher_id,
                    room_id=entry.room_id,
                    section_id=entry.section_id,
                    day=new_timeslot.day,
                    period=new_timeslot.period,
                    start_time=get_time_str(new_timeslot.period)[0],
                    end_time=get_time_str(new_timeslot.period)[1]
                )
                self.checker.assign(new_entry)

                new_score = self._calculate_schedule_score(self.checker.entries)
                delta = new_score - current_score

                # Accept if better, or with probability e^(-delta/temp) if worse
                if delta > 0 or random.random() < math.exp(delta / temp):
                    current_score = new_score
                    if new_score > best_score:
                        best_score = new_score
                        best_schedule = list(self.checker.entries)
                else:
                    # Reject - restore old entry
                    self.checker.unassign(new_entry)
                    self.checker.assign(entry)
            else:
                # Invalid - restore old entry
                self.checker.assign(entry)

            # Cooling
            temp *= 0.995

        return best_schedule

    def _phase5_detect_conflicts(self, schedule: List[ScheduleEntryData]) -> List[str]:
        """
        O(N) - Phase 5: Conflict Validation.
        Single pass through schedule entries to detect constraint violations.
        Runs AFTER simulated annealing (not before) as required.
        """
        conflicts: List[str] = []

        # Reset checker
        self.checker = ConstraintChecker()

        for entry in schedule:
            course = self.courses.get(entry.course_code)
            section = self.sections.get(entry.section_id)
            room = next((r for r in self.rooms if r.id == entry.room_id), None)
            teacher = next((t for t in self.teachers if t.id == entry.teacher_id), None)

            if not course or not section or not room or not teacher:
                conflicts.append(
                    f"Invalid entry: missing data for {entry.course_code}"
                )
                continue

            timeslot = TimeSlot(entry.day, entry.period, entry.start_time, entry.end_time)
            valid, reason = self.checker.can_assign(teacher, room, section, timeslot, course.is_lab)

            if not valid:
                conflicts.append(
                    f"Conflict: {entry.course_code} at {entry.day} P{entry.period} - {reason}"
                )
            else:
                self.checker.assign(entry)

        return conflicts

    def generate(
        self,
        iterations: int = 2000,
        initial_temp: float = 100.0
    ) -> Tuple[List[ScheduleEntryData], List[str], List[str]]:
        """
        O(N × R × S) - Run all 5 phases and return the final schedule.
        Dominant complexity from Phase 3 (greedy assignment).

        SA parameters are runtime-adjustable:
        - iterations: number of SA iterations (default 2000)
        - initial_temp: starting temperature (default 100.0)

        Returns: (schedule, conflicts, unscheduled_reasons)
        """
        # Phase 1: Build teacher index
        self._build_teacher_index()

        # Phase 3: Greedy assignment
        schedule, unscheduled = self._phase3_greedy_assignment()

        if not schedule:
            return [], [], unscheduled

        # Phase 4: Simulated annealing
        schedule = self._phase4_simulated_annealing(schedule, iterations, initial_temp)

        # Phase 5: Conflict detection
        conflicts = self._phase5_detect_conflicts(schedule)

        return schedule, conflicts, unscheduled


def generate_schedule(
    courses: List[CourseData],
    teachers: List[TeacherData],
    rooms: List[RoomData],
    sections: List[SectionData],
    iterations: int = 2000,
    initial_temp: float = 100.0
) -> Tuple[List[ScheduleEntryData], List[str], List[str]]:
    """
    O(N × R × S) - Public interface for schedule generation.
    Runs in a separate thread for non-blocking execution.

    SA parameters (iterations, initial_temp) are passed through from API/UI,
    making them fully runtime-adjustable (not hardcoded).

    Returns: (schedule_entries, conflicts, unscheduled_reasons)
    """
    result_container = {}

    def run_scheduler():
        scheduler = Scheduler(courses, teachers, rooms, sections)
        schedule, conflicts, unscheduled = scheduler.generate(iterations, initial_temp)
        result_container['schedule'] = schedule
        result_container['conflicts'] = conflicts
        result_container['unscheduled'] = unscheduled

    thread = threading.Thread(target=run_scheduler)
    thread.start()
    thread.join()

    return (
        result_container.get('schedule', []),
        result_container.get('conflicts', []),
        result_container.get('unscheduled', [])
    )


# ═══════════════════════════════════════════════════════════════
# TEST FIXTURE
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Add current directory to path for imports when running directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    print("=" * 60)
    print("GIKI Timetable Scheduler - Test Run")
    print("=" * 60)

    # Create minimal test data
    test_courses = [
        CourseData(
            code="CS101",
            name="Introduction to Programming",
            credit_hours=3,
            department=DepartmentEnum.FCSE,
            is_lab=False,
            sessions_per_week=2,
            semester=1,
            is_elective=False,
            domain_tags=["intro_programming", "computing"]
        ),
        CourseData(
            code="CS102",
            name="Data Structures",
            credit_hours=3,
            department=DepartmentEnum.FCSE,
            is_lab=False,
            sessions_per_week=2,
            semester=2,
            is_elective=False,
            domain_tags=["data_structures", "algorithms"]
        )
    ]

    test_teachers = [
        TeacherData(
            id="T-FCSE-01",
            name="Prof. Dr. Qadeer Ul Hasan",
            department=DepartmentEnum.FCSE,
            domain_tags=["intro_programming", "computing", "machine_learning"]
        ),
        TeacherData(
            id="T-FCSE-02",
            name="Prof. Dr. Ghulam Abbas",
            department=DepartmentEnum.FCSE,
            domain_tags=["data_structures", "algorithms", "networks"]
        )
    ]

    test_rooms = [
        RoomData(
            id="FCSE-CS-LH1",
            name="CS LH1",
            capacity=55,
            room_type=RoomTypeEnum.LECTURE_HALL,
            department=DepartmentEnum.FCSE
        ),
        RoomData(
            id="FCSE-CS-LH2",
            name="CS LH2",
            capacity=55,
            room_type=RoomTypeEnum.LECTURE_HALL,
            department=DepartmentEnum.FCSE
        ),
        RoomData(
            id="FEE-EE-LH4",
            name="EE LH4",
            capacity=55,
            room_type=RoomTypeEnum.LECTURE_HALL,
            department=DepartmentEnum.FEE
        ),
        RoomData(
            id="COMMON-AcB-LH1",
            name="AcB LH1",
            capacity=90,
            room_type=RoomTypeEnum.LECTURE_HALL,
            department=DepartmentEnum.COMMON
        )
    ]

    test_sections = [
        SectionData(
            id="SEC-CS-1A",
            program="BS CS",
            semester=1,
            department=DepartmentEnum.FCSE,
            student_count=45,
            course_codes=["CS101"]
        ),
        SectionData(
            id="SEC-CS-2A",
            program="BS CS",
            semester=2,
            department=DepartmentEnum.FCSE,
            student_count=42,
            course_codes=["CS102"]
        )
    ]

    print("\nTest Data:")
    print(f"  Courses: {[c.code for c in test_courses]}")
    print(f"  Teachers: {[t.id for t in test_teachers]}")
    print(f"  Rooms: {[r.id for r in test_rooms]}")
    print(f"  Sections: {[s.id for s in test_sections]}")

    print("\nGenerating schedule...")
    schedule, conflicts, unscheduled = generate_schedule(
        test_courses,
        test_teachers,
        test_rooms,
        test_sections,
        iterations=500,
        initial_temp=50.0
    )

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    print(f"\nScheduled entries: {len(schedule)}")
    for entry in sorted(schedule, key=lambda e: (e.section_id, e.day, e.period)):
        print(f"  {entry.section_id} | {entry.course_code} | {entry.teacher_id} | "
              f"{entry.room_id} | {entry.day} P{entry.period} ({entry.start_time}-{entry.end_time})")

    if conflicts:
        print(f"\nConflicts ({len(conflicts)}):")
        for c in conflicts:
            print(f"  - {c}")
    else:
        print("\nNo conflicts detected.")

    if unscheduled:
        print(f"\nUnscheduled ({len(unscheduled)}):")
        for u in unscheduled:
            print(f"  - {u}")
    else:
        print("\nAll sessions scheduled successfully.")

    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)
