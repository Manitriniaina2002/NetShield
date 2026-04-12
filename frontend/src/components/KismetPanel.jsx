import React from 'react'
import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'

function formatLastSeen(value) {
  if (!value) return 'Unknown'
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString('fr-FR')
}

function safeList(value) {
  return Array.isArray(value) ? value : []
}

export function KismetPanel({
  status,
  networks,
  devices,
  alerts,
  loading,
  error,
  kismetUrl,
  onRefresh,
  onScan,
  onChangeUrl
}) {
  const statusLabel = status?.status || (error ? 'offline' : 'unknown')
  const statusVariant = statusLabel === 'online' ? 'success' : statusLabel === 'offline' ? 'destructive' : 'warning'

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader className="border-b border-slate-200">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <CardTitle>Kismet</CardTitle>
              <CardDescription>Surveillance avancée, appareils détectés et alertes en temps réel.</CardDescription>
            </div>
            <Badge variant={statusVariant}>{statusLabel}</Badge>
          </div>
        </CardHeader>
        <CardContent className="grid gap-4 py-6 lg:grid-cols-[1fr_1fr]">
          <div className="space-y-3">
            <label className="text-sm font-medium text-slate-700">URL Kismet</label>
            <input
              type="text"
              value={kismetUrl}
              onChange={(e) => onChangeUrl(e.target.value)}
              className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
              placeholder="http://localhost:2501"
            />
            <p className="text-xs text-slate-500">Par défaut, Kismet écoute sur le port 2501.</p>
          </div>

          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-end">
            <Button variant="secondary" onClick={onRefresh} disabled={loading}>
              Rafraîchir
            </Button>
            <Button onClick={onScan} disabled={loading}>
              {loading ? 'Connexion…' : 'Lancer un scan Kismet'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {error && (
        <Card className="border-rose-200 bg-rose-50/70">
          <CardContent className="space-y-2 py-4 text-sm text-rose-700">
            <p>{error}</p>
            <p className="text-xs text-rose-600">
              Démarrage recommandé: <span className="font-mono">sudo kismet</span> puis cliquez sur <strong>Rafraîchir</strong>.
            </p>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-6 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader className="border-b border-slate-200">
            <CardTitle>Réseaux suivis</CardTitle>
            <CardDescription>{safeList(networks).length} réseau(x) détecté(s) par Kismet.</CardDescription>
          </CardHeader>
          <CardContent className="p-0">
            {safeList(networks).length === 0 ? (
              <div className="px-6 py-12 text-center text-sm text-slate-500">Aucun réseau Kismet disponible pour le moment.</div>
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
                      <th className="px-6 py-3">Dernière vue</th>
                    </tr>
                  </thead>
                  <tbody>
                    {safeList(networks).map((network, index) => (
                      <tr key={`${network.bssid || 'network'}-${index}`} className="border-t border-slate-100">
                        <td className="px-6 py-4 font-medium text-slate-900">{network.ssid || 'SSID masqué'}</td>
                        <td className="px-6 py-4 font-mono text-xs text-slate-500">{network.bssid || '—'}</td>
                        <td className="px-6 py-4 text-center text-slate-700">{network.channel ?? '—'}</td>
                        <td className="px-6 py-4 text-center"><Badge variant="info">{network.security || 'Unknown'}</Badge></td>
                        <td className="px-6 py-4 text-center text-slate-700">{network.signal_percentage ?? 0}%</td>
                        <td className="px-6 py-4 text-center text-slate-700">{network.clients ?? 0}</td>
                        <td className="px-6 py-4 text-slate-700">{formatLastSeen(network.last_seen)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader className="border-b border-slate-200">
              <CardTitle>Statut serveur</CardTitle>
              <CardDescription>Informations renvoyées par le daemon Kismet.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 pt-4 text-sm text-slate-600">
              <div><strong className="text-slate-800">Version:</strong> {status?.server_info?.kismet_version || status?.kismet_version || 'Unknown'}</div>
              <div><strong className="text-slate-800">Appareils:</strong> {status?.server_info?.devices_count ?? safeList(devices).length}</div>
              <div><strong className="text-slate-800">Session timeout:</strong> {status?.server_info?.http_session_timeout || 'Unknown'}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="border-b border-slate-200">
              <CardTitle>Appareils détectés</CardTitle>
              <CardDescription>{safeList(devices).length} appareil(s) suivi(s).</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 pt-4">
              {safeList(devices).length === 0 ? (
                <p className="text-sm text-slate-500">Aucun appareil pour l’instant.</p>
              ) : (
                safeList(devices).slice(0, 5).map((device, index) => (
                  <div key={`${device.device_key || 'device'}-${index}`} className="rounded-2xl border border-slate-200 bg-slate-50 p-3">
                    <div className="flex items-center justify-between gap-3">
                      <p className="font-medium text-slate-900">{device.device_name || device.mac_address || device.device_key || 'Device'}</p>
                      <Badge variant="secondary">{device.device_type || 'unknown'}</Badge>
                    </div>
                    <p className="mt-1 text-xs text-slate-500">{device.mac_address || device.device_key || '—'}</p>
                  </div>
                ))
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="border-b border-slate-200">
              <CardTitle>Alertes</CardTitle>
              <CardDescription>{safeList(alerts).length} définition(s) disponible(s).</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 pt-4">
              {safeList(alerts).length === 0 ? (
                <p className="text-sm text-slate-500">Aucune alerte chargée.</p>
              ) : (
                safeList(alerts).slice(0, 5).map((alert, index) => (
                  <div key={`${alert.alert_name || 'alert'}-${index}`} className="rounded-2xl border border-slate-200 bg-white p-3">
                    <p className="font-medium text-slate-900">{alert.alert_name || alert.name || 'Alert'}</p>
                    <p className="mt-1 text-xs text-slate-500">{alert.description || alert.alert_description || 'No description'}</p>
                  </div>
                ))
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default KismetPanel