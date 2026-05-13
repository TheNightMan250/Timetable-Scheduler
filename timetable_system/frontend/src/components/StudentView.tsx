import { useState, useRef } from 'react'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useAppStore } from '@/store'
import { DAYS } from '@/lib/constants'
import { getCourseColor, mapToPeriod, calculatePeriodSpan, PERIOD_STARTS } from '@/lib/timetableExport'
import html2canvas from 'html2canvas'

export default function StudentView() {
  const { lastSchedule, sections, courses, teachers } = useAppStore()
  const [selectedSectionId, setSelectedSectionId] = useState<string>('')
  const [selectedElectives, setSelectedElectives] = useState<Set<string>>(new Set())
  const exportRef = useRef<HTMLDivElement>(null)

  // Get courses for selected section
  const sectionCourses = selectedSectionId
    ? courses.filter(c => {
        const section = sections.find(s => s.id === selectedSectionId)
        return section?.course_codes.includes(c.code)
      })
    : []

  // Separate core and elective courses
  const coreCourses = sectionCourses.filter(c => !c.is_elective)
  const electiveCourses = sectionCourses.filter(c => c.is_elective)

  // Filter schedule by section and selected courses
  const filteredSchedule = selectedSectionId
    ? lastSchedule.filter(entry => {
        if (entry.section_id !== selectedSectionId) return false
        const course = courses.find(c => c.code === entry.course_code)
        if (!course) return false
        if (!course.is_elective) return true // Core courses always included
        return selectedElectives.has(course.code) // Electives only if selected
      })
    : []

  // Detect conflicts (same day and period for different courses)
  const conflicts = new Set<string>()
  const scheduleMap = new Map<string, string[]>()
  filteredSchedule.forEach(entry => {
    const key = `${entry.day}-${entry.period}`
    if (!scheduleMap.has(key)) {
      scheduleMap.set(key, [])
    }
    scheduleMap.get(key)!.push(entry.course_code)
  })
  scheduleMap.forEach((courseCodes, key) => {
    if (courseCodes.length > 1) {
      conflicts.add(key)
    }
  })

  // Handle elective toggle
  const toggleElective = (courseCode: string) => {
    const newSet = new Set(selectedElectives)
    if (newSet.has(courseCode)) {
      newSet.delete(courseCode)
    } else {
      newSet.add(courseCode)
    }
    setSelectedElectives(newSet)
  }

  // Download as image
  const handleDownload = async () => {
    if (!exportRef.current || !selectedSectionId) return
    const canvas = await html2canvas(exportRef.current, { scale: 2 })
    const link = document.createElement('a')
    link.download = `timetable_${selectedSectionId}.png`
    link.href = canvas.toDataURL()
    link.click()
  }

  // Time slot labels
  const timeLabels = [
    '08:00–08:50',
    '09:00–09:50',
    '10:30–11:20',
    '11:30–12:20',
    '12:30–13:20',
    'BREAK',
    '14:30–15:20',
    '15:30–16:20',
    '16:30–17:20',
  ]

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Student View</CardTitle>
            {selectedSectionId && (
              <Button onClick={handleDownload} size="sm">
                Download as Image
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Section Selector */}
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium">Select Section:</label>
            <Select value={selectedSectionId} onValueChange={setSelectedSectionId}>
              <SelectTrigger className="w-[200px]">
                <SelectValue placeholder="Choose section" />
              </SelectTrigger>
              <SelectContent>
                {sections.map(section => (
                  <SelectItem key={section.id} value={section.id}>
                    {section.id}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Elective Toggles */}
          {selectedSectionId && electiveCourses.length > 0 && (
            <div className="space-y-2">
              <label className="text-sm font-medium">Select Your Electives:</label>
              <div className="flex flex-wrap gap-4">
                {electiveCourses.map(course => (
                  <div key={course.code} className="flex items-center gap-2">
                    <Checkbox
                      id={course.code}
                      checked={selectedElectives.has(course.code)}
                      onCheckedChange={() => toggleElective(course.code)}
                    />
                    <label htmlFor={course.code} className="text-sm">
                      {course.code} - {course.name}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Weekly Grid */}
          {selectedSectionId && (
            <div className="overflow-x-auto">
              <div className="grid grid-cols-10 gap-1 min-w-[800px]">
                {/* Header row */}
                <div className="p-2 font-bold">Day</div>
                {timeLabels.map((label, i) => (
                  <div
                    key={i}
                    className={`p-2 font-bold text-center ${label === 'BREAK' ? 'bg-gray-200' : ''}`}
                  >
                    {label}
                  </div>
                ))}

                {/* Data rows */}
                {DAYS.map(day => (
                  <>
                    <div key={`day-${day}`} className="p-2 font-medium">{day}</div>
                    {timeLabels.map((label, periodIdx) => {
                      if (label === 'BREAK') {
                        return (
                          <div key={`${day}-break`} className="p-2 bg-gray-200 text-center text-sm font-medium">
                            BREAK
                          </div>
                        )
                      }

                      const period = periodIdx < 5 ? periodIdx + 1 : periodIdx
                      const entry = filteredSchedule.find(
                        e => e.day === day && e.period === period
                      )
                      const isConflict = conflicts.has(`${day}-${period}`)

                      return (
                        <div
                          key={`${day}-${period}`}
                          className={`p-2 min-h-[60px] border rounded ${
                            entry ? '' : 'border-dashed border-muted'
                          } ${isConflict ? 'bg-red-200' : ''}`}
                          style={entry ? { backgroundColor: getCourseColor(entry.course_code) } : {}}
                        >
                          {entry && (
                            <div className="text-xs">
                              <div className="font-bold">{entry.course_code}</div>
                              <div className="text-muted-foreground">{entry.room_id}</div>
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </>
                ))}
              </div>

              {filteredSchedule.length === 0 && (
                <p className="text-center text-muted-foreground py-8">
                  No schedule for this section. Generate a timetable first.
                </p>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Hidden off-screen renderer for image export */}
      {selectedSectionId && (
        <div
          ref={exportRef}
          style={{
            position: 'fixed',
            left: '-9999px',
            top: '0',
            width: '1000px',
            padding: '20px',
            backgroundColor: 'white',
            fontFamily: 'Arial, sans-serif',
          }}
        >
          <h2 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '10px' }}>
            {selectedSectionId} — Personal Timetable
          </h2>
          {selectedElectives.size > 0 && (
            <p style={{ fontSize: '14px', marginBottom: '20px' }}>
              Electives: {Array.from(selectedElectives).join(', ')}
            </p>
          )}

          <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '20px' }}>
            <thead>
              <tr>
                <th style={{ border: '1px solid #ccc', padding: '8px', backgroundColor: '#f0f0f0' }}>Day</th>
                {timeLabels.map((label, i) => (
                  <th
                    key={i}
                    style={{
                      border: '1px solid #ccc',
                      padding: '8px',
                      backgroundColor: label === 'BREAK' ? '#e5e7eb' : '#f0f0f0',
                      width: label === 'BREAK' ? '40px' : '100px',
                    }}
                  >
                    {label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {DAYS.map(day => (
                <tr key={day}>
                  <td style={{ border: '1px solid #ccc', padding: '8px', fontWeight: 'bold' }}>{day}</td>
                  {timeLabels.map((label, periodIdx) => {
                    if (label === 'BREAK') {
                      return (
                        <td
                          key={`${day}-break`}
                          style={{
                            border: '1px solid #ccc',
                            padding: '8px',
                            backgroundColor: '#e5e7eb',
                            textAlign: 'center',
                            fontWeight: 'bold',
                            width: '40px',
                          }}
                        >
                          BREAK
                        </td>
                      )
                    }

                    const period = periodIdx < 5 ? periodIdx + 1 : periodIdx
                    const entry = filteredSchedule.find(
                      e => e.day === day && e.period === period
                    )
                    const isConflict = conflicts.has(`${day}-${period}`)

                    return (
                      <td
                        key={`${day}-${period}`}
                        style={{
                          border: '1px solid #ccc',
                          padding: '8px',
                          backgroundColor: isConflict ? '#fecaca' : entry ? getCourseColor(entry.course_code) : 'white',
                          minHeight: '60px',
                        }}
                      >
                        {entry && (
                          <div>
                            <div style={{ fontWeight: 'bold', fontSize: '12px' }}>{entry.course_code}</div>
                            <div style={{ fontSize: '11px' }}>{entry.room_id}</div>
                          </div>
                        )}
                      </td>
                    )
                  })}
                </tr>
              ))}
            </tbody>
          </table>

          {/* Legend */}
          <div style={{ borderTop: '1px solid #ccc', paddingTop: '10px' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '10px' }}>Legend</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
              {Array.from(new Set(filteredSchedule.map(e => e.course_code))).map(courseCode => {
                const course = courses.find(c => c.code === courseCode)
                const teacher = teachers.find(t => t.id === filteredSchedule.find(e => e.course_code === courseCode)?.teacher_id)
                return (
                  <div key={courseCode} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div
                      style={{
                        width: '20px',
                        height: '20px',
                        backgroundColor: getCourseColor(courseCode),
                        border: '1px solid #ccc',
                      }}
                    />
                    <span style={{ fontSize: '12px' }}>
                      <strong>{courseCode}</strong> - {course?.name} ({teacher?.name})
                    </span>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
