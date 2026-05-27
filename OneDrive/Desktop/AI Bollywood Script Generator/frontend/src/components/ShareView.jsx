import React, {useEffect, useState} from 'react'

export default function ShareView({slug}){
  const [item, setItem] = useState(null)

  useEffect(()=>{
    const store = JSON.parse(localStorage.getItem('drama_shares')||'{}')
    setItem(store[slug] || null)
  },[slug])

  if(!slug) return null
  if(!item) return <div className="mb-4 rounded-3xl border border-white/10 bg-white/5 p-4 text-gray-300">Shared drama not found.</div>

  const d = item.drama
  return (
    <div className="mb-4 rounded-[2rem] border border-white/10 bg-[linear-gradient(180deg,rgba(15,15,15,0.95),rgba(8,8,8,0.96))] p-5 shadow-[0_24px_90px_rgba(0,0,0,0.35)] sm:p-6">
      <div className="text-xs uppercase tracking-[0.3em] text-[#c59a6a]">Shared drama</div>
      <h2 className="mt-2 text-3xl font-semibold text-white">{d.movie_title}</h2>
      <p className="mt-2 max-w-3xl text-gray-300">{d.tagline}</p>
      <div className="mt-5 grid gap-3 md:grid-cols-2">
        {d.scenes.map(s=> (
          <div key={s.scene_index} className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="text-xs uppercase tracking-[0.25em] text-[#c59a6a]">Scene {s.scene_index}</div>
            <div className="mt-1 font-semibold text-white">{s.scene_title}</div>
            <div className="mt-2 text-sm leading-6 text-gray-300">{s.scene_description}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
