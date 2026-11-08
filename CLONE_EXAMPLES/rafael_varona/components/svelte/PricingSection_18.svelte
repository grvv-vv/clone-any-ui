<script lang="ts">
  let isAnnual = true;
</script>

<section id="pricing" class="py-24 sm:py-32 bg-zinc-50/50 dark:bg-zinc-900/30">
  <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-2xl text-center">
      <h2 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50">
        PricingSection_18 Title
      </h2>
      <p class="mt-4 text-base text-zinc-600 dark:text-zinc-400">
        Subtext or descriptive copy supporting the primary message.
      </p>

      <div class="mt-8 flex items-center justify-center gap-3">
        <span class="text-sm font-medium text-zinc-600 dark:text-zinc-400">Monthly</span>
        <button
          on:click={() => isAnnual = !isAnnual}
          class="relative inline-flex h-7 w-12 shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-zinc-300 transition-colors duration-300 ease-out focus:outline-none dark:bg-zinc-700"
          role="switch"
          aria-checked={isAnnual}
        >
          <span class="inline-block h-6 w-6 transform rounded-full bg-white shadow-md transition-transform duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] {isAnnual ? 'translate-x-5 !bg-blue-600' : 'translate-x-0'}" />
        </button>
        <span class="text-sm font-medium text-zinc-900 dark:text-zinc-50">
          Annual <span class="inline-block rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-xs font-semibold text-emerald-600 dark:text-emerald-400 animate-pulse">Save 20%</span>
        </span>
      </div>
    </div>

    <div class="mx-auto mt-16 grid max-w-lg grid-cols-1 gap-8 lg:max-w-4xl lg:grid-cols-2">
      <div class="group rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl dark:border-zinc-800 dark:bg-zinc-900">
        <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Starter</h3>
        <p class="mt-4 text-4xl font-bold text-zinc-900 dark:text-zinc-50">
          {isAnnual ? '$24' : '$29'}<span class="text-sm font-normal text-zinc-500">/mo</span>
        </p>
        <p class="mt-2 text-sm text-zinc-500">For individuals and rapid prototyping.</p>
        <button class="mt-8 w-full rounded-xl border border-zinc-300 py-3 text-sm font-semibold transition-all duration-200 hover:bg-zinc-50 hover:border-zinc-400 active:scale-98 dark:border-zinc-700 dark:hover:bg-zinc-800">
          Get Started
        </button>
      </div>

      <div class="group relative rounded-2xl border-2 border-blue-600 bg-white p-8 shadow-lg shadow-blue-500/10 transition-all duration-300 ease-out hover:-translate-y-2.5 hover:shadow-2xl hover:shadow-blue-500/25 dark:bg-zinc-900">
        <span class="absolute -top-3.5 right-6 rounded-full bg-blue-600 px-3.5 py-1 text-xs font-bold text-white shadow-md animate-pulse">
          Most Popular
        </span>
        <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Pro</h3>
        <p class="mt-4 text-4xl font-bold text-zinc-900 dark:text-zinc-50">
          {isAnnual ? '$69' : '$79'}<span class="text-sm font-normal text-zinc-500">/mo</span>
        </p>
        <p class="mt-2 text-sm text-zinc-500">For growing engineering teams requiring full parity.</p>
        <button class="mt-8 w-full rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white shadow-md shadow-blue-500/25 transition-all duration-300 hover:bg-blue-500 hover:shadow-lg hover:shadow-blue-500/35 active:scale-98">
          Upgrade to Pro
        </button>
      </div>
    </div>
  </div>
</section>
