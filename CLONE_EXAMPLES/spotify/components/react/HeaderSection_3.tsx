import React, { useState } from 'react';

export function HeaderSection_3() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-zinc-200/80 bg-white/80 backdrop-blur-md transition-all duration-300 dark:border-zinc-800/80 dark:bg-zinc-950/80">
      <div className="container mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand Logo with Interactive Tilt */}
        <a href="#" className="group flex items-center gap-2.5 font-bold text-xl tracking-tight text-zinc-900 dark:text-zinc-50 cursor-pointer">
          <span className="h-7 w-7 rounded-lg bg-blue-600 inline-flex items-center justify-center text-white text-xs font-black shadow-md shadow-blue-500/25 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6">
            ⚡
          </span>
          <span className="transition-colors duration-200 group-hover:text-blue-600 dark:group-hover:text-blue-400">Brand</span>
        </a>

        {/* Desktop Navigation with Animated Underline Effect */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-600 dark:text-zinc-400">
          <a href="#features" className="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Features</a>
          <a href="#pricing" className="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Pricing</a>
          <a href="#testimonials" className="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Testimonials</a>
        </nav>

        {/* Interactive CTA Button with Hover Physics */}
        <div className="hidden md:flex items-center gap-4">
          <button className="relative overflow-hidden rounded-xl bg-zinc-900 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all duration-300 ease-out hover:-translate-y-0.5 hover:shadow-lg hover:shadow-zinc-900/10 hover:bg-zinc-800 active:translate-y-0 active:scale-95 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200">
            Get Started
          </button>
        </div>

        {/* Mobile Drawer Toggle */}
        <button
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="md:hidden inline-flex items-center justify-center p-2 rounded-lg text-zinc-700 dark:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          aria-expanded={isMobileMenuOpen}
        >
          <span className="sr-only">Toggle navigation menu</span>
          <span className={`text-lg transition-transform duration-200 ${isMobileMenuOpen ? 'rotate-90' : ''}`}>
            {isMobileMenuOpen ? '✕' : '☰'}
          </span>
        </button>
      </div>

      {/* Mobile Drawer Menu with Smooth Entrance */}
      {isMobileMenuOpen && (
        <div className="md:hidden border-b border-zinc-200 dark:border-zinc-800 bg-white/95 dark:bg-zinc-950/95 px-6 pt-3 pb-6 space-y-3 animate-fade-in-down shadow-xl backdrop-blur-md">
          <a href="#features" className="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600 transition-colors">Features</a>
          <a href="#pricing" className="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600 transition-colors">Pricing</a>
          <a href="#testimonials" className="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600 transition-colors">Testimonials</a>
          <button className="w-full mt-2 rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white shadow-md hover:bg-blue-500 transition-all duration-200 active:scale-98">
            Get Started
          </button>
        </div>
      )}
    </header>
  );
}
