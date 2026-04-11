import React from 'react'
import { cn } from '../../lib/utils'

const variants = {
  default: 'border-slate-200 bg-slate-50 text-slate-700',
  success: 'border-emerald-200 bg-emerald-50 text-emerald-700',
  warning: 'border-amber-200 bg-amber-50 text-amber-700',
  destructive: 'border-rose-200 bg-rose-50 text-rose-700',
  info: 'border-sky-200 bg-sky-50 text-sky-700',
}

export function Badge({ className, variant = 'default', ...props }) {
  return <span className={cn('inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium', variants[variant], className)} {...props} />
}

export default Badge