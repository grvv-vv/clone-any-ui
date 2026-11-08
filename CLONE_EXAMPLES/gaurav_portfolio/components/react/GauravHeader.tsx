import React, { useState, useEffect, useRef } from 'react';

interface GauravHeaderProps {
  currentRoute?: 'about' | 'projects' | 'engineering';
  onNavigate?: (route: 'about' | 'projects' | 'engineering') => void;
  enableSound?: boolean;
}

export function GauravHeader({ currentRoute = 'about', onNavigate, enableSound = true }: GauravHeaderProps) {
  const [activeTab, setActiveTab] = useState<'about' | 'projects' | 'engineering'>(currentRoute);
  const [pillStyle, setPillStyle] = useState<{ left: number; width: number }>({ left: 0, width: 64 });
  const [isAudioActive, setIsAudioActive] = useState(enableSound);
  const navRef = useRef<HTMLDivElement>(null);

  const routes = [
    { id: 'about' as const, label: 'About', keyHint: '1', href: './index.html' },
    { id: 'projects' as const, label: 'Projects', keyHint: '2', href: './projects/index.html' },
    { id: 'engineering' as const, label: '& Engineering', keyHint: '3', href: './engineering/index.html' },
  ];

  const updatePill = (tabId: 'about' | 'projects' | 'engineering') => {
    if (!navRef.current) return;
    const item = navRef.current.querySelector(`[data-route="${tabId}"]`) as HTMLElement;
    if (item) {
      const navRect = navRef.current.getBoundingClientRect();
      const itemRect = item.getBoundingClientRect();
      setPillStyle({
        left: itemRect.left - navRect.left,
        width: itemRect.width,
      });
    }
  };

  useEffect(() => {
    setActiveTab(currentRoute);
    updatePill(currentRoute);
  }, [currentRoute]);

  // Global Keyboard Shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) return;
      if (e.key === '1') onNavigate?.('about');
      if (e.key === '2') onNavigate?.('projects');
      if (e.key === '3') onNavigate?.('engineering');
      if (e.key.toLowerCase() === 'm') setIsAudioActive((prev) => !prev);
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onNavigate]);

  const handleSelect = (routeId: 'about' | 'projects' | 'engineering') => {
    setActiveTab(routeId);
    updatePill(routeId);
    onNavigate?.(routeId);
  };

  return (
    <header className="sticky top-0 z-50 w-full bg-white/90 dark:bg-black/90 backdrop-blur-md border-b border-black/5 dark:border-white/10 transition-colors">
      <div className="relative mx-auto flex h-14 max-w-5xl items-center justify-between px-6">
        {/* Subtle Decorative Ruler Lines */}
        <div className="absolute inset-x-0 bottom-0 h-px bg-gradient-to-r from-transparent via-black/10 dark:via-white/10 to-transparent" aria-hidden="true" />

        {/* Brand / Logo */}
        <div className="text-sm font-bold tracking-tight text-zinc-900 dark:text-white flex items-center gap-1.5">
          <span>Gaurav</span>
          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-500">AI</span>
        </div>

        {/* Central Capsule Navigation Track */}
        <div
          ref={navRef}
          className="relative flex items-center gap-1 p-1 rounded-full bg-zinc-100/80 dark:bg-zinc-900/80 border border-zinc-200/80 dark:border-zinc-800 shadow-inner"
          onMouseLeave={() => updatePill(activeTab)}
        >
          {/* Animated Active Pill Indicator */}
          <div
            className="absolute top-1 bottom-1 rounded-full bg-black dark:bg-white shadow-sm transition-all duration-300 ease-out pointer-events-none"
            style={{
              left: `${pillStyle.left}px`,
              width: `${pillStyle.width}px`,
            }}
          />

          {routes.map((route) => {
            const isActive = activeTab === route.id;
            return (
              <a
                key={route.id}
                data-route={route.id}
                href={route.href}
                onClick={(e) => {
                  if (onNavigate) {
                    e.preventDefault();
                    handleSelect(route.id);
                  }
                }}
                onMouseEnter={() => updatePill(route.id)}
                className={`relative z-10 px-4 py-1.5 text-xs font-semibold rounded-full transition-colors duration-200 flex items-center gap-1.5 ${
                  isActive
                    ? 'text-white dark:text-black'
                    : 'text-zinc-600 dark:text-zinc-400 hover:text-black dark:hover:text-white'
                }`}
              >
                <span>{route.label}</span>
                <span className={`text-[9px] font-mono opacity-50 ${isActive ? 'text-white dark:text-black' : ''}`}>
                  [{route.keyHint}]
                </span>
              </a>
            );
          })}
        </div>

        {/* Audio Haptics Toggle Button */}
        <button
          type="button"
          onClick={() => setIsAudioActive(!isAudioActive)}
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono transition-all border ${
            isAudioActive
              ? 'bg-zinc-100 dark:bg-zinc-800 border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100'
              : 'border-transparent text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200'
          }`}
          title="Toggle audio feedback (Shortcut: M)"
        >
          <span className="flex items-end gap-0.5 h-2.5">
            <span className={`w-0.5 bg-current rounded-full transition-all ${isAudioActive ? 'h-2.5' : 'h-1'}`} />
            <span className={`w-0.5 bg-current rounded-full transition-all ${isAudioActive ? 'h-1.5' : 'h-1'}`} />
            <span className={`w-0.5 bg-current rounded-full transition-all ${isAudioActive ? 'h-2' : 'h-1'}`} />
          </span>
          <span className="hidden sm:inline">{isAudioActive ? 'Audio ON' : 'Muted'}</span>
        </button>
      </div>
    </header>
  );
}
export default GauravHeader;
