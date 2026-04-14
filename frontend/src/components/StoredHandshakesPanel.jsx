import React, { useState, useEffect } from 'react'
import { MdCheckCircle } from 'react-icons/md'
import { Card } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { cn } from '../lib/utils'
import { wifiAPI } from '../api'

export const StoredHandshakesPanel = ({ onSelectHandshake, selectedNetwork = null }) => {
  const [handshakes, setHandshakes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [selectedHandshake, setSelectedHandshake] = useState(null)
  const [filterSuccessful, setFilterSuccessful] = useState(true)
  const [statistics, setStatistics] = useState(null)

  useEffect(() => {
    fetchHandshakes()
    fetchStatistics()
  }, [filterSuccessful, selectedNetwork])

  const fetchHandshakes = async () => {
    try {
      setLoading(true)
      setError(null)

      let response
      if (selectedNetwork?.bssid) {
        response = await wifiAPI.getStoredHandshakesByNetwork(selectedNetwork.bssid, filterSuccessful)
      } else {
        response = await wifiAPI.getStoredHandshakes(filterSuccessful, 100)
      }

      setHandshakes(Array.isArray(response?.data) ? response.data : [])
    } catch (err) {
      setError(err.message)
      console.error('Error fetching handshakes:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchStatistics = async () => {
    try {
      const response = await wifiAPI.getStoredHandshakeStatistics()
      if (response?.data) {
        setStatistics(response.data)
      }
    } catch (err) {
      console.error('Error fetching statistics:', err)
    }
  }

  const handleSelectHandshake = (handshake) => {
    setSelectedHandshake(handshake)
    if (onSelectHandshake) {
      onSelectHandshake({
        id: handshake.id,
        capture_id: handshake.capture_id,
        ssid: handshake.network_ssid,
        bssid: handshake.network_bssid,
        file_format: handshake.file_format,
        file_size: handshake.file_size,
        deauth_sent: handshake.deauth_used
      })
    }
  }

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return 'N/A'
    }
  }

  const getStatusBadge = (handshake) => {
    if (handshake.success && handshake.handshake_found) {
      return <Badge className="bg-green-500 text-white flex items-center gap-1 w-fit"><MdCheckCircle /> Succès</Badge>
    }
    if (handshake.success) {
      return <Badge className="bg-blue-500 text-white">Capturé</Badge>
    }
    return <Badge className="bg-gray-500 text-white">Échec</Badge>
  }

  return (
    <div className="space-y-4">
      <Card className="p-4">
        <h2 className="text-lg font-bold mb-4">Handshakes Stockés</h2>

        {/* Statistics Summary */}
        {statistics && (
          <div className="grid grid-cols-4 gap-2 mb-4 p-3 bg-gray-50 rounded">
            <div className="text-center">
              <div className="text-2xl font-bold">{statistics.total_captures}</div>
              <div className="text-xs text-gray-600">Captures totales</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{statistics.successful_captures}</div>
              <div className="text-xs text-gray-600">Réussies</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{statistics.successful_cracks}</div>
              <div className="text-xs text-gray-600">Mots de passe trouvés</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{statistics.unique_networks}</div>
              <div className="text-xs text-gray-600">Réseaux uniques</div>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex gap-2 mb-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={filterSuccessful}
              onChange={(e) => setFilterSuccessful(e.target.checked)}
              className="rounded border-gray-300"
            />
            <span className="text-sm">Uniquement les réussis</span>
          </label>
          <Button
            onClick={fetchHandshakes}
            size="sm"
            variant="outline"
            disabled={loading}
          >
            {loading ? 'Chargement...' : 'Rafraîchir'}
          </Button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded p-3 text-red-700 text-sm mb-4">
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center py-8 text-gray-500">
            Chargement des handshakes...
          </div>
        )}

        {/* Handshakes List */}
        {!loading && handshakes.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            Aucun handshake stocké
          </div>
        )}

        {!loading && handshakes.length > 0 && (
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {handshakes.map((handshake) => (
              <div
                key={handshake.capture_id}
                onClick={() => handleSelectHandshake(handshake)}
                className={cn(
                  'p-3 rounded border cursor-pointer transition-colors',
                  selectedHandshake?.capture_id === handshake.capture_id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:bg-gray-50'
                )}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1">
                    <div className="font-semibold">{handshake.network_ssid}</div>
                    <div className="text-xs text-gray-600">{handshake.network_bssid}</div>
                    <div className="text-xs text-gray-500 mt-1">
                      Capturé: {formatDate(handshake.created_at)}
                    </div>
                  </div>
                  <div className="flex flex-col gap-2">
                    {getStatusBadge(handshake)}
                    <div className="text-xs text-gray-600 text-right">
                      {handshake.file_size > 0 && (
                        <div>{(handshake.file_size / 1024).toFixed(2)} KB</div>
                      )}
                      {handshake.deauth_used && (
                        <div className="text-blue-600 font-medium">Déauth: {handshake.deauth_count}x</div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Handshake Details */}
                <div className="mt-2 grid grid-cols-4 gap-2 text-xs p-2 bg-gray-50 rounded">
                  <div>
                    <span className="text-gray-600">Durée:</span>
                    <span className="ml-1 font-medium">{handshake.duration_seconds}s</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Paquets:</span>
                    <span className="ml-1 font-medium">{handshake.packets_captured}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Format:</span>
                    <span className="ml-1 font-medium">{handshake.file_format}</span>
                  </div>
                </div>

                {handshake.notes && (
                  <div className="mt-2 text-xs italic text-gray-600 p-2 bg-yellow-50 rounded">
                    {handshake.notes}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Selected Handshake Info */}
        {selectedHandshake && (
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded">
            <div className="text-sm font-medium text-blue-900 flex items-center gap-2">
              <MdCheckCircle className="text-green-600" /> Handshake sélectionné
            </div>
            <div className="text-sm text-blue-800 mt-1">
              {selectedHandshake.network_ssid} ({selectedHandshake.network_bssid})
            </div>
          </div>
        )}
      </Card>
    </div>
  )
}

export default StoredHandshakesPanel
