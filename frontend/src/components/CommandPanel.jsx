import React, { useState, useEffect } from 'react'
import AdminAuthModal from './AdminAuthModal'

/**
 * Composant de panneau d'exécution de commandes système
 * Interface sécurisée avec authentification admin requise
 */
export function CommandPanel() {
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

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-[#33cc00] font-mono uppercase tracking-wider flex items-center gap-2">
              ⚙ Panneau de Commandes Système
            </h2>
            <p className="text-[#9ca3af] mt-1 font-mono">
              Exécution sécurisée de commandes système (avec authentification admin)
            </p>
          </div>
          
          {isAuthenticated && (
            <div className="bg-[#10b981]/20 border border-[#10b981]/40 text-[#34d399] px-4 py-2 rounded-lg">
              <div className="text-sm font-semibold font-mono">✓ Authentifié</div>
              <div className="text-xs mt-1 font-mono">Session active (1 heure)</div>
            </div>
          )}
        </div>
      </div>

      {/* Zone des commandes */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Sélecteur de commande */}
        <div className="lg:col-span-2 card">
          <h3 className="text-lg font-bold text-[#33cc00] mb-4 font-mono uppercase tracking-wider">
            ⚙ Sélectionnez une Commande
          </h3>

          {/* Liste des commandes */}
          <div className="space-y-2 mb-4 max-h-64 overflow-y-auto">
            {commands.map((cmd) => (
              <button
                key={cmd.name}
                onClick={() => setSelectedCommand(cmd.name)}
                className={`w-full text-left px-4 py-3 rounded-lg border-2 transition font-mono
                  ${selectedCommand === cmd.name
                    ? 'border-[#33cc00] bg-[#33cc00]/10'
                    : 'border-[#2a2f4a] hover:border-[#33cc00]/50'
                  }
                `}
              >
                <div className={`font-bold ${selectedCommand === cmd.name ? 'text-[#33cc00]' : 'text-[#e5e7eb]'}`}>
                  {cmd.name}
                </div>
                <div className="text-sm text-[#9ca3af]">
                  {cmd.description}
                </div>
              </button>
            ))}
          </div>

          {/* Champ arguments */}
          <div>
            <label className="block text-sm font-bold text-[#33cc00] mb-2 font-mono uppercase">
              ✑ Arguments (optionnel)
            </label>
            <input
              type="text"
              value={commandArgs}
              onChange={(e) => setCommandArgs(e.target.value)}
              placeholder="ex: wlan0 start"
              disabled={!selectedCommand || loading}
              className="w-full px-4 py-2 border border-[#2a2f4a] rounded-lg
                bg-[#151a3a] text-[#e5e7eb] font-mono
                focus:ring-2 focus:ring-[#33cc00] focus:border-[#33cc00] focus:outline-none
                disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>

          {/* Boutons d'action */}
          <div className="flex gap-3 mt-4">
            <button
              onClick={handleExecuteClick}
              disabled={!selectedCommand || loading}
              className="flex-1 px-4 py-2 bg-gradient-to-r from-[#33cc00] to-[#28a300] text-[#0a0e27] rounded-lg transition
                disabled:opacity-50 disabled:cursor-not-allowed font-bold flex items-center justify-center gap-2 font-mono"
            >
              {loading ? (
                <>
                  <span className="animate-spin">◌</span>
                  Exécution...
                </>
              ) : (
                <>
                  ▶ Exécuter
                </>
              )}
            </button>

            {isAuthenticated && (
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-[#ef4444] hover:bg-[#f87171] text-white rounded-lg transition font-bold font-mono"
              >
                ⌂ Déconnecter
              </button>
            )}
          </div>
        </div>

        {/* Informations */}
        <div className="card">
          <h3 className="text-lg font-bold text-[#33cc00] mb-4 font-mono uppercase">
            ⓘ Informations
          </h3>
          
          <div className="space-y-3 text-sm">
            <div className="bg-[#1a5f4a]/20 border border-[#10b981]/30 p-3 rounded font-mono">
              <div className="font-bold text-[#34d399]">
                ◇ Sécurité
              </div>
              <p className="text-[#a7f3d0] text-xs mt-1">
                Authentification admin requise pour chaque exécution
              </p>
            </div>

            <div className="bg-[#5f4a1a]/20 border border-[#f59e0b]/30 p-3 rounded font-mono">
              <div className="font-bold text-[#fbbf24]">
                ▦ Whitelist
              </div>
              <p className="text-[#fde047] text-xs mt-1">
                Seules les commandes sûres sont autorisées
              </p>
            </div>

            <div className="bg-[#1a5f3a]/20 border border-[#33cc00]/30 p-3 rounded font-mono">
              <div className="font-bold text-[#33cc00]">
                ✓ Statut
              </div>
              <p className="text-[#4dff00] text-xs mt-1">
                {isAuthenticated ? '✓ Authentifié' : '◌ Non authentifié'}
              </p>
            </div>

            <div className="bg-[#2a2f4a]/50 border border-[#9ca3af]/30 p-3 rounded font-mono">
              <div className="font-bold text-[#9ca3af]">
                ⏱️ Session
              </div>
              <p className="text-[#b8bcc6] text-xs mt-1">
                {isAuthenticated ? '1 heure restante' : 'Non connecté'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Messages d'erreur */}
      {error && (
        <div className="bg-[#ef4444]/15 border border-[#ef4444]/40 rounded-lg p-4">
          <div className="text-sm text-[#fca5a5] font-mono">
            <span className="font-bold">✕ Erreur:</span> {error}
          </div>
        </div>
      )}

      {/* Output */}
      {output && (
        <div className="card">
          <h3 className="text-lg font-bold text-[#33cc00] mb-4 font-mono uppercase">
            ↑ Résultat
          </h3>
          <div className="bg-[#0a0e27]/80 p-4 rounded-lg font-mono text-sm
            text-[#33cc00] overflow-x-auto max-h-96 overflow-y-auto border border-[#2a2f4a]">
            {output.split('\n').map((line, idx) => (
              <div key={idx} className="leading-relaxed">{line}</div>
            ))}
          </div>
        </div>
      )}

      {/* Modale d'authentification */}
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
