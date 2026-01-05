/**
 * Footer Component
 */

import React from 'react';

export function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-sm text-gray-500">
            © 2024 PPR501 Final Project — Student Management System
          </p>
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <span>FastAPI + React + PostgreSQL</span>
            <span className="hidden sm:inline">•</span>
            <span className="hidden sm:inline">API returns XML</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
