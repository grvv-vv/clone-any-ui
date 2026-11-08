import React from 'react';

export function GauravAboutBio() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-16 font-sans text-zinc-900 dark:text-zinc-100">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-16">
        {/* Section 1: Hero Intro */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold tracking-tight">Gaurav</h2>
          <p className="text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
            AI engineer and Computer Science undergraduate specializing in deep learning, large language models (LLMs), and autonomous agent architectures. Currently diving deep into neural reasoning, multimodal models, and building high-performance AI systems in college.
            <br className="my-2" />
            Building <a href="./engineering/index.html" className="underline underline-offset-4 decoration-zinc-400 hover:text-black dark:hover:text-white transition-colors">autonomous agents &amp; neural tools</a> and exploring <a href="./projects/index.html" className="underline underline-offset-4 decoration-zinc-400 hover:text-black dark:hover:text-white transition-colors">open-source AI projects</a>.
          </p>
        </div>

        {/* Section 2: AI Systems & Projects */}
        <div className="space-y-4 md:text-right">
          <h2 className="text-xl font-bold tracking-tight">AI Systems &amp; Projects</h2>
          <p className="text-sm leading-relaxed text-zinc-600 dark:text-zinc-400 space-y-1">
            <a href="./projects/yescheff/index.html" className="block underline underline-offset-4 decoration-zinc-400 hover:text-black dark:hover:text-white transition-colors">YesCheff AI — Multimodal Recipe Engine</a>
            <a href="./engineering/index.html" className="block underline underline-offset-4 decoration-zinc-400 hover:text-black dark:hover:text-white transition-colors">Autonomous Agent Orchestrator</a>
            <a href="./projects/index.html" className="block underline underline-offset-4 decoration-zinc-400 hover:text-black dark:hover:text-white transition-colors">Neural Search &amp; Vector Embeddings</a>
            <a href="./projects/index.html" className="block underline underline-offset-4 decoration-zinc-400 hover:text-black dark:hover:text-white transition-colors">Domain LLM Fine-Tuning &amp; Eval</a>
            <a href="./projects/index.html" className="block text-xs font-semibold text-zinc-500 hover:text-black dark:hover:text-white transition-colors pt-2">Explore all AI &amp; engineering projects →</a>
          </p>
        </div>

        {/* Section 3: Education & Experience */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold tracking-tight">Education &amp; Experience</h2>
          <p className="text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
            B.Tech Computer Science &amp; Engineering: Undergraduate (2023 - Present)<br />
            AI Research Intern: Foundation Models &amp; Multi-Agent Systems (2024 - Present)<br />
            Lead Contributor: Open-Source Machine Learning &amp; PyTorch Ecosystem (2023 - Present)<br />
            Campus AI Lead: University Machine Learning &amp; Robotics Lab (2023 - Present)
          </p>
        </div>

        {/* Section 4: Hackathons, Honors & Research */}
        <div className="space-y-4 md:text-right">
          <h2 className="text-xl font-bold tracking-tight">Hackathons, Honors &amp; Research</h2>
          <p className="text-sm leading-relaxed text-zinc-600 dark:text-zinc-400 space-y-1">
            <a href="https://github.com/" target="_blank" rel="noopener noreferrer" className="block underline underline-offset-4 decoration-zinc-400 hover:text-black dark:hover:text-white transition-colors">GitHub AI Innovation Spotlight</a>
            <a href="https://kaggle.com/" target="_blank" rel="noopener noreferrer" className="block underline underline-offset-4 decoration-zinc-400 hover:text-black dark:hover:text-white transition-colors">Kaggle Expert — Deep Learning &amp; Vision</a>
            <span className="block text-zinc-500">1st Place Winner: National Autonomous AI Hackathon (2024)</span>
            <span className="block text-zinc-500">Smart India Hackathon Finalist — Generative AI Track</span>
            <a href="https://huggingface.co/" target="_blank" rel="noopener noreferrer" className="block underline underline-offset-4 decoration-zinc-400 hover:text-black dark:hover:text-white transition-colors">Hugging Face Open Source Contributor</a>
          </p>
        </div>
      </div>

      {/* Footer Socials */}
      <footer className="mt-20 pt-10 border-t border-zinc-200 dark:border-zinc-800">
        <div className="flex flex-wrap items-center justify-center gap-6 text-xs font-medium text-zinc-500 dark:text-zinc-400 mb-12">
          <a href="mailto:gaurav.ai.eng@gmail.com" className="hover:text-black dark:hover:text-white transition-colors">Mail</a>
          <a href="https://www.linkedin.com/in/gaurav-ai" target="_blank" rel="noopener noreferrer" className="hover:text-black dark:hover:text-white transition-colors">LinkedIn</a>
          <a href="https://github.com/gaurav" target="_blank" rel="noopener noreferrer" className="hover:text-black dark:hover:text-white transition-colors">GitHub</a>
          <a href="https://x.com/gaurav_ai" target="_blank" rel="noopener noreferrer" className="hover:text-black dark:hover:text-white transition-colors">Twitter / X</a>
          <a href="https://huggingface.co/gaurav-ai" target="_blank" rel="noopener noreferrer" className="hover:text-black dark:hover:text-white transition-colors">Hugging Face</a>
        </div>

        {/* Bespoke Monumental Architectural Wordmark */}
        <div className="w-full flex justify-center overflow-hidden py-4">
          <svg width="100%" height="auto" viewBox="0 0 1416 260" fill="none" xmlns="http://www.w3.org/2000/svg" className="max-h-56 block">
            <text x="50%" y="205" textAnchor="middle" fontFamily="'Manufacturing Consent', 'Times New Roman', Georgia, serif" fontSize="240" fontWeight="900" letterSpacing="18" fill="currentColor">
              GAURAV
            </text>
          </svg>
        </div>
      </footer>
    </main>
  );
}
export default GauravAboutBio;
