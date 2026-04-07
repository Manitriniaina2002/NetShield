import React, { useState } from 'react'

export function Header() {
  const [darkMode, setDarkMode] = useState(true)
  const [showLegal, setShowLegal] = useState(false)

  return (
    <>
      <header className="bg-gradient-to-r from-[#0a0e27] via-[#151a3a] to-[#0f1423] shadow-lg border-b border-[#2a2f4a]">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-[#33cc00] to-[#28a300] rounded-lg flex items-center justify-center text-[#0a0e27] font-bold font-mono text-lg shadow-lg shadow-[#33cc00]/50">
              NS
            </div>
            <div>
              <h1 className="text-2xl font-bold text-[#33cc00] font-mono">NetShield</h1>
              <p className="text-[#9ca3af] text-sm font-mono">Wi-Fi Security Audit Lab</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Bouton Info Légale */}
            <button
              onClick={() => setShowLegal(!showLegal)}
              className="px-4 py-2 bg-[#1a1f3a] hover:bg-[#1e2449] text-[#e5e7eb] rounded-lg text-sm transition-all border border-[#2a2f4a] hover:border-[#33cc00] font-mono font-semibold"
            >
              ⚠ Mentions Légales
            </button>

            {/* Toggle Dark Mode */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="px-4 py-2 bg-[#1a1f3a] hover:bg-[#1e2449] text-[#e5e7eb] rounded-lg transition-all border border-[#2a2f4a] hover:border-[#33cc00] font-mono font-semibold"
            >
              {darkMode ? '☼' : '◯'}
            </button>
          </div>
        </div>
      </header>

      {/* Modal Mentions Légales */}
      {showLegal && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
          <div className="bg-gradient-to-br from-[#1a1f3a] to-[#151a3a] rounded-lg max-w-2xl max-h-96 overflow-y-auto border border-[#ef4444] border-2 p-6 shadow-2xl shadow-[#ef4444]/20">
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-2xl font-bold text-[#ef4444] font-mono">⚠ AVERTISSEMENT LÉGAL ET ÉTHIQUE</h2>
              <button
                onClick={() => setShowLegal(false)}
                className="text-2xl text-[#9ca3af] hover:text-[#33cc00] transition-colors"
              >
                ✕
              </button>
            </div>

            <div className="text-[#e5e7eb] space-y-4 text-sm font-mono">
              <div>
                <h3 className="text-lg font-semibold text-[#33cc00] mb-2 uppercase tracking-wider">• Utilisation Autorisée</h3>
                <p className="text-[#9ca3af]">
                  Cet outil est destiné UNIQUEMENT à :
                </p>
                <ul className="list-disc list-inside mt-2 text-[#9ca3af] space-y-1">
                  <li>Des fins ÉDUCATIVES</li>
                  <li>Des tests de sécurité AUTORISÉS (pentest avec consentement écrit)</li>
                  <li>Un environnement CONTRÔLÉ (laboratoire, sandboxe)</li>
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-[#ef4444] mb-2 uppercase tracking-wider">✕ Utilisation Interdite</h3>
                <ul className="list-disc list-inside text-[#fca5a5] space-y-1">
                  <li>Tout accès NON AUTORISÉ à des réseaux Wi-Fi</li>
                  <li>Tests sur des réseaux tiers SANS CONSENTEMENT</li>
                  <li>Toute activité violant les lois locales/nationales</li>
                </ul>
              </div>

              <div className="bg-[#ef4444]/10 border border-[#ef4444]/30 rounded-lg p-4 mt-4">
                <p className="text-[#fca5a5] font-semibold">
                  L'utilisateur assume l'entière responsabilité légale de l'utilisation de cet outil.
                  NetShield Labs décline toute responsabilité pour les usages malveillants.
                </p>
              </div>
            </div>

            <button
              onClick={() => setShowLegal(false)}
              className="mt-6 w-full px-4 py-2 bg-gradient-to-r from-[#33cc00] to-[#28a300] text-[#0a0e27] rounded-lg transition-all font-mono font-bold hover:from-[#4dff00] hover:to-[#33cc00] shadow-lg"
            >
              ✓ J'ai compris
            </button>
          </div>
        </div>
      )}
    </>
  )
}

export default Header
