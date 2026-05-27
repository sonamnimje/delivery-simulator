import React from 'react'

export default function SidebarHistory({items=[]}){
  return (
    <div className="rounded-[2rem] border border-white/10 bg-[linear-gradient(180deg,rgba(13,13,13,0.94),rgba(7,7,7,0.98))] p-4 shadow-[0_24px_90px_rgba(0,0,0,0.35)] backdrop-blur-xl">
      <div className="flex items-end justify-between gap-3">
        <div>
          <div className="text-xs uppercase tracking-[0.3em] text-[#c59a6a]">Archive</div>
          <h3 className="mt-1 text-xl font-semibold text-white">History</h3>
        </div>
        <div className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-gray-300">{items.length}</div>
      </div>
      <div className="mt-4 max-h-[70vh] space-y-3 overflow-auto pr-1">
        {items.length===0 && <div className="rounded-2xl border border-dashed border-white/10 bg-white/5 p-4 text-sm text-gray-400">No history yet. Your first generated drama will appear here.</div>}
        {items.map(it=> (
          <div key={it.id} className="rounded-2xl border border-white/8 bg-white/5 p-3 transition hover:border-white/15 hover:bg-white/8">
            <div className="font-medium text-white">{it.data.movie_title || it.situation}</div>
            <div className="mt-1 text-xs uppercase tracking-[0.2em] text-[#f3d4ab]">{it.mood}</div>
            <div className="mt-2 text-sm text-gray-400">{new Date(it.id).toLocaleString()}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
