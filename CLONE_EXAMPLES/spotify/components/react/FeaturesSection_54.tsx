import React from 'react';

export function FeaturesSection_54() {
  return (
    <section id="features" className="py-24 sm:py-32">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50 animate-fade-in-up">
            Manage Consent Preferences
          </h2>
          <p className="mt-4 text-base text-zinc-600 dark:text-zinc-400">
            These cookies are necessary for the service to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the service will not then work.
          </p>
        </div>

        {/* Bento Grid with Exact Mirrored Visuals & Hover Physics */}
        <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:grid-cols-2 lg:max-w-none lg:grid-cols-3">
          {/* Card 1 */}
          <div className="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
            <div className="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600/10 text-xl text-blue-600 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6 dark:bg-blue-400/10 dark:text-blue-400">
                ⚡
              </div>
            <h3 className="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
              <span>Strictly Necessary Cookies</span>
              <span className="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
                &rarr;
              </span>
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
              These cookies enable us to provide enhanced functionality and personalisation. Without these cookies, some or all of these services may not function properly.
            </p>
          </div>

          {/* Card 2 */}
          <div className="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
            <div className="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600/10 text-xl text-blue-600 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6 dark:bg-blue-400/10 dark:text-blue-400">
                ⚡
              </div>
            <h3 className="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
              <span>First Party Functional Cookies</span>
              <span className="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
                &rarr;
              </span>
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
              These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our services. They help us to know which pages are the most and least popular and see how visitors move around the platform. Without these cookies, we are unable to monitor the performance of our services.
            </p>
          </div>

          {/* Card 3 */}
          <div className="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
            <div className="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600/10 text-xl text-blue-600 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6 dark:bg-blue-400/10 dark:text-blue-400">
                ⚡
              </div>
            <h3 className="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
              <span>First Party Performance Cookies</span>
              <span className="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
                &rarr;
              </span>
            </h3>
            <p className="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
              These cookies may be used to deliver targeted advertisements and to build a profile of your interests. If you do not allow these cookies you will still experience advertising but it will be less tailored to you.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
