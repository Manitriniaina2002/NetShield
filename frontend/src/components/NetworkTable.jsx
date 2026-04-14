import React, { useState } from 'react'
import { MdTableChart, MdGridView, MdSearch, MdLock } from 'react-icons/md'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card'
import { Badge } from './ui/badge'

export function NetworkTable({ networks, onSelectNetwork }) {
  const [viewMode, setViewMode] = useState('table') // 'table' or 'grid'
  const [sortBy, setSortBy] = useState('signal')
  const [filterSecurity, setFilterSecurity] = useState('all')

  const securityVariant = (security) => {
    if (security === 'Open' || security === 'WEP') return 'destructive'
    if (security === 'WPA' || security === 'WPA2') return 'warning'
    return 'success'
  }

  const securityColor = (security) => {
    if (security === 'Open' || security === 'WEP') return 'from-red-500 to-red-600'
    if (security === 'WPA' || security === 'WPA2') return 'from-yellow-500 to-yellow-600'
    return 'from-accent-500 to-accent-600'
  }

  // Filter networks
  const filteredNetworks = filterSecurity === 'all' 
    ? networks 
    : networks.filter(n => n.security === filterSecurity)

  // Sort networks
  const sortedNetworks = [...filteredNetworks].sort((a, b) => {
    switch (sortBy) {
      case 'signal':
        return (b.signal_percentage || 0) - (a.signal_percentage || 0)
      case 'ssid':
        return (a.ssid || '').localeCompare(b.ssid || '')
      case 'security':
        return (a.security || '').localeCompare(b.security || '')
      default:
        return 0
    }
  })

  const uniqueSecurities = [...new Set(networks.map(n => n.security))]

  // Grid View Component
  const GridView = () => (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {sortedNetworks.map((net, idx) => (
        <div
          key={idx}
          className="group card hover:shadow-lg hover:-translate-y-1 cursor-pointer transition-all duration-300 p-5"
          onClick={() => onSelectNetwork(net)}
        >
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-slate-900 truncate text-lg">
                {net.ssid ? net.ssid : <span className="flex items-center gap-2"><MdLock className="text-base" /> Hidden</span>}
              </h3>
              <p className="text-xs text-slate-500 font-mono mt-1 truncate">{net.bssid}</p>
            </div>
            <div className="flex-shrink-0 ml-2">
              <Badge variant={securityVariant(net.security)} className="whitespace-nowrap">
                {net.security}
              </Badge>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-3 gap-3 mb-4">
            {/* Signal */}
            <div className="bg-gradient-to-br from-primary-50 to-primary-100 rounded-lg p-3">
              <div className="text-sm text-primary-600 font-medium">Signal</div>
              <div className="text-2xl font-bold text-primary-700">{net.signal_percentage || 0}%</div>
              <div className="text-xs text-primary-600">{net.signal_strength} dBm</div>
            </div>

            {/* Channel */}
            <div className="bg-gradient-to-br from-secondary-50 to-secondary-100 rounded-lg p-3">
              <div className="text-sm text-secondary-600 font-medium">Canal</div>
              <div className="text-2xl font-bold text-secondary-700">{net.channel}</div>
              <div className="text-xs text-secondary-600">2.4/5.0 GHz</div>
            </div>

            {/* Clients */}
            <div className="bg-gradient-to-br from-accent-50 to-accent-100 rounded-lg p-3">
              <div className="text-sm text-accent-600 font-medium">Clients</div>
              <div className="text-2xl font-bold text-accent-700">{net.clients || 0}</div>
              <div className="text-xs text-accent-600">Connectés</div>
            </div>
          </div>

          {/* Action Button */}
          <button className="w-full px-4 py-2.5 rounded-lg bg-primary-600 text-white font-medium hover:bg-primary-700 transition-colors shadow-md hover:shadow-lg group-hover:shadow-lg">
            Analyser →
          </button>
        </div>
      ))}
    </div>
  )

  // Table View Component
  const TableView = () => (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm">
        <thead className="bg-gradient-to-r from-secondary-50 to-secondary-100 border-b border-slate-200">
          <tr>
            <th className="px-6 py-4 text-left text-xs font-semibold text-secondary-700 uppercase tracking-wider">SSID</th>
            <th className="px-6 py-4 text-left text-xs font-semibold text-secondary-700 uppercase tracking-wider">BSSID</th>
            <th className="px-6 py-4 text-center text-xs font-semibold text-secondary-700 uppercase tracking-wider">Canal</th>
            <th className="px-6 py-4 text-center text-xs font-semibold text-secondary-700 uppercase tracking-wider">Sécurité</th>
            <th className="px-6 py-4 text-center text-xs font-semibold text-secondary-700 uppercase tracking-wider">Signal</th>
            <th className="px-6 py-4 text-center text-xs font-semibold text-secondary-700 uppercase tracking-wider">Clients</th>
            <th className="px-6 py-4 text-right text-xs font-semibold text-secondary-700 uppercase tracking-wider">Action</th>
          </tr>
        </thead>
        <tbody>
          {sortedNetworks.map((net, idx) => (
            <tr key={idx} className="border-b border-slate-200 hover:bg-slate-50 transition-colors duration-200">
              <td className="px-6 py-4 font-medium text-slate-900">
                <div className="flex items-center gap-2">
                  {net.ssid || <span className="text-slate-400 italic">Hidden Network</span>}
                </div>
              </td>
              <td className="px-6 py-4 font-mono text-xs text-slate-500">{net.bssid}</td>
              <td className="px-6 py-4 text-center">
                <span className="inline-flex items-center justify-center px-3 py-1 rounded-full bg-primary-100 text-primary-700 font-medium text-sm">
                  {net.channel}
                </span>
              </td>
              <td className="px-6 py-4 text-center">
                <Badge variant={securityVariant(net.security)} className="justify-center">
                  {net.security}
                </Badge>
              </td>
              <td className="px-6 py-4 text-center">
                <div className="flex items-center justify-center gap-2">
                  <div className="w-24 h-2 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full bg-gradient-to-r ${securityColor(net.security)}`}
                      style={{ width: `${net.signal_percentage || 0}%` }}
                    ></div>
                  </div>
                  <span className="font-medium text-slate-700 text-xs ml-1">{net.signal_percentage || 0}%</span>
                </div>
              </td>
              <td className="px-6 py-4 text-center font-medium text-slate-700">{net.clients || 0}</td>
              <td className="px-6 py-4 text-right">
                <button
                  onClick={() => onSelectNetwork(net)}
                  className="px-4 py-2 rounded-lg bg-primary-600 text-white font-medium hover:bg-primary-700 transition-colors shadow-sm hover:shadow-md text-sm"
                >
                  Analyser
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )

  return (
    <Card className="card-elevated">
      <CardHeader className="border-b border-slate-200 bg-gradient-to-r from-white to-slate-50">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <CardTitle className="text-2xl">Réseaux Wi-Fi Détectés</CardTitle>
            <CardDescription>
              {sortedNetworks.length} réseau{sortedNetworks.length !== 1 ? 'x' : ''} trouvé{sortedNetworks.length !== 1 ? 's' : ''}
            </CardDescription>
          </div>

          {/* Controls */}
          <div className="flex flex-col sm:flex-row gap-3">
            {/* View Toggle */}
            <div className="flex gap-2 bg-slate-100 p-1 rounded-lg">
              <button
                onClick={() => setViewMode('table')}
                className={`px-3 py-2 rounded font-medium transition-colors text-sm flex items-center gap-1.5 ${
                  viewMode === 'table'
                    ? 'bg-white text-primary-600 shadow-sm'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <MdTableChart className="text-base" /> Tableau
              </button>
              <button
                onClick={() => setViewMode('grid')}
                className={`px-3 py-2 rounded font-medium transition-colors text-sm flex items-center gap-1.5 ${
                  viewMode === 'grid'
                    ? 'bg-white text-primary-600 shadow-sm'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <MdGridView className="text-base" /> Grille
              </button>
            </div>

            {/* Sort Select */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="input text-sm py-2"
            >
              <option value="signal">Trier par Signal</option>
              <option value="ssid">Trier par SSID</option>
              <option value="security">Trier par Sécurité</option>
            </select>

            {/* Security Filter */}
            <select
              value={filterSecurity}
              onChange={(e) => setFilterSecurity(e.target.value)}
              className="input text-sm py-2"
            >
              <option value="all">Tous les réseaux</option>
              {uniqueSecurities.map(sec => (
                <option key={sec} value={sec}>{sec}</option>
              ))}
            </select>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-6">
        {sortedNetworks.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-5xl mb-3 flex justify-center">
              <MdSearch className="text-slate-300" />
            </div>
            <p className="text-slate-600 font-medium">Aucun réseau trouvé</p>
            <p className="text-slate-500 text-sm mt-1">Lancez un scan pour détecter les réseaux Wi-Fi</p>
          </div>
        ) : viewMode === 'grid' ? (
          <GridView />
        ) : (
          <TableView />
        )}
      </CardContent>
    </Card>
  )
}

export default NetworkTable
