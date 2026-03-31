import React from 'react'

export function NetworkTable({ networks, onSelectNetwork }) {
  return (
    <div className="card overflow-x-auto">
      <h2 className="text-xl font-bold mb-4 text-white">Réseaux Détectés</h2>
      
      {networks.length === 0 ? (
        <p className="text-gray-400 text-center py-8">
          Aucun réseau détecté. Lancez un scan d'abord.
        </p>
      ) : (
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-600 bg-gray-900">
              <th className="text-left px-4 py-3 text-gray-300">SSID</th>
              <th className="text-left px-4 py-3 text-gray-300">BSSID</th>
              <th className="text-center px-4 py-3 text-gray-300">Canal</th>
              <th className="text-center px-4 py-3 text-gray-300">Sécurité</th>
              <th className="text-center px-4 py-3 text-gray-300">Signal</th>
              <th className="text-center px-4 py-3 text-gray-300">Clients</th>
              <th className="text-center px-4 py-3 text-gray-300">Action</th>
            </tr>
          </thead>
          <tbody>
            {networks.map((net, idx) => (
              <tr key={idx} className="table-row">
                <td className="px-4 py-3 font-mono text-white">{net.ssid || '(Hidden)'}</td>
                <td className="px-4 py-3 font-mono text-gray-400 text-xs">{net.bssid}</td>
                <td className="text-center px-4 py-3 text-gray-300">{net.channel}</td>
                <td className="text-center px-4 py-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    net.security === 'Open' ? 'bg-red-900 text-red-200' :
                    net.security === 'WEP' ? 'bg-red-900 text-red-200' :
                    net.security === 'WPA' ? 'bg-orange-900 text-orange-200' :
                    net.security === 'WPA2' ? 'bg-yellow-900 text-yellow-200' :
                    'bg-green-900 text-green-200'
                  }`}>
                    {net.security}
                  </span>
                </td>
                <td className="text-center px-4 py-3">
                  <div className="flex justify-center gap-2">
                    <span className="text-gray-300 font-mono">{net.signal_percentage || 0}%</span>
                    <span className="text-gray-400">{net.signal_strength}dBm</span>
                  </div>
                </td>
                <td className="text-center px-4 py-3 text-gray-300">{net.clients || 0}</td>
                <td className="text-center px-4 py-3">
                  <button
                    onClick={() => onSelectNetwork(net)}
                    className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs transition-colors"
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
