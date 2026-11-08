<script setup lang="ts">
// FeaturesSection_3 Component
</script>

<template>
  <section id="features" class="py-24 sm:py-32">
    <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-2xl text-center">
        <h2 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50 animate-fade-in-up">
          Top restaurant chains in Bangalore
        </h2>
        <p class="mt-4 text-base text-zinc-600 dark:text-zinc-400">
          Pizzas, Fast Food, Pastas
        </p>
      </div>

      <div class="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:grid-cols-2 lg:max-w-none lg:grid-cols-3">
        <!-- Card 1 -->
        <div class="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
          <div class="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
            <img
              src="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&auto=format&fit=crop&q=80"
              alt="Pizza Hut"
              class="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
              loading="lazy"
            />
          </div>
          <h3 class="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
            <span>Pizza Hut</span>
            <span class="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
              &rarr;
            </span>
          </h3>
          <p class="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
            Koramangala
          </p>
        </div>

        <!-- Card 2 -->
        <div class="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
          <div class="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
            <img
              src="https://images.unsplash.com/photo-1550547660-d9450f859349?w=600&auto=format&fit=crop&q=80"
              alt="Burger King"
              class="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
              loading="lazy"
            />
          </div>
          <h3 class="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
            <span>Burger King</span>
            <span class="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
              &rarr;
            </span>
          </h3>
          <p class="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
            Burgers, American, Shakes
          </p>
        </div>

        <!-- Card 3 -->
        <div class="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
          <div class="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
            <img
              src="https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=600&auto=format&fit=crop&q=80"
              alt="Meghana Foods"
              class="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
              loading="lazy"
            />
          </div>
          <h3 class="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
            <span>Meghana Foods</span>
            <span class="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
              &rarr;
            </span>
          </h3>
          <p class="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
            Indiranagar
          </p>
        </div>

        <!-- Card 4 -->
        <div class="group relative overflow-hidden rounded-2xl border border-zinc-200/80 bg-white p-6 shadow-sm transition-all duration-300 ease-out hover:-translate-y-2 hover:shadow-xl hover:shadow-zinc-900/5 hover:border-blue-500/40 dark:border-zinc-800/80 dark:bg-zinc-900 dark:hover:border-blue-500/40">
          <div class="relative mb-5 h-44 w-full overflow-hidden rounded-xl bg-zinc-100 dark:bg-zinc-800">
            <img
              src="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&auto=format&fit=crop&q=80"
              alt="KFC Chicken"
              class="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
              loading="lazy"
            />
          </div>
          <h3 class="flex items-center justify-between text-lg font-semibold text-zinc-900 dark:text-zinc-50">
            <span>KFC</span>
            <span class="text-blue-600 opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
              &rarr;
            </span>
          </h3>
          <p class="mt-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
            Biryani, Andhra, South Indian
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
