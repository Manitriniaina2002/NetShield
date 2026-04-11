import React from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card'
import { Badge } from './ui/badge'

export function RecommendationPanel({ recommendations }) {
  const groupByPriority = {
    Critique: recommendations.filter(r => r.priority.includes('Critique')),
    Élevée: recommendations.filter(r => r.priority.includes('Élevée')),
    Moyen: recommendations.filter(r => r.priority.includes('Moyen')),
    Faible: recommendations.filter(r => r.priority.includes('Faible')),
  }

  const priorityVariant = (priority) => {
    if (priority === 'Critique') return 'destructive'
    if (priority === 'Élevée') return 'warning'
    if (priority === 'Moyen') return 'info'
    return 'success'
  }

  return (
    <Card>
      <CardHeader className="border-b border-slate-200">
        <CardTitle>Recommandations de sécurité</CardTitle>
        <CardDescription>{recommendations.length} action(s) proposées pour durcir les réseaux détectés.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {recommendations.length === 0 ? (
          <div className="py-10 text-center text-sm text-slate-500">Aucune recommandation disponible.</div>
        ) : (
          Object.entries(groupByPriority).map(([priority, recs]) =>
            recs.length > 0 && (
              <div key={priority} className="space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-base font-semibold text-slate-900">{priority}</h3>
                  <Badge variant={priorityVariant(priority)}>{recs.length}</Badge>
                </div>

                <div className="space-y-3">
                  {recs.map((rec, idx) => (
                    <div key={idx} className="rounded-2xl border border-slate-200 bg-slate-50/80 p-4">
                      <div className="space-y-2">
                        <h4 className="font-medium text-slate-900">{rec.title}</h4>
                        <p className="text-sm text-slate-600">{rec.description}</p>
                      </div>

                      <div className="mt-4 rounded-2xl border border-slate-200 bg-white p-4">
                        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-slate-500">Étapes à suivre</p>
                        <ol className="space-y-1 text-sm text-slate-600">
                          {rec.action_steps.slice(0, 3).map((step, i) => (
                            <li key={i} className="flex gap-2">
                              <span className="font-medium text-emerald-600">{i + 1}.</span>
                              <span>{step}</span>
                            </li>
                          ))}
                          {rec.action_steps.length > 3 && (
                            <li className="text-slate-400">… et {rec.action_steps.length - 3} autre(s) étape(s)</li>
                          )}
                        </ol>
                      </div>

                      <div className="mt-4 flex flex-wrap gap-3 text-xs text-slate-500">
                        <span><strong className="text-slate-700">Catégorie:</strong> {rec.category}</span>
                        <span><strong className="text-slate-700">Effort:</strong> {rec.estimated_effort}</span>
                        <span><strong className="text-slate-700">Impact:</strong> {rec.impact}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )
          )
        )}
      </CardContent>
    </Card>
  )
}

export default RecommendationPanel
