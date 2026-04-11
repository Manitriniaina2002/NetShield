import React, { useState } from 'react'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'

export function Header() {
  const [showLegal, setShowLegal] = useState(false)
  const logoSrc = '/logo-netshield.png'

  return (
    <>
      <header className="sticky top-0 z-40 border-b border-slate-200/80 bg-white/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center">
            <div className="h-14 w-14 overflow-hidden rounded-2xl border border-slate-200 bg-slate-100 shadow-sm sm:h-16 sm:w-16">
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
              <div className="hidden h-full w-full items-center justify-center bg-gradient-to-br from-emerald-500 to-teal-500 text-sm font-semibold text-white">
                NS
              </div>
            </div>
          </div>

          <Button variant="outline" onClick={() => setShowLegal(true)}>
            Mentions légales
          </Button>
        </div>
      </header>

      {showLegal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/45 p-4 backdrop-blur-sm">
          <Card className="w-full max-w-2xl animate-fade-up overflow-hidden shadow-2xl">
            <CardHeader className="border-b border-slate-200 bg-slate-50/80">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <Badge variant="destructive" className="mb-3">Avis important</Badge>
                  <CardTitle>Utilisation autorisée uniquement dans un cadre défensif</CardTitle>
                </div>
                <Button variant="ghost" size="icon" onClick={() => setShowLegal(false)} aria-label="Fermer">
                  ✕
                </Button>
              </div>
            </CardHeader>

            <CardContent className="space-y-6 p-6 text-sm text-slate-600">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
                  <h3 className="mb-2 text-sm font-semibold text-emerald-700">Utilisation autorisée</h3>
                  <ul className="list-disc space-y-1 pl-5">
                    <li>Fins éducatives</li>
                    <li>Tests autorisés avec consentement écrit</li>
                    <li>Environnement contrôlé de laboratoire</li>
                  </ul>
                </div>
                <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4">
                  <h3 className="mb-2 text-sm font-semibold text-rose-700">Utilisation interdite</h3>
                  <ul className="list-disc space-y-1 pl-5">
                    <li>Accès non autorisé à des réseaux tiers</li>
                    <li>Tests sans consentement explicite</li>
                    <li>Activités contraires aux lois locales</li>
                  </ul>
                </div>
              </div>

              <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-amber-800">
                L'utilisateur assume l'entière responsabilité légale de l'utilisation de cet outil. NetShield Labs décline toute responsabilité pour les usages malveillants.
              </div>

              <div className="flex justify-end gap-3">
                <Button variant="secondary" onClick={() => setShowLegal(false)}>Fermer</Button>
                <Button onClick={() => setShowLegal(false)}>J'ai compris</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </>
  )
}

export default Header
