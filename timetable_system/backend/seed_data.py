"""
GIKI Timetable Scheduler - Seed Data Module

This module provides:
- RAW_ROOMS: Room definitions
- RAW_TEACHERS: Teacher definitions with domain tags from TAG_TAXONOMY only
- CURRICULUM: Program → Semester → Course codes mapping
- Helper functions to generate sections from curriculum

All domain tags MUST come from TAG_TAXONOMY in data_models.py.
"""

# Handle imports for both direct execution and module import
try:
    from backend.data_models import DepartmentEnum as Department, RoomTypeEnum, DepartmentEnum, TAG_TAXONOMY
except ImportError:
    from data_models import DepartmentEnum as Department, RoomTypeEnum, DepartmentEnum, TAG_TAXONOMY


# ═════════════════════════════════════════════════════════════════
# VALIDATION: Ensure all tags used are in TAG_TAXONOMY
# ═════════════════════════════════════════════════════════════════

ALL_VALID_TAGS = set()
for category, tags in TAG_TAXONOMY.items():
    ALL_VALID_TAGS.update(tags)


def validate_teacher_tags():
    """Validate that all teacher domain tags are in TAG_TAXONOMY."""
    invalid_tags = set()
    for teacher in RAW_TEACHERS:
        for tag in teacher[3]:  # domain_tags at index 3
            if tag not in ALL_VALID_TAGS:
                invalid_tags.add(tag)
    if invalid_tags:
        raise ValueError(f"Invalid domain tags not in TAG_TAXONOMY: {invalid_tags}")


def validate_course_tags():
    """Validate that all course domain tags are in TAG_TAXONOMY."""
    invalid_tags = set()
    for course in RAW_COURSES:
        for tag in course.get("domain_tags", []):
            if tag not in ALL_VALID_TAGS:
                invalid_tags.add(tag)
    if invalid_tags:
        raise ValueError(f"Invalid course domain tags not in TAG_TAXONOMY: {invalid_tags}")

# Rooms data as per specification
ROOMS = [
    # FCSE
    {"id": "FCSE-CS-LH1", "name": "CS LH1", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FCSE},
    {"id": "FCSE-CS-LH2", "name": "CS LH2", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FCSE},
    {"id": "FCSE-CS-LH3", "name": "CS LH3", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FCSE},
    {"id": "FCSE-SE-Lab", "name": "SE Lab", "capacity": 45, "room_type": RoomTypeEnum.LAB, "department": DepartmentEnum.FCSE},

    # FEE
    {"id": "FEE-EE-LH4", "name": "EE LH4", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FEE},
    {"id": "FEE-EE-LH5", "name": "EE LH5", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FEE},
    {"id": "FEE-EE-LH6", "name": "EE LH6", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FEE},
    {"id": "FEE-EE-Main", "name": "EE Main", "capacity": 120, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FEE},

    # BASIC_SCIENCE
    {"id": "BS-ES-LH1", "name": "ES LH1", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.BASIC_SCIENCE},
    {"id": "BS-ES-LH2", "name": "ES LH2", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.BASIC_SCIENCE},
    {"id": "BS-ES-LH3", "name": "ES LH3", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.BASIC_SCIENCE},
    {"id": "BS-ES-Main", "name": "ES Main", "capacity": 120, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.BASIC_SCIENCE},
    {"id": "BS-PC-Lab", "name": "PC Lab", "capacity": 45, "room_type": RoomTypeEnum.LAB, "department": DepartmentEnum.BASIC_SCIENCE},
    {"id": "BS-PH-Lab", "name": "PH Lab", "capacity": 45, "room_type": RoomTypeEnum.LAB, "department": DepartmentEnum.BASIC_SCIENCE},

    # COMMON (AcB)
] + [
    {"id": f"COMMON-AcB-LH{i}", "name": f"AcB LH{i}", "capacity": 90, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.COMMON} for i in range(1, 13)
] + [
    {"id": f"COMMON-AcB-Main{i}", "name": f"AcB Main{i}", "capacity": 200, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.COMMON} for i in range(1, 4)
] + [
    {"id": "COMMON-Sim-Lab", "name": "Sim Lab", "capacity": 50, "room_type": RoomTypeEnum.LAB, "department": DepartmentEnum.COMMON},
    {"id": "COMMON-Incubator", "name": "Incubator", "capacity": 45, "room_type": RoomTypeEnum.LAB, "department": DepartmentEnum.COMMON},
    {"id": "COMMON-Seminar-Hall", "name": "Seminar Hall", "capacity": 150, "room_type": RoomTypeEnum.SEMINAR, "department": DepartmentEnum.COMMON}
] + [
    {"id": "SMS-BB-Main", "name": "BB Main", "capacity": 120, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.SMS},
    {"id": "SMS-BB-LH2", "name": "BB LH2", "capacity": 120, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.SMS}
] + [
    {"id": f"SMS-BB-EH{i}", "name": f"BB EH{i}", "capacity": 110, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.SMS} for i in range(1, 5)
] + [
    {"id": "SMS-Old-PC-Lab", "name": "Old PC Lab", "capacity": 50, "room_type": RoomTypeEnum.LAB, "department": DepartmentEnum.SMS},
    {"id": "SMS-New-PC-Lab", "name": "New PC Lab", "capacity": 50, "room_type": RoomTypeEnum.LAB, "department": DepartmentEnum.SMS}
] + [
    {"id": "FME-ME-LH1", "name": "ME LH1", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FME},
    {"id": "FME-ME-LH2", "name": "ME LH2", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FME},
    {"id": "FME-ME-LH3", "name": "ME LH3", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FME},
    {"id": "FME-ME-Main", "name": "ME Main", "capacity": 120, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FME}
] + [
    {"id": f"FMCE-MCE-LH{i}", "name": f"MCE LH{i}", "capacity": 55, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FMCE} for i in range(1, 5)
] + [
    {"id": "FMCE-MCE-Main", "name": "MCE Main", "capacity": 120, "room_type": RoomTypeEnum.LECTURE_HALL, "department": DepartmentEnum.FMCE},
    {"id": "FMCE-Mat-Lab", "name": "Mat. Lab", "capacity": 45, "room_type": RoomTypeEnum.LAB, "department": DepartmentEnum.FMCE}
]

# ═════════════════════════════════════════════════════════════════
# RAW TEACHERS DATA
# ═════════════════════════════════════════════════════════════════
# Format: (id, name, department, domain_tags)
# All domain_tags MUST be from TAG_TAXONOMY

