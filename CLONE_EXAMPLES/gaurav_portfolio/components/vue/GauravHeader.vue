<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = withDefaults(
  defineProps<{
    currentRoute?: 'about' | 'projects' | 'engineering';
    enableSound?: boolean;
  }>(),
  {
    currentRoute: 'about',
    enableSound: true,
  }
);

const emit = defineEmits<{
  (e: 'navigate', route: 'about' | 'projects' | 'engineering'): void;
}>();

const activeTab = ref<'about' | 'projects' | 'engineering'>(props.currentRoute);
const isAudioActive = ref(props.enableSound);
const pillStyle = ref({ left: 0, width: 64 });
const navRef = ref<HTMLElement | null>(null);

const routes = [
  { id: 'about' as const, label: 'About', keyHint: '1', href: './index.html' },
  { id: 'projects' as const, label: 'Projects', keyHint: '2', href: './projects/index.html' },
  { id: 'engineering' as const, label: '& Engineering', keyHint: '3', href: './engineering/index.html' },
];

const updatePill = (tabId: 'about' | 'projects' | 'engineering') => {
  if (!navRef.value) return;
  const item = navRef.value.querySelector(`[data-route="${tabId}"]`) as HTMLElement;
  if (item) {
    const navRect = navRef.value.getBoundingClientRect();
    const itemRect = item.getBoundingClientRect();
    pillStyle.value = {
      left: itemRect.left - navRect.left,
      width: itemRect.width,
    };
  }
};

const handleSelect = (routeId: 'about' | 'projects' | 'engineering') => {
  activeTab.value = routeId;
  updatePill(routeId);
  emit('navigate', routeId);
};

const handleKeyDown = (e: KeyboardEvent) => {
  if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) return;
  if (e.key === '1') handleSelect('about');
  if (e.key === '2') handleSelect('projects');
  if (e.key === '3') handleSelect('engineering');
  if (e.key.toLowerCase() === 'm') isAudioActive.value = !isAudioActive.value;
};

watch(() => props.currentRoute, (newVal) => {
  activeTab.value = newVal;
  updatePill(newVal);
});

onMounted(() => {
  updatePill(activeTab.value);
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<template>
  <header class="sticky top-0 z-50 w-full bg-white/90 dark:bg-black/90 backdrop-blur-md border-b border-black/5 dark:border-white/10 transition-colors">
    <div class="relative mx-auto flex h-14 max-w-5xl items-center justify-between px-6">
      <div class="absolute inset-x-0 bottom-0 h-px bg-gradient-to-r from-transparent via-black/10 dark:via-white/10 to-transparent" aria-hidden="true" />

      <!-- Brand -->
      <div class="text-sm font-bold tracking-tight text-zinc-900 dark:text-white flex items-center gap-1.5">
        <span>Gaurav</span>
        <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-500">AI</span>
      </div>

      <!-- Capsule Nav -->
      <div
        ref="navRef"
        class="relative flex items-center gap-1 p-1 rounded-full bg-zinc-100/80 dark:bg-zinc-900/80 border border-zinc-200/80 dark:border-zinc-800 shadow-inner"
        @mouseleave="updatePill(activeTab)"
      >
        <div
          class="absolute top-1 bottom-1 rounded-full bg-black dark:bg-white shadow-sm transition-all duration-300 ease-out pointer-events-none"
          :style="{ left: `${pillStyle.left}px`, width: `${pillStyle.width}px` }"
        />

        <a
          v-for="route in routes"
          :key="route.id"
          :data-route="route.id"
          :href="route.href"
          @click.prevent="handleSelect(route.id)"
          @mouseenter="updatePill(route.id)"
          :class="[
            'relative z-10 px-4 py-1.5 text-xs font-semibold rounded-full transition-colors duration-200 flex items-center gap-1.5',
            activeTab === route.id
              ? 'text-white dark:text-black'
              : 'text-zinc-600 dark:text-zinc-400 hover:text-black dark:hover:text-white'
          ]"
        >
          <span>{{ route.label }}</span>
          <span :class="['text-[9px] font-mono opacity-50', activeTab === route.id ? 'text-white dark:text-black' : '']">
            [{{ route.keyHint }}]
          </span>
        </a>
      </div>

      <!-- Sound Toggle -->
      <button
        type="button"
        @click="isAudioActive = !isAudioActive"
        :class="[
          'flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono transition-all border',
          isAudioActive
            ? 'bg-zinc-100 dark:bg-zinc-800 border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100'
            : 'border-transparent text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200'
        ]"
        title="Toggle audio feedback (Shortcut: M)"
      >
        <span class="flex items-end gap-0.5 h-2.5">
          <span :class="['w-0.5 bg-current rounded-full transition-all', isAudioActive ? 'h-2.5' : 'h-1']" />
          <span :class="['w-0.5 bg-current rounded-full transition-all', isAudioActive ? 'h-1.5' : 'h-1']" />
          <span :class="['w-0.5 bg-current rounded-full transition-all', isAudioActive ? 'h-2' : 'h-1']" />
        </span>
        <span class="hidden sm:inline">{{ isAudioActive ? 'Audio ON' : 'Muted' }}</span>
      </button>
    </div>
  </header>
</template>
