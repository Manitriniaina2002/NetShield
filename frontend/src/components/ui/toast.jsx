import React from 'react'
import { MdCheckCircle, MdError, MdWarning, MdInfo, MdClose } from 'react-icons/md'

export function Toast({ 
  message, 
  type = 'info',
  onClose = null,
  duration = 4000,
  action = null
}) {
  React.useEffect(() => {
    if (duration && onClose) {
      const timer = setTimeout(onClose, duration)
      return () => clearTimeout(timer)
    }
  }, [duration, onClose])

  const typeClasses = {
    success: {
      bg: 'bg-accent-50 border-accent-300',
      icon: MdCheckCircle,
      text: 'text-accent-900',
      button: 'bg-accent-100 hover:bg-accent-200'
    },
    error: {
      bg: 'bg-red-50 border-red-300',
      icon: MdError,
      text: 'text-red-900',
      button: 'bg-red-100 hover:bg-red-200'
    },
    warning: {
      bg: 'bg-yellow-50 border-yellow-300',
      icon: MdWarning,
      text: 'text-yellow-900',
      button: 'bg-yellow-100 hover:bg-yellow-200'
    },
    info: {
      bg: 'bg-primary-50 border-primary-300',
      icon: MdInfo,
      text: 'text-primary-900',
      button: 'bg-primary-100 hover:bg-primary-200'
    }
  }

  const styles = typeClasses[type] || typeClasses.info
  const IconComponent = styles.icon

  return (
    <div className={`animate-fade-up fixed bottom-6 right-6 max-w-sm border-l-4 rounded-lg shadow-lg p-4 ${styles.bg} ${styles.text} flex items-start gap-3 z-50`}>
      <IconComponent className="text-xl flex-shrink-0 mt-1" />
      <div className="flex-1">
        <p className="font-medium">{message}</p>
      </div>
      <div className="flex gap-2 flex-shrink-0">
        {action && (
          <button 
            onClick={action.onClick}
            className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${styles.button}`}
          >
            {action.label}
          </button>
        )}
        {onClose && (
          <button 
            onClick={onClose}
            className={`px-3 py-1.5 rounded text-sm transition-colors ${styles.button}`}
          >
            <MdClose />
          </button>
        )}
      </div>
    </div>
  )
}

export default Toast
