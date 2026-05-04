import { useState } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useAppStore } from '@/store'
import { DAYS, PERIODS } from '@/lib/constants'
import { cn } from '@/lib/utils'

export default function Timetable() {
  const { lastSchedule, sections, conflicts } = useAppStore()
  const [activeTab, setActiveTab] = useState('table')

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Timetable</h2>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="table">Schedule Table</TabsTrigger>
          <TabsTrigger value="grid">Weekly Grid</TabsTrigger>
          <TabsTrigger value="stats">Statistics</TabsTrigger>
        </TabsList>

        <TabsContent value="table" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Schedule Table</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-2">Day</th>
                      <th className="text-left p-2">Period</th>
                      <th className="text-left p-2">Course</th>
                      <th className="text-left p-2">Section</th>
                      <th className="text-left p-2">Teacher</th>
                      <th className="text-left p-2">Room</th>
                    </tr>
                  </thead>
                  <tbody>
                    {lastSchedule.slice(0, 20).map((entry, idx) => (
                      <tr key={idx} className="border-b border-muted">
                        <td className="p-2">{entry.day}</td>
                        <td className="p-2">{entry.period}</td>
                        <td className="p-2">{entry.course_code}</td>
                        <td className="p-2">{entry.section_id}</td>
                        <td className="p-2">{entry.teacher_id}</td>
                        <td className="p-2">{entry.room_id}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {lastSchedule.length === 0 && (
                  <p className="text-center text-muted-foreground py-8">
                    No schedule generated yet. Go to Dashboard to generate a timetable.
                  </p>
                )}
                {lastSchedule.length > 20 && (
                  <p className="text-center text-muted-foreground py-4">
                    ... and {lastSchedule.length - 20} more entries
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="grid" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Weekly Grid</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <div className="grid grid-cols-6 gap-1 min-w-[600px]">
                  <div className="p-2 font-bold">Period</div>
                  {DAYS.map((day) => (
                    <div key={day} className="p-2 font-bold text-center">{day}</div>
                  ))}
                  
                  {PERIODS.map((period) => (
                    <>
                      <div key={`p-${period}`} className="p-2 font-medium">{period}</div>
                      {DAYS.map((day) => {
                        const entry = lastSchedule.find(
                          (e) => e.day === day && e.period === period
                        )
                        return (
                          <div
                            key={`${day}-${period}`}
                            className={cn(
                              'p-2 min-h-[60px] border rounded',
                              entry ? 'bg-secondary' : 'border-dashed border-muted'
                            )}
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
              </div>
              {lastSchedule.length === 0 && (
                <p className="text-center text-muted-foreground py-8">
                  No schedule generated yet. Go to Dashboard to generate a timetable.
                </p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="stats" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Statistics</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div className="p-4 bg-secondary rounded">
                  <div className="text-2xl font-bold">{lastSchedule.length}</div>
                  <div className="text-sm text-muted-foreground">Total Sessions</div>
                </div>
                <div className="p-4 bg-secondary rounded">
                  <div className="text-2xl font-bold">{conflicts.length}</div>
                  <div className="text-sm text-muted-foreground">Conflicts</div>
                </div>
                <div className="p-4 bg-secondary rounded">
                  <div className="text-2xl font-bold">{sections.length}</div>
                  <div className="text-sm text-muted-foreground">Sections</div>
                </div>
              </div>
              
              {conflicts.length > 0 && (
                <div className="mt-4">
                  <h4 className="font-medium mb-2">Conflicts</h4>
                  <ul className="space-y-1">
                    {conflicts.map((conflict, idx) => (
                      <li key={idx} className="p-2 bg-destructive/10 rounded text-sm">
                        {conflict}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
