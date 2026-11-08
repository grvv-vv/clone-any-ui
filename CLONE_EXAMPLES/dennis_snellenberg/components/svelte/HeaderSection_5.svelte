<script lang="ts">
  let isMobileMenuOpen = false;
</script>

<header class="sticky top-0 z-50 w-full border-b border-zinc-200/80 bg-white/80 backdrop-blur-md transition-all duration-300 dark:border-zinc-800/80 dark:bg-zinc-950/80">
  <div class="container mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
    <a href="#" class="group flex items-center gap-2.5 font-bold text-xl tracking-tight text-zinc-900 dark:text-zinc-50 cursor-pointer">
      <span class="h-7 w-7 rounded-lg bg-blue-600 inline-flex items-center justify-center text-white text-xs font-black shadow-md shadow-blue-500/25 transition-transform duration-300 ease-out group-hover:scale-110 group-hover:rotate-6">
        ⚡
      </span>
      <span class="transition-colors duration-200 group-hover:text-blue-600 dark:group-hover:text-blue-400">Brand</span>
    </a>

    <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-600 dark:text-zinc-400">
      <a href="#features" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Features</a>
      <a href="#pricing" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Pricing</a>
      <a href="#testimonials" class="relative py-1 transition hover:text-zinc-900 dark:hover:text-zinc-50 after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 hover:after:w-full after:bg-blue-600 after:transition-all after:duration-300">Testimonials</a>
    </nav>

    <div class="hidden md:flex items-center gap-4">
      <button class="relative overflow-hidden rounded-xl bg-zinc-900 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all duration-300 ease-out hover:-translate-y-0.5 hover:shadow-lg hover:shadow-zinc-900/10 hover:bg-zinc-800 active:translate-y-0 active:scale-95 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200">
        Get Started
      </button>
    </div>

    <button
      on:click={() => isMobileMenuOpen = !isMobileMenuOpen}
      class="md:hidden inline-flex items-center justify-center p-2 rounded-lg text-zinc-700 dark:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
      aria-expanded={isMobileMenuOpen}
    >
      <span class="sr-only">Toggle navigation menu</span>
      <span>{isMobileMenuOpen ? '✕' : '☰'}</span>
    </button>
  </div>

  {#if isMobileMenuOpen}
    <div class="md:hidden border-b border-zinc-200 dark:border-zinc-800 bg-white/95 dark:bg-zinc-950/95 px-6 pt-3 pb-6 space-y-3 animate-fade-in-down shadow-xl backdrop-blur-md">
      <a href="#features" class="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600">Features</a>
      <a href="#pricing" class="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600">Pricing</a>
      <a href="#testimonials" class="block text-sm font-medium py-2 text-zinc-700 dark:text-zinc-200 hover:text-blue-600">Testimonials</a>
      <button class="w-full mt-2 rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white shadow-md hover:bg-blue-500 transition-all duration-200">
        Get Started
      </button>
    </div>
  {/if}
</header>
