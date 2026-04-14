import React from 'react'
import { cn } from '../../lib/utils'

const variantClasses = {
  default: 'bg-primary-600 text-white hover:bg-primary-700 shadow-md hover:shadow-lg active:shadow-sm active:scale-95 transition-all',
  primary: 'bg-primary-600 text-white hover:bg-primary-700 shadow-md hover:shadow-lg active:shadow-sm active:scale-95 transition-all',
  secondary: 'border border-slate-300 bg-white text-slate-900 hover:bg-slate-50 shadow-sm hover:shadow-md active:scale-95 transition-all',
  success: 'bg-accent-600 text-white hover:bg-accent-700 shadow-md hover:shadow-lg active:shadow-sm active:scale-95 transition-all',
  outline: 'border-2 border-primary-300 bg-transparent text-primary-700 hover:bg-primary-50 active:scale-95 transition-all',
  destructive: 'bg-red-600 text-white hover:bg-red-700 shadow-md hover:shadow-lg active:shadow-sm active:scale-95 transition-all',
  danger: 'bg-red-600 text-white hover:bg-red-700 shadow-md hover:shadow-lg active:shadow-sm active:scale-95 transition-all',
  warning: 'bg-yellow-600 text-white hover:bg-yellow-700 shadow-md hover:shadow-lg active:shadow-sm active:scale-95 transition-all',
  ghost: 'bg-transparent text-slate-700 hover:bg-slate-100 active:scale-95 transition-all',
  link: 'text-primary-600 underline-offset-4 hover:underline transition-colors',
}

const sizeClasses = {
  xs: 'h-8 px-2.5 text-xs rounded-md',
  sm: 'h-9 px-3 text-sm rounded-lg',
  default: 'h-10 px-4 py-2 rounded-lg text-sm',
  md: 'h-11 px-5 text-base rounded-lg',
  lg: 'h-12 px-6 text-base rounded-lg',
  xl: 'h-14 px-8 text-lg rounded-xl',
  icon: 'h-10 w-10 p-0 rounded-lg',
  'icon-sm': 'h-8 w-8 p-0 rounded-md',
  'icon-lg': 'h-12 w-12 p-0 rounded-lg',
}

export function Button({ 
  className, 
  variant = 'default', 
  size = 'default', 
  asChild = false,
  loading = false,
  disabled = false,
  ...props 
}) {
  const Comp = asChild ? 'span' : 'button'

  return (
    <Comp
      className={cn(
        'inline-flex items-center justify-center gap-2 font-medium transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 disabled:cursor-not-allowed',
        variantClasses[variant] || variantClasses.default,
        sizeClasses[size] || sizeClasses.default,
        className,
      )}
      disabled={loading || disabled}
      {...props}
    >
      {loading && (
        <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      )}
      {props.children}
    </Comp>
  )
}

export default Button