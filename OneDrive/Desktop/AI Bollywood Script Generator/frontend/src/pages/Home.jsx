import React, {useState, useEffect} from 'react'
import InputForm from '../components/InputForm'
import SidebarHistory from '../components/SidebarHistory'
import Hero from '../components/Hero'
import ShareView from '../components/ShareView'
import Footer from '../components/Footer'

export default function Home(){
  const [history, setHistory] = useState([])

  useEffect(()=>{
    try{
      const h = JSON.parse(localStorage.getItem('drama_history')||'[]')
      setHistory(h)
    }catch(e){setHistory([])}
  },[])

  const params = new URLSearchParams(window.location.search)
  const share = params.get('share')

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
      <Hero />

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="rounded-3xl border border-white/10 bg-white/5 p-4 backdrop-blur-sm shadow-[0_20px_80px_rgba(0,0,0,0.35)]">
          <div className="text-xs uppercase tracking-[0.3em] text-[#c59a6a]">Instant drama</div>
          <div className="mt-2 text-2xl font-semibold">From ordinary to absurd in one prompt.</div>
        </div>
        <div className="rounded-3xl border border-white/10 bg-white/5 p-4 backdrop-blur-sm">
          <div className="text-xs uppercase tracking-[0.3em] text-[#c59a6a]">Refined scenes</div>
          <div className="mt-2 text-2xl font-semibold">Character cards, dialogue beats, and cinematic pacing.</div>
        </div>
        <div className="rounded-3xl border border-white/10 bg-white/5 p-4 backdrop-blur-sm">
          <div className="text-xs uppercase tracking-[0.3em] text-[#c59a6a]">Shareable output</div>
          <div className="mt-2 text-2xl font-semibold">Save drafts locally and share a polished version.</div>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1fr)_340px]">
        <main className="space-y-6">
          {share ? <ShareView slug={share} /> : null}
          <InputForm onSave={(d)=>{setHistory(prev=>{const next=[d,...prev].slice(0,50); localStorage.setItem('drama_history', JSON.stringify(next)); return next})}} />
        </main>
        <aside className="lg:sticky lg:top-6 lg:self-start">
          <SidebarHistory items={history} />
        </aside>
      </div>
      <Footer />
    </div>
  )
}
