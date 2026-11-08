import React from 'react';

export function HeroSection_2() {
  return (
    <section className="relative overflow-hidden py-24 sm:py-32">
      {/* Ambient Animated Background Glow */}
      <div className="pointer-events-none absolute -top-40 left-1/2 -z-10 -translate-x-1/2 transform-gpu overflow-hidden blur-3xl" aria-hidden="true">
        <div className="aspect-[1155/678] w-[68rem] bg-gradient-to-tr from-blue-600 to-cyan-400 opacity-20 animate-pulse-glow" />
      </div>

      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          {/* Floating Badge with Live Ping Indicator */}
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-1.5 text-xs font-semibold text-blue-600 dark:text-blue-400 shadow-sm backdrop-blur-sm animate-float">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex h-2 w-2 rounded-full bg-blue-500"></span>
            </span>
            <span>✨ Autonomous Replication Ready</span>
          </div>

          {/* Staggered Animated Headline */}
          <h1 className="text-4xl font-extrabold tracking-tight text-zinc-900 sm:text-6xl dark:text-zinc-50 leading-[1.1] animate-fade-in-up">
            What's on your mind?
          </h1>

          {/* Subtitle with Subtle Delay */}
          <p className="mt-6 text-lg leading-8 text-zinc-600 dark:text-zinc-400 animate-fade-in-up [animation-delay:150ms]">
            Biryani
          </p>

          {/* Interactive CTA Button Group */}
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4 animate-fade-in-up [animation-delay:300ms]">
            <button className="relative overflow-hidden rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/25 transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-xl hover:shadow-blue-500/35 hover:bg-blue-500 active:translate-y-0 active:scale-95">
              ←
            </button>
            <a href="#demo" className="group inline-flex items-center gap-1.5 text-sm font-semibold leading-6 text-zinc-900 transition-all duration-200 hover:text-blue-600 hover:translate-x-1 dark:text-zinc-50 dark:hover:text-blue-400">
              Live Interactive Demo <span className="transition-transform duration-200 group-hover:translate-x-1">&rarr;</span>
            </a>
          </div>
        </div>

        {/* Exact Mirrored Hero Image Showcase with Ambient Glow */}
        <div className="mt-14 relative mx-auto max-w-5xl overflow-hidden rounded-2xl border border-zinc-200/80 bg-zinc-900/5 p-2 shadow-2xl backdrop-blur-sm transition-all duration-500 ease-out hover:shadow-blue-500/10 hover:border-zinc-300 dark:border-zinc-800/80 dark:bg-zinc-900/50">
          <img
            src="https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=280&auto=format&fit=crop&q=80"
            alt="Biryani"
            className="w-full rounded-xl object-cover shadow-inner transition-transform duration-700 ease-out hover:scale-[1.01]"
            loading="eager"
          />
        </div>

        {/* Continuous Infinite Logo Marquee Ticker */}
        <div className="mt-20 w-full overflow-hidden border-y border-zinc-200/60 dark:border-zinc-800/60 py-6">
          <p className="text-center text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-4">
            Trusted by world-class frontend teams
          </p>
          <div className="flex gap-12 items-center whitespace-nowrap animate-marquee">
            <img src="https://images.unsplash.com/photo-1513104890138-7c749659a591?w=280&auto=format&fit=crop&q=80" alt="Pizza" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
            <img src="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=280&auto=format&fit=crop&q=80" alt="Burger" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
            <img src="https://images.unsplash.com/photo-1630383249896-424e482df921?w=280&auto=format&fit=crop&q=80" alt="North Indian" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
            <img src="https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=280&auto=format&fit=crop&q=80" alt="South Indian Dosa" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
            <img src="https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=280&auto=format&fit=crop&q=80" alt="Cake Desserts" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
            <img src="https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=280&auto=format&fit=crop&q=80" alt="Rolls & Wraps" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
            <img src="https://images.unsplash.com/photo-1513104890138-7c749659a591?w=280&auto=format&fit=crop&q=80" alt="Pizza" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
            <img src="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=280&auto=format&fit=crop&q=80" alt="Burger" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
            <img src="https://images.unsplash.com/photo-1630383249896-424e482df921?w=280&auto=format&fit=crop&q=80" alt="North Indian" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
            <img src="https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=280&auto=format&fit=crop&q=80" alt="South Indian Dosa" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
            <img src="https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=280&auto=format&fit=crop&q=80" alt="Cake Desserts" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
            <img src="https://images.unsplash.com/photo-1541696432-82c6da8ce7bf?w=280&auto=format&fit=crop&q=80" alt="Rolls & Wraps" className="h-7 max-h-7 w-auto object-contain grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all duration-300" />
          </div>
        </div>
      </div>
    </section>
  );
}
