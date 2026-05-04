from enum import Enum
from typing import List, Dict
from pydantic import BaseModel
from dataclasses import dataclass


class DepartmentEnum(str, Enum):
    FCSE = "FCSE"
    FEE = "FEE"
    FME = "FME"
    FMCE = "FMCE"
    CIVIL = "CIVIL"
    SMS = "SMS"
    BASIC_SCIENCE = "BASIC_SCIENCE"
    COMMON = "COMMON"


class RoomTypeEnum(str, Enum):
    LECTURE_HALL = "LECTURE_HALL"
    LAB = "LAB"
    SEMINAR = "SEMINAR"
    AUDITORIUM = "AUDITORIUM"


# Pydantic models
class Course(BaseModel):
    code: str
    name: str
    credit_hours: int
    department: DepartmentEnum
    is_lab: bool
    sessions_per_week: int
    semester: int
    is_elective: bool
    domain_tags: List[str]


class Teacher(BaseModel):
    id: str
    name: str
    department: DepartmentEnum
    domain_tags: List[str]
    max_sessions_per_week: int = 15


class Room(BaseModel):
    id: str
    name: str
    capacity: int
    room_type: RoomTypeEnum
    department: DepartmentEnum


class Section(BaseModel):
    id: str
    program: str
    semester: int
    department: DepartmentEnum
    student_count: int
    course_codes: List[str]


class TimeSlot(BaseModel):
    day: str  # Mon-Fri
    period: int  # 1-8
    start_time: str
    end_time: str


class ScheduleEntry(BaseModel):
    course_code: str
    teacher_id: str
    room_id: str
    section_id: str
    day: str
    period: int
    start_time: str
    end_time: str


# Dataclasses
@dataclass
class CourseData:
    code: str
    name: str
    credit_hours: int
    department: DepartmentEnum
    is_lab: bool
    sessions_per_week: int
    semester: int
    is_elective: bool
    domain_tags: List[str]


@dataclass
class TeacherData:
    id: str
    name: str
    department: DepartmentEnum
    domain_tags: List[str]
    max_sessions_per_week: int = 15


@dataclass
class RoomData:
    id: str
    name: str
    capacity: int
    room_type: RoomTypeEnum
    department: DepartmentEnum


@dataclass
class SectionData:
    id: str
    program: str
    semester: int
    department: DepartmentEnum
    student_count: int
    course_codes: List[str]


@dataclass
class TimeSlotData:
    day: str  # Mon-Fri
    period: int  # 1-8
    start_time: str
    end_time: str


@dataclass
class ScheduleEntryData:
    course_code: str
    teacher_id: str
    room_id: str
    section_id: str
    day: str
    period: int
    start_time: str
    end_time: str


TAG_TAXONOMY: Dict[str, List[str]] = {
    "Mathematics": [
        "calculus", "linear_algebra", "discrete_math", "numerical_analysis",
        "differential_equations", "statistics", "probability", "mathematics"
    ],
    "CS Core": [
        "algorithms", "complexity", "data_structures", "operating_systems",
        "computer_organization", "digital_logic", "compiler", "formal_languages",
        "intro_programming", "oop", "databases", "ict", "computing", "advanced_dbms"
    ],
    "CS Advanced": [
        "networks", "distributed", "parallel_computing", "cloud",
        "computer_architecture", "microprocessor", "embedded", "hardware", "iot",
        "unix_admin"
    ],
    "Bioinformatics": [
        "bioinformatics"
    ],
    "AI & Data": [
        "ai", "machine_learning", "deep_learning", "neural_networks",
        "computer_vision", "nlp", "knowledge_representation", "data_science", "big_data",
        "data_mining", "visualization", "reinforcement_learning", "image_processing",
        "data_warehousing", "data_engineering", "theory_of_data_science", "inferential_stats"
    ],
    "Security": [
        "cyber_security", "cryptography", "information_security", "digital_forensics",
        "ethical_hacking", "secure_software"
    ],
    "Software Engineering": [
        "software_engineering", "requirements", "architecture",
        "software_construction", "quality", "devops", "web_engineering", "mobile",
        "project_management", "professional_issues", "ui_ux", "design_patterns"
    ],
    "Electrical Engineering": [
        "circuit_analysis", "electrical_networks", "electronic_devices",
        "signals", "dsp", "electromagnetic", "power", "power_electronics", "power_distribution",
        "electric_machines", "drives", "instrumentation", "control_systems",
        "communication_systems", "robotics", "applied_ee"
    ],
    "Mechanical Engineering": [
        "statics", "dynamics", "mechanics", "mechanics_of_solids",
        "thermodynamics", "heat_transfer", "fluid_mechanics", "manufacturing", "machine_elements",
        "theory_of_machines", "vibration", "stress_analysis", "workshop", "engineering_graphics"
    ],
    "Materials Engineering": [
        "materials_science", "thermodynamics_mm", "phase_equilibria",
        "strength_materials", "alloy", "materials_chemistry", "ceramics", "polymers",
        "mineral_processing", "xrd", "nanotechnology", "materials_lab", "manufacturing_mm",
        "materials_evaluation", "deformation_fracture", "heat_treatment", "joining_materials",
        "cad_cam", "corrosion"
    ],
    "Chemical Engineering": [
        "chemical_engineering", "thermodynamics_ch", "mass_transfer",
        "heat_transfer_ch", "fluid_mechanics_ch", "reaction_kinetics", "process_modelling",
        "particle_technology", "analytical_chemistry", "energy_engineering",
        "environmental_engineering", "separation_processes", "plant_design", "transport"
    ],
    "Civil Engineering": [
        "surveying", "structural_analysis", "rc_design", "steel_design",
        "mechanics_of_solids", "soil_mechanics", "geotechnical", "fluid_mechanics_cv",
        "hydrology", "transportation", "highway", "geology", "concrete_technology",
        "construction", "environmental_engineering_cv", "geo_informatics", "construction_management",
        "cost_estimation"
    ],
    "Management & Humanities": [
        "business_mathematics", "accounting", "financial_management",
        "business_finance", "marketing", "management", "hrm", "organizational_behavior",
        "economics", "microeconomics", "macroeconomics", "entrepreneurship", "supply_chain",
        "operations_management", "business_analytics", "strategy", "research_methods",
        "decision_analysis", "leadership", "engineering_economy", "consumer_behavior"
    ],
    "Humanities & Common": [
        "communication_skills", "critical_thinking", "writing",
        "islamic_studies", "pakistan_studies", "ideology", "civics", "sociology", "humanities",
        "law", "ethics", "professional_ethics", "business_comm", "innovation_lab", "makers_lab",
        "understanding_quran", "technical_writing", "art_of_learning", "history",
        "ir_affairs", "anthropology", "oral_communication"
    ],
    "Physics & Chemistry": [
        "physics", "applied_physics", "chemistry", "occupational_health"
    ]
}
