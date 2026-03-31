import React, { useState } from 'react'

export function Header() {
  const [darkMode, setDarkMode] = useState(true)
  const [showLegal, setShowLegal] = useState(false)

  return (
    <>
      <header className="bg-gradient-to-r from-blue-900 to-blue-800 shadow-lg border-b border-blue-700">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-400 rounded-lg flex items-center justify-center text-white font-bold">
              NS
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">NetShield</h1>
              <p className="text-blue-200 text-sm">Wi-Fi Security Audit Lab</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Bouton Info Légale */}
            <button
              onClick={() => setShowLegal(!showLegal)}
              className="px-3 py-2 bg-blue-700 hover:bg-blue-600 text-white rounded-lg text-sm transition-colors"
            >
              ⚠️ Mentions Légales
            </button>

            {/* Toggle Dark Mode */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="px-3 py-2 bg-blue-700 hover:bg-blue-600 text-white rounded-lg transition-colors"
            >
              {darkMode ? '☀️' : '🌙'}
            </button>
          </div>
        </div>
      </header>

      {/* Modal Mentions Légales */}
      {showLegal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-lg max-w-2xl max-h-96 overflow-y-auto border border-red-600 p-6">
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-2xl font-bold text-red-500">⚠️ AVERTISSEMENT LÉGAL ET ÉTHIQUE</h2>
              <button
                onClick={() => setShowLegal(false)}
                className="text-2xl text-gray-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <div className="text-gray-300 space-y-4 text-sm">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Utilisation Autorisée</h3>
                <p className="text-gray-400">
                  Cet outil est destiné UNIQUEMENT à :
                </p>
                <ul className="list-disc list-inside mt-2 text-gray-400">
                  <li>Des fins ÉDUCATIVES</li>
                  <li>Des tests de sécurité AUTORISÉS (pentest avec consentement écrit)</li>
                  <li>Un environnement CONTRÔLÉ (laboratoire, sandboxe)</li>
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Utilisation Interdite</h3>
                <ul className="list-disc list-inside text-gray-400">
                  <li>Tout accès NON AUTORISÉ à des réseaux Wi-Fi</li>
                  <li>Tests sur des réseaux tiers SANS CONSENTEMENT</li>
                  <li>Toute activité violant les lois locales/nationales</li>
                </ul>
              </div>

              <div className="bg-red-900 bg-opacity-30 border border-red-600 rounded-lg p-4 mt-4">
                <p className="text-red-300 font-semibold">
                  L'utilisateur assume l'entière responsabilité légale de l'utilisation de cet outil.
                  NetShield Labs décline toute responsabilité pour les usages malveillants.
                </p>
              </div>
            </div>

            <button
              onClick={() => setShowLegal(false)}
              className="mt-6 w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              J'ai compris
            </button>
          </div>
        </div>
      )}
    </>
  )
}

export default Header
