import React from 'react';

export function FeaturesSection_70() {
  return (
    <section id="features" className="py-24 sm:py-32">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50 animate-fade-in-up">
            AI and<br>automations
          </h2>
          <p className="mt-4 text-base text-zinc-600 dark:text-zinc-400">
            Build and deploy AI agents that work alongside you as teammates. Work on complex tasks together or delegate entire issues end-to-end.
          </p>
        </div>

        {/* Bento Grid with Exact Mirrored Visuals & Hover Physics */}
        <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:grid-cols-2 lg:max-w-none lg:grid-cols-3">
          {/* Card 1 */}
          <div className="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
            <div className="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
                <img
                  src="./assets/images/f_auto_fit_scale-down_me_37786.webp"
                  alt="Autonomous Parity Engine"
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
              what are the three most important customer requests around permissions? add them to the Access Controls project
            </p>
          </div>

          {/* Card 2 */}
          <div className="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
            <div className="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
                <img
                  src="./assets/images/f_auto_fit_scale-down_me_64363.webp"
                  alt="Linear"
                  className="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
                  loading="lazy"
                />
              </div>
            <h3 className="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
              <span>Fluid Spring Physics</span>
              <span className="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
                &rarr;
              </span>
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
              Three issues ranked by customer impact:
            </p>
          </div>

          {/* Card 3 */}
          <div className="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
            <div className="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
                <img
                  src="./assets/images/f_auto_fit_scale-down_me_64363.webp"
                  alt="Linear"
                  className="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
                  loading="lazy"
                />
              </div>
            <h3 className="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
              <span>WCAG AA Accessibility</span>
              <span className="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
                &rarr;
              </span>
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
              I’ve added them to Access Controls
            </p>
          </div>

          {/* Card 4 */}
          <div className="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
            <div className="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
                <img
                  src="./assets/images/f_auto_fit_scale-down_me_85069.webp"
                  alt="ChatPRD"
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
              add retry handling for failed image uploads described in this issue
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
