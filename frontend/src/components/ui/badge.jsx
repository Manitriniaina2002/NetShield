import React from 'react'
import { cn } from '../../lib/utils'

const variants = {
  default: 'border border-slate-300 bg-slate-100 text-slate-700 hover:bg-slate-200',
  primary: 'border border-primary-300 bg-primary-100 text-primary-700 hover:bg-primary-200',
  success: 'border border-accent-300 bg-accent-100 text-accent-700 hover:bg-accent-200',
  warning: 'border border-yellow-300 bg-yellow-100 text-yellow-700 hover:bg-yellow-200',
  destructive: 'border border-red-300 bg-red-100 text-red-700 hover:bg-red-200',
  error: 'border border-red-300 bg-red-100 text-red-700 hover:bg-red-200',
  info: 'border border-primary-300 bg-primary-100 text-primary-700 hover:bg-primary-200',
  outline: 'border-2 border-current text-current bg-transparent',
}

const sizes = {
  sm: 'px-2 py-0.5 text-xs',
  default: 'px-3 py-1 text-sm',
  lg: 'px-4 py-1.5 text-base',
}

export function Badge({ 
  className, 
  variant = 'default', 
  size = 'default',
  children,
  ...props 
}) {
  return (
    <span 
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full font-medium transition-colors duration-200 whitespace-nowrap',
        variants[variant],
        sizes[size],
        className
      )} 
      {...props}
    >
      {children}
    </span>
  )
}

export default Badge