import React from 'react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card'
import { Badge } from './ui/badge'

export function NetworkTable({ networks, onSelectNetwork }) {
  const securityVariant = (security) => {
    if (security === 'Open' || security === 'WEP') return 'destructive'
    if (security === 'WPA' || security === 'WPA2') return 'warning'
    return 'success'
  }

  return (
    <Card>
      <CardHeader className="border-b border-slate-200">
        <CardTitle>Réseaux détectés</CardTitle>
        <CardDescription>Choisissez un réseau pour afficher les vulnérabilités et les stratégies.</CardDescription>
      </CardHeader>
      <CardContent className="p-0">
        {networks.length === 0 ? (
          <div className="px-6 py-12 text-center text-sm text-slate-500">Aucun réseau détecté. Lancez d'abord un scan.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead className="bg-slate-50 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                <tr>
                  <th className="px-6 py-3">SSID</th>
                  <th className="px-6 py-3">BSSID</th>
                  <th className="px-6 py-3 text-center">Canal</th>
                  <th className="px-6 py-3 text-center">Sécurité</th>
                  <th className="px-6 py-3 text-center">Signal</th>
                  <th className="px-6 py-3 text-center">Clients</th>
                  <th className="px-6 py-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {networks.map((net, idx) => (
                  <tr key={idx} className="table-row">
                    <td className="px-6 py-4 font-medium text-slate-900">{net.ssid || '(Hidden)'}</td>
                    <td className="px-6 py-4 font-mono text-xs text-slate-500">{net.bssid}</td>
                    <td className="px-6 py-4 text-center text-slate-700">{net.channel}</td>
                    <td className="px-6 py-4 text-center"><Badge variant={securityVariant(net.security)}>{net.security}</Badge></td>
                    <td className="px-6 py-4 text-center text-slate-700">{net.signal_percentage || 0}% <span className="text-slate-400">({net.signal_strength} dBm)</span></td>
                    <td className="px-6 py-4 text-center text-slate-700">{net.clients || 0}</td>
                    <td className="px-6 py-4 text-right">
                      <Button size="sm" onClick={() => onSelectNetwork(net)}>Analyser</Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default NetworkTable
