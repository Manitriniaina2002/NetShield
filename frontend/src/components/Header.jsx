import React, { useState } from 'react'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'

export function Header() {
  const [showLegal, setShowLegal] = useState(false)
  const logoSrc = '/logo-netshield.png'

  return (
    <>
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-white/80 border-b border-slate-200/50 shadow-sm">
        <div className="mx-auto max-w-full px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo and Branding */}
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-primary-600 to-primary-700 rounded-xl blur-lg opacity-75"></div>
                <div className="relative h-12 w-12 overflow-hidden rounded-xl border border-primary-400/30 bg-gradient-to-br from-primary-500 to-primary-700 shadow-lg flex items-center justify-center">
                  <img
                    src={logoSrc}
                    alt="NetShield logo"
                    className="h-full w-full object-cover"
                    onError={(e) => {
                      e.currentTarget.style.display = 'none'
                      const fallback = e.currentTarget.nextElementSibling
                      if (fallback) fallback.style.display = 'flex'
                    }}
                  />
                  <div className="hidden h-full w-full items-center justify-center bg-gradient-to-br from-primary-500 to-primary-700 text-sm font-bold text-white">
                    NS
                  </div>
                </div>
              </div>

              <div className="hidden sm:block">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-700 bg-clip-text text-transparent">
                  NetShield
                </h1>
                <p className="text-xs text-slate-500 font-medium">Professional Security Auditor</p>
              </div>
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center gap-4">
              {/* Status Badge */}
              <div className="hidden md:flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-50/50 border border-accent-200/50">
                <div className="w-2 h-2 rounded-full bg-accent-600 animate-pulse"></div>
                <span className="text-sm font-medium text-accent-700">Active</span>
              </div>

              {/* Legal Button */}
              <button
                onClick={() => setShowLegal(true)}
                className="hidden md:inline-flex px-4 py-2 rounded-lg text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors"
              >
                Avis légal
              </button>

              {/* Menu Icon */}
              <button
                onClick={() => setShowLegal(true)}
                className="md:hidden p-2 rounded-lg hover:bg-slate-100 text-slate-600 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.5 6h.008v.008h-.008V6zm0 3h.008v.008h-.008V9zm0 3h.008v.008h-.008V12zm3-3h.008v.008h-.008V9zm0 3h.008v.008h-.008V12z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Legal Modal */}
      {showLegal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 p-4 backdrop-blur-sm animate-fade-in">
          <Card className="w-full max-w-2xl shadow-2xl border-0 max-h-[90vh] overflow-y-auto">
            <CardHeader className="bg-gradient-to-br from-primary-50 to-primary-100/50 border-b border-primary-200/30">
              <div className="flex items-start justify-between gap-4 mb-4">
                <div>
                  <Badge className="mb-3 bg-primary-600 text-white">Avis Important</Badge>
                  <CardTitle className="text-2xl">Utilisation Autorisée Uniquement</CardTitle>
                  <p className="mt-2 text-sm text-slate-600">Cadre Défensif &amp; Éducatif</p>
                </div>
                <button
                  onClick={() => setShowLegal(false)}
                  className="p-2 hover:bg-white/50 rounded-lg transition-colors"
                  aria-label="Fermer"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </CardHeader>

            <CardContent className="space-y-6 p-6">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="rounded-lg border-2 border-accent-200 bg-accent-50 p-5 hover:shadow-md transition-shadow">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-2xl"></span>
                    <h3 className="font-semibold text-accent-900">Utilisation Autorisée</h3>
                  </div>
                  <ul className="space-y-2 text-sm text-accent-800">
                    <li className="flex gap-2"><span></span><span>Fins éducatives et d'apprentissage</span></li>
                    <li className="flex gap-2"><span></span><span>Tests de sécurité autorisés avec consentement écrit</span></li>
                    <li className="flex gap-2"><span></span><span>Environnement contrôlé et laboratoire</span></li>
                    <li className="flex gap-2"><span></span><span>Audit de vos propres systèmes</span></li>
                  </ul>
                </div>

                <div className="rounded-lg border-2 border-red-200 bg-red-50 p-5 hover:shadow-md transition-shadow">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-2xl"></span>
                    <h3 className="font-semibold text-red-900">Utilisation Interdite</h3>
                  </div>
                  <ul className="space-y-2 text-sm text-red-800">
                    <li className="flex gap-2"><span></span><span>Accès non autorisé à des réseaux tiers</span></li>
                    <li className="flex gap-2"><span></span><span>Tests sans consentement explicite écrit</span></li>
                    <li className="flex gap-2"><span></span><span>Activités contraires aux lois locales/nationales</span></li>
                    <li className="flex gap-2"><span></span><span>Usage à des fins malveillantes ou criminelles</span></li>
                  </ul>
                </div>
              </div>

              <div className="rounded-lg border-l-4 border-yellow-400 bg-yellow-50 p-5">
                <div className="flex gap-3">
                  <span className="text-2xl flex-shrink-0"></span>
                  <div>
                    <h4 className="font-semibold text-yellow-900 mb-2">Clause de Non-Responsabilité</h4>
                    <p className="text-sm text-yellow-800">L'utilisateur assume l'entière responsabilité légale. NetShield Labs décline toute responsabilité pour les usages malveillants.</p>
                  </div>
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-200">
                <button onClick={() => setShowLegal(false)} className="px-6 py-2.5 rounded-lg bg-slate-100 text-slate-700 font-medium hover:bg-slate-200 transition-colors">
                  Fermer
                </button>
                <button onClick={() => setShowLegal(false)} className="px-6 py-2.5 rounded-lg bg-primary-600 text-white font-medium hover:bg-primary-700 transition-colors shadow-md hover:shadow-lg">
                  Accepté
                </button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </>
  )
}

export default Header
