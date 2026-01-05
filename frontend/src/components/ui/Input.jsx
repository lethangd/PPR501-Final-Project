/**
 * Input Component
 * 
 * Text input với label và error state.
 */

import React from 'react';
import clsx from 'clsx';

/**
 * @param {Object} props
 * @param {string} props.label
 * @param {string} props.error
 * @param {string} props.hint
 */
export function Input({
  label,
  error,
  hint,
  className,
  id,
  ...props
}) {
  const inputId = id || `input-${label?.toLowerCase().replace(/\s+/g, '-')}`;
  
  return (
    <div className="space-y-1">
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-gray-700"
        >
          {label}
        </label>
      )}
      
      <input
        id={inputId}
        className={clsx(
          'block w-full px-3 py-2 text-sm',
          'border rounded-lg transition-colors duration-200',
          'placeholder:text-gray-400',
          'focus:outline-none focus:ring-2 focus:ring-offset-0',
          'disabled:bg-gray-100 disabled:cursor-not-allowed',
          error
            ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
            : 'border-gray-300 focus:border-primary-500 focus:ring-primary-500',
          className
        )}
        {...props}
      />
      
      {hint && !error && (
        <p className="text-xs text-gray-500">{hint}</p>
      )}
      
      {error && (
        <p className="text-xs text-red-600">{error}</p>
      )}
    </div>
  );
}
