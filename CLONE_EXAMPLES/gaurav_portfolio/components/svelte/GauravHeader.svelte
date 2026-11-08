<!-- GauravHeader - Svelte 5 Component -->
<script lang="ts">
  import { onMount } from 'svelte';

  export let currentRoute: 'about' | 'projects' | 'engineering' = 'about';
  export let enableSound: boolean = true;

  let activeTab = currentRoute;
  let isAudioActive = enableSound;
  let pillStyle = { left: 0, width: 64 };
  let navRef: HTMLElement;

  const routes = [
    { id: 'about' as const, label: 'About', keyHint: '1', href: './index.html' },
    { id: 'projects' as const, label: 'Projects', keyHint: '2', href: './projects/index.html' },
    { id: 'engineering' as const, label: '& Engineering', keyHint: '3', href: './engineering/index.html' },
  ];

  function updatePill(tabId: string) {
    if (!navRef) return;
    const item = navRef.querySelector(`[data-route="${tabId}"]`) as HTMLElement;
    if (item) {
      const navRect = navRef.getBoundingClientRect();
      const itemRect = item.getBoundingClientRect();
      pillStyle = {
        left: itemRect.left - navRect.left,
        width: itemRect.width,
      };
    }
  }

  onMount(() => {
    updatePill(activeTab);
    const handleKeyDown = (e: KeyboardEvent) => {
      if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) return;
      if (e.key === '1') activeTab = 'about';
      if (e.key === '2') activeTab = 'projects';
      if (e.key === '3') activeTab = 'engineering';
      if (e.key.toLowerCase() === 'm') isAudioActive = !isAudioActive;
      updatePill(activeTab);
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  });
</script>

<header class="sticky top-0 z-50 w-full bg-white/90 dark:bg-black/90 backdrop-blur-md border-b border-black/5 dark:border-white/10 transition-colors">
  <div class="relative mx-auto flex h-14 max-w-5xl items-center justify-between px-6">
    <div class="absolute inset-x-0 bottom-0 h-px bg-gradient-to-r from-transparent via-black/10 dark:via-white/10 to-transparent" aria-hidden="true"></div>

    <div class="text-sm font-bold tracking-tight text-zinc-900 dark:text-white flex items-center gap-1.5">
      <span>Gaurav</span>
      <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-500">AI</span>
    </div>

    <div
      bind:this={navRef}
      class="relative flex items-center gap-1 p-1 rounded-full bg-zinc-100/80 dark:bg-zinc-900/80 border border-zinc-200/80 dark:border-zinc-800 shadow-inner"
      on:mouseleave={() => updatePill(activeTab)}
    >
      <div
        class="absolute top-1 bottom-1 rounded-full bg-black dark:bg-white shadow-sm transition-all duration-300 ease-out pointer-events-none"
        style="left: {pillStyle.left}px; width: {pillStyle.width}px;"
      ></div>

      {#each routes as route}
        <a
          data-route={route.id}
          href={route.href}
          on:mouseenter={() => updatePill(route.id)}
          on:click={() => { activeTab = route.id; updatePill(route.id); }}
          class="relative z-10 px-4 py-1.5 text-xs font-semibold rounded-full transition-colors duration-200 flex items-center gap-1.5 {activeTab === route.id ? 'text-white dark:text-black' : 'text-zinc-600 dark:text-zinc-400 hover:text-black dark:hover:text-white'}"
        >
          <span>{route.label}</span>
          <span class="text-[9px] font-mono opacity-50 {activeTab === route.id ? 'text-white dark:text-black' : ''}">
            [{route.keyHint}]
          </span>
        </a>
      {/each}
    </div>

    <button
      type="button"
      on:click={() => isAudioActive = !isAudioActive}
      class="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono transition-all border {isAudioActive ? 'bg-zinc-100 dark:bg-zinc-800 border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100' : 'border-transparent text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200'}"
      title="Toggle audio feedback (Shortcut: M)"
    >
      <span class="flex items-end gap-0.5 h-2.5">
        <span class="w-0.5 bg-current rounded-full transition-all {isAudioActive ? 'h-2.5' : 'h-1'}"></span>
        <span class="w-0.5 bg-current rounded-full transition-all {isAudioActive ? 'h-1.5' : 'h-1'}"></span>
        <span class="w-0.5 bg-current rounded-full transition-all {isAudioActive ? 'h-2' : 'h-1'}"></span>
      </span>
      <span class="hidden sm:inline">{isAudioActive ? 'Audio ON' : 'Muted'}</span>
    </button>
  </div>
</header>

