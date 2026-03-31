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
    setOutput(`✅ Authentification réussie!\n${authData.message}`)
    
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
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
              ⚙️ Panneau de Commandes Système
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Exécution sécurisée de commandes système (avec authentification admin)
            </p>
          </div>
          
          {isAuthenticated && (
            <div className="bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200 px-4 py-2 rounded-lg">
              <div className="text-sm font-semibold">✅ Authentifié</div>
              <div className="text-xs mt-1">Session active (1 heure)</div>
            </div>
          )}
        </div>
      </div>

      {/* Zone des commandes */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Sélecteur de commande */}
        <div className="lg:col-span-2 bg-white dark:bg-slate-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            🔧 Sélectionnez une Commande
          </h3>

          {/* Liste des commandes */}
          <div className="space-y-2 mb-4">
            {commands.map((cmd) => (
              <button
                key={cmd.name}
                onClick={() => setSelectedCommand(cmd.name)}
                className={`w-full text-left px-4 py-3 rounded-lg border-2 transition
                  ${selectedCommand === cmd.name
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                  }
                `}
              >
                <div className="font-semibold text-gray-900 dark:text-white">
                  {cmd.name}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  {cmd.description}
                </div>
              </button>
            ))}
          </div>

          {/* Champ arguments */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              📝 Arguments (optionnel)
            </label>
            <input
              type="text"
              value={commandArgs}
              onChange={(e) => setCommandArgs(e.target.value)}
              placeholder="ex: wlan0 start"
              disabled={!selectedCommand || loading}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg
                bg-white dark:bg-slate-700 text-gray-900 dark:text-white
                focus:ring-2 focus:ring-blue-500 focus:border-transparent
                disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>

          {/* Boutons d'action */}
          <div className="flex gap-3 mt-4">
            <button
              onClick={handleExecuteClick}
              disabled={!selectedCommand || loading}
              className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition
                disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <span className="animate-spin">⏳</span>
                  Exécution...
                </>
              ) : (
                <>
                  ▶️ Exécuter
                </>
              )}
            </button>

            {isAuthenticated && (
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition font-medium"
              >
                🚪 Déconnecter
              </button>
            )}
          </div>
        </div>

        {/* Informations */}
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            ℹ️ Informations
          </h3>
          
          <div className="space-y-3 text-sm">
            <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded">
              <div className="font-semibold text-blue-900 dark:text-blue-200">
                🔐 Sécurité
              </div>
              <p className="text-blue-800 dark:text-blue-300 text-xs mt-1">
                Authentification admin requise pour chaque exécution
              </p>
            </div>

            <div className="bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded">
              <div className="font-semibold text-yellow-900 dark:text-yellow-200">
                📋 Whitelist
              </div>
              <p className="text-yellow-800 dark:text-yellow-300 text-xs mt-1">
                Seules les commandes sûres sont autorisées
              </p>
            </div>

            <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded">
              <div className="font-semibold text-green-900 dark:text-green-200">
                ✅ Statut
              </div>
              <p className="text-green-800 dark:text-green-300 text-xs mt-1">
                {isAuthenticated ? '✅ Authentifié' : '⏳ Non authentifié'}
              </p>
            </div>

            <div className="bg-gray-50 dark:bg-gray-900/20 p-3 rounded">
              <div className="font-semibold text-gray-900 dark:text-gray-200">
                ⏱️ Session
              </div>
              <p className="text-gray-800 dark:text-gray-300 text-xs mt-1">
                {isAuthenticated ? '1 heure restante' : 'Non connecté'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Messages d'erreur */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg p-4">
          <div className="text-sm text-red-800 dark:text-red-200">
            <span className="font-semibold">❌ Erreur:</span> {error}
          </div>
        </div>
      )}

      {/* Output */}
      {output && (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            📤 Résultat
          </h3>
          <div className="bg-gray-50 dark:bg-slate-900 p-4 rounded-lg font-mono text-sm
            text-gray-900 dark:text-gray-100 overflow-x-auto max-h-96 overflow-y-auto">
            {output.split('\n').map((line, idx) => (
              <div key={idx}>{line}</div>
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
