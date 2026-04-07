import React from 'react'

export function NetworkTable({ networks, onSelectNetwork }) {
  return (
    <div className="card overflow-x-auto">
      <h2 className="text-xl font-bold mb-4 text-[#22c55e] font-mono uppercase tracking-wider">⟿ Réseaux Détectés</h2>
      
      {networks.length === 0 ? (
        <p className="text-[#6b7280] text-center py-8 font-mono">
          Aucun réseau détecté. Lancez un scan d'abord.
        </p>
      ) : (
        <table className="w-full text-sm font-mono">
          <thead>
            <tr className="border-b border-[#e5e7eb] bg-[#f9fafb]/50">
              <th className="text-left px-4 py-3 text-[#22c55e] font-bold uppercase text-xs tracking-wider">SSID</th>
              <th className="text-left px-4 py-3 text-[#22c55e] font-bold uppercase text-xs tracking-wider">BSSID</th>
              <th className="text-center px-4 py-3 text-[#22c55e] font-bold uppercase text-xs tracking-wider">Canal</th>
              <th className="text-center px-4 py-3 text-[#22c55e] font-bold uppercase text-xs tracking-wider">Sécurité</th>
              <th className="text-center px-4 py-3 text-[#22c55e] font-bold uppercase text-xs tracking-wider">Signal</th>
              <th className="text-center px-4 py-3 text-[#22c55e] font-bold uppercase text-xs tracking-wider">Clients</th>
              <th className="text-center px-4 py-3 text-[#22c55e] font-bold uppercase text-xs tracking-wider">Action</th>
            </tr>
          </thead>
          <tbody>
            {networks.map((net, idx) => (
              <tr key={idx} className="table-row border-b border-[#e5e7eb] hover:bg-[#22c55e]/5">
                <td className="px-4 py-3 font-mono text-[#1f2937]">{net.ssid || '(Hidden)'}</td>
                <td className="px-4 py-3 font-mono text-[#6b7280] text-xs">{net.bssid}</td>
                <td className="text-center px-4 py-3 text-[#1f2937]">{net.channel}</td>
                <td className="text-center px-4 py-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                    net.security === 'Open' ? 'bg-[#fee2e2] text-[#991b1b] border border-[#fecaca]' :
                    net.security === 'WEP' ? 'bg-[#fee2e2] text-[#991b1b] border border-[#fecaca]' :
                    net.security === 'WPA' ? 'bg-[#fef3c7] text-[#92400e] border border-[#fde68a]' :
                    net.security === 'WPA2' ? 'bg-[#fef3c7] text-[#92400e] border border-[#fde68a]' :
                    'bg-[#dcfce7] text-[#166534] border border-[#bbf7d0]'
                  }`}>
                    {net.security}
                  </span>
                </td>
                <td className="text-center px-4 py-3">
                  <div className="flex justify-center gap-2">
                    <span className="text-[#22c55e] font-bold">{net.signal_percentage || 0}%</span>
                    <span className="text-[#6b7280]">{net.signal_strength}dBm</span>
                  </div>
                </td>
                <td className="text-center px-4 py-3 text-[#1f2937]">{net.clients || 0}</td>
                <td className="text-center px-4 py-3">
                  <button
                    onClick={() => onSelectNetwork(net)}
                    className="px-3 py-1 bg-gradient-to-r from-[#22c55e] to-[#16a34a] text-white rounded text-xs font-bold transition-all hover:from-[#4ade80] hover:to-[#22c55e] shadow-md"
                  >
                    Analyser
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default NetworkTable
