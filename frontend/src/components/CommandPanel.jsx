import React, { useState, useEffect } from 'react'
import AdminAuthModal from './AdminAuthModal'
import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { Input } from './ui/input'

const COMMAND_ARGUMENT_HINTS = {
  ifconfig: {
    description: 'Afficher les interfaces et adresses réseau.',
    templates: ['-a']
  },
  ip: {
    description: 'Commandes réseau Linux modernes.',
    templates: ['addr show', 'link show', 'route']
  },
  'airmon-ng': {
    description: 'Activer/Désactiver le mode monitor.',
    templates: ['start wlan0', 'stop wlan0mon']
  },
  'airodump-ng': {
    description: 'Scanner ou cibler un réseau Wi-Fi.',
    templates: ['wlan0mon', '--bssid <BSSID> -c <CHANNEL> wlan0mon', '-w capture wlan0mon']
  },
  'aircrack-ng': {
    description: 'Lancer un test de craquage sur capture.',
    templates: ['-w /usr/share/wordlists/rockyou.txt capture.cap', '-b <BSSID> -w /usr/share/wordlists/rockyou.txt capture.cap']
  },
  hashcat: {
    description: 'Craquage accéléré GPU (si disponible).',
    templates: ['-m 22000 handshake.hc22000 /usr/share/wordlists/rockyou.txt']
  },
  john: {
    description: 'Test de dictionnaire avec John the Ripper.',
    templates: ['--wordlist=/usr/share/wordlists/rockyou.txt hashes.txt']
  },
  ps: {
    description: 'Lister les processus actifs.',
    templates: ['aux', '-ef']
  },
  kill: {
    description: 'Terminer un processus par PID.',
    templates: ['-9 <PID>']
  }
}

/**
 * Composant de panneau d'exécution de commandes système
 * Interface sécurisée avec authentification admin requise
 */
