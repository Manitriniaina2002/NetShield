import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor pour les erreurs
api.interceptors.response.use(
  response => response,
  error => {
    const status = error.response?.status
    const requestUrl = error.config?.url || ''
    const isExpectedKismetOffline = status === 503 && requestUrl.includes('/kismet/')

    if (!isExpectedKismetOffline) {
      console.error('Erreur API:', error.response?.data || error.message)
    }

    return Promise.reject(error)
  }
)

const normalizeCrackingMethod = (method) => {
  const aliases = {
    aircrack_ng: 'aircrack-ng',
    'aircrack-ng': 'aircrack-ng',
    hashcat: 'hashcat',
    john_ripper: 'john',
    john: 'john'
  }

  return aliases[method] || method
}

export const wifiAPI = {
  // Scan Wi-Fi
  scanNetworks: (duration = 10, name = 'Audit Scan', includeDemoData = true, includeDemoFailed = false) =>
    api.post('/scan/networks', null, {
      params: {
        duration,
        name,
        include_demo_data: includeDemoData,
        include_demo_failed: includeDemoFailed
      }
    }),
  
  getNetworkDetails: (bssid, channel = 6) =>
    api.get(`/scan/networks/${bssid}`, { params: { channel } }),
  
  // Vulnérabilités
  analyzeNetwork: (bssid, network) =>
    api.post(`/vulnerabilities/analyze/${bssid}`, network),
  
  analyzeBatch: (networks) =>
    api.post('/vulnerabilities/analyze-batch', networks),
  
  // Cracking strategies
  getCrackingStrategy: (bssid, network) =>
    api.post(`/vulnerabilities/cracking-strategy/${bssid}`, network),
  
  getCrackingStrategiesBatch: (networks) =>
    api.post('/vulnerabilities/cracking-strategies-batch', networks),
  
  // Recommandations
  generateRecommendations: (vulnerabilities, networks) =>
    api.post('/recommendations/generate', { vulnerabilities, networks }),
  
  // Rapports
  generatePDF: (report) =>
    api.post('/reports/pdf', report, { responseType: 'blob' }),
  
  saveReport: (report, filename = null) =>
    api.post('/reports/save', report, { params: { filename } }),
  
  exportJSON: (report) =>
    api.post('/reports/json', report, { responseType: 'blob' }),
  
  // Commandes
  getAllowedCommands: () =>
    api.get('/commands/allowed'),
  
  executeCommand: (command, args = null) =>
    api.post('/commands/execute', null, { params: { command, args } }),
  
  // Cracking
  getCrackingStatus: () =>
    api.get('/cracking/status'),
  
  getAvailableWordlists: () =>
    api.get('/cracking/wordlists'),
  
  getCrackingMethods: () =>
    api.get('/cracking/methods'),
  
  startCrackingJob: (networkBssid, method = 'aircrack-ng', wordlist = 'academic', gpuEnabled = false, handshakeId = null) =>
    api.post('/cracking/start', {
      network_bssid: networkBssid,
      method: normalizeCrackingMethod(method),
      wordlist,
      gpu_enabled: gpuEnabled,
      handshake_id: handshakeId
    }),
  
  getJobStatus: (jobId) =>
    api.get(`/cracking/job/${jobId}`),
  
  listActiveJobs: () =>
    api.get('/cracking/jobs'),
  
  pauseJob: (jobId) =>
    api.post(`/cracking/job/${jobId}/pause`),
  
  cancelJob: (jobId) =>
    api.post(`/cracking/job/${jobId}/cancel`),
  
  getHandshakeCaptureGuide: () =>
    api.get('/cracking/handshake-capture-guide'),

  // Handshake Capture
  startHandshakeCapture: (network, duration = 60, enableDeauth = false, deauthCount = 5) =>
    api.post('/handshake/capture/start', { network, duration, enable_deauth: enableDeauth, deauth_count: deauthCount }),
  
  getHandshakeCaptureStatus: (captureId) =>
    api.get(`/handshake/capture/status/${captureId}`),
  
  listActiveCaptures: () =>
    api.get('/handshake/capture/list'),
  
  cancelCapture: (captureId) =>
    api.post(`/handshake/capture/cancel/${captureId}`),
  
  getAvailableWiFiInterfaces: () =>
    api.get('/handshake/interfaces'),
  
  useCaptureForcCracking: (captureId, passwordList = null, crackingMethod = 'aircrack_ng') =>
    api.post(`/handshake/capture/integrated/${captureId}`, null, { 
      params: { 
        password_list: passwordList,
        cracking_method: crackingMethod
      }
    }),

  // Stored Handshakes
  getStoredHandshakes: (successfulOnly = false, limit = 100) =>
    api.get('/stored/handshakes', { params: { successful_only: successfulOnly, limit } }),
  
  getStoredHandshakesByNetwork: (bssid, successfulOnly = false) =>
    api.get(`/stored/handshakes/network/${bssid}`, { params: { successful_only: successfulOnly } }),
  
  getStoredHandshakeDetails: (captureId) =>
    api.get(`/stored/handshakes/${captureId}`),
  
  getStoredHandshakeCrackingHistory: (captureId) =>
    api.get(`/stored/handshakes/${captureId}/cracking-history`),
  
  getStoredHandshakeStatistics: () =>
    api.get('/stored/statistics'),
  
  getSuccessfulCracksForNetwork: (bssid) =>
    api.get(`/stored/cracking-results/network/${bssid}`),
  
  deleteStoredHandshake: (captureId) =>
    api.delete(`/stored/handshakes/${captureId}`),
  
  cleanupOldCaptures: (daysOld = 30) =>
    api.post('/stored/cleanup/old-captures', { days_old: daysOld })
}

// API Kismet pour scanning avancé
export const kismetAPI = {
  // Scan Wi-Fi via Kismet
  scanNetworks: (duration = 30, kismetUrl = 'http://localhost:2501', name = 'Kismet Scan') =>
    api.post('/kismet/networks/scan', null, { params: { duration, kismet_url: kismetUrl, name } }),
  
  // Récupérer les réseaux actuellement suivis par Kismet
  getNetworks: (kismetUrl = 'http://localhost:2501') =>
    api.get('/kismet/networks', { params: { kismet_url: kismetUrl } }),
  
  // Récupérer tous les appareils détectés par Kismet
  getDevices: (kismetUrl = 'http://localhost:2501') =>
    api.get('/kismet/devices', { params: { kismet_url: kismetUrl } }),
  
  // Récupérer les alertes Kismet
  getAlerts: (kismetUrl = 'http://localhost:2501') =>
    api.get('/kismet/alerts', { params: { kismet_url: kismetUrl } }),
  
  // Récupérer le statut du serveur Kismet
  getStatus: (kismetUrl = 'http://localhost:2501') =>
    api.get('/kismet/status', { params: { kismet_url: kismetUrl } })
}

export default api
