import React, { useState, useEffect, useRef } from 'react'
import { MdWifi, MdWarning, MdLightbulb, MdDashboard } from 'react-icons/md'
import { wifiAPI, kismetAPI } from '../api'
import NetworkTable from './NetworkTable'
import VulnerabilityPanel from './VulnerabilityPanel'
import RecommendationPanel from './RecommendationPanel'
import CommandPanel from './CommandPanel'
import CrackingPanel from './CrackingPanel'
import KismetPanel from './KismetPanel'
import HandshakeCapturePanel from './HandshakeCapturePanel'
import { NavBar } from './NavBar'
import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { Progress } from './ui/progress'

export function Dashboard() {
  const [scanInProgress, setScanInProgress] = useState(false)
  const [networks, setNetworks] = useState([])
  const [vulnerabilities, setVulnerabilities] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [selectedNetwork, setSelectedNetwork] = useState(null)
  const [scanStats, setScanStats] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')
  const [scanSource, setScanSource] = useState('standard')
  const [kismetUrl, setKismetUrl] = useState('http://localhost:2501')
  const [kismetStatus, setKismetStatus] = useState(null)
  const [kismetNetworks, setKismetNetworks] = useState([])
  const [kismetDevices, setKismetDevices] = useState([])
  const [kismetAlerts, setKismetAlerts] = useState([])
  const [kismetLoading, setKismetLoading] = useState(false)
  const [kismetError, setKismetError] = useState(null)
  const [reportMode, setReportMode] = useState(false)
  const [toast, setToast] = useState(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [selectedCapture, setSelectedCapture] = useState(null)
  const hasInitialized = useRef(false)
  const logoSrc = '/logo-netshield.png'

  // Handle capture selection for cracking
  const handleCaptureForCracking = (capture) => {
    setSelectedCapture(capture)
    setSelectedNetwork({
      ssid: capture.network_ssid,
      bssid: capture.network_bssid,
      security: 'WPA2' // Default, can be enhanced with capture metadata
    })
    setActiveTab('cracking')
    showToast(`Handshake de "${capture.network_ssid}" prêt pour le cracking`, 'success')
  }

  // Effectuer un scan réel au démarrage
  useEffect(() => {
    if (hasInitialized.current) {
      return
    }

    hasInitialized.current = true
    performRealScan()
  }, [])

  useEffect(() => {
    if (scanSource === 'kismet') {
      refreshKismetData()
    }
  }, [scanSource, kismetUrl])

  useEffect(() => {
    if (activeTab === 'kismet') {
      refreshKismetData()
    }
  }, [activeTab])

  const refreshKismetData = async () => {
    setKismetLoading(true)
    setKismetError(null)

    try {
      // Vérifier d'abord le statut; si offline, éviter les appels secondaires bruyants.
      const statusRes = await kismetAPI.getStatus(kismetUrl)
      setKismetStatus(statusRes.data)

      const [networksRes, devicesRes, alertsRes] = await Promise.all([
        kismetAPI.getNetworks(kismetUrl),
        kismetAPI.getDevices(kismetUrl),
        kismetAPI.getAlerts(kismetUrl)
      ])

      const networksPayload = networksRes.data
      const resolvedNetworks = networksPayload.networks || networksPayload.results || []
      setKismetNetworks(resolvedNetworks)
      if (scanSource === 'kismet') {
        setNetworks(resolvedNetworks)
      }

      const devicesPayload = devicesRes.data
      setKismetDevices(devicesPayload.devices || devicesPayload.results || [])

      const alertsPayload = alertsRes.data
      setKismetAlerts(alertsPayload.alerts || alertsPayload.results || [])
    } catch (error) {
      setKismetStatus((prev) => ({ ...(prev || {}), status: 'offline' }))
      setKismetError(error.response?.data?.detail || error.message)
    } finally {
      setKismetLoading(false)
    }
  }

  const getUnifiedNetworks = () => {
    if (scanSource === 'kismet' && kismetNetworks.length > 0) {
      return kismetNetworks
    }

    return networks
  }

  const kismetBadgeVariant = kismetStatus?.status === 'online'
    ? 'success'
    : kismetStatus?.status === 'offline'
      ? 'destructive'
      : 'warning'

  const kismetBadgeLabel = scanSource === 'kismet'
    ? `Kismet ${kismetStatus?.status || 'pending'}`
    : kismetStatus?.status
      ? `Kismet ${kismetStatus.status}`
      : 'Kismet non vérifié'

  const performRealScan = async (source = scanSource) => {
    setScanInProgress(true)
    showToast('Démarrage du scan Wi-Fi...', 'info')
    try {
      console.log('Démarrage d\'un scan Wi-Fi réel...')
      const response = source === 'kismet'
        ? await kismetAPI.scanNetworks(20, kismetUrl, 'Advanced Kismet Scan')
        : await wifiAPI.scanNetworks(15, 'Real Scan')
      
      if (response.data.networks && response.data.networks.length > 0) {
        console.log(`${response.data.networks.length} réseaux détectés`)
        setNetworks(response.data.networks)
        showToast(`${response.data.networks.length} réseaux détectés`, 'success')
        
        // Analyser automatiquement les réseaux détectés
        await analyzeNetworks(response.data.networks)
      } else {
        console.warn('Aucun réseau détecté lors du scan')
        showToast('Aucun réseau détecté', 'warning')
        setNetworks([])
      }
      
      // Show scan mode
      const scanMode = response.data.mode || 'simulation'
      if (scanMode === 'simulation_fallback') {
        showToast('Scan en mode simulation (fallback)', 'warning')
      }
      
      setScanStats({
        total: response.data.networks_found || 0,
        timestamp: new Date().toLocaleTimeString('fr-FR')
      })
    } catch (error) {
      console.error('Erreur lors du scan réel:', error)
      showToast('Erreur lors du scan: ' + (error.response?.data?.detail || error.message), 'error')
      setNetworks([])
    } finally {
      setScanInProgress(false)
    }
  }

  const handleScan = async (source = scanSource) => {
    setScanInProgress(true)
    showToast(source === 'kismet' ? 'Démarrage d\'un scan Kismet...' : 'Démarrage d\'un scan...', 'info')
    try {
      const response = source === 'kismet'
        ? await kismetAPI.scanNetworks(20, kismetUrl, 'Security Audit Kismet')
        : await wifiAPI.scanNetworks(10, 'Security Audit')
      setNetworks(response.data.networks || [])
      setScanStats({
        total: response.data.networks_found,
        timestamp: new Date().toLocaleTimeString('fr-FR')
      })
      showToast(`${response.data.networks_found} réseaux trouvés`, 'success')
      // Analyser automatiquement
      await analyzeNetworks(response.data.networks)
    } catch (error) {
      console.error('Erreur lors du scan:', error)
      showToast('✗ Erreur lors du scan', 'error')
    } finally {
      setScanInProgress(false)
    }
  }

  const analyzeNetworks = async (nets) => {
    setAnalyzing(true)
    try {
      showToast('Analyse en cours...', 'info')
      const result = await wifiAPI.analyzeBatch(nets)
      setVulnerabilities(result.data.vulnerabilities || [])
      
      // Générer les recommandations
      const recsResponse = await wifiAPI.generateRecommendations(
        result.data.vulnerabilities,
        nets
      )
      setRecommendations(recsResponse.data || [])
      showToast('Analyse completée', 'success')
    } catch (error) {
      console.error('Erreur lors de l\'analyse:', error)
      showToast('✗ Erreur lors de l\'analyse', 'error')
    } finally {
      setAnalyzing(false)
    }
  }

  const showToast = (message, type = 'info') => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  const handleSelectNetwork = async (network) => {
    setSelectedNetwork(network)
    setActiveTab('cracking')
  }

  const getRiskScore = () => {
    if (vulnerabilities.length === 0) return 10
    const critical = vulnerabilities.filter(v => v.severity === 'Critique').length
    const high = vulnerabilities.filter(v => v.severity === 'Élevée').length
    return Math.min(100, (critical * 25 + high * 10 + vulnerabilities.length * 2))
  }

  const generatePDF = async () => {
    try {
      showToast('▦ Génération du rapport PDF...', 'info')
      const report = {
        report_title: 'Audit Sécurité Wi-Fi - NetShield',
        project_name: 'Audit Complet',
        author: 'Administrateur',
        total_networks: networks.length,
        vulnerabilities: vulnerabilities.slice(0, 10),
        recommendations: recommendations.slice(0, 10),
        critical_vulnerabilities: vulnerabilities.filter(v => v.severity === 'Critique').length,
        high_vulnerabilities: vulnerabilities.filter(v => v.severity === 'Élevée').length,
        medium_vulnerabilities: vulnerabilities.filter(v => v.severity === 'Moyen').length,
        low_vulnerabilities: vulnerabilities.filter(v => v.severity === 'Faible').length,
        executive_summary: 'Audit de sécurité Wi-Fi complet réalisé en mode simulation/laboratoire.',
        risk_assessment: getRiskScore() > 70 ? 'Risque ÉLEVÉ' : 'Risque MODÉRÉ',
        overall_risk_score: getRiskScore(),
        methodology: 'Scan passif avec simulation d\'attaques',
        testing_period: new Date().toLocaleDateString('fr-FR')
      }
      
      const response = await wifiAPI.generatePDF(report)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `netshield_report_${Date.now()}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      showToast('Rapport PDF téléchargé', 'success')
    } catch (error) {
      console.error('Erreur PDF:', error)
      showToast('✗ Erreur lors de la génération du PDF', 'error')
    }
  }

  return (
    <div className="min-h-screen">
      <NavBar activeTab={activeTab} onTabChange={setActiveTab} onScan={handleScan} scanInProgress={scanInProgress} />

      {toast && (
        <div className="fixed right-4 top-4 z-50 animate-fade-up">
          <Card className={`max-w-sm border-l-4 px-4 py-3 ${
            toast.type === 'success' ? 'border-l-emerald-500' :
            toast.type === 'error' ? 'border-l-rose-500' :
            toast.type === 'warning' ? 'border-l-amber-500' :
            'border-l-sky-500'
          }`}>
            <p className="text-sm font-medium text-slate-800">{toast.message}</p>
          </Card>
        </div>
      )}

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <Card className="mb-8 overflow-hidden border-slate-200 bg-white/90">
          <div className="grid gap-3 p-6 sm:grid-cols-2 lg:p-8 lg:grid-cols-4">
            <Card className="border-slate-200 bg-slate-50">
              <CardHeader className="pb-2">
                <div className="mb-2 flex items-center gap-2 rounded-lg bg-sky-100 px-3 py-1.5 w-fit">
                  <MdWifi className="text-base text-sky-700" />
                  <span className="text-xs font-semibold uppercase text-sky-700">Réseaux</span>
                </div>
                <CardDescription className="text-slate-600">Détectés</CardDescription>
                <CardTitle className="text-3xl text-slate-900">{getUnifiedNetworks().length}</CardTitle>
              </CardHeader>
              <CardContent className="pt-0"><Progress value={(getUnifiedNetworks().length / 20) * 100} /></CardContent>
            </Card>
            <Card className="border-slate-200 bg-slate-50">
              <CardHeader className="pb-2">
                <div className="mb-2 flex items-center gap-2 rounded-lg bg-rose-100 px-3 py-1.5 w-fit">
                  <MdWarning className="text-base text-rose-700" />
                  <span className="text-xs font-semibold uppercase text-rose-700">Vulnérabilités</span>
                </div>
                <CardDescription className="text-slate-600">Identifiées</CardDescription>
                <CardTitle className="text-3xl text-slate-900">{vulnerabilities.length}</CardTitle>
              </CardHeader>
              <CardContent className="pt-0"><Progress value={(vulnerabilities.length / 50) * 100} /></CardContent>
            </Card>
            <Card className="border-slate-200 bg-slate-50">
              <CardHeader className="pb-2">
                <div className="mb-2 flex items-center gap-2 rounded-lg bg-amber-100 px-3 py-1.5 w-fit">
                  <MdLightbulb className="text-base text-amber-700" />
                  <span className="text-xs font-semibold uppercase text-amber-700">Recommandations</span>
                </div>
                <CardDescription className="text-slate-600">À appliquer</CardDescription>
                <CardTitle className="text-3xl text-slate-900">{recommendations.length}</CardTitle>
              </CardHeader>
              <CardContent className="pt-0"><Progress value={(recommendations.length / 30) * 100} /></CardContent>
            </Card>
            <Card className="border-slate-200 bg-slate-50">
              <CardHeader className="pb-2">
                <div className="mb-2 flex items-center gap-2 rounded-lg bg-emerald-100 px-3 py-1.5 w-fit">
                  <MdDashboard className="text-base text-emerald-700" />
                  <span className="text-xs font-semibold uppercase text-emerald-700">Score</span>
                </div>
                <CardDescription className="text-slate-600">De risque</CardDescription>
                <CardTitle className={`text-3xl ${getRiskScore() > 70 ? 'text-rose-600' : 'text-amber-600'}`}>
                  {getRiskScore().toFixed(0)}<span className="text-base text-slate-500">/100</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-0"><Progress value={getRiskScore()} /></CardContent>
            </Card>
          </div>
        </Card>

        <div className="mx-auto max-w-7xl space-y-6 px-4 py-8 sm:px-6 lg:px-8">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <>
              {scanSource === 'kismet' && (
                <Card className="border-sky-200 bg-sky-50/70">
                  <CardContent className="flex flex-col gap-4 p-4 lg:flex-row lg:items-center lg:justify-between">
                    <div>
                      <p className="font-medium text-sky-800">Kismet activé</p>
                      <p className="text-sm text-sky-700">
                        {kismetStatus?.status === 'online'
                          ? 'Le daemon Kismet répond correctement.'
                          : 'Le frontend utilisera Kismet dès qu’il sera disponible sur l’URL configurée.'}
                      </p>
                    </div>
                    <Button variant="secondary" onClick={refreshKismetData} disabled={kismetLoading}>
                      {kismetLoading ? 'Actualisation…' : 'Actualiser Kismet'}
                    </Button>
                  </CardContent>
                </Card>
              )}

              {analyzing && (
                <Card className="border-emerald-200 bg-emerald-50/70">
                  <CardContent className="flex items-center gap-4 p-4">
                    <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
                    <div>
                      <p className="font-medium text-emerald-800">Analyse en cours…</p>
                      <p className="text-sm text-emerald-700">Vulnérabilités et recommandations</p>
                    </div>
                  </CardContent>
                </Card>
              )}

              <NetworkTable networks={getUnifiedNetworks()} onSelectNetwork={handleSelectNetwork} />
            </>
          )}

          {activeTab === 'kismet' && (
            <KismetPanel
              status={kismetStatus}
              networks={kismetNetworks}
              devices={kismetDevices}
              alerts={kismetAlerts}
              loading={kismetLoading}
              error={kismetError}
              kismetUrl={kismetUrl}
              onRefresh={refreshKismetData}
              onScan={async () => {
                setScanSource('kismet')
                await handleScan('kismet')
                await refreshKismetData()
              }}
              onChangeUrl={setKismetUrl}
            />
          )}

          {/* Handshake Capture Tab */}
          {activeTab === 'handshake' && (
            <HandshakeCapturePanel 
              networks={getUnifiedNetworks()} 
              onCaptureForCracking={handleCaptureForCracking}
            />
          )}

          {/* Vulnerabilities Tab */}
          {activeTab === 'vulnerabilities' && (
            <VulnerabilityPanel vulnerabilities={vulnerabilities} />
          )}

          {/* Recommendations Tab */}
          {activeTab === 'recommendations' && (
            <RecommendationPanel recommendations={recommendations} />
          )}

          {/* Cracking Tab */}
          {activeTab === 'cracking' && (
            <CrackingPanel 
              selectedNetwork={selectedNetwork} 
              vulnerabilities={vulnerabilities}
              selectedCapture={selectedCapture}
            />
          )}

          {/* Commands Tab */}
          {activeTab === 'commands' && (
            <CommandPanel networks={getUnifiedNetworks()} />
          )}

          {/* Report Tab */}
          {activeTab === 'report' && (
            <Card>
              <CardHeader>
                <CardTitle>Rapport d’audit</CardTitle>
                <CardDescription>Exportez les résultats et les recommandations dans un format exploitable.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid gap-4 md:grid-cols-3">
                  <Button onClick={generatePDF} disabled={networks.length === 0}>Générer PDF</Button>
                  <Button
                    variant="secondary"
                    onClick={() => {
                      const report = { networks, vulnerabilities, recommendations, timestamp: new Date().toISOString() }
                      const link = document.createElement('a')
                      link.href = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)]))
                      link.download = `netshield_report_${Date.now()}.json`
                      link.click()
                    }}
                  >
                    Exporter JSON
                  </Button>
                  <Button variant="outline" disabled>Aperçu rapport</Button>
                </div>

                <div className="grid gap-4 md:grid-cols-4">
                  <Card className="bg-slate-50"><CardHeader className="pb-2"><CardDescription>Total réseaux</CardDescription><CardTitle>{networks.length}</CardTitle></CardHeader></Card>
                  <Card className="bg-slate-50"><CardHeader className="pb-2"><CardDescription>Vulnérabilités</CardDescription><CardTitle>{vulnerabilities.length}</CardTitle></CardHeader></Card>
                  <Card className="bg-slate-50"><CardHeader className="pb-2"><CardDescription>Critiques</CardDescription><CardTitle>{vulnerabilities.filter(v => v.severity === 'Critique').length}</CardTitle></CardHeader></Card>
                  <Card className="bg-slate-50"><CardHeader className="pb-2"><CardDescription>Recommandations</CardDescription><CardTitle>{recommendations.length}</CardTitle></CardHeader></Card>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </main>
    </div>
  )
}

export default Dashboard
