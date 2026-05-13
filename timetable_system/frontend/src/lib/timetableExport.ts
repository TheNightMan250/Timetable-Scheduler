// Period start times in minutes from midnight
export const PERIOD_STARTS = [
  { period: 1, minutes: 480 },  // 08:00
  { period: 2, minutes: 540 },  // 09:00
  { period: 3, minutes: 630 },  // 10:30
  { period: 4, minutes: 690 },  // 11:30
  { period: 5, minutes: 750 },  // 12:30
  { period: 6, minutes: 870 },  // 14:30
  { period: 7, minutes: 930 },  // 15:30
  { period: 8, minutes: 990 },  // 16:30
];

export function mapToPeriod(startTime: string): number {
  const [h, m] = startTime.split(':').map(Number);
  const mins = h * 60 + m;
  return PERIOD_STARTS.reduce((closest, p) =>
    Math.abs(p.minutes - mins) < Math.abs(closest.minutes - mins) ? p : closest
  ).period;
}

// Generate consistent color for a course code using hash-to-hue
export function getCourseColor(courseCode: string): string {
  let hash = 0;
  for (let i = 0; i < courseCode.length; i++) {
    hash = courseCode.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = Math.abs(hash) % 360;
  return `hsl(${hue}, 70%, 85%)`;
}

// Calculate number of periods a time range spans
export function calculatePeriodSpan(startTime: string, endTime: string): number {
  const startPeriod = mapToPeriod(startTime);
  const endPeriod = mapToPeriod(endTime);
  return endPeriod - startPeriod + 1;
}
