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

export function formatText(count: number, singular: string) {
  if (count % 10 === 1) {
    return `${count} ${singular}u`
  }
  else if (count % 10 >= 2 && count % 10 <= 4) {
    return `${count} ${singular}e`
  }
  else {
    return `${count} ${singular}a`
  }
}

export function trim(text: string, maxLength: number) {
  if (text.length <= maxLength) {
    return text
  }
  return `${text.slice(0, maxLength)}...`
}
