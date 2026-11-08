import React from 'react';

export function FooterSection_23() {
  return (
    <footer className="border-t border-zinc-200 bg-white py-12 dark:border-zinc-800 dark:bg-zinc-950 transition-colors">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-6 sm:flex-row">
          <div className="flex items-center gap-3">
            <img src="./assets/images/e0554b_f234c2b7282949538_98440.jpg" alt="instagram_icon_grey" className="h-7 w-auto object-contain opacity-80 hover:opacity-100 transition-opacity" />
            <p className="text-sm text-zinc-500 dark:text-zinc-400">
              &copy; {new Date().getFullYear()} All rights reserved. Built with fluid 60fps animations.
            </p>
          </div>
          <div className="flex gap-6 text-sm text-zinc-500">
            <a href="#" className="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">Privacy</a>
            <a href="#" className="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">Terms</a>
            <a href="#" className="transition hover:text-zinc-900 hover:-translate-y-0.5 dark:hover:text-zinc-50">GitHub</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
