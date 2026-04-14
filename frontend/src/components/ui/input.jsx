import React, { useState } from 'react'
import { cn } from '../../lib/utils'

export function Input({ 
  className, 
  error = false, 
  success = false, 
  icon: Icon = null,
  iconPosition = 'left',
  type = 'text',
  ...props 
}) {
  const [focused, setFocused] = useState(false)

  const inputClasses = cn(
    'w-full px-4 py-2.5 rounded-lg border-2 bg-white text-slate-900 font-normal shadow-sm outline-none',
    'placeholder:text-slate-400 transition-all duration-200',
    'focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 focus:shadow-md',
    'disabled:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50',
    'hover:border-slate-300',
    error ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' :
    success ? 'border-accent-500 focus:border-accent-500 focus:ring-accent-500/20' :
    'border-slate-200',
    Icon && iconPosition === 'left' ? 'pl-10' : '',
    Icon && iconPosition === 'right' ? 'pr-10' : '',
    className
  )

  return (
    <div className="relative w-full">
      {Icon && (
        <div className={cn(
          'absolute top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none',
          iconPosition === 'left' ? 'left-3' : 'right-3'
        )}>
          <Icon className="w-5 h-5" />
        </div>
      )}
      <input 
        type={type}
        className={inputClasses}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        {...props} 
      />
    </div>
  )
}

export default Input