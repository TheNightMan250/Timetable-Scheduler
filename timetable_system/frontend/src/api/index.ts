import axios from 'axios'
import { toast } from 'sonner'
import type {
  Course,
  Teacher,
  Room,
  Section,
  ScheduleEntry,
  ScheduleGenerateRequest,
  ScheduleResult,
  TeacherMatch,
  ConflictsResponse,
  CurriculumEntry,
  TagTaxonomy,
} from '@/types'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Global error interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'An error occurred'
    toast.error(message)
    return Promise.reject(error)
  }
)

// Courses API
export const coursesApi = {
  getAll: () => api.get<Course[]>('/api/courses').then((r) => r.data),
  create: (course: Course) =>
    api.post('/api/courses', course).then((r) => r.data),
  update: (code: string, course: Course) =>
    api.put(`/api/courses/${code}`, course).then((r) => r.data),
  delete: (code: string) =>
    api.delete(`/api/courses/${code}`).then((r) => r.data),
}

// Teachers API
export const teachersApi = {
  getAll: () => api.get<Teacher[]>('/api/teachers').then((r) => r.data),
  create: (teacher: Teacher) =>
    api.post('/api/teachers', teacher).then((r) => r.data),
  update: (id: string, teacher: Teacher) =>
    api.put(`/api/teachers/${id}`, teacher).then((r) => r.data),
  delete: (id: string) =>
    api.delete(`/api/teachers/${id}`).then((r) => r.data),
  getMatches: (id: string) =>
    api.get<{ teacher_id: string; matches: TeacherMatch[]; total_matches: number }>(
      `/api/teachers/${id}/matches`
    ).then((r) => r.data),
}

// Rooms API
export const roomsApi = {
  getAll: () => api.get<Room[]>('/api/rooms').then((r) => r.data),
  create: (room: Room) =>
    api.post('/api/rooms', room).then((r) => r.data),
  update: (id: string, room: Room) =>
    api.put(`/api/rooms/${id}`, room).then((r) => r.data),
  delete: (id: string) =>
    api.delete(`/api/rooms/${id}`).then((r) => r.data),
}

// Sections API
export const sectionsApi = {
  getAll: () => api.get<Section[]>('/api/sections').then((r) => r.data),
  create: (section: Section) =>
    api.post('/api/sections', section).then((r) => r.data),
}

// Tags API
export const tagsApi = {
  getAll: () => api.get<TagTaxonomy>('/api/tags').then((r) => r.data),
}

// Curriculum API
export const curriculumApi = {
  getAll: () => api.get<Record<string, string[]>>('/api/curriculum').then((r) => r.data),
  update: (entry: CurriculumEntry) =>
    api.put('/api/curriculum', entry).then((r) => r.data),
}

// Schedule API
export const scheduleApi = {
  generate: (params: ScheduleGenerateRequest) =>
    api.post<ScheduleResult>('/api/schedule/generate', params).then((r) => r.data),
  getResults: () =>
    api.get<ScheduleEntry[]>('/api/schedule/results').then((r) => r.data),
  getConflicts: () =>
    api.get<ConflictsResponse>('/api/schedule/conflicts').then((r) => r.data),
  exportCSV: () =>
    api.get('/api/schedule/export/csv', { responseType: 'blob' }).then((r) => r.data),
}

export default api
