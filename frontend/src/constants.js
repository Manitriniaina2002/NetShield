export const SECURITY_LEVELS = {
  'Open': { color: 'bg-red-600', label: '🔓 Ouvert', priority: 'Critique' },
  'WEP': { color: 'bg-red-600', label: '🔴 WEP', priority: 'Critique' },
  'WPA': { color: 'bg-orange-500', label: '🟠 WPA', priority: 'Élevé' },
  'WPA2': { color: 'bg-yellow-500', label: '🟡 WPA2', priority: 'Moyen' },
  'WPA3': { color: 'bg-green-500', label: '🟢 WPA3', priority: 'Sécurisé' },
}

export const RISK_COLORS = {
  'Critique': 'text-red-600 bg-red-900 bg-opacity-20',
  'Élevée': 'text-orange-500 bg-orange-900 bg-opacity-20',
  'Moyen': 'text-yellow-500 bg-yellow-900 bg-opacity-20',
  'Faible': 'text-green-500 bg-green-900 bg-opacity-20'
}

export const formatSignal = (dbm) => {
  if (dbm >= -30) return 100
  if (dbm <= -90) return 0
  return 2 * (dbm + 100)
}

export const getSignalBar = (percentage) => {
  const filled = Math.floor(percentage / 20)
  const empty = 5 - filled
  return '█'.repeat(filled) + '░'.repeat(empty)
}
