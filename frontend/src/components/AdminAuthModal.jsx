import React, { useState } from 'react'
import { wifiAPI } from '../api'

/**
 * Composant de modale d'authentification administrateur
 * Demande un mot de passe avant d'exécuter des commandes système
 */
export function AdminAuthModal({ isOpen, onClose, onSuccess, commandPreview }) {
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // Appeler l'endpoint d'authentification
      const response = await fetch('http://localhost:8000/api/commands/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          password: password,
          description: commandPreview
        })
      })

      const data = await response.json()

      if (response.ok && data.success) {
        // Authentification réussie
        setPassword('')
        if (onSuccess) {
          onSuccess(data.session_id, data)
        }
        handleClose()
      } else {
        setError(data.detail || 'Authentification échouée')
      }
    } catch (err) {
      setError('Erreur de connexion au serveur')
      console.error('Auth error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleClose = () => {
    setPassword('')
    setError(null)
    setShowPassword(false)
    if (onClose) {
      onClose()
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-2xl max-w-md w-full mx-4">
        
        {/* Header */}
        <div className="bg-red-600 text-white px-6 py-4 rounded-t-lg">
          <h2 className="text-xl font-bold flex items-center gap-2">
            🔒 Authentification Administrateur Requise
          </h2>
          <p className="text-red-100 text-sm mt-2">
            Les commandes système nécessitent une authentification root/admin
          </p>
        </div>

        {/* Content */}
        <div className="px-6 py-4">
          
          {/* Commande à exécuter */}
          {commandPreview && (
            <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700 rounded p-3 mb-4">
              <p className="text-xs font-semibold text-amber-900 dark:text-amber-200 mb-1">
                Commande à exécuter:
              </p>
              <code className="text-xs text-amber-900 dark:text-amber-100 break-all">
                {commandPreview}
              </code>
            </div>
          )}

          {/* Formulaire */}
          <form onSubmit={handleSubmit} className="space-y-4">
            
            {/* Champ mot de passe */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                🔐 Mot de passe Administrateur
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Entrez votre mot de passe"
                  disabled={loading}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg
                    bg-white dark:bg-slate-700 text-gray-900 dark:text-white
                    focus:ring-2 focus:ring-red-500 focus:border-transparent
                    disabled:opacity-50 disabled:cursor-not-allowed
                    placeholder-gray-400 dark:placeholder-gray-500"
                  autoFocus
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={loading}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700
                    dark:text-gray-400 dark:hover:text-gray-300 disabled:opacity-50"
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Mode simulation: tapez n'importe quel password (min. 4 caractères)
              </p>
            </div>

            {/* Message d'erreur */}
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded p-3">
                <p className="text-sm text-red-800 dark:text-red-200 font-semibold">
                  ⚠️ Erreur: {error}
                </p>
              </div>
            )}

            {/* Avertissement de sécurité */}
            <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 rounded p-3">
              <p className="text-xs text-yellow-800 dark:text-yellow-200">
                <span className="font-semibold">⚠️ Attention:</span> Cette action va acquérir les droits administrateur. 
                Ne confirmez que si vous faites confiance à cette application.
              </p>
            </div>

            {/* Boutons */}
            <div className="flex gap-3 pt-4">
              <button
                type="button"
                onClick={handleClose}
                disabled={loading}
                className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300
                  rounded-lg hover:bg-gray-50 dark:hover:bg-slate-700 transition
                  disabled:opacity-50 disabled:cursor-not-allowed font-medium"
              >
                Annuler
              </button>
              
              <button
                type="submit"
                disabled={loading || !password}
                className="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition
                  disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <span className="animate-spin">⏳</span>
                    Authentification...
                  </>
                ) : (
                  <>
                    🔓 S'authentifier
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 dark:bg-slate-900 px-6 py-3 rounded-b-lg border-t border-gray-200 dark:border-gray-700">
          <p className="text-xs text-gray-600 dark:text-gray-400">
            🛡️ <strong>Politique de sécurité:</strong> La session reste active 1 heure. 
            Votre mot de passe n'est jamais stocké.
          </p>
        </div>
      </div>
    </div>
  )
}

export default AdminAuthModal
