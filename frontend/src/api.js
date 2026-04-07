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
    console.error('Erreur API:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const wifiAPI = {
  // Scan Wi-Fi
  scanNetworks: (duration = 10, name = 'Audit Scan') =>
    api.post('/scan/networks', null, { params: { duration, name } }),
  
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
  
  startCrackingJob: (networkBssid, method = 'aircrack-ng', wordlist = 'academic', gpuEnabled = false) =>
    api.post('/cracking/start', {
      network_bssid: networkBssid,
      method,
      wordlist,
      gpu_enabled: gpuEnabled
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
    api.get('/cracking/handshake-capture-guide')
}

export default api
