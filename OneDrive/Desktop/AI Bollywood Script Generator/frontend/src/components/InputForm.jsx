import React, {useState} from 'react'
import axios from 'axios'
import SkeletonScene from './SkeletonScene'

const moods = ["Bollywood Masala","Dark Thriller","Sci-Fi Action","Emotional Drama","South Indian Mass","Hollywood Epic"]

export default function InputForm({onSave}){
  const [situation, setSituation] = useState('')
  const [mood, setMood] = useState(moods[0])
  const [loading, setLoading] = useState(false)
  const [drama, setDrama] = useState(null)

  async function handleRegenerate(){
    if(!drama) return
    setLoading(true)
    try{
      const res = await axios.post('/api/generate', {situation, mood})
      setDrama(res.data)
      onSave({id: Date.now(), slug: String(Date.now()), situation, mood, data: res.data})
    }catch(err){
      const m = err?.response?.data?.detail || err.message
      window.dispatchEvent(new CustomEvent('app:toast', {detail: m}))
    }finally{setLoading(false)}
  }

  async function handleRegenerateScene(scene_index){
    if(!drama) return
    setLoading(true)
    try{
      const payload = { drama, scene_index }
      const res = await axios.post('/api/generate/regenerate-scene', payload)
      const newScene = res.data.scene
      // replace scene in drama
      const next = {...drama}
      next.scenes = next.scenes.map(s=> s.scene_index===newScene.scene_index? newScene : s)
      setDrama(next)
      onSave({id: Date.now(), slug: String(Date.now()), situation, mood, data: next})
    }catch(err){
      const m = err?.response?.data?.detail || err.message
      window.dispatchEvent(new CustomEvent('app:toast', {detail: m}))
    }finally{setLoading(false)}
  }

  function handleShare(){
    if(!drama) return
    const slug = Date.now().toString(36)
    const store = JSON.parse(localStorage.getItem('drama_shares')||'{}')
    store[slug] = {slug, drama, situation, mood, created: Date.now()}
    localStorage.setItem('drama_shares', JSON.stringify(store))
    navigator.clipboard?.writeText(window.location.href.split('#')[0] + `?share=${slug}`)
    window.dispatchEvent(new CustomEvent('app:toast', {detail: 'Share link copied to clipboard!'}))
  }

  async function handleSubmit(e){
    e.preventDefault()
    setLoading(true)
    try{
      const res = await axios.post('/api/generate', {situation, mood})
      setDrama(res.data)
      onSave({id: Date.now(), slug: String(Date.now()), situation, mood, data: res.data})
    }catch(err){
      const m = err?.response?.data?.detail || err.message
      window.dispatchEvent(new CustomEvent('app:toast', {detail: m}))
    }finally{setLoading(false)}
  }

  return (
    <div className="rounded-[2rem] border border-white/10 bg-[linear-gradient(180deg,rgba(15,15,15,0.92),rgba(8,8,8,0.96))] p-5 shadow-[0_30px_100px_rgba(0,0,0,0.45)] backdrop-blur-xl sm:p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div className="text-xs uppercase tracking-[0.3em] text-[#c59a6a]">Script studio</div>
          <h2 className="mt-2 text-2xl font-semibold">Describe the setup. We’ll add the chaos.</h2>
        </div>
        <div className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.25em] text-gray-300">
          {situation.trim().length} chars
        </div>
      </div>

      <form onSubmit={handleSubmit} className="mt-5 space-y-4">
        <label className="block text-sm text-gray-300">Describe a normal situation</label>
        <textarea
          value={situation}
          onChange={(e)=>setSituation(e.target.value)}
          placeholder="Two roommates arguing over AC temperature"
          rows={5}
          className="w-full rounded-2xl border border-white/10 bg-black/40 p-4 text-base text-white outline-none transition placeholder:text-gray-500 focus:border-[#c59a6a]/60 focus:ring-2 focus:ring-[#c59a6a]/20"
        />

        <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
          <div className="flex flex-wrap gap-2">
            {moods.map((option)=> (
              <button
                key={option}
                type="button"
                onClick={()=>setMood(option)}
                className={`rounded-full border px-4 py-2 text-sm transition ${mood===option ? 'border-[#c59a6a] bg-[#c59a6a]/15 text-[#f5d0a4]' : 'border-white/10 bg-white/5 text-gray-300 hover:border-white/20 hover:bg-white/10'}`}
              >
                {option}
              </button>
            ))}
          </div>
          <div className="ml-auto flex gap-2">
            <button type="button" onClick={()=>{setSituation(''); setDrama(null)}} className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-gray-300 transition hover:bg-white/10">
              Reset
            </button>
            <button type="submit" disabled={loading || !situation.trim()} className="rounded-full bg-gradient-to-r from-[#f3c977] via-[#d58b43] to-[#b23c2e] px-5 py-2.5 font-semibold text-black shadow-[0_15px_40px_rgba(213,139,67,0.25)] transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-60">
              {loading ? 'Composing the montage...' : 'Generate Drama'}
            </button>
          </div>
        </div>
      </form>

      {loading && !drama && (
        <div className="mt-6 rounded-3xl border border-white/10 bg-white/5 p-4">
          <div className="text-sm text-gray-300">Calling background dancers...</div>
          <div className="mt-4 space-y-3">
            <SkeletonScene />
            <SkeletonScene />
            <SkeletonScene />
          </div>
        </div>
      )}

      {drama && (
        <div className="mt-6 space-y-4">
          <div className="rounded-[2rem] border border-white/10 bg-white/5 p-5 backdrop-blur-sm sm:p-6">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <div className="text-xs uppercase tracking-[0.3em] text-[#c59a6a]">Generated feature</div>
                <h2 className="mt-2 text-3xl font-bold text-[#f6ddbf] sm:text-4xl">{drama.movie_title}</h2>
                <p className="mt-2 max-w-3xl text-base text-gray-300 sm:text-lg">{drama.tagline}</p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-black/30 px-4 py-3 text-sm text-gray-300">
                <div className="text-xs uppercase tracking-[0.25em] text-[#c59a6a]">Mood</div>
                <div className="mt-1 font-semibold text-white">{mood}</div>
              </div>
            </div>

            <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {drama.characters.map((character, index)=> (
                <div key={`${character.name}-${index}`} className="rounded-2xl border border-white/10 bg-black/30 p-4">
                  <div className="text-xs uppercase tracking-[0.25em] text-[#c59a6a]">Character</div>
                  <div className="mt-2 text-lg font-semibold text-white">{character.name}</div>
                  <div className="text-sm text-[#f0c78b]">{character.role}</div>
                  <div className="mt-2 text-sm text-gray-300">{character.description}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-4">
            {drama.scenes.map(s=> (
              <div key={s.scene_index} className="rounded-[1.75rem] border border-white/10 bg-[linear-gradient(180deg,rgba(18,18,18,0.96),rgba(9,9,9,0.98))] p-4 shadow-[0_18px_60px_rgba(0,0,0,0.35)] sm:p-5">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="text-xs uppercase tracking-[0.3em] text-[#c59a6a]">Scene {s.scene_index}</div>
                    <div className="mt-1 text-xl font-semibold text-white">{s.scene_title}</div>
                    <div className="mt-2 max-w-3xl text-sm leading-6 text-gray-300">{s.scene_description}</div>
                  </div>
                  <div className="rounded-full border border-[#c59a6a]/30 bg-[#c59a6a]/10 px-3 py-1 text-xs uppercase tracking-[0.25em] text-[#f3d4ab]">{s.mood}</div>
                </div>
                <div className="mt-4 space-y-3">
                  {s.dialogues.map((d,i)=> (
                    <div key={i} className="flex gap-3 rounded-2xl border border-white/8 bg-white/5 p-3">
                      <div className="min-w-24 font-semibold text-[#f3d4ab]">{d.character}:</div>
                      <div className="text-gray-100">{d.line}</div>
                    </div>
                  ))}
                </div>
                <div className="mt-4 flex flex-wrap gap-2">
                  <button type="button" onClick={()=>handleRegenerateScene(s.scene_index)} className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-gray-200 transition hover:bg-white/10">Regenerate Scene</button>
                  <button type="button" onClick={()=>{navigator.clipboard?.writeText(JSON.stringify(s)); window.dispatchEvent(new CustomEvent('app:toast', {detail: 'Scene JSON copied'}))}} className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-gray-200 transition hover:bg-white/10">Copy Scene</button>
                </div>
              </div>
            ))}
          </div>
          <div className="flex flex-wrap gap-3">
            <button onClick={handleRegenerate} className="rounded-full bg-gradient-to-r from-[#f3c977] via-[#d58b43] to-[#b23c2e] px-5 py-3 font-semibold text-black transition hover:scale-[1.01]">Regenerate Script</button>
            <button onClick={handleShare} className="rounded-full border border-white/10 bg-white/5 px-5 py-3 text-gray-100 transition hover:bg-white/10">Share Drama</button>
          </div>
        </div>
      )}
    </div>
  )
}
