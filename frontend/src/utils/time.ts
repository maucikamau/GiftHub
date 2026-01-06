export function formatTimestamp(timestamp: number) {
  return new Date(timestamp).toLocaleTimeString('hr-HR', {
    hour: '2-digit',
    minute: '2-digit',
  })
}
