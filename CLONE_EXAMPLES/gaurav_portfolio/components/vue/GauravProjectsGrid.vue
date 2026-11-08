<script setup lang="ts">
import { ref, computed } from 'vue';

interface ProjectItem {
  id: string;
  title: string;
  categories: string[];
  type: 'image' | 'video';
  mediaUrl: string;
  posterUrl?: string;
  isCaseStudy?: boolean;
}

const SAMPLE_PROJECTS: ProjectItem[] = [
  {
    id: 'yescheff-main',
    title: 'YesCheff',
    categories: ['Components', 'Product', 'Case studies'],
    type: 'video',
    mediaUrl: 'https://deji-ajetomobi.b-cdn.net/YesCheff/iPhone-16-109.webm',
    isCaseStudy: true,
  },
  {
    id: 'ams-sma-motion',
    title: 'AMS / SMA',
    categories: ['Brand', 'Animated', 'Wise'],
    type: 'video',
    mediaUrl: 'https://deji-ajetomobi.b-cdn.net/AMS-SMA/Art_Meets_Science_Science_Meets_Art_motion_14_gkzone-720.mp4',
    posterUrl: 'https://deji-ajetomobi.b-cdn.net/AMS-SMA/Art_Meets_Science_Science_Meets_Art_motion_14_gkzone-poster.jpg',
  },
  {
    id: 'finy-brand',
    title: 'Finy',
    categories: ['Icons & Illos', 'Brand', 'Case studies'],
    type: 'image',
    mediaUrl: 'https://deji-ajetomobi.b-cdn.net/Finy/FINY_brand_9_yjzlpo-1200.webp',
  },
  {
    id: 'deskhq-brand',
    title: 'Deskhq',
    categories: ['Brand', 'Case studies'],
    type: 'image',
    mediaUrl: 'https://deji-ajetomobi.b-cdn.net/Deskhq/Deskhq_brand_18_hvthrv-1200.webp',
  },
  {
    id: 'fesac-brand',
    title: 'Fesac',
    categories: ['Brand'],
    type: 'image',
    mediaUrl: 'https://deji-ajetomobi.b-cdn.net/Fesac/64abe820032d0b717c1cb117_Asset 27.webp',
  },
  {
    id: 'glyko-brand',
    title: 'Glyko',
    categories: ['Brand'],
    type: 'image',
    mediaUrl: 'https://deji-ajetomobi.b-cdn.net/Glyko/glyko-30Brand_Brand_j0sq8v-1200.webp',
  },
  {
    id: 'augment-motion',
    title: 'Augment finance',
    categories: ['Icons & Illos', 'Animated'],
    type: 'video',
    mediaUrl: 'https://deji-ajetomobi.b-cdn.net/Augment/Augment_motion_2_daz7f8-poster.jpg',
    posterUrl: 'https://deji-ajetomobi.b-cdn.net/Augment/Augment_motion_2_daz7f8-poster.jpg',
  },
  {
    id: 'republic-poster',
    title: 'Republic 63',
    categories: ['Brand', 'Posters'],
    type: 'image',
    mediaUrl: 'https://deji-ajetomobi.b-cdn.net/REPUBLIC%2063/Frame_73_ewk1og-1200.webp',
  },
];

const CATEGORIES = [
  'All',
  'Case studies',
  'Product',
  'Components',
  'Brand',
  'Wise',
  'Web',
  'Animated',
  'Swag',
  'Posters',
  'Icons & Illos',
  'Explorations',
];

const activeCategory = ref('All');
const selectedLightbox = ref<ProjectItem | null>(null);

const filteredProjects = computed(() => {
  return SAMPLE_PROJECTS.filter((proj) => {
    if (activeCategory.value === 'All') return true;
    return proj.categories.some((c) => c.toLowerCase() === activeCategory.value.toLowerCase());
  });
});

