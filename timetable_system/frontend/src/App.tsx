import { Routes, Route } from 'react-router-dom'
import { useEffect } from 'react'
import { useAppStore } from '@/store'
import { coursesApi, teachersApi, roomsApi, sectionsApi, scheduleApi } from '@/api'
import Layout from '@/components/layout'
import Dashboard from '@/pages/Dashboard'
import Manage from '@/pages/Manage'
import Timetable from '@/pages/Timetable'

function App() {
  const {
    setCourses,
    setTeachers,
    setRooms,
    setSections,
    setLastSchedule,
    setConflicts,
  } = useAppStore()

  useEffect(() => {
    const loadData = async () => {
      try {
        const [courses, teachers, rooms, sections, schedule, conflicts] = await Promise.all([
          coursesApi.getAll(),
          teachersApi.getAll(),
          roomsApi.getAll(),
          sectionsApi.getAll(),
          scheduleApi.getResults(),
          scheduleApi.getConflicts(),
        ])
        setCourses(courses)
        setTeachers(teachers)
        setRooms(rooms)
        setSections(sections)
        setLastSchedule(schedule)
        setConflicts(conflicts.conflicts)
      } catch (error) {
        console.error('Failed to load initial data:', error)
      }
    }
    loadData()
  }, [setCourses, setTeachers, setRooms, setSections, setLastSchedule, setConflicts])

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/manage" element={<Manage />} />
        <Route path="/timetable" element={<Timetable />} />
      </Routes>
    </Layout>
  )
}

export default App