export function CommandPanel({ networks = [] }) {
  const [commands, setCommands] = useState([])
  const [selectedCommand, setSelectedCommand] = useState(null)
  const [commandArgs, setCommandArgs] = useState('')
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  // État d'authentification
  const [sessionId, setSessionId] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [authModal, setAuthModal] = useState(false)
  const [commandPreview, setCommandPreview] = useState('')

  // Charger les commandes autorisées
  useEffect(() => {
    loadAllowedCommands()
  }, [])

  const loadAllowedCommands = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/commands/allowed')
      const data = await response.json()
      const cmdList = Object.entries(data.commands || data).map(([cmd, desc]) => ({
        name: cmd,
        description: desc
      }))
      setCommands(cmdList)
    } catch (err) {
      console.error('Erreur lors du chargement des commandes:', err)
    }
  }

  const handleExecuteClick = () => {
    if (!isAuthenticated) {
      // Ouvrir la modale d'authentification
      const preview = selectedCommand ? selectedCommand + (commandArgs ? ` ${commandArgs}` : '') : ''
      setCommandPreview(preview)
      setAuthModal(true)
    } else {
      // Exécuter directement
      executeCommand()
    }
  }

  const handleAuthSuccess = (newSessionId, authData) => {
    setSessionId(newSessionId)
    setIsAuthenticated(true)
    setOutput(`✓ Authentification réussie!\n${authData.message}`)
    
    // Exécuter la commande après authentification
    setTimeout(() => {
      executeCommand(newSessionId)
    }, 500)
  }

  const executeCommand = async (sessionIdToUse = sessionId) => {
    if (!selectedCommand) {
      setError('Sélectionnez une commande')
      return
    }

    setLoading(true)
    setError(null)
    setOutput('')

    try {
      const args = commandArgs.trim() ? commandArgs.trim().split(' ') : []
      
      const response = await fetch('http://localhost:8000/api/commands/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          command: selectedCommand,
          args: args,
          session_id: sessionIdToUse
        })
      })

      const data = await response.json()

      if (response.ok && data.success) {
        setOutput(data.output || 'Commande exécutée avec succès')
      } else if (data.require_auth) {
        setIsAuthenticated(false)
        setSessionId(null)
        setCommandPreview(selectedCommand + (commandArgs ? ` ${commandArgs}` : ''))
        setAuthModal(true)
      } else {
        setError(data.error || 'Erreur lors de l\'exécution')
      }
    } catch (err) {
      setError('Erreur de connexion: ' + err.message)
      console.error('Command execution error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    setSessionId(null)
    setIsAuthenticated(false)
    setOutput('')
    setError(null)
  }

  const insertArgument = (value) => {
    setCommandArgs((prev) => (prev ? `${prev} ${value}` : value))
  }

  const commandHelp = selectedCommand ? COMMAND_ARGUMENT_HINTS[selectedCommand] : null
  const networkSuggestions = networks
    .filter((net) => net && net.bssid)
    .slice(0, 8)

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader className="flex flex-col gap-4 border-b border-slate-200 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <CardTitle>Panneau de commandes système</CardTitle>
            <CardDescription>Exécution sécurisée avec authentification administrateur.</CardDescription>
          </div>
          {isAuthenticated ? <Badge variant="success">Session active</Badge> : <Badge variant="warning">Non authentifié</Badge>}
        </CardHeader>
      </Card>

      <div className="grid gap-6 lg:grid-cols-[1.4fr_0.6fr]">
        <Card>
          <CardHeader>
            <CardTitle>Sélectionnez une commande</CardTitle>
            <CardDescription>Les commandes sont filtrées côté backend par une whitelist.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="max-h-72 space-y-2 overflow-y-auto pr-1">
              {commands.map((cmd) => (
                <button
                  key={cmd.name}
                  onClick={() => setSelectedCommand(cmd.name)}
                  className={`w-full rounded-2xl border p-4 text-left transition ${
                    selectedCommand === cmd.name
                      ? 'border-emerald-300 bg-emerald-50 shadow-sm'
                      : 'border-slate-200 bg-white hover:border-emerald-200 hover:bg-slate-50'
                  }`}
                >
                  <div className="font-mono text-sm font-semibold text-slate-900">{cmd.name}</div>
                  <div className="mt-1 text-sm text-slate-500">{cmd.description}</div>
                </button>
              ))}
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">Arguments (optionnel)</label>
              <Input
                type="text"
                value={commandArgs}
                onChange={(e) => setCommandArgs(e.target.value)}
                placeholder="ex: wlan0 start"
                disabled={!selectedCommand || loading}
              />
            </div>

            {selectedCommand && (
              <div className="space-y-3 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <div>
                  <p className="text-sm font-semibold text-slate-800">Arguments suggérés</p>
                  <p className="text-xs text-slate-500">
                    {commandHelp?.description || 'Utilisez les exemples ci-dessous pour remplir rapidement les arguments.'}
                  </p>
                </div>

                <div className="flex flex-wrap gap-2">
                  {(commandHelp?.templates || []).map((template) => (
                    <button
                      key={template}
                      type="button"
                      onClick={() => insertArgument(template)}
                      className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:border-emerald-300 hover:bg-emerald-50 hover:text-emerald-700"
                      disabled={loading}
                    >
                      {template}
                    </button>
                  ))}
                </div>

                <div className="space-y-2">
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Réseaux scannés (suggestions)</p>
                  {networkSuggestions.length > 0 ? (
                    <div className="space-y-2">
                      {networkSuggestions.map((net) => (
                        <div key={net.bssid} className="rounded-xl border border-slate-200 bg-white p-2.5">
                          <div className="mb-2 text-xs text-slate-500">
                            {net.ssid || 'SSID masqué'}
                          </div>
                          <div className="flex flex-wrap gap-2">
                            <button
                              type="button"
                              onClick={() => insertArgument(net.bssid)}
                              className="rounded-full border border-slate-200 px-2.5 py-1 text-xs font-mono text-slate-700 hover:border-emerald-300 hover:bg-emerald-50"
                              disabled={loading}
                            >
                              BSSID: {net.bssid}
                            </button>
                            {net.channel && (
                              <button
                                type="button"
                                onClick={() => insertArgument(String(net.channel))}
                                className="rounded-full border border-slate-200 px-2.5 py-1 text-xs text-slate-700 hover:border-sky-300 hover:bg-sky-50"
                                disabled={loading}
                              >
                                Canal: {net.channel}
                              </button>
                            )}
                            {net.ssid && (
                              <button
                                type="button"
                                onClick={() => insertArgument(`"${net.ssid}"`)}
                                className="rounded-full border border-slate-200 px-2.5 py-1 text-xs text-slate-700 hover:border-amber-300 hover:bg-amber-50"
                                disabled={loading}
                              >
                                SSID: "{net.ssid}"
                              </button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-slate-500">Aucun réseau scanné disponible. Lancez un scan dans l’onglet Vue d’ensemble.</p>
                  )}
                </div>
              </div>
            )}

            <div className="flex gap-3">
              <Button onClick={handleExecuteClick} disabled={!selectedCommand || loading} className="flex-1">
                {loading ? 'Exécution…' : 'Exécuter'}
              </Button>
              {isAuthenticated && (
                <Button variant="destructive" onClick={handleLogout}>
                  Déconnecter
                </Button>
              )}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Informations</CardTitle>
            <CardDescription>État d’accès et garde-fous de sécurité.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-slate-600">
            <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
              <div className="font-medium text-emerald-800">Sécurité</div>
              <p className="mt-1 text-emerald-700">Authentification admin requise pour chaque exécution.</p>
            </div>
            <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4">
              <div className="font-medium text-amber-800">Whitelist</div>
              <p className="mt-1 text-amber-700">Seules les commandes sûres sont autorisées.</p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="font-medium text-slate-800">Statut</div>
              <p className="mt-1 text-slate-600">{isAuthenticated ? 'Authentifié' : 'Non authentifié'}</p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="font-medium text-slate-800">Session</div>
              <p className="mt-1 text-slate-600">{isAuthenticated ? '1 heure restante' : 'Non connecté'}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {error && <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">{error}</div>}

      {output && (
        <Card>
          <CardHeader>
            <CardTitle>Résultat</CardTitle>
            <CardDescription>Sortie brute de la commande exécutée.</CardDescription>
          </CardHeader>
          <CardContent>
            <pre className="max-h-96 overflow-auto rounded-2xl border border-slate-200 bg-slate-950 p-4 font-mono text-sm text-emerald-300">
              {output}
            </pre>
          </CardContent>
        </Card>
      )}

      <AdminAuthModal
        isOpen={authModal}
        onClose={() => setAuthModal(false)}
        onSuccess={handleAuthSuccess}
        commandPreview={commandPreview}
      />
    </div>
  )
}

export default CommandPanel
