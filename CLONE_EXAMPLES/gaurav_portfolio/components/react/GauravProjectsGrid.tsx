import React, { useState } from 'react';

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

export function GauravProjectsGrid() {
  const [activeCategory, setActiveCategory] = useState('All');
  const [selectedLightbox, setSelectedLightbox] = useState<ProjectItem | null>(null);

  const filteredProjects = SAMPLE_PROJECTS.filter((proj) => {
    if (activeCategory === 'All') return true;
    return proj.categories.some((c) => c.toLowerCase() === activeCategory.toLowerCase());
  });

  return (
    <div className="w-full min-h-screen bg-zinc-50 dark:bg-black font-sans text-zinc-900 dark:text-zinc-100">
      {/* Category Filter Navigation Bar */}
      <div className="sticky top-14 z-40 w-full overflow-x-auto border-b border-black/5 dark:border-white/10 bg-zinc-50/90 dark:bg-black/90 backdrop-blur-md px-4 py-2.5">
        <div className="mx-auto flex max-w-5xl items-center gap-2 text-xs">
          {CATEGORIES.map((cat) => {
            const isActive = activeCategory === cat;
            return (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`whitespace-nowrap px-3 py-1 rounded-full transition-all text-xs font-medium cursor-pointer ${
                  isActive
                    ? 'bg-black text-white dark:bg-white dark:text-black font-semibold shadow-sm'
                    : 'text-zinc-500 hover:text-black dark:text-zinc-400 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5'
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>
      </div>

      {/* Responsive Work Showcase Grid */}
      <div className="mx-auto max-w-5xl px-4 py-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProjects.map((proj) => (
            <div
              key={proj.id}
              onClick={() => {
                if (proj.isCaseStudy) {
                  window.location.href = './projects/yescheff/index.html';
                } else {
                  setSelectedLightbox(proj);
                }
              }}
              className="group relative cursor-pointer overflow-hidden rounded-xl border border-black/5 dark:border-white/10 bg-zinc-200/50 dark:bg-zinc-900/50 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl dark:hover:shadow-2xl dark:hover:shadow-black/50"
            >
              <div className="aspect-[4/3] w-full overflow-hidden bg-zinc-900/10 dark:bg-zinc-800/40">
                {proj.type === 'video' ? (
                  <video
                    src={proj.mediaUrl}
                    poster={proj.posterUrl}
                    muted
                    loop
                    playsInline
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                    onMouseEnter={(e) => (e.target as HTMLVideoElement).play().catch(() => {})}
                    onMouseLeave={(e) => (e.target as HTMLVideoElement).pause()}
                  />
                ) : (
                  <img
                    src={proj.mediaUrl}
                    alt={proj.title}
                    loading="lazy"
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />
                )}
              </div>

              {/* Title & Category Tags */}
              <div className="p-4 flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-semibold tracking-tight">{proj.title}</h3>
                  <div className="flex gap-1.5 mt-1">
                    {proj.categories.slice(0, 2).map((c) => (
                      <span key={c} className="text-[10px] font-mono text-zinc-500 dark:text-zinc-400 bg-black/5 dark:bg-white/5 px-1.5 py-0.5 rounded">
                        {c}
                      </span>
                    ))}
                  </div>
                </div>

                {proj.isCaseStudy && (
                  <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full">
                    Case Study ↗
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Lightbox Modal */}
      {selectedLightbox && (
        <div
          onClick={() => setSelectedLightbox(null)}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-md p-4 animate-fade-in"
        >
          <div className="relative max-h-[85vh] max-w-4xl overflow-hidden rounded-xl bg-zinc-950 p-2 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <button
              onClick={() => setSelectedLightbox(null)}
              className="absolute top-4 right-4 z-10 flex h-8 w-8 items-center justify-center rounded-full bg-white/20 text-white text-sm hover:bg-white/30 transition-colors cursor-pointer"
            >
              ✕
            </button>
            {selectedLightbox.type === 'video' ? (
              <video src={selectedLightbox.mediaUrl} autoPlay loop muted controls className="max-h-[75vh] w-full rounded-lg object-contain" />
            ) : (
              <img src={selectedLightbox.mediaUrl} alt={selectedLightbox.title} className="max-h-[75vh] w-full rounded-lg object-contain" />
            )}
            <div className="p-4 text-white">
              <h4 className="text-sm font-bold">{selectedLightbox.title}</h4>
              <p className="text-xs text-zinc-400">{selectedLightbox.categories.join(' · ')}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
export default GauravProjectsGrid;

