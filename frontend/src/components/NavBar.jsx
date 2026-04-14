import React, { useState } from 'react'
import { MdDashboard, MdWarning, MdLock, MdHandshake, MdLightbulb, MdSignalCellularAlt, MdTerminal, MdDescription, MdWifi } from 'react-icons/md'

const NAV_ITEMS = [
  { 
    id: 'overview', 
    label: 'Vue d\'ensemble',
    icon: MdDashboard
  },
  { 
    id: 'vulnerabilities', 
    label: 'Vulnérabilités',
    icon: MdWarning
  },
  { 
    id: 'cracking', 
    label: 'Craquage',
    icon: MdLock
  },
  { 
    id: 'handshake', 
    label: 'Handshakes',
    icon: MdHandshake
  },
  { 
    id: 'recommendations', 
    label: 'Recommandations',
    icon: MdLightbulb
  },
  { 
    id: 'kismet', 
    label: 'Kismet',
    icon: MdSignalCellularAlt
  },
  { 
    id: 'commands', 
    label: 'Commandes',
    icon: MdTerminal
  },
  { 
    id: 'report', 
    label: 'Rapport',
    icon: MdDescription
  }
]

export function NavBar({ activeTab, onTabChange, onScan, scanInProgress = false }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <>
      {/* Main Navbar */}
      <nav className="sticky top-0 z-40 bg-white shadow-md border-b border-slate-100">
        <div className="mx-auto max-w-full px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo Area */}
            <div className="flex items-center gap-3 flex-1 md:flex-none">
              <div className="flex items-center justify-center h-10 w-10 rounded-lg overflow-hidden bg-white border border-slate-200 shadow-sm">
                <img 
                  src="/logo-netshield.png"
                  alt="NetShield logo"
                  className="h-full w-full object-cover"
                />
              </div>
              <div className="hidden md:block">
                <h1 className="text-xl font-bold text-slate-900">NetShield</h1>
                <p className="text-xs text-slate-500">Security Auditor</p>
              </div>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-1">
              {NAV_ITEMS.map(item => {
                const IconComponent = item.icon
                return (
                  <button
                    key={item.id}
                    onClick={() => onTabChange(item.id)}
                    className={`group relative px-3 py-2 rounded-lg transition-all duration-200 text-sm font-medium ${
                      activeTab === item.id
                        ? 'bg-primary-50 text-primary-700 shadow-sm'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                    }`}
                    aria-current={activeTab === item.id ? 'page' : undefined}
                  >
                    <span className="flex items-center gap-2">
                      <IconComponent className="text-lg" />
                      <span className="hidden lg:inline">{item.label}</span>
                    </span>
                    {activeTab === item.id && (
                      <div className="absolute bottom-0 left-0 right-0 h-1 bg-primary-600 rounded-t-full animate-fade-in" />
                    )}
                  </button>
                )
              })}
            </div>

            {/* Scan Button */}
            {onScan && (
              <button
                onClick={onScan}
                disabled={scanInProgress}
                className="hidden md:flex items-center gap-2 ml-4 px-4 py-2.5 rounded-lg bg-gradient-to-r from-primary-600 to-primary-700 text-white font-medium text-sm hover:from-primary-700 hover:to-primary-800 shadow-md hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <MdWifi className={`text-lg ${scanInProgress ? 'animate-spin' : ''}`} />
                <span>{scanInProgress ? 'Scan...' : 'Scan'}</span>
              </button>
            )}

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-lg hover:bg-slate-100 text-slate-600"
              aria-label="Menu"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>

          {/* Mobile Navigation */}
          {mobileMenuOpen && (
            <div className="md:hidden pb-4 animate-fade-down">
              <div className="flex flex-wrap gap-2 mb-3">
                {/* Mobile Scan Button */}
                {onScan && (
                  <button
                    onClick={() => {
                      onScan()
                      setMobileMenuOpen(false)
                    }}
                    disabled={scanInProgress}
                    className="w-full px-3 py-2 rounded-lg transition-all duration-200 text-sm font-medium bg-gradient-to-r from-primary-600 to-primary-700 text-white hover:from-primary-700 hover:to-primary-800 shadow-md flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <MdWifi className={`text-base ${scanInProgress ? 'animate-spin' : ''}`} />
                    <span>{scanInProgress ? 'Scan en cours...' : 'Démarrer un scan'}</span>
                  </button>
                )}
              </div>
              <div className="flex flex-wrap gap-2">
                {NAV_ITEMS.map(item => {
                  const IconComponent = item.icon
                  return (
                    <button
                      key={item.id}
                      onClick={() => {
                        onTabChange(item.id)
                        setMobileMenuOpen(false)
                      }}
                      className={`flex-1 min-w-[calc(50%-4px)] px-3 py-2 rounded-lg transition-all duration-200 text-xs font-medium ${
                        activeTab === item.id
                          ? 'bg-primary-600 text-white shadow-md'
                          : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                      }`}
                    >
                      <div className="flex items-center justify-center gap-1">
                        <IconComponent className="text-lg" />
                        <span>{item.label}</span>
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Scroll Indicator */}
      <div className="hidden md:block h-1 bg-gradient-to-r from-primary-600 via-accent-600 to-primary-600 opacity-0 group-has-scroll:opacity-100 transition-opacity duration-200" />
    </>
  )
}
