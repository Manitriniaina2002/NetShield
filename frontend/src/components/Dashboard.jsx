import React, { useState, useEffect } from 'react'
import { wifiAPI } from '../api'
import NetworkTable from './NetworkTable'
import VulnerabilityPanel from './VulnerabilityPanel'
import RecommendationPanel from './RecommendationPanel'
import CommandPanel from './CommandPanel'
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

  // Charger les données simulées au démarrage
  useEffect(() => {
    loadDemoData()
  }, [])

  const loadDemoData = async () => {
    try {
      // Utiliser les données simulées du backend
      const response = await wifiAPI.scanNetworks(5, 'Demo Scan')
      setNetworks(response.data.networks || [])
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error)
      // Charger manuellement las données de test
      setNetworks([
        {
          ssid: 'FreeFi_Public',
          bssid: 'AA:11:22:33:44:55',
          channel: 6, frequency: '2.4GHz', security: 'Open',
          signal_strength: -45, signal_percentage: 75, clients: 12
        },
        {
          ssid: 'CoffeShop_WiFi',
          bssid: 'BB:22:33:44:55:66',
          channel: 11, frequency: '2.4GHz', security: 'WEP',
          signal_strength: -55, signal_percentage: 65, clients: 8
        },
        {
          ssid: 'HomeNetwork',
          bssid: 'CC:33:44:55:66:77',
          channel: 1, frequency: '2.4GHz', security: 'WPA',
          signal_strength: -35, signal_percentage: 85, clients: 5
        },
        {
          ssid: 'SecureOffice',
          bssid: 'DD:44:55:66:77:88',
          channel: 48, frequency: '5GHz', security: 'WPA2',
          signal_strength: -50, signal_percentage: 70, clients: 15
        },
        {
          ssid: 'ModernHome',
          bssid: 'EE:55:66:77:88:99',
          channel: 36, frequency: '5GHz', security: 'WPA3',
          signal_strength: -40, signal_percentage: 80, clients: 3
        }
      ])
    }
  }

  const handleScan = async () => {
    setScanInProgress(true)
    try {
      const response = await wifiAPI.scanNetworks(10, 'Security Audit')
      setNetworks(response.data.networks || [])
      setScanStats({
        total: response.data.networks_found,
        critical: response.data.networks_found,
        timestamp: new Date().toLocaleTimeString()
      })
      // Analyser automatiquement
      await analyzeNetworks(response.data.networks)
    } catch (error) {
      console.error('Erreur lors du scan:', error)
    } finally {
      setScanInProgress(false)
    }
  }

  const analyzeNetworks = async (nets) => {
    try {
      const result = await wifiAPI.analyzeBatch(nets)
      setVulnerabilities(result.data.vulnerabilities || [])
      
      // Générer les recommandations
      const recsResponse = await wifiAPI.generateRecommendations(
        result.data.vulnerabilities,
        nets
      )
      setRecommendations(recsResponse.data || [])
    } catch (error) {
      console.error('Erreur lors de l\'analyse:', error)
    }
  }

  const handleSelectNetwork = async (network) => {
    setSelectedNetwork(network)
    setActiveTab('details')
  }

  const getRiskScore = () => {
    if (vulnerabilities.length === 0) return 10
    const critical = vulnerabilities.filter(v => v.severity === 'Critique').length
    const high = vulnerabilities.filter(v => v.severity === 'Élevée').length
    return Math.min(100, (critical * 25 + high * 10 + vulnerabilities.length * 2))
  }

  const generatePDF = async () => {
    try {
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
        testing_period: new Date().toLocaleDateString()
      }
      
      const response = await wifiAPI.generatePDF(report)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `netshield_report_${Date.now()}.pdf`)
      document.body.appendChild(link)
      link.click()
    } catch (error) {
      alert('Erreur lors de la génération du PDF')
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Dashboard Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="card">
            <p className="text-gray-400 text-sm">Réseaux Détectés</p>
            <p className="text-3xl font-bold text-blue-400">{networks.length}</p>
          </div>
          
          <div className="card">
            <p className="text-gray-400 text-sm">Vulnérabilités</p>
            <p className="text-3xl font-bold text-red-400">{vulnerabilities.length}</p>
          </div>
          
          <div className="card">
            <p className="text-gray-400 text-sm">Recommandations</p>
            <p className="text-3xl font-bold text-yellow-400">{recommendations.length}</p>
          </div>
          
          <div className="card">
            <p className="text-gray-400 text-sm">Score de Risque</p>
            <p className={`text-3xl font-bold ${getRiskScore() > 70 ? 'text-red-400' : 'text-yellow-400'}`}>
              {getRiskScore().toFixed(0)}/100
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-6 border-b border-gray-700">
          {['overview', 'vulnerabilities', 'recommendations', 'commands', 'report'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 font-semibold transition-colors border-b-2 ${
                activeTab === tab
                  ? 'text-blue-400 border-blue-400'
                  : 'text-gray-400 border-transparent hover:text-white'
              }`}
            >
              {tab === 'overview' && 'Vue d\'ensemble'}
              {tab === 'vulnerabilities' && 'Vulnérabilités'}
              {tab === 'recommendations' && 'Recommandations'}
              {tab === 'commands' && '⚙️ Commandes'}
              {tab === 'report' && 'Rapport'}
            </button>
          ))}
        </div>

        {/* Main Content */}
        <div className="space-y-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <>
              <div className="flex gap-4">
                <button
                  onClick={handleScan}
                  disabled={scanInProgress}
                  className={`px-6 py-3 rounded-lg font-semibold transition-colors ${
                    scanInProgress
                      ? 'bg-gray-600 cursor-not-allowed'
                      : 'bg-blue-600 hover:bg-blue-700'
                  }`}
                >
                  {scanInProgress ? '⏳ Scan en cours...' : '🔍 Démarrer un Scan'}
                </button>
              </div>

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

          {/* Commands Tab */}
          {activeTab === 'commands' && (
            <CommandPanel />
          )}

          {/* Report Tab */}
          {activeTab === 'report' && (
            <div className="card">
              <h2 className="text-2xl font-bold mb-6 text-white">Générer un Rapport</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                  onClick={generatePDF}
                  disabled={networks.length === 0}
                  className="p-6 bg-blue-900 hover:bg-blue-800 disabled:bg-gray-700 rounded-lg transition-colors text-center"
                >
                  <p className="text-2xl mb-2">📄</p>
                  <p className="font-semibold">Générer PDF</p>
                  <p className="text-sm text-gray-400 mt-2">Rapport professionnel complet</p>
                </button>

                <button
                  className="p-6 bg-green-900 hover:bg-green-800 rounded-lg transition-colors text-center"
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
                  <p className="text-2xl mb-2">📋</p>
                  <p className="font-semibold">Exporter JSON</p>
                  <p className="text-sm text-gray-400 mt-2">Données structurées</p>
                </button>

                <button
                  className="p-6 bg-purple-900 hover:bg-purple-800 rounded-lg transition-colors text-center"
                >
                  <p className="text-2xl mb-2">📊</p>
                  <p className="font-semibold">Aperçu Rapport</p>
                  <p className="text-sm text-gray-400 mt-2">Vérifier avant génération</p>
                </button>
              </div>

              {/* Rapport Summary */}
              <div className="mt-8 p-6 bg-gray-800 rounded-lg border border-gray-700">
                <h3 className="text-lg font-bold text-white mb-4">Résumé du Rapport</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <p className="text-gray-400">Total Réseaux</p>
                    <p className="text-xl font-bold text-white">{networks.length}</p>
                  </div>
                  <div>
                    <p className="text-gray-400">Vulnérabilités</p>
                    <p className="text-xl font-bold text-red-400">{vulnerabilities.length}</p>
                  </div>
                  <div>
                    <p className="text-gray-400">Critiques</p>
                    <p className="text-xl font-bold text-red-300">
                      {vulnerabilities.filter(v => v.severity === 'Critique').length}
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-400">Recommandations</p>
                    <p className="text-xl font-bold text-yellow-400">{recommendations.length}</p>
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
