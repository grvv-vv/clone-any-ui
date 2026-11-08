<script setup lang="ts">
import { ref } from 'vue';

interface EngineeringProject {
  id: string;
  title: string;
  tagline: string;
  url: string;
  featured?: boolean;
}

const PROJECTS: EngineeringProject[] = [
  {
    id: 'yescheff',
    title: 'Yescheff.co',
    tagline: 'Smart recipe extraction from social media videos using multimodal AI.',
    url: 'https://www.yescheff.co/',
    featured: true,
  },
  {
    id: 'art-meets-science',
    title: 'Art Meets Science',
    tagline: 'Interactive micro-experience exploring generative algorithms and mathematics.',
    url: 'https://art-meets-science.wise.design/',
  },
  {
    id: 'dither',
    title: 'Dither Generator',
    tagline: 'Real-time Bayer and Floyd-Steinberg dithering engine in WebGL.',
    url: 'https://plaque-formal-77240094.figma.site/',
  },
  {
    id: 'dynamic-form-group',
    title: 'Dynamic Form Group',
    tagline: 'Maps unstructured clipboard data into validated schemas using local LLMs.',
    url: 'https://github.com/gaurav/dynamic-form-group',
  },
  {
    id: 'factor-x',
    title: 'Factor X',
    tagline: 'Audio spectrum and microphone acoustic visualizer built on Canvas 2D.',
    url: 'https://github.com/gaurav/factor-x',
  },
];

const selectedProject = ref<EngineeringProject>(PROJECTS[0]);
const isLoading = ref(false);

const handleSelect = (project: EngineeringProject) => {
  isLoading.value = true;
  selectedProject.value = project;
};

const handleIframeLoaded = () => {
  isLoading.value = false;
};
</script>

<template>
  <div class="flex h-[calc(100vh-56px)] w-full overflow-hidden bg-zinc-950 font-sans text-zinc-100">
    <!-- Sidebar Navigation -->
    <nav aria-label="Engineering projects" class="w-80 shrink-0 overflow-y-auto border-r border-white/10 p-6 space-y-3">
      <h2 class="text-xs font-mono uppercase tracking-wider text-zinc-500 mb-4">Selected Systems &amp; Code</h2>
      <button
        v-for="proj in PROJECTS"
        :key="proj.id"
        @click="handleSelect(proj)"
        :class="[
          'w-full text-left p-3.5 rounded-xl border transition-all duration-200 block',
          selectedProject.id === proj.id
            ? 'bg-white/10 border-white/20 shadow-sm'
            : 'border-transparent hover:bg-white/5 hover:border-white/5 text-zinc-400 hover:text-white'
        ]"
      >
        <div class="flex items-center justify-between">
          <span class="text-sm font-semibold tracking-tight text-white">{{ proj.title }}</span>
          <span v-if="proj.featured" class="text-[9px] bg-emerald-500/20 text-emerald-400 font-mono px-1.5 py-0.5 rounded">Featured</span>
        </div>
        <p class="text-xs text-zinc-400 mt-1 line-clamp-2 leading-relaxed">{{ proj.tagline }}</p>
      </button>
    </nav>

    <!-- Main Live Showcase Viewport -->
    <main class="flex-1 flex flex-col overflow-hidden bg-black relative">
      <!-- Toolbar -->
      <header class="h-12 border-b border-white/10 px-6 flex items-center justify-between bg-zinc-950/60 backdrop-blur-md shrink-0">
        <div class="flex items-center gap-3">
          <span class="text-xs font-mono text-zinc-400 truncate max-w-md">{{ selectedProject.url }}</span>
        </div>
        <a
          :href="selectedProject.url"
          target="_blank"
          rel="noopener noreferrer"
          class="text-xs font-medium text-white bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5"
        >
          <span>Open Live Site</span>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
            <polyline points="15 3 21 3 21 9" />
            <line x1="10" y1="14" x2="21" y2="3" />
          </svg>
        </a>
      </header>

      <!-- Viewport Frame -->
      <div class="flex-1 relative w-full h-full">
        <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-zinc-950 z-10">
          <div class="animate-spin rounded-full h-8 w-8 border-2 border-white/20 border-t-white" />
        </div>
        <iframe
          :key="selectedProject.id"
          :src="selectedProject.url"
          :title="selectedProject.title"
          class="w-full h-full border-none bg-white"
          @load="handleIframeLoaded"
        />
      </div>
    </main>
  </div>
</template>

