/**
 * Header Component
 * 
 * Header của ứng dụng với branding và navigation.
 */

import React from 'react';
import { AcademicCapIcon } from '@heroicons/react/24/solid';

export function Header() {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Title */}
          <div className="flex items-center gap-3">
            <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-primary-500 to-purple-600 rounded-xl flex items-center justify-center">
              <AcademicCapIcon className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-900">
                Student Management
              </h1>
              <p className="text-xs text-gray-500 -mt-0.5">
                PPR501 Final Project
              </p>
            </div>
          </div>

          {/* Right side - API info */}
          <div className="flex items-center gap-4">
            <span className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-700 text-xs font-medium">
              <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
              API: XML
            </span>
            <a
              href="/api/students"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-primary-600 hover:text-primary-700 font-medium"
            >
              View XML →
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}
