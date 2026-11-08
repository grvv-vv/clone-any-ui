<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue';

const props = withDefaults(
  defineProps<{
    isOpen?: boolean;
  }>(),
  {
    isOpen: true,
  }
);

const emit = defineEmits<{
  (e: 'close'): void;
}>();

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    emit('close');
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<template>
  <div
    v-if="isOpen"
    role="dialog"
    aria-modal="true"
    aria-label="YesCheff Case Study"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-xl p-4 sm:p-8 animate-fade-in"
    @click="emit('close')"
  >
    <div
      class="relative max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-2xl bg-zinc-950 border border-white/10 shadow-2xl p-6 sm:p-10 text-zinc-100"
      @click.stop
    >
      <!-- Close Button -->
      <button
        @click="emit('close')"
        aria-label="Close project"
        class="absolute top-6 right-6 z-10 flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20 transition-all cursor-pointer"
      >
        ✕
      </button>

      <!-- Header Hero -->
      <div class="space-y-4 mb-8">
        <div class="flex items-center gap-2">
          <span class="text-xs font-mono uppercase bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-md">
            Case Study
          </span>
          <span class="text-xs text-zinc-500">Multimodal AI · Computer Vision · Product</span>
        </div>
        <h1 class="text-3xl sm:text-4xl font-black tracking-tight">YesCheff</h1>
        <p class="text-base text-zinc-400 leading-relaxed max-w-2xl">
          Cooking from video usually means pausing repeatedly to note ingredients and quantities. YesCheff uses multimodal vision models and structured OCR to convert culinary videos into legible, actionable step-by-step guides.
        </p>
        <a
          href="https://www.yescheff.co/"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center gap-2 text-xs font-semibold text-emerald-400 hover:text-emerald-300 transition-colors"
        >
          <span>Visit YesCheff.co</span>
          <span>→</span>
        </a>
      </div>

      <!-- Video Demonstration -->
      <div class="rounded-xl overflow-hidden bg-black border border-white/10 mb-8 aspect-video flex items-center justify-center">
        <video
          src="https://deji-ajetomobi.b-cdn.net/YesCheff/iPhone-16-109.webm"
          autoplay
          muted
          loop
          playsinline
          controls
          class="w-full h-full object-contain"
        />
      </div>

      <!-- Feature Details Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 pt-6 border-t border-white/10 text-xs">
        <div>
          <span class="text-zinc-500 block uppercase tracking-wider font-mono">Role</span>
          <p class="text-zinc-200 mt-1 font-medium">Founder &amp; AI Systems Engineer</p>
        </div>
        <div>
          <span class="text-zinc-500 block uppercase tracking-wider font-mono">Tech Stack</span>
          <p class="text-zinc-200 mt-1 font-medium">Vision-Language Models, Python, Next.js, FastAPI</p>
        </div>
        <div>
          <span class="text-zinc-500 block uppercase tracking-wider font-mono">Status</span>
          <p class="text-zinc-200 mt-1 font-medium">In Beta · Testing with 1,200+ users</p>
        </div>
      </div>
    </div>
  </div>
</template>

