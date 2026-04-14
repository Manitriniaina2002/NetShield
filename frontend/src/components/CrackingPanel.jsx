import React, { useState, useEffect } from 'react'
import { wifiAPI } from '../api'
import StoredHandshakesPanel from './StoredHandshakesPanel'

const WORKFLOW_STEPS = [
  {
    id: 1,
    title: 'Capturer le handshake WPA2-4way',
    description: 'Confirmer que la capture handshake est disponible avant toute tentative de craquage.'
  },
  {
    id: 2,
    title: 'Convertir en format approprié (.hccapx pour hashcat)',
    description: 'Préparer le fichier pour le moteur choisi afin d’éviter les erreurs de format.'
  },
  {
    id: 3,
    title: 'Utiliser GPU (hashcat) pour accélération',
    description: 'Activer hashcat + GPU si la machine supporte l’accélération matérielle.'
  },
  {
    id: 4,
    title: 'Tester avec dictionnaire, puis règles, puis force brute (si temps)',
    description: 'Suivre un ordre d’attaque progressif pour optimiser le temps de calcul.'
  },
  {
    id: 5,
    title: 'Considérer attaque PMKID si support 802.11w',
    description: 'Évaluer les alternatives de collecte selon les capacités du point d’accès.'
  }
]

function CrackingPanel({ selectedNetwork, vulnerabilities }) {
  const normalizeMethodId = (methodId) => {
    const aliases = {
      aircrack_ng: 'aircrack-ng',
      'aircrack-ng': 'aircrack-ng',
      hashcat: 'hashcat',
      john_ripper: 'john',
      john: 'john'
    }

    return aliases[methodId] || methodId
  }

  const [crackingJobs, setCrackingJobs] = useState([])
  const [selectedMethod, setSelectedMethod] = useState('aircrack-ng')
  const [selectedWordlist, setSelectedWordlist] = useState('academic')
  const [gpuEnabled, setGpuEnabled] = useState(false)
  const [methods, setMethods] = useState([])
  const [wordlists, setWordlists] = useState([])
  const [crackingStatus, setCrackingStatus] = useState(null)
  const [strategy, setStrategy] = useState(null)
  const [loading, setLoading] = useState(false)
  const [pollingInterval, setPollingInterval] = useState(null)
  const [activeTab, setActiveTab] = useState('jobs')
  const [error, setError] = useState(null)
  const [completedSteps, setCompletedSteps] = useState([])
  const [activeStep, setActiveStep] = useState(1)
  const [workflowByNetwork, setWorkflowByNetwork] = useState({})
  const [selectedStoredHandshake, setSelectedStoredHandshake] = useState(null)

  // Load cracking info on component mount
  useEffect(() => {
    loadCrackingInfo()
  }, [])

  // Load strategy when network selected
  useEffect(() => {
    if (selectedNetwork) {
      loadStrategy()
    }
  }, [selectedNetwork])

  // Restaurer le workflow propre à chaque réseau quand la sélection change.
  useEffect(() => {
    const networkKey = selectedNetwork?.bssid
    if (!networkKey) {
      setCompletedSteps([])
      setActiveStep(1)
      return
    }

    const savedState = workflowByNetwork[networkKey]
    if (savedState) {
      setCompletedSteps(savedState.completedSteps || [])
      setActiveStep(savedState.activeStep || 1)
      return
    }

    setCompletedSteps([])
    setActiveStep(1)
  }, [selectedNetwork?.bssid])

  // Polling for job updates
  useEffect(() => {
    if (crackingJobs.length > 0) {
      const interval = setInterval(() => {
        updateJobStatuses()
      }, 2000)
      setPollingInterval(interval)
      return () => clearInterval(interval)
    }
  }, [crackingJobs])

  const loadCrackingInfo = async () => {
    try {
      const [statusRes, methodRes, wordlistRes] = await Promise.all([
        wifiAPI.getCrackingStatus(),
        wifiAPI.getCrackingMethods(),
        wifiAPI.getAvailableWordlists()
      ])
      
      setCrackingStatus(statusRes.data)
      const methodsSource = Object.keys(methodRes.data || {}).length > 0
        ? methodRes.data
        : (statusRes.data.available_tools || {})

      const normalizedMethods = Object.entries(methodsSource).map(([key, val]) => ({
        id: normalizeMethodId(key),
        name: val.name || key,
        description: val.description,
        available: Boolean(val.available ?? val.is_available)
      }))

      setMethods(normalizedMethods)
      if (!normalizedMethods.some(m => m.id === selectedMethod)) {
        const firstAvailable = normalizedMethods.find(m => m.available)
        setSelectedMethod(firstAvailable?.id || 'aircrack-ng')
      }
      
      setWordlists(Object.entries(wordlistRes.data || {}).map(([key, val]) => ({
        id: key,
        ...val
      })))
    } catch (error) {
      console.error('Error loading cracking info:', error)
    }
  }

  const loadStrategy = async () => {
    if (!selectedNetwork) return
    try {
      const response = await wifiAPI.getCrackingStrategy(selectedNetwork.bssid, selectedNetwork)
      setStrategy(response.data.cracking_strategy)
    } catch (error) {
      console.error('Error loading strategy:', error)
    }
  }

  const startCrackingJob = async () => {
    if (!selectedNetwork) {
      alert('Please select a network first')
      return
    }

    setLoading(true)
    try {
      const response = await wifiAPI.startCrackingJob(
        selectedNetwork.bssid,
        normalizeMethodId(selectedMethod),
        selectedWordlist,
        gpuEnabled,
        selectedStoredHandshake ? selectedStoredHandshake.id : null
      )

      const newJob = {
        job_id: response.data.job_id,
        network_bssid: response.data.network_bssid,
        network_ssid: response.data.network_ssid,
        method: response.data.method,
        status: response.data.status,
        progress: response.data.progress,
        wordlist: selectedWordlist,
        startTime: new Date(),
        password_found: null,
        error_message: null,
        handshake_id: selectedStoredHandshake ? selectedStoredHandshake.id : null
      }

      setCrackingJobs([...crackingJobs, newJob])
      setActiveTab('jobs')
    } catch (error) {
      console.error('Error starting cracking job:', error)
      alert('Failed to start cracking job')
    } finally {
      setLoading(false)
    }
  }

  const updateJobStatuses = async () => {
    const updatedJobs = await Promise.all(
      crackingJobs.map(async (job) => {
        try {
          const response = await wifiAPI.getJobStatus(job.job_id)
          return {
            ...job,
            status: response.data.status,
            progress: response.data.progress,
            password_found: response.data.password_found || null,
            error_message: response.data.error_message || null,
            attempts: response.data.attempts || 0,
            start_time: response.data.start_time,
            end_time: response.data.end_time
          }
        } catch (error) {
          return job
        }
      })
    )
    setCrackingJobs(updatedJobs)
  }

  const handlePauseJob = async (jobId) => {
    try {
      await wifiAPI.pauseJob(jobId)
      const updatedJobs = crackingJobs.map(job =>
        job.job_id === jobId ? { ...job, status: 'paused' } : job
      )
      setCrackingJobs(updatedJobs)
    } catch (error) {
      console.error('Error pausing job:', error)
    }
  }

  const handleCancelJob = async (jobId) => {
    try {
      await wifiAPI.cancelJob(jobId)
      const updatedJobs = crackingJobs.map(job =>
        job.job_id === jobId ? { ...job, status: 'cancelled' } : job
      )
      setCrackingJobs(updatedJobs)
    } catch (error) {
      console.error('Error cancelling job:', error)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      'running': '#3498db',
      'completed': '#27ae60',
      'failed': '#e74c3c',
      'paused': '#f39c12',
      'timeout': '#e67e22',
      'background_running': '#9b59b6'
    }
    return colors[status] || '#95a5a6'
  }

  const getSecurityLevel = () => {
    if (!selectedNetwork) return null
    const levels = {
      'Open': 'Critique',
      'WEP': 'Critique',
      'WPA': 'Élevé',
      'WPA2': 'Moyen',
      'WPA3': 'Faible'
    }
    return levels[selectedNetwork.security] || 'Inconnu'
  }

  const getStatusBadge = (status) => {
    const statusConfig = {
      'running': { bg: 'bg-blue-500/20', border: 'border-blue-500/40', text: 'text-blue-300', icon: '▶' },
      'completed': { bg: 'bg-green-500/20', border: 'border-green-500/40', text: 'text-green-300', icon: '✓' },
      'failed': { bg: 'bg-red-500/20', border: 'border-red-500/40', text: 'text-red-300', icon: '✕' },
      'paused': { bg: 'bg-yellow-500/20', border: 'border-yellow-500/40', text: 'text-yellow-300', icon: '⏸' }
    }
    return statusConfig[status] || statusConfig['failed']
  }

  const toggleStepCompletion = (stepId) => {
    const networkKey = selectedNetwork?.bssid
    const nextCompleted = completedSteps.includes(stepId)
      ? completedSteps.filter((id) => id !== stepId)
      : [...completedSteps, stepId]

    setCompletedSteps(nextCompleted)
    setActiveStep(stepId)

    if (networkKey) {
      setWorkflowByNetwork((prev) => ({
        ...prev,
        [networkKey]: {
          completedSteps: nextCompleted,
          activeStep: stepId
        }
      }))
    }

    // Préremplissage léger pour accélérer l'exécution côté UI.
    if (stepId === 3) {
      setSelectedMethod('hashcat')
      setGpuEnabled(true)
      setActiveTab('start')
    }

    if (stepId === 4) {
      setSelectedWordlist('academic')
      setActiveTab('start')
    }
  }

  const workflowProgress = Math.round((completedSteps.length / WORKFLOW_STEPS.length) * 100)

  return (
    <div className="space-y-6">
      {/* Tabs */}
      <div className="flex gap-1 border-b border-[#e5e7eb]">
        {['jobs', 'workflow', 'strategies', 'stored', 'start'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-6 py-3 font-mono text-sm font-semibold transition-all border-b-2 ${
              activeTab === tab
                ? 'text-[#22c55e] border-[#22c55e] bg-[#22c55e]/5'
                : 'text-[#6b7280] border-transparent hover:text-[#1f2937]'
            }`}
          >
            {tab === 'jobs' && `◇ Travaux (${crackingJobs.length})`}
            {tab === 'workflow' && `◎ Workflow (${workflowProgress}%)`}
            {tab === 'strategies' && '▦ Stratégies'}
            {tab === 'stored' && '💾 Captures'}
            {tab === 'start' && '→ Lancer'}
          </button>
        ))}
      </div>

      {/* Workflow Tab */}
      {activeTab === 'workflow' && (
        <div className="card">
          <div className="mb-5 flex items-center justify-between gap-3">
            <h3 className="text-lg font-bold text-[#22c55e] font-mono">◎ Workflow complet de craquage</h3>
            <span className="rounded border border-[#22c55e]/40 bg-[#22c55e]/10 px-3 py-1 text-xs font-mono font-bold text-[#22c55e]">
              {completedSteps.length}/{WORKFLOW_STEPS.length} étapes validées
            </span>
          </div>

          <div className="mb-6 h-2 w-full overflow-hidden rounded-full bg-[#0a0e27]/40">
            <div
              className="h-full bg-gradient-to-r from-[#22c55e] to-[#4ade80] transition-all duration-300"
              style={{ width: `${workflowProgress}%` }}
            />
          </div>

          {!selectedNetwork ? (
            <div className="text-center py-8 px-4">
              <p className="text-[#9ca3af] font-mono">Sélectionnez un réseau depuis "Vue d’ensemble" pour dérouler le workflow.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {WORKFLOW_STEPS.map((step) => {
                const completed = completedSteps.includes(step.id)
                const active = activeStep === step.id

                return (
                  <button
                    key={step.id}
                    type="button"
                    onClick={() => toggleStepCompletion(step.id)}
                    className={`w-full rounded-lg border p-4 text-left transition-all ${
                      completed
                        ? 'border-[#22c55e]/50 bg-[#22c55e]/10'
                        : active
                          ? 'border-[#38bdf8]/50 bg-[#0ea5e9]/10'
                          : 'border-[#2a2f4a] bg-gradient-to-br from-[#1a1f3a] to-[#151a3a] hover:border-[#22c55e]/40'
                    }`}
                  >
                    <div className="mb-1 flex items-center gap-3">
                      <span className={`inline-flex h-6 w-6 items-center justify-center rounded-full border text-xs font-mono font-bold ${
                        completed
                          ? 'border-[#22c55e] bg-[#22c55e]/20 text-[#86efac]'
                          : 'border-[#64748b] text-[#cbd5e1]'
                      }`}>
                        {completed ? '✓' : step.id}
                      </span>
                      <p className="text-sm font-bold text-[#e5e7eb] font-mono">{step.title}</p>
                    </div>
                    <p className="pl-9 text-xs text-[#9ca3af] font-mono">{step.description}</p>
                  </button>
                )
              })}

              <div className="mt-4 rounded-lg border border-[#2a2f4a] bg-[#1a1f3a] p-4">
                <p className="text-xs font-mono text-[#9ca3af]">
                  Astuce: cliquez les étapes dans l’ordre, puis allez sur l’onglet "→ Lancer" pour exécuter avec les paramètres préremplis.
                </p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Jobs Tab */}
      {activeTab === 'jobs' && (
        <div className="card">
          <h3 className="text-lg font-bold text-[#22c55e] mb-4 font-mono">◇ Travaux de Craquage Actifs</h3>
          {crackingJobs.length === 0 ? (
            <div className="text-center py-8 px-4">
              <p className="text-[#6b7280] mb-4 font-mono">Aucun travail en cours</p>
              <button 
                onClick={() => setActiveTab('start')}
                className="px-4 py-2 bg-gradient-to-r from-[#22c55e] to-[#16a34a] text-white rounded font-mono font-semibold hover:from-[#4ade80] hover:to-[#22c55e]"
              >
                Lancer un craquage
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {crackingJobs.map(job => {
                const statusConfig = getStatusBadge(job.status)
                return (
                  <div key={job.job_id} className="border border-[#e5e7eb] rounded-lg p-4 bg-gradient-to-br from-white to-[#f9fafb]">
                    {/* Header */}
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h4 className="text-[#1f2937] font-mono font-bold">{job.network_ssid}</h4>
                        <p className="text-[#6b7280] text-sm font-mono">{job.network_bssid}</p>
                      </div>
                      <span className={`px-3 py-1 rounded text-xs font-mono font-bold uppercase tracking-wider ${statusConfig.bg} ${statusConfig.border} border ${statusConfig.text}`}>
                        {statusConfig.icon} {job.status}
                      </span>
                    </div>

                    {/* Method and Wordlist */}
                    <div className="grid grid-cols-2 gap-4 mb-3 text-sm">
                      <div>
                        <p className="text-[#9ca3af] font-mono text-xs uppercase">Méthode</p>
                        <p className="text-[#33cc00] font-mono">{job.method}</p>
                      </div>
                      <div>
                        <p className="text-[#9ca3af] font-mono text-xs uppercase">Dictionnaire</p>
                        <p className="text-[#33cc00] font-mono">{job.wordlist}</p>
                      </div>
                    </div>

                    {/* Progress Bar */}
                    <div className="mb-3">
                      <div className="flex justify-between text-xs text-[#9ca3af] mb-1 font-mono">
                        <span>Progression</span>
                        <span>{job.progress}%</span>
                      </div>
                      <div className="w-full h-2 bg-[#0a0e27]/50 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-[#33cc00] to-[#4dff00] transition-all"
                          style={{ width: `${job.progress}%` }}
                        />
                      </div>
                    </div>

                    {/* Password Found */}
                    {job.password_found && (
                      <div className="bg-[#10b981]/20 border border-[#10b981]/40 rounded p-3 mb-3">
                        <p className="text-xs text-[#10b981] font-mono font-bold mb-1">★ MOT DE PASSE TROUVÉ!</p>
                        <p className="text-[#34d399] font-mono font-bold text-sm">{job.password_found}</p>
                      </div>
                    )}

                    {/* Error */}
                    {job.error_message && (
                      <div className="bg-[#ef4444]/20 border border-[#ef4444]/40 rounded p-3 mb-3">
                        <p className="text-xs text-[#fca5a5] font-mono">⚠ {job.error_message}</p>
                      </div>
                    )}

                    {/* Stats */}
                    <div className="flex justify-between text-xs text-[#9ca3af] font-mono mb-3">
                      <span>Tentatives: {job.attempts || 0}</span>
                      {job.start_time && <span>Démarré: {new Date(job.start_time).toLocaleTimeString('fr-FR')}</span>}
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2">
                      {job.status === 'running' && (
                        <>
                          <button 
                            onClick={() => handlePauseJob(job.job_id)}
                            className="px-3 py-1 bg-[#f59e0b]/20 text-[#fbbf24] rounded text-xs font-mono font-bold hover:bg-[#f59e0b]/30 border border-[#f59e0b]/40"
                          >
                            ⏸ Pause
                          </button>
                          <button 
                            onClick={() => handleCancelJob(job.job_id)}
                            className="px-3 py-1 bg-[#ef4444]/20 text-[#fca5a5] rounded text-xs font-mono font-bold hover:bg-[#ef4444]/30 border border-[#ef4444]/40"
                          >
                            ⊗ Annuler
                          </button>
                        </>
                      )}
                      {job.status === 'paused' && (
                        <button 
                          onClick={() => handleCancelJob(job.job_id)}
                          className="px-3 py-1 bg-[#ef4444]/20 text-[#fca5a5] rounded text-xs font-mono font-bold hover:bg-[#ef4444]/30 border border-[#ef4444]/40"
                        >
                        ⊗ Annuler
                        </button>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}

      {/* Strategies Tab */}
      {activeTab === 'strategies' && (
        <div className="card">
          <h3 className="text-lg font-bold text-[#33cc00] mb-4 font-mono">▦ Stratégies de Craquage</h3>
          {!selectedNetwork ? (
            <div className="text-center py-8 px-4">
              <p className="text-[#9ca3af] font-mono">Sélectionnez un réseau pour voir les stratégies</p>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Network Info */}
              <div className="bg-gradient-to-br from-[#1a1f3a] to-[#151a3a] rounded-lg p-4 border border-[#2a2f4a] border-l-4 border-l-[#33cc00]">
                <h4 className="text-[#e5e7eb] font-mono font-bold mb-2">{selectedNetwork.ssid}</h4>
                <div className="grid grid-cols-2 gap-2 text-xs text-[#9ca3af] font-mono">
                  <p><span className="text-[#33cc00]">BSSID:</span> {selectedNetwork.bssid}</p>
                  <p><span className="text-[#33cc00]">Sécurité:</span> {selectedNetwork.security}</p>
                  <p><span className="text-[#33cc00]">Risque:</span> {getSecurityLevel()}</p>
                </div>
              </div>

              {/* Strategy Details */}
              {strategy ? (
                <div className="space-y-3">
                  <div className="bg-gradient-to-br from-[#1a1f3a] to-[#151a3a] rounded-lg p-4 border border-[#2a2f4a]">
                    <p className="text-xs font-bold text-[#9ca3af] mb-2 uppercase tracking-wider">Faisabilité</p>
                    <span className={`text-sm font-bold font-mono ${strategy.viable ? 'text-[#10b981]' : 'text-[#ef4444]'}`}>
                      {strategy.viable ? '✓ CRAQUABLE' : '✕ NON RECOMMANDÉ'}
                    </span>
                  </div>

                  {strategy.viable && (
                    <>
                      <div className="bg-gradient-to-br from-[#1a1f3a] to-[#151a3a] rounded-lg p-4 border border-[#2a2f4a]">
                        <p className="text-xs font-bold text-[#9ca3af] mb-2 uppercase tracking-wider">Méthode</p>
                        <p className="text-[#e5e7eb] font-mono">{strategy.method}</p>
                      </div>

                      {strategy.difficulty && (
                        <div className="bg-gradient-to-br from-[#1a1f3a] to-[#151a3a] rounded-lg p-4 border border-[#2a2f4a]">
                          <p className="text-xs font-bold text-[#9ca3af] mb-2 uppercase tracking-wider">Difficulté</p>
                          <p className="text-[#e5e7eb] font-mono">{strategy.difficulty}</p>
                        </div>
                      )}

                      {strategy.estimated_time && (
                        <div className="bg-gradient-to-br from-[#1a1f3a] to-[#151a3a] rounded-lg p-4 border border-[#2a2f4a]">
                          <p className="text-xs font-bold text-[#9ca3af] mb-2 uppercase tracking-wider">Temps Estimé</p>
                          <p className="text-[#e5e7eb] font-mono">{strategy.estimated_time}</p>
                        </div>
                      )}

                      {strategy.attack_flow && (
                        <div className="bg-gradient-to-br from-[#1a1f3a] to-[#151a3a] rounded-lg p-4 border border-[#2a2f4a]">
                          <p className="text-xs font-bold text-[#33cc00] mb-3 uppercase tracking-wider">Flux d'Attaque</p>
                          <ol className="text-sm text-[#9ca3af] space-y-2 font-mono">
                            {strategy.attack_flow.map((step, i) => (
                              <li key={i} className="flex gap-2">
                                <span className="text-[#33cc00] font-bold">{i + 1}.</span>{step}
                              </li>
                            ))}
                          </ol>
                        </div>
                      )}
                    </>
                  )}

                  {strategy.reason && (
                    <div className="bg-[#f59e0b]/10 border border-[#f59e0b]/30 rounded-lg p-4">
                      <p className="text-xs font-bold text-[#fbbf24] mb-2 uppercase">Raison</p>
                      <p className="text-sm text-[#9ca3af] font-mono">{strategy.reason}</p>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-[#9ca3af] text-center py-4 font-mono">Chargement de la stratégie...</p>
              )}
            </div>
          )}
        </div>
      )}

      {/* Stored Handshakes Tab */}
      {activeTab === 'stored' && (
        <StoredHandshakesPanel 
          selectedNetwork={selectedNetwork}
          onSelectHandshake={(handshake) => {
            setSelectedStoredHandshake(handshake)
            setActiveTab('start')
          }}
        />
      )}

      {/* Start Cracking Tab */}
      {activeTab === 'start' && (
        <div className="card">
          <h3 className="text-lg font-bold text-[#33cc00] mb-4 font-mono">→ Lancer un Craquage</h3>
          {!selectedNetwork ? (
            <div className="text-center py-8 px-4">
              <p className="text-[#9ca3af] font-mono">Veuillez d'abord sélectionner un réseau</p>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Network Target */}
              <div className="bg-gradient-to-br from-[#1a1f3a] to-[#151a3a] rounded-lg p-4 border border-[#2a2f4a] border-l-4 border-l-[#33cc00]">
                <p className="text-xs text-[#9ca3af] font-mono uppercase mb-2">Cible</p>
                <h4 className="text-[#e5e7eb] font-mono font-bold">{selectedNetwork.ssid}</h4>
                <p className="text-sm text-[#9ca3af] font-mono">{selectedNetwork.bssid}</p>
              </div>

              {/* Stored Handshake Selection */}
              {selectedStoredHandshake && (
                <div className="bg-gradient-to-br from-[#1a3a2a] to-[#0f2a1a] rounded-lg p-4 border border-[#2a5a3a] border-l-4 border-l-[#10b981]">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-xs text-[#10b981] font-mono uppercase mb-2">💾 Capture stockée sélectionnée</p>
                      <p className="text-[#e5e7eb] font-mono font-bold">{selectedStoredHandshake.ssid}</p>
                      <p className="text-xs text-[#9ca3af] font-mono mt-1">
                        Format: {selectedStoredHandshake.file_format} | 
                        Taille: {(selectedStoredHandshake.file_size / 1024).toFixed(2)} KB
                      </p>
                      {selectedStoredHandshake.deauth_sent && (
                        <p className="text-xs text-[#10b981] font-mono mt-1">✓ Déauthentification effectuée</p>
                      )}
                    </div>
                    <button
                      onClick={() => setSelectedStoredHandshake(null)}
                      className="px-2 py-1 text-xs rounded border border-[#ef4444] text-[#ef4444] hover:bg-[#ef4444]/10 font-mono font-bold transition"
                    >
                      ✕ Effacer
                    </button>
                  </div>
                </div>
              )}

              {/* Workflow Quick Steps */}
              <div className="rounded-lg border border-[#2a2f4a] bg-[#151a3a] p-4">
                <div className="mb-3 flex items-center justify-between">
                  <p className="text-xs font-bold text-[#33cc00] font-mono uppercase">Étapes du workflow</p>
                  <button
                    type="button"
                    onClick={() => setActiveTab('workflow')}
                    className="rounded border border-[#22c55e]/40 bg-[#22c55e]/10 px-2 py-1 text-[11px] font-mono font-bold text-[#86efac] hover:bg-[#22c55e]/20"
                  >
                    Ouvrir workflow
                  </button>
                </div>
                <div className="space-y-2">
                  {WORKFLOW_STEPS.map((step) => {
                    const completed = completedSteps.includes(step.id)
                    return (
                      <button
                        key={`quick-${step.id}`}
                        type="button"
                        onClick={() => toggleStepCompletion(step.id)}
                        className={`flex w-full items-center gap-2 rounded border px-3 py-2 text-left text-xs font-mono transition ${
                          completed
                            ? 'border-[#22c55e]/40 bg-[#22c55e]/10 text-[#86efac]'
                            : 'border-[#334155] bg-[#0f172a]/40 text-[#cbd5e1] hover:border-[#22c55e]/40'
                        }`}
                      >
                        <span className="inline-flex h-5 w-5 items-center justify-center rounded-full border border-current text-[10px] font-bold">
                          {completed ? '✓' : step.id}
                        </span>
                        <span>{step.title}</span>
                      </button>
                    )
                  })}
                </div>
              </div>

              {/* Method Selection */}
              <div>
                <label className="block text-sm font-bold text-[#33cc00] mb-2 font-mono uppercase">Méthode</label>
                <select 
                  value={selectedMethod}
                  onChange={(e) => setSelectedMethod(e.target.value)}
                  className="w-full px-4 py-2 bg-[#151a3a] border border-[#2a2f4a] rounded text-[#e5e7eb] font-mono text-sm focus:border-[#33cc00] focus:outline-none"
                >
                  {methods.map(method => (
                    <option key={method.id} value={method.id} disabled={!method.available}>
                      {method.name} {!method.available && '(Indisponible)'}
                    </option>
                  ))}
                </select>
                {methods.find(m => m.id === selectedMethod)?.description && (
                  <p className="text-xs text-[#9ca3af] mt-1 font-mono">{methods.find(m => m.id === selectedMethod).description}</p>
                )}
              </div>

              {/* Wordlist Selection */}
              <div>
                <label className="block text-sm font-bold text-[#33cc00] mb-2 font-mono uppercase">Dictionnaire</label>
                <select 
                  value={selectedWordlist}
                  onChange={(e) => setSelectedWordlist(e.target.value)}
                  className="w-full px-4 py-2 bg-[#151a3a] border border-[#2a2f4a] rounded text-[#e5e7eb] font-mono text-sm focus:border-[#33cc00] focus:outline-none"
                >
                  {wordlists.map(wl => (
                    <option key={wl.id} value={wl.id}>
                      {wl.description} ({(wl.size || 0).toLocaleString()} mots)
                    </option>
                  ))}
                </select>
              </div>

              {/* GPU Toggle */}
              <div className="flex items-center gap-3 p-3 bg-[#1a1f3a] border border-[#2a2f4a] rounded">
                <input 
                  type="checkbox"
                  id="gpu"
                  checked={gpuEnabled}
                  onChange={(e) => setGpuEnabled(e.target.checked)}
                  className="w-4 h-4"
                />
                <label htmlFor="gpu" className="text-sm text-[#e5e7eb] font-mono cursor-pointer select-none">
                  Accélération GPU (si disponible)
                </label>
              </div>

              {/* Error Display */}
              {error && (
                <div className="bg-[#ef4444]/15 border border-[#ef4444]/40 rounded p-4">
                  <p className="text-sm text-[#fca5a5] font-mono">⚠ {error}</p>
                </div>
              )}

              {/* Start Button */}
              <button 
                onClick={startCrackingJob}
                disabled={loading || !selectedNetwork}
                className={`w-full py-3 rounded font-mono font-bold text-sm transition-all ${
                  loading || !selectedNetwork
                    ? 'bg-[#2a2f4a] text-[#9ca3af] cursor-not-allowed'
                    : 'bg-gradient-to-r from-[#33cc00] to-[#28a300] text-[#0a0e27] hover:from-[#4dff00] hover:to-[#33cc00] shadow-lg hover:shadow-[0_0_20px_rgba(51,204,0,0.3)]'
                }`}
              >
                {loading ? '◌ Lancement...' : '→ Lancer le Craquage'}
              </button>

              {/* Platform Info */}
              {crackingStatus && (
                <div className="text-xs text-[#9ca3af] font-mono text-center p-3 bg-[#1a1f3a] border border-[#2a2f4a] rounded">
                  <p>Plateforme: {crackingStatus.platform} | Mode: {crackingStatus.note}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default CrackingPanel
