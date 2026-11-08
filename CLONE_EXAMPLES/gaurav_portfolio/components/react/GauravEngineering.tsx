import React, { useState } from 'react';

interface EngineeringProject {
  id: string;
  title: string;
  tagline: string;
  url: string;
  tags: string[];
  featured?: boolean;
}

const PROJECTS: EngineeringProject[] = [
  {
    id: 'yescheff',
    title: 'Yescheff.co',
    tagline: 'Multimodal AI recipe extraction from culinary videos into structured instructions.',
    url: 'https://www.yescheff.co/',
    tags: ['Vision AI', 'Whisper', 'Next.js 15'],
    featured: true,
  },
  {
    id: 'art-meets-science',
    title: 'Art Meets Science',
    tagline: 'Interactive computational micro-experience exploring generative algorithms and physics.',
    url: 'https://art-meets-science.wise.design/',
    tags: ['Generative UI', 'Three.js', 'Canvas'],
  },
  {
    id: 'dither',
    title: 'Neural Dither Studio',
    tagline: 'GPU-accelerated Bayer & Floyd-Steinberg dithering shader engine for real-time asset export.',
    url: 'https://plaque-formal-77240094.figma.site/',
    tags: ['WebGL 2.0', 'GLSL Shaders', 'Algorithms'],
  },
  {
    id: 'dynamic-form-group',
    title: 'Dynamic Schema Engine',
    tagline: 'Zero-shot extraction mapping freeform text to strictly validated JSON schemas and form inputs.',
    url: 'https://github.com/gaurav/dynamic-form-group',
    tags: ['LLM Reasoning', 'JSON Schema', 'TypeScript'],
  },
  {
    id: 'factor-x',
    title: 'Factor-X Acoustic Engine',
    tagline: 'Real-time audio spectrum Fast Fourier Transform (FFT) visualizer with kinetic responsive typography.',
    url: 'https://github.com/gaurav/factor-x',
    tags: ['Web Audio API', 'FFT Acoustics', 'Canvas 2D'],
  },
];

export function GauravEngineering() {
  const [selectedProject, setSelectedProject] = useState<EngineeringProject>(PROJECTS[0]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSelect = (project: EngineeringProject) => {
    setIsLoading(true);
    setSelectedProject(project);
  };

  return (
    <div className="flex h-[calc(100vh-56px)] w-full overflow-hidden bg-zinc-950 font-sans text-zinc-100">
      {/* Sidebar Navigation */}
      <nav aria-label="Engineering projects" className="w-80 shrink-0 overflow-y-auto border-r border-white/10 p-6 space-y-3">
        <h2 className="text-xs font-mono uppercase tracking-wider text-zinc-500 mb-4">Selected Systems &amp; Code</h2>
        {PROJECTS.map((proj) => {
          const isActive = selectedProject.id === proj.id;
          return (
            <button
              key={proj.id}
              onClick={() => handleSelect(proj)}
              className={`w-full text-left p-3.5 rounded-xl border transition-all duration-200 block ${
                isActive
                  ? 'bg-white/10 border-white/20 shadow-sm'
                  : 'border-transparent hover:bg-white/5 hover:border-white/5 text-zinc-400 hover:text-white'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold tracking-tight text-white">{proj.title}</span>
                {proj.featured && (
                  <span className="text-[9px] bg-emerald-500/20 text-emerald-400 font-mono px-1.5 py-0.5 rounded">
                    Featured
                  </span>
                )}
              </div>
              <p className="text-xs text-zinc-400 mt-1 line-clamp-2 leading-relaxed">{proj.tagline}</p>
              <div className="flex gap-1.5 mt-2 flex-wrap">
                {proj.tags.map((t) => (
                  <span key={t} className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-white/5 text-zinc-400">
                    {t}
                  </span>
                ))}
              </div>
            </button>
          );
        })}
      </nav>

      {/* Main Live Showcase Viewport */}
      <main className="flex-1 flex flex-col overflow-hidden bg-black relative">
        {/* Toolbar */}
        <header className="h-12 border-b border-white/10 px-6 flex items-center justify-between bg-zinc-950/60 backdrop-blur-md shrink-0">
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-zinc-400 truncate max-w-md">{selectedProject.url}</span>
          </div>
          <a
            href={selectedProject.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs font-medium text-white bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5"
          >
            <span>Open Live Site</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
          </a>
        </header>

        {/* Viewport Frame */}
        <div className="flex-1 relative w-full h-full">
          {isLoading && (
            <div className="absolute inset-0 flex items-center justify-center bg-zinc-950 z-10">
              <div className="animate-spin rounded-full h-8 w-8 border-2 border-white/20 border-t-white" />
            </div>
          )}
          <iframe
            key={selectedProject.id}
            src={selectedProject.url}
            title={selectedProject.title}
            className="w-full h-full border-none bg-white"
            onLoad={() => setIsLoading(false)}
          />
        </div>
      </main>
    </div>
  );
}
export default GauravEngineering;
