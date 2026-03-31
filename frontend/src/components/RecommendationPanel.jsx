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
      <h2 className="text-xl font-bold mb-4 text-white">
        Recommandations de Sécurité
        <span className="text-sm text-gray-400 ml-2">({recommendations.length} actions)</span>
      </h2>

      {recommendations.length === 0 ? (
        <p className="text-gray-400 text-center py-8">
          Aucune recommandation disponible.
        </p>
      ) : (
        <div className="space-y-6">
          {Object.entries(groupByPriority).map(([priority, recs]) => (
            recs.length > 0 && (
              <div key={priority}>
                <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                  {priority === 'Critique' && '🔴'}
                  {priority === 'Élevée' && '🟠'}
                  {priority === 'Moyen' && '🟡'}
                  {priority === 'Faible' && '🟢'}
                  {priority} ({recs.length})
                </h3>

                <div className="space-y-3">
                  {recs.map((rec, idx) => (
                    <div key={idx} className={`border-l-4 p-4 rounded bg-gray-900 ${getPriorityColor(rec.priority)}`}>
                      <h4 className="font-semibold text-white mb-2">{rec.title}</h4>
                      <p className="text-sm text-gray-300 mb-3">{rec.description}</p>

                      <div className="bg-black bg-opacity-20 rounded p-3 mb-3">
                        <p className="text-xs font-semibold text-gray-300 mb-1">Étapes à suivre:</p>
                        <ol className="text-sm text-gray-400 space-y-1">
                          {rec.action_steps.slice(0, 3).map((step, i) => (
                            <li key={i} className="flex gap-2">
                              <span className="font-semibold">{i + 1}.</span>
                              <span>{step}</span>
                            </li>
                          ))}
                          {rec.action_steps.length > 3 && (
                            <li className="text-gray-500 italic">... et {rec.action_steps.length - 3} autre(s) étape(s)</li>
                          )}
                        </ol>
                      </div>

                      <div className="flex gap-4 text-xs text-gray-400">
                        <span><strong>Catégorie:</strong> {rec.category}</span>
                        <span><strong>Effort:</strong> {rec.estimated_effort}</span>
                        <span><strong>Impact:</strong> {rec.impact}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )
          ))}
        </div>
      )}
    </div>
  )
}

export default RecommendationPanel