RAW_TEACHERS = [
    ("T-FCSE-01", "Prof. Dr. Qadeer Ul Hasan",       DepartmentEnum.FCSE, ["machine_learning", "signals", "ai", "computing"]),
    ("T-FCSE-02", "Prof. Dr. Ghulam Abbas",           DepartmentEnum.FCSE, ["networks", "distributed", "iot", "cyber_security"]),
    ("T-FCSE-03", "Prof. Dr. Masroor Hussain",        DepartmentEnum.FCSE, ["parallel_computing", "data_mining", "neural_networks", "data_science"]),
    ("T-FCSE-04", "Dr. Salman Ahmed",                 DepartmentEnum.FCSE, ["cyber_security", "operating_systems", "iot", "distributed"]),
    ("T-FCSE-05", "Dr. Ahmar Rashid",                 DepartmentEnum.FCSE, ["algorithms", "computer_vision", "bioinformatics"]),
    ("T-FCSE-06", "Dr. Muhammad Hanif",               DepartmentEnum.FCSE, ["computer_vision", "signals", "deep_learning", "image_processing"]),
    ("T-FCSE-07", "Dr. Shahabuddin Ansari",           DepartmentEnum.FCSE, ["signals", "numerical_analysis", "image_processing", "dsp"]),
    ("T-FCSE-08", "Dr. Khurram Khan Jadoon",          DepartmentEnum.FCSE, ["computer_vision", "image_processing", "deep_learning", "machine_learning"]),
    ("T-FCSE-09", "Dr. Fahad Bin Muslim",             DepartmentEnum.FCSE, ["embedded", "hardware", "machine_learning", "digital_logic"]),
    ("T-FCSE-10", "Dr. Muhammad Omer Bin Saeed",      DepartmentEnum.FCSE, ["computing"]),
    ("T-FCSE-11", "Dr. Rashad M Jillani",             DepartmentEnum.FCSE, ["signals", "dsp", "computing"]),
    ("T-FCSE-12", "Dr. Taj Muhammad Khan",            DepartmentEnum.FCSE, ["computer_architecture", "operating_systems"]),
    ("T-FCSE-13", "Dr. Waqar Ahmad",                  DepartmentEnum.FCSE, ["hardware", "embedded", "digital_logic", "cryptography"]),
    ("T-FCSE-14", "Dr. Qamar Abbas",                  DepartmentEnum.FCSE, ["iot", "networks", "signals"]),
    ("T-FCSE-15", "Dr. Ali Imran Sandhu",             DepartmentEnum.FCSE, ["electromagnetic", "signals", "machine_learning"]),
    ("T-FCSE-16", "Dr. Adnan Shah",                   DepartmentEnum.FCSE, ["signals", "image_processing", "data_science"]),
    ("T-FCSE-17", "Dr. Sarah Iqbal",                  DepartmentEnum.FCSE, ["iot", "machine_learning", "distributed"]),
    ("T-FCSE-18", "Dr. Ayaz Umer",                    DepartmentEnum.FCSE, ["deep_learning", "computer_vision", "machine_learning"]),
    ("T-FCSE-19", "Dr. Zubair Ahmad",                 DepartmentEnum.FCSE, ["cyber_security", "information_security", "iot"]),
    ("T-FCSE-20", "Dr. Shahab Haider",                DepartmentEnum.FCSE, ["cyber_security", "cryptography", "networks", "iot"]),
    ("T-FCSE-21", "Dr. Farah Saeed",                  DepartmentEnum.FCSE, ["deep_learning", "ai", "data_science", "machine_learning"]),
    ("T-FCSE-22", "Dr. Zoya",                         DepartmentEnum.FCSE, ["computing"]),
    ("T-FCSE-23", "Dr. Muhammad Fawad Khan",          DepartmentEnum.FCSE, ["reinforcement_learning", "iot", "cyber_security", "networks"]),
    ("T-FCSE-24", "Dr. Muhammad Salman",              DepartmentEnum.FCSE, ["cyber_security", "networks", "iot"]),
    ("T-FCSE-25", "Dr. Muhammad Waqas",               DepartmentEnum.FCSE, ["distributed", "software_engineering", "ai"]),
    ("T-FCSE-26", "Dr. Asad Mahmood",                 DepartmentEnum.FCSE, ["signals", "networks", "iot", "dsp"]),
    ("T-FCSE-27", "Dr. Muhammad Salman Saeed",        DepartmentEnum.FCSE, ["information_security", "cryptography", "machine_learning", "networks"]),
    ("T-FCSE-28", "Engr. Badre Munir",                DepartmentEnum.FCSE, ["image_processing", "computing", "ict"]),
    ("T-FCSE-29", "Engr. Ahsan Shah",                 DepartmentEnum.FCSE, ["data_mining", "data_science", "image_processing"]),
    ("T-FCSE-30", "Muhammad Sajid Ali",               DepartmentEnum.FCSE, ["devops", "data_science", "bioinformatics"]),
    ("T-FCSE-31", "Mr. Muhammad Qasim Riaz",          DepartmentEnum.FCSE, ["nlp", "software_engineering", "requirements"]),
    ("T-FCSE-32", "Ms. Beenish Urooj",                DepartmentEnum.FCSE, ["information_security", "cyber_security"]),
    ("T-FCSE-33", "Ms. Laraib Afzal",                 DepartmentEnum.FCSE, ["software_engineering", "cyber_security", "project_management"]),
    ("T-FCSE-34", "Mr. Said Nabi",                    DepartmentEnum.FCSE, ["machine_learning", "nlp", "project_management"]),
    ("T-FCSE-35", "Muhammad Talha Ashfaq",            DepartmentEnum.FCSE, ["ai", "deep_learning", "data_science"]),
    ("T-FCSE-36", "Salman Ashraf",                    DepartmentEnum.FCSE, ["data_science", "nlp", "machine_learning"]),
    ("T-FCSE-37", "Muhammad Huzaifa Shah",            DepartmentEnum.FCSE, ["machine_learning", "deep_learning", "computer_vision"]),
    ("T-FCSE-38", "M. Ahmad Nawaz",                   DepartmentEnum.FCSE, ["cyber_security", "cryptography", "digital_forensics", "networks"]),
    ("T-FCSE-39", "Waheed Ahmad",                     DepartmentEnum.FCSE, ["machine_learning", "nlp", "parallel_computing"]),
    ("T-FCSE-40", "Israr Ahmad",                      DepartmentEnum.FCSE, ["software_engineering", "requirements", "nlp"]),
    ("T-FCSE-41", "Hafiz Syed Muhammad Muslim",       DepartmentEnum.FCSE, ["data_science", "deep_learning", "machine_learning", "nlp"]),
    ("T-FCSE-42", "Hafiz Syed Ahmed Qasim",           DepartmentEnum.FCSE, ["deep_learning", "machine_learning", "computer_vision", "nlp"]),
    ("T-FCSE-43", "Safia Baloch",                     DepartmentEnum.FCSE, ["nlp", "deep_learning"]),
    ("T-FCSE-44", "Rabbia Hassan",                    DepartmentEnum.FCSE, ["computer_vision", "nlp", "formal_languages"]),
    ("T-FCSE-45", "Laraib Noor",                      DepartmentEnum.FCSE, ["software_engineering", "machine_learning", "iot", "nlp"]),
    ("T-FCSE-46", "Dr. Raja Hashim Ali",              DepartmentEnum.FCSE, ["ai", "machine_learning", "bioinformatics"]),
    ("T-FCSE-47", "Dr. Farhan Khan",                  Department.FCSE, ["data_science", "signals", "dsp"]),

    # FEE
    ("T-FEE-01", "Dr. Arbab Abdur Rahim",             Department.FEE, ["electromagnetic", "signals"]),
    ("T-FEE-02", "Dr. Hadeed Ahmed Sher",             Department.FEE, ["power_electronics", "power", "applied_ee"]),
    ("T-FEE-03", "Dr. Shahid Alam",                   Department.FEE, ["applied_ee", "instrumentation"]),
    ("T-FEE-04", "Dr. Ahmad Kamal Hassan",            Department.FEE, ["signals", "communication_systems", "networks"]),
    ("T-FEE-05", "Dr. Memoon Sajid",                  Department.FEE, ["instrumentation", "electronic_devices", "applied_ee"]),
    ("T-FEE-06", "Dr. Husnul Maab",                   Department.FEE, ["electromagnetic", "signals"]),
    ("T-FEE-07", "Dr. Adnan Noor",                    Department.FEE, ["electromagnetic", "applied_ee"]),
    ("T-FEE-08", "Dr. Dur-e-Zehra Baig",             Department.FEE, ["control_systems", "signals", "instrumentation", "applied_ee"]),
    ("T-FEE-09", "Dr. Ammar Arshad",                  Department.FEE, ["power", "power_distribution", "applied_ee"]),
    ("T-FEE-10", "Dr. Attique Ur Rehman",             Department.FEE, ["power", "machine_learning", "data_science"]),
    ("T-FEE-11", "Dr. Waleed Tariq Sethi",            Department.FEE, ["communication_systems", "electromagnetic", "signals"]),
    ("T-FEE-12", "Dr. Zaiwar Ali",                    Department.FEE, ["machine_learning", "neural_networks", "iot", "networks"]),
    ("T-FEE-13", "Engr. Afaq Hussain",                Department.FEE, ["power_electronics", "power", "applied_ee"]),
    ("T-FEE-14", "Umar Afzaal",                       Department.FEE, ["power", "power_distribution"]),

    # FME
    ("T-FME-01", "Dr. Taqi Ahmad Cheema",             Department.FME, ["thermodynamics", "heat_transfer", "fluid_mechanics", "manufacturing"]),
    ("T-FME-02", "Prof. Dr. Khalid Rahman",           Department.FME, ["manufacturing", "engineering_graphics", "workshop"]),
    ("T-FME-03", "Prof. Ghulam Hussain",              Department.FME, ["manufacturing", "stress_analysis"]),
    ("T-FME-04", "Dr. Ahmad Abbas",                   Department.FME, ["heat_transfer", "robotics", "mechanics"]),
    ("T-FME-05", "Dr. Massab Junaid",                 Department.FME, ["manufacturing", "mechanics_of_solids", "stress_analysis"]),
    ("T-FME-06", "Dr. Ali Turab Jafry",               Department.FME, ["manufacturing", "applied_ee"]),
    ("T-FME-07", "Dr. Abid Imran",                    Department.FME, ["robotics", "manufacturing", "machine_elements"]),
    ("T-FME-08", "Dr. Arsalan Arif",                  Department.FME, ["electric_machines", "control_systems", "applied_ee"]),
    ("T-FME-09", "Dr. Taimoor Hassan",                Department.FME, ["robotics", "mechanics", "engineering_graphics", "manufacturing"]),
    ("T-FME-10", "Dr. Muhammad Qasim Zafar",          Department.FME, ["manufacturing", "engineering_graphics", "stress_analysis"]),
    ("T-FME-11", "Dr. Shahzad Ahmad",                 Department.FME, ["manufacturing", "stress_analysis", "mechanics_of_solids"]),
    ("T-FME-12", "Dr. Muhammad Shakeel Afzal",        Department.FME, ["mechanics", "stress_analysis", "manufacturing"]),
    ("T-FME-13", "Dr. Omer Ahmed Qureshi",            Department.FME, ["thermodynamics", "heat_transfer", "fluid_mechanics"]),
    ("T-FME-14", "Mr. Faheem Ahmed",                  Department.FME, ["thermodynamics", "fluid_mechanics", "heat_transfer"]),
    ("T-FME-15", "Mr. Hamza Abbas",                   Department.FME, ["thermodynamics", "fluid_mechanics", "heat_transfer"]),
    ("T-FME-16", "Muhammad Shahab Alam",              Department.FME, ["robotics", "computer_vision", "machine_learning"]),
    ("T-FME-17", "Syed Salman Shah",                  Department.FME, ["ai", "machine_learning", "deep_learning", "robotics"]),

    # FMCE
    ("T-MM-01", "Prof. Dr. F. Ahmad Khalid",          Department.FMCE, ["materials_science", "nanotechnology", "materials_lab"]),
    ("T-MM-02", "Prof. Dr. Fahd Nawaz Khan",          Department.FMCE, ["manufacturing_mm", "materials_science"]),
    ("T-MM-03", "Dr. Muhammad Imran Khan",            Department.FMCE, ["materials_science", "nanotechnology", "materials_lab"]),
    ("T-MM-04", "Dr. Muhammad Ramzan Abdul Karim",    Department.FMCE, ["materials_science", "materials_chemistry", "materials_lab"]),
    ("T-MM-05", "Dr. Rashid Ali",                     Department.FMCE, ["materials_science", "strength_materials", "materials_lab"]),
    ("T-MM-06", "Dr. Syed Zameer Abbas",              Department.FMCE, ["materials_science", "materials_lab", "phase_equilibria"]),
    ("T-MM-07", "Dr. Shanza Rehan",                   Department.FMCE, ["materials_science", "materials_lab", "nanotechnology"]),
    ("T-MM-08", "Dr. Mohsin Ali Marwat",              Department.FMCE, ["materials_science", "nanotechnology", "materials_chemistry", "ceramics"]),
    ("T-MM-09", "Dr. Hamza Mohsin",                   Department.FMCE, ["materials_chemistry", "nanotechnology", "materials_lab"]),
    ("T-MM-10", "Dr. Tauheed Shehbaz",                Department.FMCE, ["materials_science", "strength_materials", "manufacturing_mm", "materials_lab"]),
    ("T-MM-11", "Abdullah Khan",                      Department.FMCE, ["materials_science", "nanotechnology", "materials_lab", "xrd"]),
    ("T-MM-12", "Atteeq-uz-Zaman",                    Department.FMCE, ["materials_lab"]),
    ("T-MM-13", "Muhammad Umair Naseer",              Department.FMCE, ["manufacturing_mm", "materials_lab"]),

    # CIVIL
    ("T-CV-01", "Prof. Dr. Muhammad Ashraf Tanoli",   Department.CIVIL, ["concrete_technology", "construction", "environmental_engineering_cv"]),
    ("T-CV-02", "Dr. Muhammad Faisal Javed",          Department.CIVIL, ["machine_learning", "structural_analysis", "concrete_technology"]),
    ("T-CV-03", "Dr. Shiraz Ahmed",                   Department.CIVIL, ["transportation", "highway"]),
    ("T-CV-04", "Dr. Hafiz Ahmed Waqas",              Department.CIVIL, ["structural_analysis", "mechanics_of_solids", "rc_design"]),
    ("T-CV-05", "Dr. Muhammad Waseem",                Department.CIVIL, ["hydrology", "fluid_mechanics_cv"]),
    ("T-CV-06", "Dr. Abdul Wahab",                    Department.CIVIL, ["construction", "construction_management"]),
    ("T-CV-07", "Dr. Abu Bakr Jamil",                 Department.CIVIL, ["geotechnical", "soil_mechanics", "geology"]),
    ("T-CV-08", "Dr. Zeeshan Asghar",                 Department.CIVIL, ["hydrology", "fluid_mechanics_cv"]),
    ("T-CV-09", "Dr. Adnan Akmal",                    Department.CIVIL, ["structural_analysis"]),
    ("T-CV-10", "Engr. Haidar Ali",                   Department.CIVIL, ["structural_analysis", "mechanics_of_solids", "rc_design"]),
    ("T-CV-11", "Syed Aizaz Haider",                  Department.CIVIL, ["geotechnical", "soil_mechanics"]),
    ("T-CV-12", "Shahzad Ahmed",                      Department.CIVIL, ["construction", "geo_informatics"]),
    ("T-CV-13", "Muntazir Abbas",                     Department.CIVIL, ["structural_analysis", "concrete_technology", "mechanics_of_solids"]),
    ("T-CV-14", "Dr. Khawar Rehman",                  Department.CIVIL, ["fluid_mechanics_cv", "hydrology", "environmental_engineering_cv"]),
    ("T-CV-15", "Dr. Numan Khan",                     Department.CIVIL, ["construction", "geo_informatics", "construction_management"]),

    # SMS
    ("T-SM-01", "Prof. Dr. Sami Farooq",              Department.SMS, ["supply_chain", "operations_management"]),
    ("T-SM-02", "Prof. Dr. Muhammad Sabir",           Department.SMS, ["economics", "supply_chain", "operations_management"]),
    ("T-SM-03", "Dr. Abid Ullah",                     Department.SMS, ["entrepreneurship", "management"]),
    ("T-SM-04", "Izhar Ali",                          Department.SMS, ["law", "ethics", "professional_ethics"]),
    ("T-SM-05", "Dr. Suhaib",                         Department.SMS, ["supply_chain", "operations_management", "decision_analysis"]),
    ("T-SM-06", "Dr. Saima Aftab",                    Department.SMS, ["hrm", "management", "leadership"]),
    ("T-SM-07", "Dr. Noshaba Zulfiqar",               Department.SMS, ["financial_management", "business_finance", "accounting"]),
    ("T-SM-08", "Dr. Shakir Sardar",                  Department.SMS, ["marketing", "management", "research_methods"]),
    ("T-SM-09", "Dr. Sajid Khan",                     Department.SMS, ["hrm", "management", "ethics", "leadership"]),
    ("T-SM-10", "Dr. Rubeena Slamat",                 Department.SMS, ["research_methods", "sociology"]),
    ("T-SM-11", "Dr. Muhammad Shariq",                Department.SMS, ["financial_management", "business_finance", "accounting"]),
    ("T-SM-12", "Dr. Amin Ullah Khan",                Department.SMS, ["supply_chain", "operations_management", "decision_analysis"]),
    ("T-SM-13", "Mr. Hassaan Tariq",                  Department.SMS, ["supply_chain", "operations_management"]),
    ("T-SM-14", "Ms. Umme Rabab Syed",                Department.SMS, ["economics", "business_finance", "accounting"]),
    ("T-SM-15", "Ms. Hira Ahad",                      Department.SMS, ["communication_skills", "writing", "humanities"]),
    ("T-SM-16", "Mr. Atta Ur Rehman Jadoon",          Department.SMS, ["communication_skills", "writing", "critical_thinking"]),
    ("T-SM-17", "Mr. Abrar Ahmad",                    Department.SMS, ["communication_skills", "writing", "law"]),
    ("T-SM-18", "Mr. Haseeb Ahsan",                   Department.SMS, ["communication_skills", "writing", "critical_thinking"]),
    ("T-SM-19", "Haroon Ur Rashid",                   Department.SMS, ["hrm", "management", "entrepreneurship"]),
    ("T-SM-20", "Mr. Fida Ur Rahman",                 Department.SMS, ["islamic_studies", "sociology", "humanities"]),
    ("T-SM-21", "Ms. Naveen Gul Yousafzai",           Department.SMS, ["marketing", "consumer_behavior"]),
    ("T-SM-22", "Mr. Ayman Habib",                    Department.SMS, ["marketing", "business_analytics"]),
    ("T-SM-23", "Mr. Muhammad Umer Saeed",            Department.SMS, ["economics", "business_mathematics"]),
    ("T-SM-24", "Mr. Ahmad Zaka",                     Department.SMS, ["management", "entrepreneurship"]),

    # BASIC_SCIENCE
    ("T-BS-01", "Prof. Dr. Nisar Ahmed",              Department.BASIC_SCIENCE, ["control_systems", "numerical_analysis", "mathematics"]),
    ("T-BS-02", "Prof. Dr. Zia ul Haq Abbas",         Department.BASIC_SCIENCE, ["ict", "networks", "dsp", "computing"]),
    ("T-BS-03", "Prof. Dr. Sirajul Haq",              Department.BASIC_SCIENCE, ["numerical_analysis", "mathematics"]),
    ("T-BS-04", "Dr. Muhammad Zahir Iqbal",           Department.BASIC_SCIENCE, ["physics", "applied_physics"]),
    ("T-BS-05", "Dr. Muhammad Usman",                 Department.BASIC_SCIENCE, ["applied_physics", "electronic_devices"]),
    ("T-BS-06", "Dr. Usman Habib",                    Department.BASIC_SCIENCE, ["physics", "applied_physics"]),
    ("T-BS-07", "Dr. Minhaj Zaheer",                  Department.BASIC_SCIENCE, ["applied_ee", "electric_machines", "control_systems"]),
    ("T-BS-08", "Dr. Nasir Javed",                    Department.BASIC_SCIENCE, ["applied_physics", "nanotechnology"]),
    ("T-BS-09", "Dr. Babar Zaman",                    Department.BASIC_SCIENCE, ["statistics", "probability"]),
    ("T-BS-10", "Dr. Tahir Naseem",                   Department.BASIC_SCIENCE, ["physics", "applied_physics"]),
    ("T-BS-11", "Dr. Zahid Ahmed",                    Department.BASIC_SCIENCE, ["numerical_analysis", "mathematics", "calculus"]),
    ("T-BS-12", "Dr. Mahnoor Sarfraz",                Department.BASIC_SCIENCE, ["mathematics", "calculus", "numerical_analysis", "differential_equations"]),
    ("T-BS-13", "Dr. Sheharyar Pervaiz",              Department.BASIC_SCIENCE, ["mathematics", "physics"]),
    ("T-BS-14", "Dr. Danyal Ahmad",                   Department.BASIC_SCIENCE, ["numerical_analysis", "linear_algebra", "mathematics"]),
    ("T-BS-15", "Dr. Taj Munir",                      Department.BASIC_SCIENCE, ["mathematics", "numerical_analysis", "differential_equations"]),
    ("T-BS-16", "Muhammad Saqib",                     Department.BASIC_SCIENCE, ["applied_physics", "instrumentation"]),
    ("T-BS-17", "Mazhar Javed",                       Department.BASIC_SCIENCE, ["physics", "applied_physics"]),
    ("T-BS-18", "Asif Ahmad",                         Department.BASIC_SCIENCE, ["machine_learning", "deep_learning", "mathematics"]),
    ("T-BS-19", "Engr. Muhammad Sadiq",               Department.BASIC_SCIENCE, ["control_systems", "machine_learning", "mathematics"]),
    ("T-BS-20", "Muhammad Muti ur Rehman",            Department.BASIC_SCIENCE, ["mathematics"]),
]


