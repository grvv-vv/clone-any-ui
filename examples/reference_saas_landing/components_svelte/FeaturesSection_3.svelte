<script lang="ts">
  // FeaturesSection_3 Component
</script>

<section class="py-24 sm:py-32">
  <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-2xl text-center">
      <h2 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50">
        Infrastructure Built for Heavy Workloads
      </h2>
      <p class="mt-4 text-base text-zinc-600 dark:text-zinc-400">
        Zero cold starts. Sub-5ms context synchronization.
      </p>
    </div>
    <div class="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:grid-cols-2 lg:max-w-none lg:grid-cols-3">
      {#each [1, 2, 3] as item}
        <div class="rounded-2xl border border-zinc-200/80 bg-white p-8 shadow-sm dark:border-zinc-800/80 dark:bg-zinc-900">
          <div class="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600/10 text-blue-600 dark:text-blue-400">
            ⚡
          </div>
          <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-50">Feature Card {item}</h3>
          <p class="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
            High-fidelity responsive UI component with exact token mapping and accessibility standards.
          </p>
        </div>
      {/each}
    </div>
  </div>
</section>
