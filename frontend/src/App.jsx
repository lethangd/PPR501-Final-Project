/**
 * App Component
 * 
 * Root component của ứng dụng.
 * Layout chính với Header, Main content, và Footer.
 */

import React from 'react';
import { Header, Footer } from './components/layout';
import { HomePage } from './pages';

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <Header />
      
      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <HomePage />
      </main>
      
      {/* Footer */}
      <Footer />
    </div>
  );
}