# ═════════════════════════════════════════════════════════════════
# RAW COURSES DATA - Full GIKI 2025 Catalog
# ═════════════════════════════════════════════════════════════════
# Format: {code, name, credit_hours, department, is_lab, sessions_per_week,
#          semester, is_elective, domain_tags}
# All domain_tags MUST be from TAG_TAXONOMY

RAW_COURSES = [
    # ======================== COMMON FIRST YEAR (2025) ========================
    {"code":"CS101","name":"Computing & Artificial Intelligence","credit_hours":2,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":2,"semester":1,"is_elective":False,"domain_tags":["computing","intro_programming","ai"]},
    {"code":"CS101L","name":"Computing & AI Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":1,"is_elective":False,"domain_tags":["computing","intro_programming"]},
    {"code":"HM101","name":"Communication Skills","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":1,"is_elective":False,"domain_tags":["communication_skills","writing"]},
    {"code":"IF101L","name":"Innovation & Makers Lab I","credit_hours":1,"department":DepartmentEnum.SMS,"is_lab":True,"sessions_per_week":1,"semester":1,"is_elective":False,"domain_tags":["innovation_lab","makers_lab"]},
    {"code":"MT101","name":"Calculus I","credit_hours":3,"department":DepartmentEnum.BASIC_SCIENCE,"is_lab":False,"sessions_per_week":3,"semester":1,"is_elective":False,"domain_tags":["calculus","mathematics"]},
    {"code":"PH101","name":"Applied Physics","credit_hours":3,"department":DepartmentEnum.BASIC_SCIENCE,"is_lab":False,"sessions_per_week":3,"semester":1,"is_elective":False,"domain_tags":["physics","applied_physics"]},
    {"code":"PH101L","name":"Applied Physics Lab","credit_hours":1,"department":DepartmentEnum.BASIC_SCIENCE,"is_lab":True,"sessions_per_week":1,"semester":1,"is_elective":False,"domain_tags":["physics","applied_physics"]},
    {"code":"MM101","name":"Materials, Nanotech & Sustainability","credit_hours":2,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":2,"semester":1,"is_elective":False,"domain_tags":["materials_science","nanotechnology"]},
    {"code":"MM141L","name":"Materials Lab","credit_hours":1,"department":DepartmentEnum.FMCE,"is_lab":True,"sessions_per_week":1,"semester":1,"is_elective":False,"domain_tags":["materials_lab"]},
    {"code":"CH101","name":"Chemistry, Environment & Climate Change","credit_hours":2,"department":DepartmentEnum.BASIC_SCIENCE,"is_lab":False,"sessions_per_week":2,"semester":2,"is_elective":False,"domain_tags":["chemistry","environmental_engineering"]},
    {"code":"CH161","name":"Occupational Health & Safety","credit_hours":1,"department":DepartmentEnum.BASIC_SCIENCE,"is_lab":False,"sessions_per_week":1,"semester":2,"is_elective":False,"domain_tags":["occupational_health"]},
    {"code":"CS112","name":"Object-oriented Programming & Design","credit_hours":2,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":2,"semester":2,"is_elective":False,"domain_tags":["oop","intro_programming"]},
    {"code":"CS112L","name":"OOP Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":2,"is_elective":False,"domain_tags":["oop"]},
    {"code":"AI102","name":"Python & Freelancing Essentials","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":1,"semester":2,"is_elective":False,"domain_tags":["intro_programming"]},
    {"code":"ES111","name":"Probability & Statistics","credit_hours":3,"department":DepartmentEnum.BASIC_SCIENCE,"is_lab":False,"sessions_per_week":3,"semester":2,"is_elective":False,"domain_tags":["statistics","probability"]},
    {"code":"HM102","name":"Critical Thinking & Expository Writing","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":2,"is_elective":False,"domain_tags":["critical_thinking","writing"]},
    {"code":"IF102L","name":"Innovation & Makers Lab II","credit_hours":1,"department":DepartmentEnum.SMS,"is_lab":True,"sessions_per_week":1,"semester":2,"is_elective":False,"domain_tags":["innovation_lab","makers_lab"]},
    {"code":"MT102","name":"Differential Equations & Linear Algebra I","credit_hours":3,"department":DepartmentEnum.BASIC_SCIENCE,"is_lab":False,"sessions_per_week":3,"semester":2,"is_elective":False,"domain_tags":["differential_equations","linear_algebra","mathematics"]},

    # ====================== FCSE – AI (2025) ======================
    {"code":"CS221","name":"Digital Logic Design","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["digital_logic"]},
    {"code":"CS221L","name":"Digital Logic Design Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["digital_logic"]},
    {"code":"CS202","name":"ICT","credit_hours":2,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":2,"semester":3,"is_elective":False,"domain_tags":["ict","computing"]},
    {"code":"CS222","name":"Data Structures & Algorithms","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["data_structures","algorithms"]},
    {"code":"CS222L","name":"Data Structures Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["data_structures"]},
    {"code":"CS231","name":"Discrete Mathematics","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["discrete_math"]},
    {"code":"ES205","name":"Advanced Linear Algebra","credit_hours":3,"department":DepartmentEnum.BASIC_SCIENCE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["linear_algebra","mathematics"]},
    {"code":"HM212","name":"Pakistan Studies","credit_hours":2,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":2,"semester":3,"is_elective":False,"domain_tags":["pakistan_studies"]},
    {"code":"CS223","name":"Computer Organization & Assembly Language","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["computer_organization"]},
    {"code":"CS223L","name":"Computer Organization Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["computer_organization"]},
    {"code":"AI202","name":"Concepts in AI","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["ai"]},
    {"code":"AI202L","name":"AI Concepts Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["ai"]},
    {"code":"CS232","name":"Database Management Systems","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["databases"]},
    {"code":"CS232L","name":"DBMS Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["databases"]},
    {"code":"CS225","name":"Software Engineering","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["software_engineering"]},
    {"code":"HM211","name":"Islamic Studies","credit_hours":2,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":2,"semester":4,"is_elective":False,"domain_tags":["islamic_studies"]},
    {"code":"CS311","name":"Operating Systems","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["operating_systems"]},
    {"code":"CS311L","name":"Operating Systems Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":5,"is_elective":False,"domain_tags":["operating_systems"]},
    {"code":"CS378","name":"Design & Analysis of Algorithms","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["algorithms","complexity"]},
    {"code":"AI311","name":"Knowledge Representation & Problem Solving","credit_hours":2,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":2,"semester":5,"is_elective":False,"domain_tags":["knowledge_representation","ai"]},
    {"code":"AI312","name":"Machine Learning","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["machine_learning","ai"]},
    {"code":"AI312L","name":"Machine Learning Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":5,"is_elective":False,"domain_tags":["machine_learning"]},
    {"code":"CS392","name":"Software Project Management","credit_hours":2,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":2,"semester":5,"is_elective":False,"domain_tags":["project_management","software_engineering"]},
    {"code":"HM3XX","name":"Entrepreneurship","credit_hours":2,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":2,"semester":5,"is_elective":False,"domain_tags":["entrepreneurship"]},
    {"code":"CS313","name":"Computer Communications & Networks","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["networks","communication_systems"]},
    {"code":"CS313L","name":"Networks Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["networks"]},
    {"code":"AI313","name":"Deep Neural Network","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["deep_learning","neural_networks"]},
    {"code":"AI313L","name":"DNN Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["deep_learning"]},
    {"code":"HM4xx","name":"Technical & Business Writing","credit_hours":2,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":2,"semester":6,"is_elective":False,"domain_tags":["technical_writing","communication_skills"]},
    {"code":"AI361","name":"Natural Language Processing","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["nlp","ai"]},
    {"code":"AI361L","name":"NLP Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":7,"is_elective":False,"domain_tags":["nlp"]},
    {"code":"AI441","name":"Computer Vision","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["computer_vision","ai"]},
    {"code":"AI441L","name":"Computer Vision Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":7,"is_elective":False,"domain_tags":["computer_vision"]},
    {"code":"CS417","name":"Parallel & Distributed Computing","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":False,"domain_tags":["parallel_computing","distributed"]},
    {"code":"CS417L","name":"Parallel & Distributed Computing Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":8,"is_elective":False,"domain_tags":["parallel_computing"]},
    {"code":"CS465","name":"Data & Network Security","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":False,"domain_tags":["cyber_security","information_security"]},
    {"code":"CS482","name":"Senior Design Project-III","credit_hours":2,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":2,"semester":8,"is_elective":False,"domain_tags":["project_management"]},
    {"code":"HMxxx","name":"Corporate Law & Professional Ethics","credit_hours":2,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":2,"semester":8,"is_elective":False,"domain_tags":["law","professional_ethics"]},
    {"code":"HM432","name":"Civics & Community Engagement","credit_hours":1,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":1,"semester":8,"is_elective":False,"domain_tags":["civics","sociology"]},
    {"code":"HM413","name":"Understanding of Quran-I","credit_hours":1,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":1,"semester":7,"is_elective":False,"domain_tags":["understanding_quran"]},
    {"code":"HM414","name":"Understanding of Quran-II","credit_hours":1,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":1,"semester":8,"is_elective":False,"domain_tags":["understanding_quran"]},
    {"code":"AI3xx","name":"AI Domain Elective I","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":True,"domain_tags":["ai"]},
    {"code":"AI4xx","name":"AI Domain Elective II","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":True,"domain_tags":["ai"]},

    # ====================== FCSE – CE (2025) ======================
    {"code":"CE211","name":"Circuit Analysis","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["circuit_analysis"]},
    {"code":"CE211L","name":"Circuit Analysis Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["circuit_analysis"]},
    {"code":"CE221","name":"Digital Logic Design","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["digital_logic"]},
    {"code":"CE221L","name":"Digital Logic Design Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["digital_logic"]},
    {"code":"CE222","name":"Computer Org. & Assembly","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["computer_organization"]},
    {"code":"CE222L","name":"Computer Org. Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["computer_organization"]},
    {"code":"CE231","name":"Electronic Devices & Circuits","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["electronic_devices","circuit_analysis"]},
    {"code":"CE231L","name":"Electronic Devices Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["electronic_devices"]},
    {"code":"CE324","name":"Microprocessor Interfacing","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["microprocessor","embedded"]},
    {"code":"CE324L","name":"Microprocessor Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":5,"is_elective":False,"domain_tags":["microprocessor"]},
    {"code":"CE341","name":"Signals & Systems","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["signals","dsp"]},
    {"code":"CE341L","name":"Signals & Systems Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":5,"is_elective":False,"domain_tags":["signals"]},
    {"code":"CE342","name":"Computational Methods","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["numerical_analysis","computing"]},
    {"code":"CE361","name":"Digital Signal Processing","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["dsp","signals"]},
    {"code":"CE361L","name":"DSP Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["dsp"]},
    {"code":"CS361","name":"Computer Architecture","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["computer_architecture"]},
    {"code":"CE408","name":"Cloud Computing","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["cloud","distributed"]},
    {"code":"CE436","name":"Digital System Design","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["digital_logic","hardware"]},
    {"code":"CE436L","name":"Digital System Design Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":7,"is_elective":False,"domain_tags":["digital_logic"]},
    {"code":"CS478","name":"Design & Analysis of Algorithms","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["algorithms","complexity"]},
    {"code":"CX4xx","name":"Area Elective I","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":True,"domain_tags":[]},
    {"code":"CE4xx","name":"Technical Elective","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":True,"domain_tags":[]},

    # ====================== FCSE – CS (2025) ======================
    {"code":"CS224","name":"Formal Languages & Automata","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["formal_languages","compiler"]},
    {"code":"CS272","name":"UI/UX","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["ui_ux","software_engineering"]},
    {"code":"SE202L","name":"Dev Ops Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["devops"]},
    {"code":"CS342","name":"Advanced DBMS","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["advanced_dbms","databases"]},
    {"code":"CS351","name":"Artificial Intelligence","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["ai"]},
    {"code":"CS351L","name":"AI Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":5,"is_elective":False,"domain_tags":["ai"]},
    {"code":"CS324","name":"Computer Architecture","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["computer_architecture"]},
    {"code":"CS334","name":"Compiler Construction","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["compiler","formal_languages"]},
    {"code":"CS334L","name":"Compiler Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["compiler"]},
    {"code":"CS312","name":"Web Development","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["web_engineering"]},
    {"code":"CS312L","name":"Web Dev Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["web_engineering"]},
    {"code":"CS412","name":"Advanced DBMS","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["advanced_dbms","databases"]},
    {"code":"CS424","name":"Compiler Construction","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["compiler"]},
    {"code":"CS424L","name":"Compiler Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":7,"is_elective":False,"domain_tags":["compiler"]},

    # ====================== FCSE – CyS (2025) ======================
    {"code":"CY201","name":"Cyber Security Principles","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["cyber_security","information_security"]},
    {"code":"CY211","name":"Information Security","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["information_security"]},
    {"code":"CY331","name":"Information Assurance","credit_hours":2,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":2,"semester":6,"is_elective":False,"domain_tags":["information_security"]},
    {"code":"CY341","name":"Digital Forensics","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["digital_forensics"]},
    {"code":"CY341L","name":"Digital Forensics Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["digital_forensics"]},
    {"code":"CY392","name":"Project Management for CyS","credit_hours":2,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":2,"semester":6,"is_elective":False,"domain_tags":["project_management"]},
    {"code":"CY478","name":"Secure Software Design","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["secure_software","software_engineering"]},
    {"code":"CY478L","name":"Secure Software Design Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":7,"is_elective":False,"domain_tags":["secure_software"]},
    {"code":"CY412","name":"Cryptography","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["cryptography"]},
    {"code":"CY412L","name":"Unix Administration","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":7,"is_elective":False,"domain_tags":["unix_admin","operating_systems"]},
    {"code":"CY424","name":"Ethical Hacking with AI","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":False,"domain_tags":["ethical_hacking","cyber_security","ai"]},
    {"code":"CY424L","name":"Ethical Hacking Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":8,"is_elective":False,"domain_tags":["ethical_hacking"]},
    {"code":"CS365","name":"Data & Network Security","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["cyber_security","networks"]},

    # ====================== FCSE – DS (2025) ======================
    {"code":"DS211","name":"Theory of Data Science","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["theory_of_data_science","data_science"]},
    {"code":"DS221","name":"Inferential Statistics","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["inferential_stats","statistics","data_science"]},
    {"code":"DS341","name":"Data Mining","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["data_mining","data_science"]},
    {"code":"DS331","name":"Data Warehousing & BI","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["data_warehousing","data_science","business_analytics"]},
    {"code":"DS331L","name":"Data Warehousing Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["data_warehousing","data_science"]},
    {"code":"DS351","name":"Data Visualization","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["visualization","data_science"]},
    {"code":"DS351L","name":"Data Visualization Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["visualization"]},
    {"code":"DS361","name":"Big Data Analytics","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["big_data","data_science"]},
    {"code":"DS361L","name":"Big Data Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["big_data"]},
    {"code":"DS471","name":"Data Engineering","credit_hours":2,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":2,"semester":7,"is_elective":False,"domain_tags":["data_engineering","data_science","software_engineering"]},

    # ====================== FCSE – SE (2025) ======================
    {"code":"SE201","name":"Intro to Software Engineering","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["software_engineering"]},
    {"code":"SE211","name":"Software Requirement Engineering","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["requirements","software_engineering"]},
    {"code":"SE322","name":"Software Design & Architecture","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["architecture","software_engineering","design_patterns"]},
    {"code":"SE322L","name":"Software Design Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":5,"is_elective":False,"domain_tags":["software_engineering"]},
    {"code":"SE351","name":"Web & Mobile App Dev","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["web_engineering","mobile"]},
    {"code":"SE351L","name":"Web & Mobile App Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["web_engineering"]},
    {"code":"SE323","name":"Software Construction","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["software_construction"]},
    {"code":"SE323L","name":"Software Construction Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["software_construction"]},
    {"code":"SE331","name":"Software Quality Assurance","credit_hours":3,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["quality","software_engineering"]},
    {"code":"SE302L","name":"DevOps Lab","credit_hours":1,"department":DepartmentEnum.FCSE,"is_lab":True,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["devops"]},
    {"code":"CS492","name":"Software Project Management","credit_hours":2,"department":DepartmentEnum.FCSE,"is_lab":False,"sessions_per_week":2,"semester":7,"is_elective":False,"domain_tags":["project_management","software_engineering"]},

    # ====================== FEE (2025) ======================
    {"code":"EE211","name":"Linear Circuit Analysis","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["circuit_analysis","electrical_networks"]},
    {"code":"EE211L","name":"Linear Circuit Analysis Lab","credit_hours":1,"department":DepartmentEnum.FEE,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["circuit_analysis"]},
    {"code":"EE221","name":"Digital Logic Design","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["digital_logic"]},
    {"code":"EE221L","name":"Digital Logic Design Lab","credit_hours":1,"department":DepartmentEnum.FEE,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["digital_logic"]},
    {"code":"EE222","name":"Data Structures","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["data_structures"]},
    {"code":"MT201","name":"Calculus II","credit_hours":3,"department":DepartmentEnum.BASIC_SCIENCE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["calculus","mathematics"]},
    {"code":"EE212","name":"Electrical Network Analysis","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["electrical_networks"]},
    {"code":"EE212L","name":"Electrical Network Analysis Lab","credit_hours":1,"department":DepartmentEnum.FEE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["electrical_networks"]},
    {"code":"EE223","name":"Microprocessor Systems","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["microprocessor","embedded"]},
    {"code":"EE223L","name":"Microprocessor Lab","credit_hours":1,"department":DepartmentEnum.FEE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["microprocessor"]},
    {"code":"EE231","name":"Electronic Devices & Circuits","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["electronic_devices"]},
    {"code":"EE231L","name":"Electronic Devices Lab","credit_hours":1,"department":DepartmentEnum.FEE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["electronic_devices"]},
    {"code":"MS291","name":"Engineering Economics","credit_hours":2,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":2,"semester":4,"is_elective":False,"domain_tags":["engineering_economy"]},
    {"code":"EE241","name":"Numerical Methods","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["numerical_analysis"]},
    {"code":"EE311","name":"Electric Machines","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["electric_machines"]},
    {"code":"EE311L","name":"Electric Machines Lab","credit_hours":1,"department":DepartmentEnum.FEE,"is_lab":True,"sessions_per_week":1,"semester":5,"is_elective":False,"domain_tags":["electric_machines"]},
    {"code":"EE341","name":"Signals & Systems","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["signals","dsp"]},
    {"code":"EE341L","name":"Signals & Systems Lab","credit_hours":1,"department":DepartmentEnum.FEE,"is_lab":True,"sessions_per_week":1,"semester":5,"is_elective":False,"domain_tags":["signals"]},
    {"code":"EE351","name":"Linear Control Systems","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["control_systems"]},
    {"code":"EE351L","name":"Control Systems Lab","credit_hours":1,"department":DepartmentEnum.FEE,"is_lab":True,"sessions_per_week":1,"semester":5,"is_elective":False,"domain_tags":["control_systems"]},
    {"code":"EE332","name":"Power Electronics","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["power_electronics"]},
    {"code":"EE361","name":"Communication Systems","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["communication_systems"]},
    {"code":"EE452","name":"Robotics in Automation","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["robotics","applied_ee"]},
    {"code":"EE4xx","name":"Specialization Elective","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":True,"domain_tags":["applied_ee"]},

    # ====================== FME (2025) ======================
    {"code":"ME211","name":"Statics","credit_hours":2,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":2,"semester":3,"is_elective":False,"domain_tags":["statics","mechanics"]},
    {"code":"ME204","name":"Engineering Graphics","credit_hours":2,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":2,"semester":3,"is_elective":False,"domain_tags":["engineering_graphics"]},
    {"code":"ME202","name":"Measurement & Instrumentation","credit_hours":2,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":2,"semester":3,"is_elective":False,"domain_tags":["instrumentation"]},
    {"code":"ME251","name":"Manufacturing Processes","credit_hours":2,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":2,"semester":3,"is_elective":False,"domain_tags":["manufacturing"]},
    {"code":"ME231","name":"Thermodynamics","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["thermodynamics"]},
    {"code":"ME245L","name":"Lab","credit_hours":1,"department":DepartmentEnum.FME,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["workshop"]},
    {"code":"ME212","name":"Dynamics","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["dynamics","mechanics"]},
    {"code":"ME213","name":"Mechanics of Solids I","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["mechanics_of_solids"]},
    {"code":"ME203","name":"Circuits & Electronic Devices","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["circuit_analysis","electronic_devices"]},
    {"code":"ME243L","name":"Lab","credit_hours":1,"department":DepartmentEnum.FME,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["manufacturing"]},
    {"code":"ME244L","name":"Lab","credit_hours":1,"department":DepartmentEnum.FME,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["thermodynamics"]},
    {"code":"ME321","name":"Fluid Mechanics I","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["fluid_mechanics"]},
    {"code":"ME363","name":"Machine Elements I","credit_hours":2,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":2,"semester":5,"is_elective":False,"domain_tags":["machine_elements"]},
    {"code":"ME313","name":"Theory of Machines","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["theory_of_machines"]},
    {"code":"ES341","name":"Numerical Analysis","credit_hours":3,"department":DepartmentEnum.BASIC_SCIENCE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["numerical_analysis"]},
    {"code":"ME314","name":"Mechanics of Solids II","credit_hours":2,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":2,"semester":5,"is_elective":False,"domain_tags":["mechanics_of_solids"]},
    {"code":"ME346L","name":"Lab","credit_hours":1,"department":DepartmentEnum.FME,"is_lab":True,"sessions_per_week":1,"semester":5,"is_elective":False,"domain_tags":["fluid_mechanics"]},
    {"code":"ME322","name":"Fluid Mechanics II","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["fluid_mechanics"]},
    {"code":"ME333","name":"Heat Transfer","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["heat_transfer"]},
    {"code":"ME315","name":"Mechanical Vibration","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["vibration"]},
    {"code":"ME364","name":"Machine Elements II","credit_hours":2,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":2,"semester":6,"is_elective":False,"domain_tags":["machine_elements"]},
    {"code":"ME316","name":"Computer Aided Engineering","credit_hours":2,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":2,"semester":6,"is_elective":False,"domain_tags":["engineering_graphics"]},
    {"code":"ME464","name":"System Dynamics & Control","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["control_systems","dynamics"]},
    {"code":"ME403","name":"Electrical Machines & Drives","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["electric_machines","drives"]},
    {"code":"ME467","name":"Finite Element Analysis","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":False,"domain_tags":["numerical_analysis","mechanics"]},
    {"code":"MS49x","name":"Management Elective","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":True,"domain_tags":["management"]},
    {"code":"ME4xx","name":"Technical Elective","credit_hours":3,"department":DepartmentEnum.FME,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":True,"domain_tags":[]},

    # ====================== FMCE – Materials (2025) ======================
    {"code":"MM212","name":"Materials Evaluation","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["materials_evaluation","materials_science"]},
    {"code":"MM231","name":"Thermodynamics of Materials","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["thermodynamics_mm","materials_science"]},
    {"code":"MM214","name":"Mineral Processing","credit_hours":2,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":2,"semester":3,"is_elective":False,"domain_tags":["mineral_processing"]},
    {"code":"EE213","name":"Applied EE","credit_hours":3,"department":DepartmentEnum.FEE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["applied_ee"]},
    {"code":"MM242L","name":"Materials Lab II","credit_hours":1,"department":DepartmentEnum.FMCE,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["materials_lab"]},
    {"code":"MM232","name":"Phase Equilibria","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["phase_equilibria","materials_science"]},
    {"code":"MM222","name":"Strength of Materials","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["strength_materials","mechanics_of_solids"]},
    {"code":"MM233","name":"Alloy Production & Casting","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["alloy","manufacturing_mm"]},
    {"code":"MM201","name":"Materials Chemistry","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["materials_chemistry"]},
    {"code":"MM244L","name":"Computational Tools Lab","credit_hours":1,"department":DepartmentEnum.FMCE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["computing"]},
    {"code":"MM323","name":"XRD & EM","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["xrd","materials_lab"]},
    {"code":"MM324","name":"Deformation & Fracture","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["deformation_fracture"]},
    {"code":"MM334","name":"Heat Treatment","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["heat_treatment"]},
    {"code":"MM351","name":"Joining of Materials","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["joining_materials"]},
    {"code":"MM344L","name":"Lab","credit_hours":2,"department":DepartmentEnum.FMCE,"is_lab":True,"sessions_per_week":2,"semester":5,"is_elective":False,"domain_tags":["materials_lab"]},
    {"code":"MM352","name":"Manufacturing Processes-I","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["manufacturing_mm"]},
    {"code":"MM365","name":"Polymers & Composites","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["polymers","ceramics"]},
    {"code":"MM362","name":"Ceramics & Glasses","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["ceramics"]},
    {"code":"MM435","name":"Corrosion","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["corrosion"]},
    {"code":"MM453","name":"CAD/CAM","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["cad_cam"]},
    {"code":"MM451","name":"Manufacturing Process-II","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":False,"domain_tags":["manufacturing_mm"]},

    # ====================== FMCE – Chemical (2025) ======================
    {"code":"CH201","name":"Physical & Analytical Chem","credit_hours":2,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":2,"semester":3,"is_elective":False,"domain_tags":["analytical_chemistry"]},
    {"code":"CH211","name":"Chemical Process Industries","credit_hours":2,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":2,"semester":3,"is_elective":False,"domain_tags":["chemical_engineering"]},
    {"code":"CH231","name":"Chem Engg Principles","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["chemical_engineering"]},
    {"code":"CH251L","name":"Lab","credit_hours":1,"department":DepartmentEnum.FMCE,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["chemical_engineering"]},
    {"code":"CH202","name":"Inorganic & Organic Chem","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["chemistry"]},
    {"code":"CH212","name":"Energy Engg","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["energy_engineering"]},
    {"code":"CH214","name":"Thermodynamics I","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["thermodynamics_ch"]},
    {"code":"CH241","name":"Fluid Mechanics I","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["fluid_mechanics_ch"]},
    {"code":"CH252L","name":"Energy/Thermo Lab","credit_hours":1,"department":DepartmentEnum.FMCE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["thermodynamics_ch"]},
    {"code":"CH253L","name":"Fluid Lab","credit_hours":1,"department":DepartmentEnum.FMCE,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["fluid_mechanics_ch"]},
    {"code":"CH311","name":"Heat Transfer","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["heat_transfer_ch"]},
    {"code":"CH313","name":"Mass Transfer","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["mass_transfer"]},
    {"code":"CH321","name":"Thermodynamics II","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["thermodynamics_ch"]},
    {"code":"CH341","name":"Particle Technology","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["particle_technology"]},
    {"code":"CH351L","name":"Lab","credit_hours":1,"department":DepartmentEnum.FMCE,"is_lab":True,"sessions_per_week":1,"semester":5,"is_elective":False,"domain_tags":["chemical_engineering"]},
    {"code":"CH322","name":"Reaction Kinetics & Reactor Design","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["reaction_kinetics"]},
    {"code":"CH331","name":"Process Modeling","credit_hours":2,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":2,"semester":6,"is_elective":False,"domain_tags":["process_modelling"]},
    {"code":"CH342","name":"Fluid Mechanics II","credit_hours":2,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":2,"semester":6,"is_elective":False,"domain_tags":["fluid_mechanics_ch"]},
    {"code":"CH361","name":"Environmental Engg","credit_hours":2,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":2,"semester":6,"is_elective":False,"domain_tags":["environmental_engineering"]},
    {"code":"CH411","name":"Simultaneous Heat & Mass Transfer","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["heat_transfer_ch","mass_transfer"]},
    {"code":"CH415","name":"Instrumentation & Control","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["instrumentation","control_systems"]},
    {"code":"CH412","name":"Transport Phenomena","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":False,"domain_tags":["transport"]},
    {"code":"CH441","name":"Plant Design","credit_hours":3,"department":DepartmentEnum.FMCE,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":False,"domain_tags":["plant_design"]},

    # ====================== Civil (2025) ======================
    {"code":"CV201","name":"Engineering Surveying","credit_hours":2,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":2,"semester":3,"is_elective":False,"domain_tags":["surveying"]},
    {"code":"CV201L","name":"Surveying Lab","credit_hours":1,"department":DepartmentEnum.CIVIL,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["surveying"]},
    {"code":"CV210L","name":"Drawing Lab","credit_hours":1,"department":DepartmentEnum.CIVIL,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["engineering_graphics"]},
    {"code":"CV211","name":"Mechanics of Solids I","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["mechanics_of_solids"]},
    {"code":"CV215","name":"Concrete Technology","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["concrete_technology"]},
    {"code":"CV215L","name":"Concrete Lab","credit_hours":1,"department":DepartmentEnum.CIVIL,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["concrete_technology"]},
    {"code":"CV221","name":"Fluid Mechanics","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["fluid_mechanics_cv"]},
    {"code":"CV221L","name":"Fluid Lab","credit_hours":1,"department":DepartmentEnum.CIVIL,"is_lab":True,"sessions_per_week":1,"semester":3,"is_elective":False,"domain_tags":["fluid_mechanics_cv"]},
    {"code":"CV230","name":"Geology","credit_hours":2,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":2,"semester":4,"is_elective":False,"domain_tags":["geology"]},
    {"code":"CV213","name":"Basic Structure Analysis","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["structural_analysis"]},
    {"code":"CV231","name":"Soil Mechanics","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["soil_mechanics"]},
    {"code":"CV231L","name":"Soil Lab","credit_hours":1,"department":DepartmentEnum.CIVIL,"is_lab":True,"sessions_per_week":1,"semester":4,"is_elective":False,"domain_tags":["soil_mechanics"]},
    {"code":"CV241","name":"Transportation Engg","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["transportation"]},
    {"code":"CV313","name":"Indeterminate Structural Analysis","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["structural_analysis"]},
    {"code":"CV322","name":"Fluid Mechanics II","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["fluid_mechanics_cv"]},
    {"code":"CV332","name":"Geotechnical & Foundation Engg","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":5,"is_elective":False,"domain_tags":["geotechnical","soil_mechanics"]},
    {"code":"CV323","name":"Hydrology","credit_hours":2,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":2,"semester":5,"is_elective":False,"domain_tags":["hydrology"]},
    {"code":"CV305","name":"Geo Informatics","credit_hours":1,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":1,"semester":6,"is_elective":False,"domain_tags":["geo_informatics"]},
    {"code":"CV314","name":"Reinforced Concrete Design I","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["rc_design","structural_analysis"]},
    {"code":"CV315","name":"Design of Steel Structures","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["steel_design"]},
    {"code":"CV351","name":"Construction Engg","credit_hours":2,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":2,"semester":6,"is_elective":False,"domain_tags":["construction"]},
    {"code":"CV361","name":"Environmental Engg I","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":6,"is_elective":False,"domain_tags":["environmental_engineering_cv"]},
    {"code":"CV414","name":"Reinforced Concrete Design II","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["rc_design"]},
    {"code":"CV442","name":"Highway Engg","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["highway","transportation"]},
    {"code":"CV408","name":"Machine Learning in Civil","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":False,"domain_tags":["machine_learning"]},
    {"code":"CV425","name":"Hydraulics & Irrigation","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":False,"domain_tags":["hydrology","fluid_mechanics_cv"]},
    {"code":"CV452","name":"Construction Management","credit_hours":3,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":False,"domain_tags":["construction_management"]},
    {"code":"CV407","name":"Civil Engg Economics","credit_hours":2,"department":DepartmentEnum.CIVIL,"is_lab":False,"sessions_per_week":2,"semester":7,"is_elective":False,"domain_tags":["engineering_economy"]},
    {"code":"CV403L","name":"Cost Estimation Lab","credit_hours":1,"department":DepartmentEnum.CIVIL,"is_lab":True,"sessions_per_week":1,"semester":7,"is_elective":False,"domain_tags":["cost_estimation"]},

    # ====================== SMS (2023/2024) ======================
    {"code":"MS101","name":"Business Math","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":1,"is_elective":False,"domain_tags":["business_mathematics"]},
    {"code":"MS121","name":"Fundamentals of Management","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":1,"is_elective":False,"domain_tags":["management"]},
    {"code":"MS131","name":"Principles of Marketing","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":1,"is_elective":False,"domain_tags":["marketing"]},
    {"code":"MS102","name":"Business Statistics","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":2,"is_elective":False,"domain_tags":["statistics","business_analytics"]},
    {"code":"MS122","name":"HRM","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":2,"is_elective":False,"domain_tags":["hrm"]},
    {"code":"MS141","name":"Microeconomics","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":2,"is_elective":False,"domain_tags":["microeconomics","economics"]},
    {"code":"MS151","name":"Financial Accounting","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":2,"is_elective":False,"domain_tags":["accounting"]},
    {"code":"HM203","name":"Business Communication","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["business_comm","communication_skills"]},
    {"code":"MS222","name":"Organizational Behavior","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["organizational_behavior"]},
    {"code":"MS232","name":"Marketing Management","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["marketing"]},
    {"code":"MS242","name":"Macroeconomics","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["macroeconomics","economics"]},
    {"code":"MS252","name":"Management Accounting","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["accounting"]},
    {"code":"MS203","name":"Business Research Methods","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["research_methods"]},
    {"code":"MS211","name":"Environmental Sciences","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["environmental_engineering"]},
    {"code":"MS233","name":"Consumer Behavior","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["consumer_behavior","marketing"]},
    {"code":"MS234","name":"Entrepreneurship","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["entrepreneurship"]},
    {"code":"MS253","name":"Business Finance","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["business_finance"]},
    {"code":"HM222","name":"Art of Learning","credit_hours":2,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":2,"semester":3,"is_elective":False,"domain_tags":["art_of_learning"]},
    {"code":"MS471","name":"Senior Year Project I","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["project_management"]},
    {"code":"MS472","name":"Senior Year Project II","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":8,"is_elective":False,"domain_tags":["project_management"]},
    {"code":"HM111","name":"Islamic Studies/Ethics","credit_hours":2,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":2,"semester":1,"is_elective":False,"domain_tags":["islamic_studies","ethics"]},
    {"code":"HM112","name":"Pakistan Studies","credit_hours":2,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":2,"semester":2,"is_elective":False,"domain_tags":["pakistan_studies"]},
    {"code":"HM213","name":"History","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["history"]},
    {"code":"HM221","name":"IR & Current Affairs","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":3,"is_elective":False,"domain_tags":["ir_affairs"]},
    {"code":"HM223","name":"Anthropology","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":4,"is_elective":False,"domain_tags":["anthropology"]},
    {"code":"HM404","name":"Advance Oral Communication","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":False,"domain_tags":["oral_communication"]},
    {"code":"MS4xx","name":"Management Elective","credit_hours":3,"department":DepartmentEnum.SMS,"is_lab":False,"sessions_per_week":3,"semester":7,"is_elective":True,"domain_tags":["management"]},
]


# ═════════════════════════════════════════════════════════════════
# CURRICULUM MAP: Program → Semester → Course Codes
# ═════════════════════════════════════════════════════════════════
# This is the SINGLE SOURCE OF TRUTH for what courses each section takes.
# Sections are GENERATED from this map - never hardcoded.

CURRICULUM: dict[str, list[str]] = {
    # ═════════════════════════════════════════════════════════════════
    # FCSE – Common First Year (Sem 1-2)
    # ═════════════════════════════════════════════════════════════════
    "FCSE_Common_sem1": ["CS101", "CS101L", "CL102", "CL102L", "MT101", "HM101", "HM111"],
    "FCSE_Common_sem2": ["CS102", "CS102L", "CS103", "MT102", "SS104", "HM102", "HM112", "EL101"],

    # ═════════════════════════════════════════════════════════════════
    # FCSE – AI (Sem 3-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_AI_sem3": ["AI201", "CS232", "CS232L", "SS204", "MT224", "EL201", "AI211", "AI211L"],
    "BS_AI_sem4": ["MT241", "CS251", "CS251L", "CS211", "CS211L", "CS272", "SE202L", "EL202"],
    "BS_AI_sem5": ["AI321", "AI321L", "CS342", "CS351", "CS351L", "CS365", "EL301"],
    "BS_AI_sem6": ["CS334", "CS334L", "CS312", "CS312L", "CS361", "SS302", "EL302"],
    "BS_AI_sem7": ["AI411", "AI411L", "CS408", "CS408L", "HM413", "CX4xx"],
    "BS_AI_sem8": ["AI421", "AI421L", "AI431", "AI431L", "CS417", "CS417L", "CS465", "CS482", "HMxxx", "HM432"],

    # ═════════════════════════════════════════════════════════════════
    # FCSE – CE (Sem 3-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_CE_sem3": ["CE211", "CE211L", "CE221", "CE221L", "CS232", "CS232L", "SS204", "MT224"],
    "BS_CE_sem4": ["CE222", "CE222L", "CE231", "CE231L", "CS251", "CS251L", "MT241"],
    "BS_CE_sem5": ["CE324", "CE324L", "CE341", "CE341L", "CS211", "CS211L", "CS212", "CS212L"],
    "BS_CE_sem6": ["CE342", "CE361", "CE361L", "CS361", "CS334", "CS334L", "SS302"],
    "BS_CE_sem7": ["CE408", "CE436", "CE436L", "CS478", "CX4xx"],
    "BS_CE_sem8": ["CE4xx", "HMxxx", "HM432", "HM414"],

    # ═════════════════════════════════════════════════════════════════
    # FCSE – CS (Sem 3-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_CS_sem3": ["CS201", "CS201L", "CS232", "CS232L", "SS204", "MT224", "SE201"],
    "BS_CS_sem4": ["CS251", "CS251L", "CS224", "CS272", "SE202L", "MT241", "SE211"],
    "BS_CS_sem5": ["CS342", "CS351", "CS351L", "CS365", "SE322", "SE322L"],
    "BS_CS_sem6": ["CS324", "CS334", "CS334L", "CS312", "CS312L", "CS323", "CS323L"],
    "BS_CS_sem7": ["CS412", "CS424", "CS424L", "CS492"],
    "BS_CS_sem8": ["CS417", "CS417L", "CS465", "CS482", "HMxxx", "HM432"],

    # ═════════════════════════════════════════════════════════════════
    # FCSE – CyS (Sem 3-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_CyS_sem3": ["CS201", "CS201L", "CS232", "CS232L", "SS204", "MT224", "CY201"],
    "BS_CyS_sem4": ["CS251", "CS251L", "CY201", "CY211", "MT241", "SE202L"],
    "BS_CyS_sem5": ["CS342", "CS365", "CS212", "CS212L"],
    "BS_CyS_sem6": ["CY331", "CY341", "CY341L", "CY392"],
    "BS_CyS_sem7": ["CY478", "CY478L", "CY412", "CY412L", "HM413"],
    "BS_CyS_sem8": ["CY424", "CY424L", "CS482", "HMxxx", "HM432", "HM414"],

    # ═════════════════════════════════════════════════════════════════
    # FCSE – DS (Sem 3-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_DS_sem3": ["CS201", "CS201L", "CS232", "CS232L", "SS204", "MT224"],
    "BS_DS_sem4": ["CS251", "CS251L", "DS211", "DS221", "MT241"],
    "BS_DS_sem5": ["CS342", "DS341", "CS351", "CS351L"],
    "BS_DS_sem6": ["DS331", "DS331L", "DS351", "DS351L", "DS361", "DS361L"],
    "BS_DS_sem7": ["DS471", "CS408", "CS408L"],
    "BS_DS_sem8": ["CS417", "CS417L", "CS482", "HMxxx", "HM432", "HM414"],

    # ═════════════════════════════════════════════════════════════════
    # FCSE – SE (Sem 3-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_SE_sem3": ["CS201", "CS201L", "CS232", "CS232L", "SS204", "MT224", "SE201"],
    "BS_SE_sem4": ["CS251", "CS251L", "SE211", "SE202L", "MT241"],
    "BS_SE_sem5": ["CS211", "CS211L", "SE322", "SE322L"],
    "BS_SE_sem6": ["SE351", "SE351L", "SE323", "SE323L", "SE331", "SE302L"],
    "BS_SE_sem7": ["CS492", "CS412", "CS424", "CS424L"],
    "BS_SE_sem8": ["CS482", "HMxxx", "HM432", "HM414"],

    # ═════════════════════════════════════════════════════════════════
    # FEE (Sem 3-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_EE_sem3": ["EE211", "EE211L", "EE221", "EE221L", "EE222", "MT201"],
    "BS_EE_sem4": ["EE212", "EE212L", "EE223", "EE223L", "EE231", "EE231L", "MS291", "EE241"],
    "BS_EE_sem5": ["EE311", "EE311L", "EE341", "EE341L", "EE351", "EE351L"],
    "BS_EE_sem6": ["EE332", "EE361"],
    "BS_EE_sem7": ["EE452", "EE4xx"],
    "BS_EE_sem8": ["HMxxx", "HM432", "HM414"],

    # ═════════════════════════════════════════════════════════════════
    # FME (Sem 3-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_ME_sem3": ["ME211", "ME204", "ME202", "ME251", "ME231", "ME245L"],
    "BS_ME_sem4": ["ME212", "ME213", "ME203", "ME243L", "ME244L"],
    "BS_ME_sem5": ["ME321", "ME363", "ME313", "ES341", "ME314", "ME346L"],
    "BS_ME_sem6": ["ME322", "ME333", "ME315", "ME364", "ME316"],
    "BS_ME_sem7": ["ME464", "ME403", "MS49x", "ME4xx"],
    "BS_ME_sem8": ["ME467", "HMxxx", "HM432", "HM414"],

    # ═════════════════════════════════════════════════════════════════
    # FMCE – Materials (Sem 3-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_MM_sem3": ["MM212", "MM231", "MM214", "EE213", "MM242L"],
    "BS_MM_sem4": ["MM232", "MM222", "MM233", "MM201", "MM244L"],
    "BS_MM_sem5": ["MM323", "MM324", "MM334", "MM351", "MM344L"],
    "BS_MM_sem6": ["MM352", "MM365", "MM362"],
    "BS_MM_sem7": ["MM435", "MM453"],
    "BS_MM_sem8": ["MM451", "HMxxx", "HM432", "HM414"],

    # ═════════════════════════════════════════════════════════════════
    # FMCE – Chemical (Sem 3-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_ChE_sem3": ["CH201", "CH211", "CH231", "CH251L"],
    "BS_ChE_sem4": ["CH202", "CH212", "CH214", "CH241", "CH252L", "CH253L"],
    "BS_ChE_sem5": ["CH311", "CH313", "CH321", "CH341", "CH351L"],
    "BS_ChE_sem6": ["CH322", "CH331", "CH342", "CH361"],
    "BS_ChE_sem7": ["CH411", "CH415"],
    "BS_ChE_sem8": ["CH412", "CH441", "HMxxx", "HM432", "HM414"],

    # ═════════════════════════════════════════════════════════════════
    # Civil (Sem 3-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_CvE_sem3": ["CV201", "CV201L", "CV210L", "CV211", "CV215", "CV215L", "CV221", "CV221L"],
    "BS_CvE_sem4": ["CV230", "CV213", "CV231", "CV231L", "CV241"],
    "BS_CvE_sem5": ["CV313", "CV322", "CV332", "CV323"],
    "BS_CvE_sem6": ["CV305", "CV314", "CV315", "CV351", "CV361"],
    "BS_CvE_sem7": ["CV414", "CV442", "CV407", "CV403L"],
    "BS_CvE_sem8": ["CV408", "CV425", "CV452", "HMxxx", "HM432", "HM414"],

    # ═════════════════════════════════════════════════════════════════
    # SMS (Sem 1-8)
    # ═════════════════════════════════════════════════════════════════
    "BS_MS_sem1": ["MS101", "MS121", "MS131", "HM111"],
    "BS_MS_sem2": ["MS102", "MS122", "MS141", "MS151", "HM112"],
    "BS_MS_sem3": ["MS232", "MS242", "MS252", "HM203", "MS222", "HM222", "HM213", "HM221"],
    "BS_MS_sem4": ["MS203", "MS211", "MS233", "MS234", "MS253", "HM223"],
    "BS_MS_sem7": ["MS471", "MS4xx", "HM404"],
    "BS_MS_sem8": ["MS472", "HMxxx", "HM432", "HM414"],
}

# Section generation configuration
# Format: (program, semester, department, student_count, num_sections)
SECTION_CONFIG = [
    # FCSE – Common First Year
    ("FCSE_Common", 1, DepartmentEnum.FCSE, 60, 6),  # 6 sections for all FCSE
    ("FCSE_Common", 2, DepartmentEnum.FCSE, 60, 6),

    # FCSE – AI (60 students, 2 sections per semester)
    ("BS_AI", 3, DepartmentEnum.FCSE, 30, 2),
    ("BS_AI", 4, DepartmentEnum.FCSE, 30, 2),
    ("BS_AI", 5, DepartmentEnum.FCSE, 30, 2),
    ("BS_AI", 6, DepartmentEnum.FCSE, 30, 2),
    ("BS_AI", 7, DepartmentEnum.FCSE, 30, 1),
    ("BS_AI", 8, DepartmentEnum.FCSE, 30, 1),

    # FCSE – CE
    ("BS_CE", 3, DepartmentEnum.FCSE, 30, 2),
    ("BS_CE", 4, DepartmentEnum.FCSE, 30, 2),
    ("BS_CE", 5, DepartmentEnum.FCSE, 30, 2),
    ("BS_CE", 6, DepartmentEnum.FCSE, 30, 2),
    ("BS_CE", 7, DepartmentEnum.FCSE, 30, 1),
    ("BS_CE", 8, DepartmentEnum.FCSE, 30, 1),

    # FCSE – CS
    ("BS_CS", 3, DepartmentEnum.FCSE, 45, 2),
    ("BS_CS", 4, DepartmentEnum.FCSE, 45, 2),
    ("BS_CS", 5, DepartmentEnum.FCSE, 45, 2),
    ("BS_CS", 6, DepartmentEnum.FCSE, 45, 2),
    ("BS_CS", 7, DepartmentEnum.FCSE, 45, 1),
    ("BS_CS", 8, DepartmentEnum.FCSE, 45, 1),

    # FCSE – CyS
    ("BS_CyS", 3, DepartmentEnum.FCSE, 30, 2),
    ("BS_CyS", 4, DepartmentEnum.FCSE, 30, 2),
    ("BS_CyS", 5, DepartmentEnum.FCSE, 30, 2),
    ("BS_CyS", 6, DepartmentEnum.FCSE, 30, 2),
    ("BS_CyS", 7, DepartmentEnum.FCSE, 30, 1),
    ("BS_CyS", 8, DepartmentEnum.FCSE, 30, 1),

    # FCSE – DS
    ("BS_DS", 3, DepartmentEnum.FCSE, 30, 2),
    ("BS_DS", 4, DepartmentEnum.FCSE, 30, 2),
    ("BS_DS", 5, DepartmentEnum.FCSE, 30, 2),
    ("BS_DS", 6, DepartmentEnum.FCSE, 30, 2),
    ("BS_DS", 7, DepartmentEnum.FCSE, 30, 1),
    ("BS_DS", 8, DepartmentEnum.FCSE, 30, 1),

    # FCSE – SE
    ("BS_SE", 3, DepartmentEnum.FCSE, 40, 2),
    ("BS_SE", 4, DepartmentEnum.FCSE, 40, 2),
    ("BS_SE", 5, DepartmentEnum.FCSE, 40, 2),
    ("BS_SE", 6, DepartmentEnum.FCSE, 40, 2),
    ("BS_SE", 7, DepartmentEnum.FCSE, 40, 1),
    ("BS_SE", 8, DepartmentEnum.FCSE, 40, 1),

    # FEE
    ("BS_EE", 3, DepartmentEnum.FEE, 35, 2),
    ("BS_EE", 4, DepartmentEnum.FEE, 35, 2),
    ("BS_EE", 5, DepartmentEnum.FEE, 35, 2),
    ("BS_EE", 6, DepartmentEnum.FEE, 35, 2),
    ("BS_EE", 7, DepartmentEnum.FEE, 35, 1),
    ("BS_EE", 8, DepartmentEnum.FEE, 35, 1),

    # FME
    ("BS_ME", 3, DepartmentEnum.FME, 35, 2),
    ("BS_ME", 4, DepartmentEnum.FME, 35, 2),
    ("BS_ME", 5, DepartmentEnum.FME, 35, 2),
    ("BS_ME", 6, DepartmentEnum.FME, 35, 2),
    ("BS_ME", 7, DepartmentEnum.FME, 35, 1),
    ("BS_ME", 8, DepartmentEnum.FME, 35, 1),

    # FMCE – Materials
    ("BS_MM", 3, DepartmentEnum.FMCE, 25, 2),
    ("BS_MM", 4, DepartmentEnum.FMCE, 25, 2),
    ("BS_MM", 5, DepartmentEnum.FMCE, 25, 2),
    ("BS_MM", 6, DepartmentEnum.FMCE, 25, 2),
    ("BS_MM", 7, DepartmentEnum.FMCE, 25, 1),
    ("BS_MM", 8, DepartmentEnum.FMCE, 25, 1),

    # FMCE – Chemical
    ("BS_ChE", 3, DepartmentEnum.FMCE, 25, 2),
    ("BS_ChE", 4, DepartmentEnum.FMCE, 25, 2),
    ("BS_ChE", 5, DepartmentEnum.FMCE, 25, 2),
    ("BS_ChE", 6, DepartmentEnum.FMCE, 25, 2),
    ("BS_ChE", 7, DepartmentEnum.FMCE, 25, 1),
    ("BS_ChE", 8, DepartmentEnum.FMCE, 25, 1),

    # Civil
    ("BS_CvE", 3, DepartmentEnum.CIVIL, 35, 2),
    ("BS_CvE", 4, DepartmentEnum.CIVIL, 35, 2),
    ("BS_CvE", 5, DepartmentEnum.CIVIL, 35, 2),
    ("BS_CvE", 6, DepartmentEnum.CIVIL, 35, 2),
    ("BS_CvE", 7, DepartmentEnum.CIVIL, 35, 1),
    ("BS_CvE", 8, DepartmentEnum.CIVIL, 35, 1),

    # SMS
    ("BS_MS", 1, DepartmentEnum.SMS, 40, 2),
    ("BS_MS", 2, DepartmentEnum.SMS, 40, 2),
    ("BS_MS", 3, DepartmentEnum.SMS, 40, 2),
    ("BS_MS", 4, DepartmentEnum.SMS, 40, 2),
    ("BS_MS", 7, DepartmentEnum.SMS, 40, 1),
    ("BS_MS", 8, DepartmentEnum.SMS, 40, 1),
]


def generate_sections_from_curriculum() -> list[dict]:
    """
    Generate sections from CURRICULUM map and SECTION_CONFIG.

    Each section's course_codes are derived from CURRICULUM[program_sem{semester}].
    This enforces constraint: NEVER hardcode section course lists.

    Returns: List of section dicts ready for Section model.
    """
    sections = []
    for program, semester, department, student_count, num_sections in SECTION_CONFIG:
        key = f"{program}_sem{semester}"
        course_codes = CURRICULUM.get(key, [])

        if not course_codes:
            continue  # Skip if no curriculum defined

        for i in range(1, num_sections + 1):
            section_id = f"{program}-{semester}-{chr(64 + i)}"  # e.g., BS_CS-1-A
            sections.append({
                "id": section_id,
                "program": program,
                "semester": semester,
                "department": department,
                "student_count": student_count,
                "course_codes": course_codes
            })

    return sections


def get_seed_courses() -> list[dict]:
    """Return seed courses, validating all tags are in TAG_TAXONOMY."""
    validate_course_tags()
    return RAW_COURSES


def get_seed_teachers() -> list[tuple]:
    """Return seed teachers, validating all tags are in TAG_TAXONOMY."""
    validate_teacher_tags()
    return RAW_TEACHERS


def get_seed_rooms() -> list[dict]:
    """Return seed rooms."""
    return ROOMS
