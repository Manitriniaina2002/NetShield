import React, { useState } from 'react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card'
import { Badge } from './ui/badge'
import { Input } from './ui/input'

export function AdminAuthModal({ isOpen, onClose, onSuccess, commandPreview }) {
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showPassword, setShowPassword] = useState(false)

  const handleClose = () => {
    setPassword('')
    setError(null)
    setShowPassword(false)
    onClose?.()
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/api/commands/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password, description: commandPreview }),
      })

      const data = await response.json()

      if (response.ok && data.success) {
        setPassword('')
        onSuccess?.(data.session_id, data)
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

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/45 p-4 backdrop-blur-sm">
      <Card className="w-full max-w-md animate-fade-up overflow-hidden shadow-2xl">
        <CardHeader className="border-b border-slate-200 bg-slate-50/80">
          <Badge variant="destructive" className="mb-3 w-fit">Authentification requise</Badge>
          <CardTitle>Confirmation administrateur</CardTitle>
          <CardDescription>Les commandes système exigent une validation avant exécution.</CardDescription>
        </CardHeader>

        <CardContent className="space-y-4 p-6">
          {commandPreview && (
            <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
              <p className="mb-1 text-xs font-medium uppercase tracking-wide text-amber-700">Commande à exécuter</p>
              <code className="break-all font-mono text-xs">{commandPreview}</code>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">Mot de passe administrateur</label>
              <div className="relative">
                <Input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Entrez votre mot de passe"
                  disabled={loading}
                  autoFocus
                  className="pr-12"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={loading}
                  className="absolute right-3 top-1/2 -translate-y-1/2 rounded-lg px-2 py-1 text-xs font-medium text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 disabled:opacity-50"
                >
                  {showPassword ? 'Masquer' : 'Voir'}
                </button>
              </div>
              <p className="text-xs text-slate-500">En mode réel, l'application applique les règles de validation configurées côté backend.</p>
            </div>

            {error && (
              <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">{error}</div>
            )}

            <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-xs text-amber-800">
              Cette action peut lancer une commande sensible. Ne validez que si vous faites confiance à l'application.
            </div>

            <div className="flex gap-3 pt-2">
              <Button variant="secondary" type="button" onClick={handleClose} className="flex-1" disabled={loading}>
                Annuler
              </Button>
              <Button type="submit" className="flex-1" disabled={loading || !password}>
                {loading ? 'Authentification…' : 'S’authentifier'}
              </Button>
            </div>
          </form>

          <p className="text-xs text-slate-500">La session reste active 1 heure et le mot de passe n’est jamais stocké.</p>
        </CardContent>
      </Card>
    </div>
  )
}

export default AdminAuthModal
