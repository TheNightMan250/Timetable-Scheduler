import type { Department, RoomType, Day, TagTaxonomy } from '@/types'

export const DEPARTMENTS: Department[] = [
  'FCSE',
  'FEE',
  'FME',
  'FMCE',
  'CIVIL',
  'SMS',
  'BASIC_SCIENCE',
  'COMMON',
]

export const DEPARTMENT_COLORS: Record<Department, string> = {
  FCSE: '#3b82f6',
  FEE: '#eab308',
  FME: '#22c55e',
  FMCE: '#a855f7',
  CIVIL: '#f97316',
  SMS: '#14b8a6',
  BASIC_SCIENCE: '#6b7280',
  COMMON: '#64748b',
}

export const DEPARTMENT_BG_COLORS: Record<Department, string> = {
  FCSE: 'bg-blue-500/20 border-blue-500/50',
  FEE: 'bg-yellow-500/20 border-yellow-500/50',
  FME: 'bg-green-500/20 border-green-500/50',
  FMCE: 'bg-purple-500/20 border-purple-500/50',
  CIVIL: 'bg-orange-500/20 border-orange-500/50',
  SMS: 'bg-teal-500/20 border-teal-500/50',
  BASIC_SCIENCE: 'bg-gray-500/20 border-gray-500/50',
  COMMON: 'bg-slate-500/20 border-slate-500/50',
}

export const DEPARTMENT_TEXT_COLORS: Record<Department, string> = {
  FCSE: 'text-blue-400',
  FEE: 'text-yellow-400',
  FME: 'text-green-400',
  FMCE: 'text-purple-400',
  CIVIL: 'text-orange-400',
  SMS: 'text-teal-400',
  BASIC_SCIENCE: 'text-gray-400',
  COMMON: 'text-slate-400',
}

export const ROOM_TYPES: RoomType[] = ['LECTURE_HALL', 'LAB', 'SEMINAR', 'AUDITORIUM']

export const ROOM_TYPE_LABELS: Record<RoomType, string> = {
  LECTURE_HALL: 'Lecture Hall',
  LAB: 'Laboratory',
  SEMINAR: 'Seminar Room',
  AUDITORIUM: 'Auditorium',
}

export const DAYS: Day[] = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

export const PERIODS = [1, 2, 3, 4, 5, 6, 7, 8]

export const TAG_TAXONOMY: TagTaxonomy = {
  Mathematics: [
    'calculus', 'linear_algebra', 'discrete_math', 'numerical_analysis',
    'differential_equations', 'statistics', 'probability',
  ],
  'CS Core': [
    'algorithms', 'complexity', 'data_structures', 'operating_systems',
    'computer_organization', 'digital_logic', 'compiler', 'formal_languages',
    'intro_programming', 'oop', 'databases', 'ict', 'computing',
  ],
  'CS Advanced': [
    'networks', 'distributed', 'parallel_computing', 'cloud',
    'computer_architecture', 'microprocessor', 'embedded', 'hardware',
  ],
  'AI & Data': [
    'ai', 'machine_learning', 'deep_learning', 'neural_networks',
    'computer_vision', 'nlp', 'knowledge_representation', 'data_science', 'big_data',
    'data_mining', 'visualization', 'reinforcement_learning',
  ],
  Security: [
    'cyber_security', 'cryptography', 'information_security', 'digital_forensics',
  ],
  'Software Engineering': [
    'software_engineering', 'requirements', 'architecture',
    'software_construction', 'quality', 'devops', 'web_engineering', 'mobile',
    'project_management', 'professional_issues',
  ],
  'Electrical Engineering': [
    'circuit_analysis', 'electrical_networks', 'electronic_devices',
    'signals', 'dsp', 'electromagnetic', 'power', 'power_electronics', 'power_distribution',
    'electric_machines', 'drives', 'instrumentation', 'control_systems',
    'communication_systems', 'robotics', 'applied_ee',
  ],
  'Mechanical Engineering': [
    'statics', 'dynamics', 'mechanics', 'mechanics_of_solids',
    'thermodynamics', 'heat_transfer', 'fluid_mechanics', 'manufacturing', 'machine_elements',
    'theory_of_machines', 'vibration', 'stress_analysis', 'workshop', 'engineering_graphics',
  ],
  'Materials Engineering': [
    'materials_science', 'thermodynamics_mm', 'phase_equilibria',
    'strength_materials', 'alloy', 'materials_chemistry', 'ceramics', 'polymers',
    'mineral_processing', 'xrd', 'nanotechnology', 'materials_lab', 'manufacturing_mm',
  ],
  'Chemical Engineering': [
    'chemical_engineering', 'thermodynamics_ch', 'mass_transfer',
    'heat_transfer_ch', 'fluid_mechanics_ch', 'reaction_kinetics', 'process_modelling',
    'particle_technology', 'analytical_chemistry', 'energy_engineering',
    'environmental_engineering', 'separation_processes', 'plant_design', 'transport',
  ],
  'Civil Engineering': [
    'surveying', 'structural_analysis', 'rc_design', 'steel_design',
    'mechanics_of_solids', 'soil_mechanics', 'geotechnical', 'fluid_mechanics_cv',
    'hydrology', 'transportation', 'highway', 'geology', 'concrete_technology',
    'construction', 'environmental_engineering_cv', 'geo_informatics',
  ],
  'Management & Humanities': [
    'business_mathematics', 'accounting', 'financial_management',
    'business_finance', 'marketing', 'management', 'hrm', 'organizational_behavior',
    'economics', 'microeconomics', 'macroeconomics', 'entrepreneurship', 'supply_chain',
    'operations_management', 'business_analytics', 'strategy', 'research_methods',
    'decision_analysis', 'leadership', 'engineering_economy',
  ],
  'Humanities & Common': [
    'communication_skills', 'critical_thinking', 'writing',
    'islamic_studies', 'pakistan_studies', 'ideology', 'civics', 'sociology', 'humanities',
    'law', 'ethics', 'professional_ethics', 'business_comm', 'innovation_lab', 'makers_lab',
  ],
  'Physics & Chemistry': [
    'physics', 'applied_physics', 'chemistry', 'occupational_health',
  ],
}

export const CONFLICT_COLORS = {
  0: 'bg-green-500',
  low: 'bg-amber-500',
  high: 'bg-red-500',
}

export const TYPICAL_SECTION_SIZE = 40
