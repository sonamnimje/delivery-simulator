import React from 'react'
import AnimatedTyping from './AnimatedTyping'

export default function Hero(){
  return (
    <header className="relative overflow-hidden rounded-[2rem] border border-white/10 bg-[linear-gradient(135deg,rgba(24,24,24,0.98),rgba(8,8,8,0.92))] p-6 shadow-[0_30px_120px_rgba(0,0,0,0.45)] sm:p-8">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(197,154,106,0.18),transparent_35%),radial-gradient(circle_at_bottom_left,rgba(211,75,75,0.12),transparent_28%)]" />
      <div className="relative flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div className="inline-flex items-center rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.3em] text-[#f3d4ab]">Cinematic prompt lab</div>
          <h1 className="mt-4 max-w-3xl text-4xl font-bold tracking-tight text-white sm:text-5xl lg:text-6xl">AI Bollywood Script Generator</h1>
          <p className="mt-3 max-w-2xl text-base leading-7 text-gray-300 sm:text-lg">Turn ordinary situations into absurd, cinematic dramas with movie titles, character cards, and scene-by-scene dialogue.</p>
          <div className="mt-4 text-sm text-gray-400">
            <AnimatedTyping phrases={["Adding dramatic rain...","Cue background dancers...","Cut to slow-motion..."]} />
          </div>
        </div>
        <div className="grid gap-3 sm:grid-cols-3 lg:w-[420px]">
          <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
            <div className="text-xs uppercase tracking-[0.25em] text-[#c59a6a]">Now Playing</div>
            <div className="mt-2 text-lg font-semibold text-white">The Great Sugar Wars</div>
            <div className="text-sm text-gray-400">IMDb: 9.2 | 3h 21m</div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
            <div className="text-xs uppercase tracking-[0.25em] text-[#c59a6a]">Outputs</div>
            <div className="mt-2 text-2xl font-bold text-white">Titles</div>
            <div className="text-sm text-gray-400">Taglines, scenes, dialogues</div>
          </div>
          <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
            <div className="text-xs uppercase tracking-[0.25em] text-[#c59a6a]">Speed</div>
            <div className="mt-2 text-2xl font-bold text-white">Instant</div>
            <div className="text-sm text-gray-400">Generate and share locally</div>
          </div>
        </div>
      </div>
    </header>
  )
}
