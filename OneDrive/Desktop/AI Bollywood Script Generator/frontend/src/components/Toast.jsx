import React, {useEffect, useState} from 'react'

export default function Toast(){
  const [msg, setMsg] = useState(null)

  useEffect(()=>{
    function handler(e){ setMsg(e.detail) }
    window.addEventListener('app:toast', handler)
    return ()=> window.removeEventListener('app:toast', handler)
  },[])

  useEffect(()=>{
    if(!msg) return
    const t = setTimeout(()=> setMsg(null), 3500)
    return ()=> clearTimeout(t)
  },[msg])

  if(!msg) return null

  return (
    <div className="fixed bottom-6 right-6 z-50 max-w-sm rounded-2xl border border-white/10 bg-[#0d0d0d]/95 px-4 py-3 text-sm text-white shadow-[0_20px_60px_rgba(0,0,0,0.45)] backdrop-blur">
      <div className="text-xs uppercase tracking-[0.25em] text-[#c59a6a]">Studio note</div>
      <div className="mt-1">{msg}</div>
    </div>
  )
}
