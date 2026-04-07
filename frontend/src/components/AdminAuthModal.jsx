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
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 backdrop-blur-sm">
      <div className="bg-gradient-to-br from-[#1a1f3a] to-[#151a3a] rounded-lg shadow-2xl max-w-md w-full mx-4 border border-[#2a2f4a]">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-[#ef4444] to-[#dc2626] text-white px-6 py-4 rounded-t-lg border-b border-[#2a2f4a]">
          <h2 className="text-xl font-bold flex items-center gap-2 font-mono uppercase">
            ◇ Authentification Administrateur
          </h2>
          <p className="text-[#fee2e2] text-sm mt-2 font-mono">
            Les commandes système nécessitent une authentification root/admin
          </p>
        </div>

        {/* Content */}
        <div className="px-6 py-4">
          
          {/* Commande à exécuter */}
          {commandPreview && (
            <div className="bg-[#f59e0b]/15 border border-[#f59e0b]/40 rounded p-3 mb-4">
              <p className="text-xs font-bold text-[#fbbf24] mb-1 uppercase tracking-wider">
                Commande à exécuter:
              </p>
              <code className="text-xs text-[#fde047] break-all font-mono">
                {commandPreview}
              </code>
            </div>
          )}

          {/* Formulaire */}
          <form onSubmit={handleSubmit} className="space-y-4">
            
            {/* Champ mot de passe */}
            <div>
              <label className="block text-sm font-bold text-[#33cc00] mb-2 font-mono uppercase">
                ◇ Mot de passe Administrateur
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Entrez votre mot de passe"
                  disabled={loading}
                  className="w-full px-4 py-2 border border-[#2a2f4a] rounded-lg
                    bg-[#151a3a] text-[#e5e7eb] font-mono
                    focus:ring-2 focus:ring-[#33cc00] focus:border-[#33cc00] focus:outline-none
                    disabled:opacity-50 disabled:cursor-not-allowed
                    placeholder-[#6b7280]"
                  autoFocus
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={loading}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-[#9ca3af] hover:text-[#33cc00]
                    dark:text-[#9ca3af] dark:hover:text-[#33cc00] disabled:opacity-50 transition"
                >
                  {showPassword ? '◉' : '○'}
                </button>
              </div>
              <p className="text-xs text-[#9ca3af] mt-1 font-mono">
                Mode simulation: tapez n'importe quel password (min. 4 caractères)
              </p>
            </div>

            {/* Message d'erreur */}
            {error && (
              <div className="bg-[#ef4444]/15 border border-[#ef4444]/40 rounded p-3">
                <p className="text-sm text-[#fca5a5] font-bold font-mono">
                  ⚠ Erreur: {error}
                </p>
              </div>
            )}

            {/* Avertissement de sécurité */}
            <div className="bg-[#f59e0b]/15 border border-[#f59e0b]/40 rounded p-3">
              <p className="text-xs text-[#fbbf24] font-mono">
                <span className="font-bold">⚠ Attention:</span> Cette action va acquérir les droits administrateur. 
                Ne confirmez que si vous faites confiance à cette application.
              </p>
            </div>

            {/* Boutons */}
            <div className="flex gap-3 pt-4">
              <button
                type="button"
                onClick={handleClose}
                disabled={loading}
                className="flex-1 px-4 py-2 border border-[#2a2f4a] text-[#e5e7eb]
                  rounded-lg hover:bg-[#1e2449] hover:border-[#33cc00] transition
                  disabled:opacity-50 disabled:cursor-not-allowed font-bold font-mono"
              >
                Annuler
              </button>
              
              <button
                type="submit"
                disabled={loading || !password}
                className="flex-1 px-4 py-2 bg-gradient-to-r from-[#ef4444] to-[#dc2626] hover:from-[#f87171] hover:to-[#ef4444] text-white rounded-lg transition
                  disabled:opacity-50 disabled:cursor-not-allowed font-bold flex items-center justify-center gap-2 font-mono"
              >
                {loading ? (
                  <>
                    <span className="animate-spin">◌</span>
                    Authentification...
                  </>
                ) : (
                  <>
                    ◇ S'authentifier
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Footer */}
        <div className="bg-[#0a0e27]/50 px-6 py-3 rounded-b-lg border-t border-[#2a2f4a]">
          <p className="text-xs text-[#9ca3af] font-mono">
            ✦ <strong className="text-[#33cc00]">Politique de sécurité:</strong> La session reste active 1 heure. 
            Votre mot de passe n'est jamais stocké.
          </p>
        </div>
      </div>
    </div>
  )
}

export default AdminAuthModal
