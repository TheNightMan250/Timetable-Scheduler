import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getConflictColor(count: number): string {
  if (count === 0) return 'bg-green-500'
  if (count <= 5) return 'bg-amber-500'
  return 'bg-red-500'
}

export function getConflictTextColor(count: number): string {
  if (count === 0) return 'text-green-400'
  if (count <= 5) return 'text-amber-400'
  return 'text-red-400'
}

export function getInitials(name: string): string {
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

export function formatTime(period: number): string {
  const startHour = 8 + Math.floor((period - 1) / 2)
  const startMin = (period - 1) % 2 === 0 ? '00' : '30'
  const endHour = 8 + Math.floor(period / 2)
  const endMin = period % 2 === 0 ? '00' : '30'
  return `${startHour}:${startMin}-${endHour}:${endMin}`
}

export function calculateRoomUtilization(sessionsCount: number): number {
  const totalSlots = 5 * 8 // 5 days * 8 periods
  return Math.round((sessionsCount / totalSlots) * 100)
}

export function calculateCapacityPercentage(capacity: number, typicalSize: number = 40): number {
  return Math.round((typicalSize / capacity) * 100)
}
