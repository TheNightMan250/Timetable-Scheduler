import { create } from 'zustand'
import type { Course, Teacher, Room, Section, ScheduleEntry } from '@/types'

interface AppState {
  // Data
  courses: Course[]
  teachers: Teacher[]
  rooms: Room[]
  sections: Section[]
  lastSchedule: ScheduleEntry[]
  conflicts: string[]
  unscheduledReasons: string[]
  
  // Loading states
  isGenerating: boolean
  isLoading: boolean
  
  // Actions
  setCourses: (courses: Course[]) => void
  setTeachers: (teachers: Teacher[]) => void
  setRooms: (rooms: Room[]) => void
  setSections: (sections: Section[]) => void
  setLastSchedule: (schedule: ScheduleEntry[]) => void
  setConflicts: (conflicts: string[]) => void
  setUnscheduledReasons: (reasons: string[]) => void
  setIsGenerating: (value: boolean) => void
  setIsLoading: (value: boolean) => void
  
  // Add/Remove individual items
  addCourse: (course: Course) => void
  updateCourse: (code: string, course: Course) => void
  removeCourse: (code: string) => void
  addTeacher: (teacher: Teacher) => void
  updateTeacher: (id: string, teacher: Teacher) => void
  removeTeacher: (id: string) => void
  addRoom: (room: Room) => void
  updateRoom: (id: string, room: Room) => void
  removeRoom: (id: string) => void
  addSection: (section: Section) => void
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  courses: [],
  teachers: [],
  rooms: [],
  sections: [],
  lastSchedule: [],
  conflicts: [],
  unscheduledReasons: [],
  isGenerating: false,
  isLoading: false,
  
  // Setters
  setCourses: (courses) => set({ courses }),
  setTeachers: (teachers) => set({ teachers }),
  setRooms: (rooms) => set({ rooms }),
  setSections: (sections) => set({ sections }),
  setLastSchedule: (lastSchedule) => set({ lastSchedule }),
  setConflicts: (conflicts) => set({ conflicts }),
  setUnscheduledReasons: (unscheduledReasons) => set({ unscheduledReasons }),
  setIsGenerating: (isGenerating) => set({ isGenerating }),
  setIsLoading: (isLoading) => set({ isLoading }),
  
  // CRUD operations
  addCourse: (course) =>
    set((state) => ({ courses: [...state.courses, course] })),
  updateCourse: (code, course) =>
    set((state) => ({
      courses: state.courses.map((c) => (c.code === code ? course : c)),
    })),
  removeCourse: (code) =>
    set((state) => ({
      courses: state.courses.filter((c) => c.code !== code),
    })),
  addTeacher: (teacher) =>
    set((state) => ({ teachers: [...state.teachers, teacher] })),
  updateTeacher: (id, teacher) =>
    set((state) => ({
      teachers: state.teachers.map((t) => (t.id === id ? teacher : t)),
    })),
  removeTeacher: (id) =>
    set((state) => ({
      teachers: state.teachers.filter((t) => t.id !== id),
    })),
  addRoom: (room) =>
    set((state) => ({ rooms: [...state.rooms, room] })),
  updateRoom: (id, room) =>
    set((state) => ({
      rooms: state.rooms.map((r) => (r.id === id ? room : r)),
    })),
  removeRoom: (id) =>
    set((state) => ({
      rooms: state.rooms.filter((r) => r.id !== id),
    })),
  addSection: (section) =>
    set((state) => ({ sections: [...state.sections, section] })),
}))
