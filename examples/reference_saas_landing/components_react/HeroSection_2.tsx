import React from 'react';

export function HeroSection_2() {
  return (
    <section className="relative overflow-hidden py-24 sm:py-32">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1 text-xs font-medium text-blue-600 dark:text-blue-400">
            <span>✨ New Release</span>
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight text-zinc-900 sm:text-6xl dark:text-zinc-50">
            Distributed AI Pipelines Engineered for Real-Time Execution
          </h1>
          <p className="mt-6 text-lg leading-8 text-zinc-600 dark:text-zinc-400">
            Deploy multi-agent swarms with self-healing task queues, sub-millisecond inference routing, and automated cluster elasticity.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <button className="rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white shadow-md hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600 transition">
              Start Building Free &rarr;
            </button>
            <a href="#demo" className="text-sm font-semibold leading-6 text-zinc-900 dark:text-zinc-50 hover:underline">
              Live Demo &rarr;
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
