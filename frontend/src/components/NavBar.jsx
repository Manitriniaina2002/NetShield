import React from 'react'

const NAV_ITEMS = [
  { id: 'overview', label: 'Vue d\'ensemble' },
  { id: 'kismet', label: 'Kismet' },
  { id: 'vulnerabilities', label: 'Vulnérabilités' },
  { id: 'recommendations', label: 'Recommandations' },
  { id: 'cracking', label: 'Craquage' },
  { id: 'commands', label: 'Commandes' },
  { id: 'report', label: 'Rapport' }
]

function TabIcon({ id }) {
  const base = 'h-3.5 w-3.5'

  if (id === 'overview') {
    return (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={base} aria-hidden="true">
        <rect x="3" y="3" width="8" height="8" rx="2" />
        <rect x="13" y="3" width="8" height="5" rx="2" />
        <rect x="13" y="10" width="8" height="11" rx="2" />
        <rect x="3" y="13" width="8" height="8" rx="2" />
      </svg>
    )
  }

  if (id === 'kismet') {
    return (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={base} aria-hidden="true">
        <path d="M12 3a9 9 0 019 9" />
        <path d="M12 7a5 5 0 015 5" />
        <path d="M12 11a1 1 0 110 2 1 1 0 010-2z" fill="currentColor" />
        <path d="M6.5 17.5l-1.8 1.8" />
        <path d="M17.5 17.5l1.8 1.8" />
      </svg>
    )
  }

  if (id === 'vulnerabilities') {
    return (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={base} aria-hidden="true">
        <path d="M12 3l9 4.5v5.5c0 5-3.5 8-9 10-5.5-2-9-5-9-10V7.5L12 3z" />
        <path d="M12 8v5" />
        <circle cx="12" cy="16" r="1" fill="currentColor" />
      </svg>
    )
  }

  if (id === 'recommendations') {
    return (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={base} aria-hidden="true">
        <path d="M12 3v10" />
        <path d="M8 11a4 4 0 118 0" />
        <path d="M9 17h6" />
        <path d="M10 21h4" />
      </svg>
    )
  }

  if (id === 'cracking') {
    return (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={base} aria-hidden="true">
        <rect x="4" y="11" width="16" height="10" rx="2" />
        <path d="M8 11V8a4 4 0 018 0v3" />
        <path d="M12 15v2" />
      </svg>
    )
  }

  if (id === 'commands') {
    return (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={base} aria-hidden="true">
        <path d="M4 7l4 4-4 4" />
        <path d="M10 17h10" />
      </svg>
    )
  }

  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={base} aria-hidden="true">
      <path d="M7 3h7l5 5v13H7z" />
      <path d="M14 3v6h6" />
      <path d="M10 13h6" />
      <path d="M10 17h4" />
    </svg>
  )
}

export function NavBar({ activeTab, onTabChange }) {
  return (
    <nav className="sticky top-0 z-40 border-b border-slate-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex overflow-x-auto">
          {NAV_ITEMS.map(item => (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`inline-flex items-center gap-2 whitespace-nowrap border-b-2 px-4 py-4 text-sm font-medium transition-all duration-200 ${
                activeTab === item.id
                  ? 'border-emerald-600 bg-emerald-50/70 text-emerald-700'
                  : 'border-transparent text-slate-600 hover:border-slate-300 hover:text-slate-900'
              }`}
              aria-current={activeTab === item.id ? 'page' : undefined}
            >
              <span
                className={`inline-flex h-6 w-6 items-center justify-center rounded-full transition-transform duration-200 ${
                  activeTab === item.id
                    ? 'scale-105 bg-emerald-100 text-emerald-700'
                    : 'bg-slate-100 text-slate-500'
                }`}
              >
                <TabIcon id={item.id} />
              </span>
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      </div>
    </nav>
  )
}
