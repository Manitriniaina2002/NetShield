import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { cn } from '../lib/utils';

export const HandshakeCapturePanel = ({ networks = [], onCaptureForCracking }) => {
  const [selectedNetwork, setSelectedNetwork] = useState(null);
  const [duration, setDuration] = useState(60);
  const [isCapturing, setIsCapturing] = useState(false);
  const [captures, setCaptures] = useState([]);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [interfaces, setInterfaces] = useState([]);
  const [enableDeauth, setEnableDeauth] = useState(false);
  const [deauthCount, setDeauthCount] = useState(5);

  // Récupérer les interfaces WiFi au chargement
  useEffect(() => {
    fetchInterfaces();
  }, []);

  // Mettre à jour le statut des captures actives
  useEffect(() => {
    if (isCapturing && captures.length > 0) {
      const interval = setInterval(() => {
        captures.forEach((capture) => {
          if (capture.status === 'running' || capture.status === 'pending') {
            updateCaptureStatus(capture.capture_id);
          }
        });
      }, 2000);

      return () => clearInterval(interval);
    }
  }, [isCapturing, captures]);

  const fetchInterfaces = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/handshake/interfaces');
      const data = await response.json();
      setInterfaces(data.interfaces || ['wlan0']);
    } catch (err) {
      console.error('Erreur lors de la récupération des interfaces:', err);
      setInterfaces(['wlan0']);
    }
  };

  const startCapture = async () => {
    if (!selectedNetwork) {
      setError('Veuillez sélectionner un réseau');
      return;
    }

    try {
      setError(null);
      setIsCapturing(true);

      const response = await fetch('http://127.0.0.1:8000/api/handshake/capture/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          network: selectedNetwork,
          duration: parseInt(duration),
          enable_deauth: enableDeauth,
          deauth_count: parseInt(deauthCount),
        }),
      });

      if (!response.ok) throw new Error(await response.text());

      const data = await response.json();
      setStatus(data);
      setCaptures((prev) => [
        ...prev,
        {
          capture_id: data.capture_id,
          network_ssid: data.network_ssid,
          network_bssid: data.network_bssid,
          status: 'running',
          progress: 0,
          packets_captured: 0,
          handshake_found: false,
          deauth_enabled: data.deauth_enabled,
          deauth_sent: false,
        },
      ]);
    } catch (err) {
      setError(err.message);
      setIsCapturing(false);
    }
  };

  const updateCaptureStatus = async (captureId) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/handshake/capture/status/${captureId}`
      );

      if (!response.ok) throw new Error('Erreur lors de la récupération du statut');

      const data = await response.json();

      setCaptures((prev) =>
        prev.map((capture) =>
          capture.capture_id === captureId
            ? {
                ...capture,
                status: data.status,
                progress: data.progress,
                packets_captured: data.packets_captured,
                handshake_found: data.handshake_found,
                deauth_sent: data.deauth_sent,
              }
            : capture
        )
      );

      // Arrêter la mise à jour si la capture est terminée
      if (data.status === 'completed' || data.status === 'failed') {
        const allCompleted = captures.every(
          (c) =>
            c.status === 'completed' ||
            c.status === 'failed' ||
            (c.capture_id !== captureId && c.status !== 'running')
        );
        if (allCompleted) {
          setIsCapturing(false);
        }
      }
    } catch (err) {
      console.error('Erreur lors de la mise à jour du statut:', err);
    }
  };

  const cancelCapture = async (captureId) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/handshake/capture/cancel/${captureId}`,
        { method: 'POST' }
      );

      if (!response.ok) throw new Error('Erreur lors de l\'annulation');

      setCaptures((prev) =>
        prev.map((capture) =>
          capture.capture_id === captureId
            ? { ...capture, status: 'cancelled' }
            : capture
        )
      );
    } catch (err) {
      setError(err.message);
    }
  };

  const useCaptureForCracking = (capture) => {
    // Pass the capture to the cracking workflow
    if (onCaptureForCracking) {
      onCaptureForCracking(capture)
    } else {
      console.warn('onCaptureForCracking callback not provided')
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-gray-500',
      running: 'bg-blue-500',
      paused: 'bg-yellow-500',
      completed: 'bg-green-500',
      failed: 'bg-red-500',
    };
    return colors[status] || 'bg-gray-500';
  };

  return (
    <div className="space-y-4">
      <Card className="p-4">
        <h2 className="text-lg font-bold mb-4">Capture de Handshake WiFi</h2>

        <div className="space-y-4">
          {/* Sélection du réseau */}
          <div>
            <label className="block text-sm font-medium mb-2">Réseau cible</label>
            <div className="max-h-40 overflow-y-auto border rounded p-2 space-y-2">
              {networks && networks.length > 0 ? (
                networks.map((net) => (
                  <div
                    key={net.bssid}
                    onClick={() => setSelectedNetwork(net)}
                    className={cn(
                      'p-2 rounded cursor-pointer border',
                      selectedNetwork?.bssid === net.bssid
                        ? 'bg-blue-100 border-blue-500'
                        : 'bg-gray-50 hover:bg-gray-100'
                    )}
                  >
                    <div className="font-medium">{net.ssid}</div>
                    <div className="text-xs text-gray-600">{net.bssid}</div>
                    <div className="text-xs text-gray-500">
                      Signal: {net.signal}% | Canal: {net.channel}
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-gray-500 text-sm">Aucun réseau détecté</div>
              )}
            </div>
          </div>

          {/* Configuration de la durée */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Durée de capture (secondes)
            </label>
            <Input
              type="number"
              min="10"
              max="600"
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              disabled={isCapturing}
              placeholder="60"
            />
          </div>

          {/* Configuration de la déauthentification */}
          <div className="space-y-3 border-t pt-3">
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="enableDeauth"
                checked={enableDeauth}
                onChange={(e) => setEnableDeauth(e.target.checked)}
                disabled={isCapturing}
                className="h-4 w-4 rounded border-gray-300"
              />
              <label htmlFor="enableDeauth" className="text-sm font-medium cursor-pointer">
                Activer la déauthentification
              </label>
            </div>
            
            {enableDeauth && (
              <div>
                <label className="block text-sm font-medium mb-2">
                  Nombre de paquets de déauthentification (1-20)
                </label>
                <Input
                  type="number"
                  min="1"
                  max="20"
                  value={deauthCount}
                  onChange={(e) => setDeauthCount(e.target.value)}
                  disabled={isCapturing}
                  placeholder="5"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Force les appareils à se reconnecter, générant ainsi un handshake
                </p>
              </div>
            )}
          </div>

          {/* Boutons d'action */}
          <div className="flex gap-2">
            <Button
              onClick={startCapture}
              disabled={!selectedNetwork || isCapturing}
              className="flex-1 bg-blue-600 hover:bg-blue-700"
            >
              {isCapturing ? 'Capture en cours...' : 'Démarrer la capture'}
            </Button>
            <Button
              onClick={fetchInterfaces}
              disabled={isCapturing}
              variant="outline"
            >
              Rafraîchir interfaces
            </Button>
          </div>

          {/* Affichage des erreurs */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded p-3 text-red-700 text-sm">
              {error}
            </div>
          )}
        </div>
      </Card>

      {/* Captures actives */}
      {captures.length > 0 && (
        <Card className="p-4">
          <h3 className="font-bold mb-4">Captures actives</h3>
          <div className="space-y-3">
            {captures.map((capture) => (
              <div key={capture.capture_id} className="border rounded p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">{capture.network_ssid}</div>
                    <div className="text-xs text-gray-600">{capture.network_bssid}</div>
                  </div>
                  <div className="text-right">
                    <Badge className={cn('text-white', getStatusColor(capture.status))}>
                      {capture.status}
                    </Badge>
                  </div>
                </div>

                {/* Barre de progression */}
                {(capture.status === 'running' || capture.status === 'pending') && (
                  <Progress value={capture.progress} className="h-2" />
                )}

                {/* Informations */}
                <div className="text-xs text-gray-600 space-y-1">
                  {capture.deauth_enabled && (
                    <div>
                      Déauthentification:{' '}
                      {capture.deauth_sent ? (
                        <span className="text-blue-600 font-medium">Envoyée ✓</span>
                      ) : (
                        <span className="text-gray-400">En attente...</span>
                      )}
                    </div>
                  )}
                  <div>Paquets capturés: {capture.packets_captured}</div>
                  <div>
                    Handshake:{' '}
                    {capture.handshake_found ? (
                      <span className="text-green-600 font-medium">Détecté ✓</span>
                    ) : (
                      <span className="text-gray-400">En attente...</span>
                    )}
                  </div>
                </div>

                {/* Boutons d'action */}
                <div className="flex gap-2 pt-2">
                  {capture.status === 'running' && (
                    <Button
                      onClick={() => cancelCapture(capture.capture_id)}
                      size="sm"
                      variant="destructive"
                      className="flex-1"
                    >
                      Annuler
                    </Button>
                  )}
                  {capture.handshake_found && capture.status === 'completed' && (
                    <Button
                      onClick={() => useCaptureForCracking(capture)}
                      size="sm"
                      className="flex-1 bg-green-600 hover:bg-green-700"
                    >
                      Utiliser pour le cracking
                    </Button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
};

export default HandshakeCapturePanel;
