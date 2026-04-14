import React, { useState, useEffect } from 'react'
import { MdTarget, MdChecklist, MdGlobe, MdLock, MdShowChart, MdRefresh, MdPlayArrow } from 'react-icons/md'
import { Card } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { wifiAPI } from '../api'

export const DemoWorkflowPanel = () => {
  const [workflowData, setWorkflowData] = useState(null)
  const [networks, setNetworks] = useState([])
  const [crackingResults, setCrackingResults] = useState([])
  const [statistics, setStatistics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeStep, setActiveStep] = useState(0)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDemoData()
  }, [])

  const fetchDemoData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Fetch workflow summary
      const workflowResponse = await fetch('http://127.0.0.1:8000/api/demo/workflow/summary')
      if (!workflowResponse.ok) throw new Error('Failed to fetch workflow')
      const workflow = await workflowResponse.json()
      setWorkflowData(workflow)

      // Fetch networks
      const networksResponse = await fetch('http://127.0.0.1:8000/api/demo/networks')
      if (networksResponse.ok) {
        const netData = await networksResponse.json()
        setNetworks(netData)
      }

      // Fetch cracking results
      const crackingResponse = await fetch('http://127.0.0.1:8000/api/demo/cracking-results')
      if (crackingResponse.ok) {
        const crackData = await crackingResponse.json()
        setCrackingResults(crackData)
      }

      // Fetch statistics
      const statsResponse = await fetch('http://127.0.0.1:8000/api/demo/statistics')
      if (statsResponse.ok) {
        const statsData = await statsResponse.json()
        setStatistics(statsData)
      }
    } catch (err) {
      console.error('Error fetching demo data:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (score) => {
    if (score >= 70) return 'bg-red-500'
    if (score >= 40) return 'bg-yellow-500'
    return 'bg-green-500'
  }

  const getSuccessBadge = (success) => {
    return success
      ? <Badge className="bg-green-500 text-white">✓ Success</Badge>
      : <Badge className="bg-gray-500 text-white">Attempted</Badge>
  }

  if (loading) {
    return (
      <Card className="p-6">
        <div className="text-center">
          <div className="animate-spin inline-block w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
          <p className="mt-4 text-gray-600">Loading demo workflow...</p>
        </div>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {/* Overall Statistics */}
      {statistics && (
        <Card className="p-6 bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
          <h2 className="text-2xl font-bold mb-6 text-blue-900 flex items-center gap-2"><MdTarget /> NetShield Demo Workflow</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="text-center p-3 bg-white rounded border border-blue-200">
              <p className="text-sm text-gray-600">Networks Scanned</p>
              <p className="text-2xl font-bold text-blue-600">{statistics.total_networks_scanned}</p>
            </div>
            <div className="text-center p-3 bg-white rounded border border-green-200">
              <p className="text-sm text-gray-600">Successful Captures</p>
              <p className="text-2xl font-bold text-green-600">{statistics.successful_captures}/{statistics.total_networks_scanned}</p>
              <p className="text-xs text-gray-500">{statistics.capture_success_rate.toFixed(1)}%</p>
            </div>
            <div className="text-center p-3 bg-white rounded border border-purple-200">
              <p className="text-sm text-gray-600">Passwords Cracked</p>
              <p className="text-2xl font-bold text-purple-600">{statistics.successful_cracks}</p>
              <p className="text-xs text-gray-500">{statistics.crack_success_rate.toFixed(1)}% success</p>
            </div>
            <div className={`text-center p-3 bg-white rounded border ${getRiskColor(statistics.overall_risk_score) === 'bg-red-500' ? 'border-red-300' : 'border-yellow-300'}`}>
              <p className="text-sm text-gray-600">Overall Risk</p>
              <p className={`text-2xl font-bold ${getRiskColor(statistics.overall_risk_score).replace('bg-', 'text-')}`}>
                {statistics.overall_risk_score}/100
              </p>
            </div>
          </div>

          {/* Vulnerabilities Summary */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm">
            <div className="p-2 bg-red-100 rounded">
              <span className="font-semibold text-red-700">{statistics.critical_vulnerabilities}</span>
              <p className="text-red-600">Critical</p>
            </div>
            <div className="p-2 bg-orange-100 rounded">
              <span className="font-semibold text-orange-700">{statistics.high_vulnerabilities}</span>
              <p className="text-orange-600">High</p>
            </div>
            <div className="p-2 bg-yellow-100 rounded">
              <span className="font-semibold text-yellow-700">{statistics.medium_vulnerabilities}</span>
              <p className="text-yellow-600">Medium</p>
            </div>
            <div className="p-2 bg-blue-100 rounded">
              <span className="font-semibold text-blue-700">{statistics.low_vulnerabilities}</span>
              <p className="text-blue-600">Low</p>
            </div>
          </div>
        </Card>
      )}

      {/* Workflow Steps */}
      {workflowData && (
        <Card className="p-6">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2"><MdChecklist /> Audit Workflow Steps</h3>
          
          <div className="space-y-4">
            {workflowData.steps.map((step, idx) => (
              <div
                key={idx}
                className={`border-l-4 p-4 rounded cursor-pointer transition-all ${
                  activeStep === idx
                    ? 'border-blue-500 bg-blue-50 border-l-4'
                    : 'border-gray-300 bg-white hover:bg-gray-50'
                }`}
                onClick={() => setActiveStep(idx)}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="inline-flex items-center justify-center w-8 h-8 bg-blue-500 text-white rounded-full font-bold text-sm">
                        {step.step}
                      </span>
                      <h4 className="text-lg font-semibold text-gray-900">{step.title}</h4>
                    </div>
                    <p className="text-gray-600 mb-2">{step.description}</p>
                    
                    {activeStep === idx && (
                      <div className="mt-4 space-y-3">
                        <div>
                          <p className="text-sm font-semibold text-gray-700 mb-2">Networks Involved:</p>
                          <div className="flex flex-wrap gap-2">
                            {step.networks_involved.map((net, i) => (
                              <Badge key={i} className="bg-gray-200 text-gray-800">
                                {net}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        
                        <div>
                          <p className="text-sm font-semibold text-gray-700 mb-2">Key Findings:</p>
                          <ul className="space-y-1">
                            {step.key_findings.map((finding, i) => (
                              <li key={i} className="text-sm text-gray-700 flex gap-2">
                                <MdPlayArrow className="text-blue-500 flex-shrink-0" />
                                <span>{finding}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Networks Summary */}
      {networks.length > 0 && (
        <Card className="p-6">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2"><MdGlobe /> Scanned Networks</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-100">
                <tr className="border-b">
                  <th className="p-2 text-left">SSID</th>
                  <th className="p-2 text-left">Security</th>
                  <th className="p-2 text-left">Capture</th>
                  <th className="p-2 text-left">Handshake</th>
                  <th className="p-2 text-right">Packets</th>
                  <th className="p-2 text-right">Size</th>
                </tr>
              </thead>
              <tbody>
                {networks.map((net, idx) => (
                  <tr key={idx} className="border-b hover:bg-gray-50">
                    <td className="p-2 font-mono text-blue-600">{net.ssid}</td>
                    <td className="p-2">
                      <Badge className={
                        net.security_level.includes('WEP') ? 'bg-red-500 text-white' :
                        net.security_level.includes('Open') ? 'bg-red-500 text-white' :
                        net.security_level.includes('WPA3') ? 'bg-green-500 text-white' :
                        'bg-yellow-500 text-white'
                      }>
                        {net.security_level}
                      </Badge>
                    </td>
                    <td className="p-2">{net.capture_status}</td>
                    <td className="p-2">{net.handshake_status}</td>
                    <td className="p-2 text-right">{net.packets.toLocaleString()}</td>
                    <td className="p-2 text-right">{(net.file_size / 1024).toFixed(1)} KB</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Cracking Results */}
      {crackingResults.length > 0 && (
        <Card className="p-6">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2"><MdLock /> Password Cracking Results</h3>
          <div className="space-y-3">
            {crackingResults.map((attempt, idx) => (
              <div key={idx} className="p-4 border rounded bg-white hover:bg-gray-50">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="font-semibold text-gray-900">{attempt.network_ssid}</p>
                    <p className="text-xs text-gray-500">ID: {attempt.attempt_id}</p>
                  </div>
                  {getSuccessBadge(attempt.success)}
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                  <div>
                    <p className="text-gray-600">Method</p>
                    <p className="font-mono text-gray-900">{attempt.method}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Wordlist</p>
                    <p className="font-mono text-gray-900">{attempt.wordlist}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Duration</p>
                    <p className="font-mono text-gray-900">{attempt.duration}s</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Passwords Tried</p>
                    <p className="font-mono text-gray-900">{attempt.passwords_tried.toLocaleString()}</p>
                  </div>
                </div>

                {attempt.success && attempt.password && (
                  <div className="mt-3 p-2 bg-green-100 rounded">
                    <p className="text-xs text-green-600 font-semibold">Password Found:</p>
                    <p className="font-mono text-green-900 font-bold">{attempt.password}</p>
                  </div>
                )}

                {attempt.gpu_enabled && (
                  <div className="mt-2">
                    <Badge className="bg-purple-200 text-purple-800 flex items-center gap-1"><MdShowChart /> GPU Enabled</Badge>
                  </div>
                )}
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Refresh Button */}
      <div className="flex justify-center">
        <Button 
          onClick={fetchDemoData}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 text-white flex items-center gap-2"
        >
          <MdRefresh /> Refresh Demo Data
        </Button>
      </div>

      {error && (
        <Card className="p-4 bg-red-50 border border-red-200">
          <p className="text-red-600 text-sm">Error: {error}</p>
        </Card>
      )}
    </div>
  )
}

export default DemoWorkflowPanel
