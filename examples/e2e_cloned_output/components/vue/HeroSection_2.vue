<script setup lang="ts">
const brands = ['Acme Corp', 'NextScale', 'HyperFlow', 'Veloce', 'CloudMesh', 'ApexCore', 'Acme Corp', 'NextScale', 'HyperFlow', 'Veloce', 'CloudMesh', 'ApexCore'];
</script>

<template>
  <section class="relative overflow-hidden py-24 sm:py-32">
    <div class="pointer-events-none absolute -top-40 left-1/2 -z-10 -translate-x-1/2 transform-gpu overflow-hidden blur-3xl" aria-hidden="true">
      <div class="aspect-[1155/678] w-[68rem] bg-gradient-to-tr from-blue-600 to-cyan-400 opacity-20 animate-pulse-glow" />
    </div>

    <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-3xl text-center">
        <div class="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-1.5 text-xs font-semibold text-blue-600 dark:text-blue-400 shadow-sm backdrop-blur-sm animate-float">
          <span class="relative flex h-2 w-2">
            <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75"></span>
            <span class="relative inline-flex h-2 w-2 rounded-full bg-blue-500"></span>
          </span>
          <span>✨ Autonomous Replication Ready</span>
        </div>

        <h1 class="text-4xl font-extrabold tracking-tight text-zinc-900 sm:text-6xl dark:text-zinc-50 leading-[1.1] animate-fade-in-up">
          Distributed AI Pipelines Engineered for Real-Time Execution
        </h1>

        <p class="mt-6 text-lg leading-8 text-zinc-600 dark:text-zinc-400 animate-fade-in-up [animation-delay:150ms]">
          Deploy multi-agent swarms with self-healing task queues, sub-millisecond inference routing, and automated cluster elasticity.
        </p>

        <div class="mt-10 flex flex-wrap items-center justify-center gap-4 animate-fade-in-up [animation-delay:300ms]">
          <button class="relative overflow-hidden rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/25 transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-xl hover:shadow-blue-500/35 hover:bg-blue-500 active:translate-y-0 active:scale-95">
            Start Building Free &rarr;
          </button>
          <a href="#demo" class="group inline-flex items-center gap-1.5 text-sm font-semibold leading-6 text-zinc-900 transition-all duration-200 hover:text-blue-600 hover:translate-x-1 dark:text-zinc-50 dark:hover:text-blue-400">
            Live Interactive Demo <span class="transition-transform duration-200 group-hover:translate-x-1">&rarr;</span>
          </a>
        </div>
      </div>


      <div class="mt-20 w-full overflow-hidden border-y border-zinc-200/60 dark:border-zinc-800/60 py-6">
        <p class="text-center text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-4">
          Trusted by world-class frontend teams
        </p>
        <div class="flex gap-12 whitespace-nowrap animate-marquee">
          <span v-for="(b, i) in brands" :key="i" class="text-sm font-semibold text-zinc-400 hover:text-zinc-900 dark:text-zinc-500 dark:hover:text-zinc-100 transition-colors cursor-default">
            {{ b }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>
