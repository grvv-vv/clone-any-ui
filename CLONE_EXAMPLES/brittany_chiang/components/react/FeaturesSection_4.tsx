import React from 'react';

export function FeaturesSection_4() {
  return (
    <section id="features" className="py-24 sm:py-32">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50 animate-fade-in-up">
            FeaturesSection_4 Title
          </h2>
          <p className="mt-4 text-base text-zinc-600 dark:text-zinc-400">
            Hi there! I'm Brittany, and I like building things. I'm a frontend engineer with expertise in crafting accessible, pixel-perfect user interfaces. I take pride in creating thoughtful, inclusive products and have a sharp eye for the little details that separate a good product from an exceptional one. I enjoy working most at the intersection of design and engineering, where great user experience meets clean, scalable code.
          </p>
        </div>

        {/* Bento Grid with Exact Mirrored Visuals & Hover Physics */}
        <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:grid-cols-2 lg:max-w-none lg:grid-cols-3">
          {/* Card 1 */}
          <div className="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
            <div className="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
                <img
                  src="/images/koroks/Elma.png"
                  alt="Background visual asset"
                  className="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
                  loading="lazy"
                />
              </div>
            <h3 className="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
              <span>Autonomous Parity Engine</span>
              <span className="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
                &rarr;
              </span>
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
              Currently, I'm a Senior Frontend Engineer at Klaviyo, where I work on our design system and help build new products, like Composer. I lead engineering efforts across our component library and frontend platform, partnering closely with designers and engineers to ensure accessibility is built into the foundation of everything we ship.
            </p>
          </div>

          {/* Card 2 */}
          <div className="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
            <div className="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600/10 text-xl text-blue-600 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6 dark:bg-blue-400/10 dark:text-blue-400">
                ⚡
              </div>
            <h3 className="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
              <span>Fluid Spring Physics</span>
              <span className="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
                &rarr;
              </span>
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
              In my spare time, you can usually find me climbing, playing tennis, hanging out with my wife and two cats, or running around Hyrule searching for Korok seedsKorok&nbsp;seeds.
            </p>
          </div>

          {/* Card 3 */}
          <div className="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
            <div className="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600/10 text-xl text-blue-600 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6 dark:bg-blue-400/10 dark:text-blue-400">
                ⚡
              </div>
            <h3 className="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
              <span>WCAG AA Accessibility</span>
              <span className="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
                &rarr;
              </span>
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
              Automatic focus rings, contrast checks, and prefers-reduced-motion accessibility safeguards.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
