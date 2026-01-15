export function formatTimestamp(timestamp: number) {
  return new Date(timestamp).toLocaleTimeString('hr-HR', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatCurrency(amount: number, currency: string) {
  return new Intl.NumberFormat('hr-HR', {
    style: 'currency',
    currency,
  }).format(amount)
}
