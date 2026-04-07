import React, { useState, useEffect } from 'react'
import { wifiAPI } from '../api'
import NetworkTable from './NetworkTable'
import VulnerabilityPanel from './VulnerabilityPanel'
import RecommendationPanel from './RecommendationPanel'
import CommandPanel from './CommandPanel'
import CrackingPanel from './CrackingPanel'
import Header from './Header'

export function Dashboard() {
  const [scanInProgress, setScanInProgress] = useState(false)
  const [networks, setNetworks] = useState([])
  const [vulnerabilities, setVulnerabilities] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [selectedNetwork, setSelectedNetwork] = useState(null)
  const [scanStats, setScanStats] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')
  const [reportMode, setReportMode] = useState(false)
  const [toast, setToast] = useState(null)
  const [analyzing, setAnalyzing] = useState(false)

  // Effectuer un scan réel au démarrage
  useEffect(() => {
    performRealScan()
  }, [])

  const performRealScan = async () => {
    setScanInProgress(true)
    showToast('◆ Démarrage du scan Wi-Fi...', 'info')
    try {
      console.log('◆ Démarrage d\'un scan Wi-Fi réel...')
      const response = await wifiAPI.scanNetworks(15, 'Real Scan')
      
      if (response.data.networks && response.data.networks.length > 0) {
        console.log(`✓ ${response.data.networks.length} réseaux détectés`)
        setNetworks(response.data.networks)
        showToast(`✓ ${response.data.networks.length} réseaux détectés`, 'success')
        
        // Analyser automatiquement les réseaux détectés
        await analyzeNetworks(response.data.networks)
      } else {
        console.warn('⚠ Aucun réseau détecté lors du scan')
        showToast('⚠ Aucun réseau détecté', 'warning')
        setNetworks([])
      }
      
      // Show scan mode
      const scanMode = response.data.mode || 'simulation'
      if (scanMode === 'simulation_fallback') {
        showToast('ⓘ Scan en mode simulation (fallback)', 'warning')
      }
      
      setScanStats({
        total: response.data.networks_found || 0,
        timestamp: new Date().toLocaleTimeString('fr-FR')
      })
    } catch (error) {
      console.error('✗ Erreur lors du scan réel:', error)
      showToast('✗ Erreur lors du scan: ' + (error.response?.data?.detail || error.message), 'error')
      setNetworks([])
    } finally {
      setScanInProgress(false)
    }
  }

  const handleScan = async () => {
    setScanInProgress(true)
    showToast('◆ Démarrage d\'un scan...', 'info')
    try {
      const response = await wifiAPI.scanNetworks(10, 'Security Audit')
      setNetworks(response.data.networks || [])
      setScanStats({
        total: response.data.networks_found,
        timestamp: new Date().toLocaleTimeString('fr-FR')
      })
      showToast(`✓ ${response.data.networks_found} réseaux trouvés`, 'success')
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
      showToast('◆ Analyse en cours...', 'info')
      const result = await wifiAPI.analyzeBatch(nets)
      setVulnerabilities(result.data.vulnerabilities || [])
      
      // Générer les recommandations
      const recsResponse = await wifiAPI.generateRecommendations(
        result.data.vulnerabilities,
        nets
      )
      setRecommendations(recsResponse.data || [])
      showToast('✓ Analyse completée', 'success')
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
      showToast('✓ Rapport PDF téléchargé', 'success')
    } catch (error) {
      console.error('Erreur PDF:', error)
      showToast('✗ Erreur lors de la génération du PDF', 'error')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-gray-50 to-gray-100">
      <Header />

      {/* Toast Notification */}
      {toast && (
        <div className={`fixed top-4 right-4 p-4 rounded-lg font-mono font-semibold text-sm z-50 animate-pulse ${
          toast.type === 'success' ? 'bg-[#10b981]/10 border border-[#10b981]/40 text-[#059669]' :
          toast.type === 'error' ? 'bg-[#ef4444]/10 border border-[#ef4444]/40 text-[#dc2626]' :
          toast.type === 'warning' ? 'bg-[#f59e0b]/10 border border-[#f59e0b]/40 text-[#d97706]' :
          'bg-[#3b82f6]/10 border border-[#3b82f6]/40 text-[#1d4ed8]'
        }`}>
          {toast.message}
        </div>
      )}

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Dashboard Summary - Green Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="card border-l-4 border-l-[#22c55e] hover:border-l-[#4ade80]">
            <p className="text-[#6b7280] text-sm font-mono uppercase tracking-wide">Réseaux Détectés</p>
            <p className="text-4xl font-bold text-[#22c55e] mt-2">{networks.length}</p>
            <div className="w-full h-1 bg-[#e5e7eb] rounded-full mt-3 overflow-hidden">
              <div className="h-full bg-gradient-to-r from-[#22c55e] to-[#4ade80]" style={{width: `${(networks.length / 20) * 100}%`}}></div>
            </div>
          </div>
          
          <div className="card border-l-4 border-l-[#ef4444] hover:border-l-[#f87171]">
            <p className="text-[#6b7280] text-sm font-mono uppercase tracking-wide">Vulnérabilités</p>
            <p className="text-4xl font-bold text-[#ef4444] mt-2">{vulnerabilities.length}</p>
            <div className="w-full h-1 bg-[#e5e7eb] rounded-full mt-3 overflow-hidden">
              <div className="h-full bg-gradient-to-r from-[#ef4444] to-[#f87171]" style={{width: `${(vulnerabilities.length / 50) * 100}%`}}></div>
            </div>
          </div>
          
          <div className="card border-l-4 border-l-[#f59e0b] hover:border-l-[#fbbf24]">
            <p className="text-[#6b7280] text-sm font-mono uppercase tracking-wide">Recommandations</p>
            <p className="text-4xl font-bold text-[#f59e0b] mt-2">{recommendations.length}</p>
            <div className="w-full h-1 bg-[#e5e7eb] rounded-full mt-3 overflow-hidden">
              <div className="h-full bg-gradient-to-r from-[#f59e0b] to-[#fbbf24]" style={{width: `${(recommendations.length / 30) * 100}%`}}></div>
            </div>
          </div>
          
          <div className={`card border-l-4 ${getRiskScore() > 70 ? 'border-l-[#ef4444]' : 'border-l-[#f59e0b]'}`}>
            <p className="text-[#6b7280] text-sm font-mono uppercase tracking-wide">Score de Risque</p>
            <p className={`text-4xl font-bold mt-2 ${getRiskScore() > 70 ? 'text-[#ef4444]' : 'text-[#f59e0b]'}`}>
              {getRiskScore().toFixed(0)}<span className="text-xl">/100</span>
            </p>
            <div className="w-full h-1 bg-[#e5e7eb] rounded-full mt-3 overflow-hidden">
              <div className={`h-full ${getRiskScore() > 70 ? 'bg-[#ef4444]' : 'bg-[#f59e0b]'}`} style={{width: `${getRiskScore()}%`}}></div>
            </div>
          </div>
        </div>

        {/* Tabs - Light Theme Style */}
        <div className="mb-6">
          <div className="flex gap-1 border-b border-[#e5e7eb] overflow-x-auto pb-0">
            {['overview', 'vulnerabilities', 'recommendations', 'cracking', 'commands', 'report'].map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-4 font-mono text-sm font-semibold transition-all whitespace-nowrap border-b-2 ${
                  activeTab === tab
                    ? 'text-[#22c55e] border-[#22c55e] bg-[#22c55e]/5'
                    : 'text-[#6b7280] border-transparent hover:text-[#1f2937] hover:border-[#22c55e]/30'
                }`}
              >
                {tab === 'overview' && '◘ Vue d\'ensemble'}
                {tab === 'vulnerabilities' && '◆ Vulnérabilités'}
                {tab === 'recommendations' && '◗ Recommandations'}
                {tab === 'cracking' && '◇ Craquage'}
                {tab === 'commands' && '⚙ Commandes'}
                {tab === 'report' && '▦ Rapport'}
              </button>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="space-y-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <>
              <div className="flex gap-4">
                <button
                  onClick={handleScan}
                  disabled={scanInProgress || analyzing}
                  className={`px-6 py-3 rounded-lg font-mono font-bold transition-all flex items-center gap-2 ${
                    scanInProgress || analyzing
                      ? 'bg-[#e5e7eb] text-[#9ca3af] cursor-not-allowed'
                      : 'bg-gradient-to-r from-[#22c55e] to-[#16a34a] text-white hover:from-[#4ade80] hover:to-[#22c55e] shadow-lg hover:shadow-[0_0_20px_rgba(34,197,94,0.3)]'
                  }`}
                >
                  {scanInProgress ? '◌ Scan en cours...' : analyzing ? '◆ Analyse en cours...' : '◆ Démarrer un Scan'}
                </button>
              </div>

              {analyzing && (
                <div className="card bg-gradient-to-br from-[#dcfce7]/40 to-[#f0fdf4]/40 border border-[#22c55e]/30">
                  <div className="flex items-center gap-4 p-4">
                    <div className="animate-spin">⚙</div>
                    <div>
                      <p className="text-[#22c55e] font-bold font-mono">Analyse en cours...</p>
                      <p className="text-[#6b7280] text-sm font-mono">Vulnérabilités et recommandations</p>
                    </div>
                  </div>
                </div>
              )}

              <NetworkTable networks={networks} onSelectNetwork={handleSelectNetwork} />
            </>
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
            <CrackingPanel selectedNetwork={selectedNetwork} vulnerabilities={vulnerabilities} />
          )}

          {/* Commands Tab */}
          {activeTab === 'commands' && (
            <CommandPanel />
          )}

          {/* Report Tab */}
          {activeTab === 'report' && (
            <div className="card">
              <h2 className="text-2xl font-bold mb-6 text-[#22c55e] font-mono">⬜ Générer un Rapport</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                  onClick={generatePDF}
                  disabled={networks.length === 0}
                  className={`p-6 rounded-lg transition-all border border-[#e5e7eb] hover:border-[#22c55e] ${
                    networks.length === 0 
                      ? 'bg-[#f3f4f6] text-[#9ca3af] cursor-not-allowed' 
                      : 'bg-white hover:bg-[#f9fafb] text-[#1f2937]'
                  }`}
                >
                  <p className="text-3xl mb-2">✑</p>
                  <p className="font-semibold font-mono">Générer PDF</p>
                  <p className="text-xs text-[#6b7280] mt-2">Rapport professionnel complet</p>
                </button>

                <button
                  className="p-6 bg-white hover:bg-[#f9fafb] rounded-lg transition-all text-center border border-[#e5e7eb] hover:border-[#22c55e]"
                  onClick={() => {
                    const report = {
                      networks,
                      vulnerabilities,
                      recommendations,
                      timestamp: new Date().toISOString()
                    }
                    const link = document.createElement('a')
                    link.href = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)]))
                    link.download = `netshield_report_${Date.now()}.json`
                    link.click()
                  }}
                >
                  <p className="text-3xl mb-2">↑</p>
                  <p className="font-semibold font-mono text-[#1f2937]">Exporter JSON</p>
                  <p className="text-xs text-[#6b7280] mt-2">Données structurées</p>
                </button>

                <button
                  className="p-6 bg-white hover:bg-[#f9fafb] rounded-lg transition-all text-center border border-[#e5e7eb] hover:border-[#22c55e]"
                >
                  <p className="text-3xl mb-2">⬜</p>
                  <p className="font-semibold font-mono text-[#1f2937]">Aperçu Rapport</p>
                  <p className="text-xs text-[#6b7280] mt-2">Vérifier avant génération</p>
                </button>
              </div>

              {/* Rapport Summary */}
              <div className="mt-8 p-6 bg-gradient-to-br from-white to-[#f9fafb] rounded-lg border border-[#e5e7eb] border-l-4 border-l-[#22c55e]">
                <h3 className="text-lg font-bold text-[#22c55e] mb-4 font-mono">⬜ Résumé du Rapport</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <p className="text-[#9ca3af] font-mono text-xs uppercase">Total Réseaux</p>
                    <p className="text-2xl font-bold text-[#33cc00]">{networks.length}</p>
                  </div>
                  <div>
                    <p className="text-[#9ca3af] font-mono text-xs uppercase">Vulnérabilités</p>
                    <p className="text-2xl font-bold text-[#ef4444]">{vulnerabilities.length}</p>
                  </div>
                  <div>
                    <p className="text-[#9ca3af] font-mono text-xs uppercase">Critiques</p>
                    <p className="text-2xl font-bold text-[#f87171]">
                      {vulnerabilities.filter(v => v.severity === 'Critique').length}
                    </p>
                  </div>
                  <div>
                    <p className="text-[#9ca3af] font-mono text-xs uppercase">Recommandations</p>
                    <p className="text-2xl font-bold text-[#f59e0b]">{recommendations.length}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default Dashboard
