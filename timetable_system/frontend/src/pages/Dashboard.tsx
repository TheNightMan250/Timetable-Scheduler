import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { BookOpen, Users, Building, Layers, Play, Download, Settings, Loader2 } from 'lucide-react'
import { toast } from 'sonner'
import { useAppStore } from '@/store'
import { scheduleApi } from '@/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Slider } from '@/components/ui/slider'
import { Label } from '@/components/ui/label'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import { cn, getConflictColor, getConflictTextColor } from '@/lib/utils'

export default function Dashboard() {
  const navigate = useNavigate()
  const [showGenerateDialog, setShowGenerateDialog] = useState(false)
  const [iterations, setIterations] = useState([2000])
  const [initialTemp, setInitialTemp] = useState([100])

  const {
    courses,
    teachers,
    rooms,
    sections,
    lastSchedule,
    conflicts,
    isGenerating,
    setIsGenerating,
    setLastSchedule,
    setConflicts,
  } = useAppStore()

  const handleGenerate = async () => {
    setIsGenerating(true)
    try {
      const result = await scheduleApi.generate({
        iterations: iterations[0],
        initial_temp: initialTemp[0],
      })
      
      const [schedule, conflictsData] = await Promise.all([
        scheduleApi.getResults(),
        scheduleApi.getConflicts(),
      ])
      
      setLastSchedule(schedule)
      setConflicts(conflictsData.conflicts)
      
      toast.success(result.message)
      setShowGenerateDialog(false)
    } catch (error) {
      toast.error('Failed to generate schedule')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleExport = async () => {
    try {
      const blob = await scheduleApi.exportCSV()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `giki_schedule_${new Date().toISOString().slice(0, 10)}.csv`
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
      toast.success('Schedule exported successfully')
    } catch (error) {
      toast.error('Failed to export schedule')
    }
  }

  const conflictCount = conflicts.length

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <div className="flex gap-2">
          <Button onClick={() => setShowGenerateDialog(true)} disabled={isGenerating}>
            {isGenerating ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Play className="mr-2 h-4 w-4" />
            )}
            Generate Timetable
          </Button>
          <Button variant="outline" onClick={() => navigate('/manage')}>
            <Settings className="mr-2 h-4 w-4" />
            Go to Manage
          </Button>
          <Button variant="outline" onClick={handleExport}>
            <Download className="mr-2 h-4 w-4" />
            Export CSV
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Sections</CardTitle>
            <Layers className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{sections.length}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Courses</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{courses.length}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Teachers</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{teachers.length}</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Rooms</CardTitle>
            <Building className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{rooms.length}</div>
          </CardContent>
        </Card>
      </div>

      {/* Schedule Stats */}
      <Card>
        <CardHeader>
          <CardTitle>Last Schedule Run</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <div>
              <p className="text-sm text-muted-foreground">Scheduled Entries</p>
              <p className="text-2xl font-bold">{lastSchedule.length}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Conflicts</p>
              <div className="flex items-center gap-2">
                <p className={cn('text-2xl font-bold', getConflictTextColor(conflictCount))}>
                  {conflictCount}
                </p>
                <Badge
                  variant="outline"
                  className={cn(
                    'text-white',
                    getConflictColor(conflictCount)
                  )}
                >
                  {conflictCount === 0 ? 'Clean' : conflictCount <= 5 ? 'Warning' : 'Critical'}
                </Badge>
              </div>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Status</p>
              <p className="text-lg font-medium">
                {lastSchedule.length > 0 ? 'Generated' : 'Not Generated'}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Generate Dialog */}
      <Dialog open={showGenerateDialog} onOpenChange={setShowGenerateDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Generate Timetable</DialogTitle>
            <DialogDescription>
              Configure simulated annealing parameters for schedule generation.
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-6 py-4">
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Iterations</Label>
                <span className="text-sm text-muted-foreground">{iterations[0]}</span>
              </div>
              <Slider
                value={iterations}
                onValueChange={setIterations}
                min={500}
                max={5000}
                step={100}
              />
              <p className="text-xs text-muted-foreground">More iterations = better results but slower</p>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>Initial Temperature</Label>
                <span className="text-sm text-muted-foreground">{initialTemp[0]}</span>
              </div>
              <Slider
                value={initialTemp}
                onValueChange={setInitialTemp}
                min={10}
                max={500}
                step={10}
              />
              <p className="text-xs text-muted-foreground">Higher temp = more exploration</p>
            </div>
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowGenerateDialog(false)}>
              Cancel
            </Button>
            <Button onClick={handleGenerate} disabled={isGenerating}>
              {isGenerating && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Generate
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
