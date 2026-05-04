import { useState } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useAppStore } from '@/store'

export default function Manage() {
  const { courses, teachers, rooms } = useAppStore()
  const [activeTab, setActiveTab] = useState('courses')

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Manage Data</h2>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="courses">Courses ({courses.length})</TabsTrigger>
          <TabsTrigger value="teachers">Teachers ({teachers.length})</TabsTrigger>
          <TabsTrigger value="rooms">Rooms ({rooms.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="courses" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Courses</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                {courses.length} courses loaded from backend.
              </p>
              <ul className="mt-4 space-y-2">
                {courses.slice(0, 10).map((course) => (
                  <li key={course.code} className="p-2 bg-secondary rounded">
                    <strong>{course.code}</strong> - {course.name} ({course.department})
                  </li>
                ))}
                {courses.length > 10 && (
                  <li className="text-muted-foreground">
                    ... and {courses.length - 10} more
                  </li>
                )}
              </ul>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="teachers" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Teachers</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                {teachers.length} teachers loaded from backend.
              </p>
              <ul className="mt-4 space-y-2">
                {teachers.slice(0, 10).map((teacher) => (
                  <li key={teacher.id} className="p-2 bg-secondary rounded">
                    <strong>{teacher.name}</strong> ({teacher.id}) - {teacher.department}
                  </li>
                ))}
                {teachers.length > 10 && (
                  <li className="text-muted-foreground">
                    ... and {teachers.length - 10} more
                  </li>
                )}
              </ul>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="rooms" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Rooms</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                {rooms.length} rooms loaded from backend.
              </p>
              <ul className="mt-4 space-y-2">
                {rooms.slice(0, 10).map((room) => (
                  <li key={room.id} className="p-2 bg-secondary rounded">
                    <strong>{room.name}</strong> - Capacity: {room.capacity} ({room.room_type})
                  </li>
                ))}
                {rooms.length > 10 && (
                  <li className="text-muted-foreground">
                    ... and {rooms.length - 10} more
                  </li>
                )}
              </ul>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