const handleVideoHover = (e: Event, isEnter: boolean) => {
  const vid = e.target as HTMLVideoElement;
  if (!vid) return;
  if (isEnter) {
    vid.play().catch(() => {});
  } else {
    vid.pause();
  }
};
</script>

<template>
  <div class="w-full min-h-screen bg-zinc-50 dark:bg-black font-sans text-zinc-900 dark:text-zinc-100">
    <!-- Filter Navigation Bar -->
    <header class="sticky top-0 z-40 bg-zinc-50/80 dark:bg-black/80 backdrop-blur-md border-b border-zinc-200 dark:border-zinc-800">
      <div class="max-w-7xl mx-auto px-4 py-3 overflow-x-auto scrollbar-none flex items-center gap-2">
        <button
          v-for="cat in CATEGORIES"
          :key="cat"
          @click="activeCategory = cat"
          :class="[
            'px-3.5 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all duration-200',
            activeCategory === cat
              ? 'bg-black text-white dark:bg-white dark:text-black shadow-sm'
              : 'text-zinc-600 dark:text-zinc-400 hover:text-black dark:hover:text-white hover:bg-zinc-200 dark:hover:bg-zinc-800'
          ]"
        >
          {{ cat }}
        </button>
      </div>
    </header>

    <!-- Projects Grid Container -->
    <main class="max-w-7xl mx-auto px-4 py-8">
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="proj in filteredProjects"
          :key="proj.id"
          class="group relative rounded-xl overflow-hidden bg-zinc-200 dark:bg-zinc-900 aspect-square cursor-pointer transition-transform duration-300 hover:-translate-y-1"
          @click="selectedLightbox = proj"
        >
          <!-- Video Card -->
          <video
            v-if="proj.type === 'video'"
            :src="proj.mediaUrl"
            :poster="proj.posterUrl"
            muted
            loop
            playsinline
            class="w-full h-full object-cover"
            @mouseenter="handleVideoHover($event, true)"
            @mouseleave="handleVideoHover($event, false)"
          />

          <!-- Image Card -->
          <img
            v-else
            :src="proj.mediaUrl"
            :alt="proj.title"
            loading="lazy"
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />

          <!-- Overlay Badge -->
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 p-4 flex flex-col justify-end">
            <span class="text-white text-sm font-semibold tracking-wide drop-shadow-sm">{{ proj.title }}</span>
            <div class="flex flex-wrap gap-1.5 mt-1">
              <span
                v-for="c in proj.categories"
                :key="c"
                class="text-[10px] bg-white/20 backdrop-blur-sm text-white px-2 py-0.5 rounded-full"
              >
                {{ c }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Lightbox Modal -->
    <div
      v-if="selectedLightbox"
      class="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 backdrop-blur-sm"
      @click="selectedLightbox = null"
    >
      <div
        class="relative max-w-4xl max-h-[90vh] flex flex-col items-center justify-center bg-zinc-950 p-2 rounded-2xl border border-zinc-800"
        @click.stop
      >
        <button
          @click="selectedLightbox = null"
          class="absolute -top-3 -right-3 z-10 w-8 h-8 rounded-full bg-white text-black font-bold flex items-center justify-center shadow-lg hover:scale-110 transition-transform"
        >
          ✕
        </button>
        <video
          v-if="selectedLightbox.type === 'video'"
          :src="selectedLightbox.mediaUrl"
          controls
          autoplay
          loop
          class="max-w-full max-h-[80vh] rounded-xl"
        />
        <img
          v-else
          :src="selectedLightbox.mediaUrl"
          :alt="selectedLightbox.title"
          class="max-w-full max-h-[80vh] object-contain rounded-xl"
        />
        <div class="w-full px-4 py-3 flex justify-between items-center text-xs text-zinc-400">
          <span class="font-bold text-white text-sm">{{ selectedLightbox.title }}</span>
          <a
            v-if="selectedLightbox.isCaseStudy"
            href="./projects/yescheff/index.html"
            class="text-emerald-400 hover:underline font-semibold"
          >
            Open Full Case Study →
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

