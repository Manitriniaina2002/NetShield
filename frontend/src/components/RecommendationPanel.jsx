import React from 'react'

export function RecommendationPanel({ recommendations }) {
  const getPriorityColor = (priority) => {
    if (priority.includes('Critique')) return 'bg-red-900 text-red-200 border-red-700'
    if (priority.includes('Élevée')) return 'bg-orange-900 text-orange-200 border-orange-700'
    if (priority.includes('Moyen')) return 'bg-yellow-900 text-yellow-200 border-yellow-700'
    return 'bg-green-900 text-green-200 border-green-700'
  }

  const groupByPriority = {
    'Critique': recommendations.filter(r => r.priority.includes('Critique')),
    'Élevée': recommendations.filter(r => r.priority.includes('Élevée')),
    'Moyen': recommendations.filter(r => r.priority.includes('Moyen')),
    'Faible': recommendations.filter(r => r.priority.includes('Faible'))
  }

  return (
    <div className="card">
      <h2 className="text-xl font-bold mb-4 text-[#33cc00] font-mono uppercase tracking-wider">
        ▬ Recommandations de Sécurité
        <span className="text-sm text-[#9ca3af] ml-2 font-mono">({recommendations.length} actions)</span>
      </h2>

      {recommendations.length === 0 ? (
        <p className="text-[#9ca3af] text-center py-8 font-mono">
          Aucune recommandation disponible.
        </p>
      ) : (
        <div className="space-y-6">
          {Object.entries(groupByPriority).map(([priority, recs]) => {
            const priorityConfig = {
              'Critique': { bg: 'bg-[#ef4444]/15', border: 'border-l-[#ef4444]', icon: '●', text: 'text-[#fca5a5]' },
              'Élevée': { bg: 'bg-[#f59e0b]/15', border: 'border-l-[#f59e0b]', icon: '◐', text: 'text-[#fbbf24]' },
              'Moyen': { bg: 'bg-[#eab308]/15', border: 'border-l-[#eab308]', icon: '◑', text: 'text-[#fde047]' },
              'Faible': { bg: 'bg-[#10b981]/15', border: 'border-l-[#10b981]', icon: '◯', text: 'text-[#34d399]' }
            }
            const config = priorityConfig[priority]
            
            return recs.length > 0 && (
              <div key={priority}>
                <h3 className={`text-lg font-bold font-mono mb-3 flex items-center gap-2 uppercase tracking-wider ${config.text}`}>
                  {config.icon}
                  {priority} ({recs.length})
                </h3>

                <div className="space-y-3">
                  {recs.map((rec, idx) => (
                    <div key={idx} className={`border-l-4 p-4 rounded ${config.border} ${config.bg} border border-[#2a2f4a]`}>
                      <h4 className="font-mono font-bold text-[#e5e7eb] mb-2">{rec.title}</h4>
                      <p className="text-sm text-[#9ca3af] mb-3 font-mono">{rec.description}</p>

                      <div className="bg-[#0a0e27]/50 rounded p-3 mb-3 border border-[#2a2f4a]">
                        <p className="text-xs font-bold text-[#33cc00] mb-2 uppercase tracking-wider">• Étapes à suivre:</p>
                        <ol className="text-sm text-[#9ca3af] space-y-1 font-mono">
                          {rec.action_steps.slice(0, 3).map((step, i) => (
                            <li key={i} className="flex gap-2">
                              <span className="font-bold text-[#33cc00]">{i + 1}.</span>
                              <span>{step}</span>
                            </li>
                          ))}
                          {rec.action_steps.length > 3 && (
                            <li className="text-[#9ca3af] italic">... et {rec.action_steps.length - 3} autre(s) étape(s)</li>
                          )}
                        </ol>
                      </div>

                      <div className="flex gap-4 text-xs text-[#9ca3af] font-mono flex-wrap">
                        <span><strong className="text-[#33cc00]">Catégorie:</strong> {rec.category}</span>
                        <span><strong className="text-[#33cc00]">Effort:</strong> {rec.estimated_effort}</span>
                        <span><strong className="text-[#33cc00]">Impact:</strong> {rec.impact}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default RecommendationPanel
