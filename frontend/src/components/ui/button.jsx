import React from 'react'
import { cn } from '../../lib/utils'

const variantClasses = {
  default: 'bg-emerald-600 text-white hover:bg-emerald-500 shadow-sm',
  secondary: 'border border-slate-200 bg-white text-slate-900 hover:bg-slate-50 shadow-sm',
  outline: 'border border-slate-200 bg-transparent text-slate-900 hover:bg-slate-50',
  destructive: 'bg-rose-600 text-white hover:bg-rose-500 shadow-sm',
  ghost: 'bg-transparent text-slate-700 hover:bg-slate-100',
}

const sizeClasses = {
  default: 'h-10 px-4 py-2',
  sm: 'h-9 px-3 text-sm',
  lg: 'h-11 px-6',
  icon: 'h-10 w-10 p-0',
}

export function Button({ className, variant = 'default', size = 'default', asChild = false, ...props }) {
  const Comp = asChild ? 'span' : 'button'

  return (
    <Comp
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-xl text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
        variantClasses[variant],
        sizeClasses[size],
        className,
      )}
      {...props}
    />
  )
}

export default Button