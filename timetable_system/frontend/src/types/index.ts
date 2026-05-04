export interface Course {
  code: string
  name: string
  credit_hours: number
  department: Department
  is_lab: boolean
  sessions_per_week: number
  semester: number
  is_elective: boolean
  domain_tags: string[]
}

export interface Teacher {
  id: string
  name: string
  department: Department
  domain_tags: string[]
  max_sessions_per_week: number
}

export interface Room {
  id: string
  name: string
  capacity: number
  room_type: RoomType
  department: Department
}

export interface Section {
  id: string
  program: string
  semester: number
  department: Department
  student_count: number
  course_codes: string[]
}

export interface ScheduleEntry {
  course_code: string
  teacher_id: string
  room_id: string
  section_id: string
  day: Day
  period: number
  start_time: string
  end_time: string
}

export interface TeacherMatch {
  course: Course
  overlap_tags: string[]
  overlap_count: number
  score: number
}

export interface ScheduleResult {
  success: boolean
  entries_scheduled: number
  entries_unscheduled: number
  conflicts_detected: number
  message: string
}

export interface ScheduleGenerateRequest {
  iterations: number
  initial_temp: number
}

export interface CurriculumEntry {
  program: string
  semester: number
  course_codes: string[]
}

export interface ConflictsResponse {
  conflicts: string[]
  count: number
}

export type Department =
  | 'FCSE'
  | 'FEE'
  | 'FME'
  | 'FMCE'
  | 'CIVIL'
  | 'SMS'
  | 'BASIC_SCIENCE'
  | 'COMMON'

export type RoomType = 'LECTURE_HALL' | 'LAB' | 'SEMINAR' | 'AUDITORIUM'

export type Day = 'Mon' | 'Tue' | 'Wed' | 'Thu' | 'Fri'

export interface TagTaxonomy {
  [category: string]: string[]
}

export interface UnscheduledReason {
  course_code: string
  reason: string
}
