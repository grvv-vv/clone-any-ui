import React, { useEffect } from 'react';

interface GauravYesCheffModalProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export function GauravYesCheffModal({ isOpen = true, onClose }: GauravYesCheffModalProps) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && onClose) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="YesCheff Case Study"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-xl p-4 sm:p-8 animate-fade-in"
      onClick={onClose}
    >
      <div
        className="relative max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-2xl bg-zinc-950 border border-white/10 shadow-2xl p-6 sm:p-10 text-zinc-100"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          aria-label="Close project"
          className="absolute top-6 right-6 z-10 flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20 transition-all cursor-pointer"
        >
          ✕
        </button>

        {/* Header Hero */}
        <div className="space-y-4 mb-8">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono uppercase bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-md">
              Case Study
            </span>
            <span className="text-xs text-zinc-500">Brand · Product · Engineering</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-black tracking-tight">YesCheff</h1>
          <p className="text-sm sm:text-base text-zinc-400 leading-relaxed max-w-2xl">
            From brand to product, I designed and built the experience, including recipe creation, serving adjustments, interactive timers, and nutritional intelligence.
          </p>
        </div>

        {/* Video Showcase Loop */}
        <div className="overflow-hidden rounded-xl bg-zinc-900 border border-white/5 aspect-[16/9] mb-8">
          <video
            src="https://deji-ajetomobi.b-cdn.net/YesCheff/iPhone-16-109.webm"
            autoPlay
            loop
            muted
            playsInline
            className="h-full w-full object-cover"
          />
        </div>

        {/* Feature Highlights Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          <div className="p-4 rounded-xl bg-white/[0.03] border border-white/5 space-y-1">
            <h4 className="text-xs font-mono text-zinc-500 uppercase">Servings Engine</h4>
            <p className="text-sm font-semibold text-white">Dynamic ingredient scaling</p>
          </div>
          <div className="p-4 rounded-xl bg-white/[0.03] border border-white/5 space-y-1">
            <h4 className="text-xs font-mono text-zinc-500 uppercase">Interactive Timers</h4>
            <p className="text-sm font-semibold text-white">Multi-step cooking alerts</p>
          </div>
          <div className="p-4 rounded-xl bg-white/[0.03] border border-white/5 space-y-1">
            <h4 className="text-xs font-mono text-zinc-500 uppercase">Voice &amp; Video</h4>
            <p className="text-sm font-semibold text-white">Hands-free kitchen mode</p>
          </div>
        </div>

        {/* Action Link */}
        <div className="flex items-center justify-between pt-6 border-t border-white/10">
          <span className="text-xs text-zinc-500">Live platform launched in 2024</span>
          <a
            href="https://www.yescheff.co/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-xs font-semibold bg-white text-black px-4 py-2 rounded-xl hover:bg-zinc-200 transition-all shadow-md"
          >
            <span>Visit Yescheff.co</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
          </a>
        </div>
      </div>
    </div>
  );
}
export default GauravYesCheffModal;

