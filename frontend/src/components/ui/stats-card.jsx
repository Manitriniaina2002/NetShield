import React from 'react'
import { MdTrendingUp, MdTrendingDown } from 'react-icons/md'

export function StatsCard({ 
  title, 
  value, 
  subtitle, 
  icon: Icon = null,
  trend = null,
  color = 'primary',
  size = 'default'
}) {
  const sizeClasses = {
    sm: 'p-4',
    default: 'p-6',
    lg: 'p-8'
  }

  const bgClasses = {
    primary: 'from-primary-50 to-primary-100/50',
    success: 'from-accent-50 to-accent-100/50',
    warning: 'from-yellow-50 to-yellow-100/50',
    danger: 'from-red-50 to-red-100/50',
    info: 'from-sky-50 to-sky-100/50'
  }

  const textClasses = {
    primary: 'text-primary-700',
    success: 'text-accent-700',
    warning: 'text-yellow-700',
    danger: 'text-red-700',
    info: 'text-sky-700'
  }

  const borderClasses = {
    primary: 'border-primary-200',
    success: 'border-accent-200',
    warning: 'border-yellow-200',
    danger: 'border-red-200',
    info: 'border-sky-200'
  }

  return (
    <div className={`card group overflow-hidden transition-all hover:shadow-lg hover:-translate-y-1 ${sizeClasses[size]} bg-gradient-to-br ${bgClasses[color]} border-2 ${borderClasses[color]}`}>
      <div className="flex items-start justify-between mb-4">
        {Icon && (
          <div className={`p-2.5 rounded-lg bg-white/50 group-hover:bg-white transition-colors`}>
            <Icon className={`w-6 h-6 ${textClasses[color]}`} />
          </div>
        )}
        {trend && (
          <div className={`px-2.5 py-1 rounded font-medium text-xs flex items-center gap-1 ${trend.up ? 'bg-accent-100 text-accent-700' : 'bg-red-100 text-red-700'}`}>
            {trend.up ? <MdTrendingUp className="text-base" /> : <MdTrendingDown className="text-base" />} {trend.value}%
          </div>
        )}
      </div>
      
      <div>
        <p className={`text-sm font-medium ${textClasses[color]}`}>{title}</p>
        <p className="text-3xl font-bold text-slate-900 mt-2">{value}</p>
        {subtitle && (
          <p className="text-xs text-slate-600 mt-2">{subtitle}</p>
        )}
      </div>
    </div>
  )
}

export default StatsCard
