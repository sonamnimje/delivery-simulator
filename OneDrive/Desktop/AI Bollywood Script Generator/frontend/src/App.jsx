import React from 'react'
import Home from './pages/Home'
import Toast from './components/Toast'
import ErrorBoundary from './components/ErrorBoundary'

export default function App(){
  return (
    <ErrorBoundary>
      <div className="min-h-screen relative overflow-hidden text-white bg-[#050505]">
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute -top-32 left-0 h-80 w-80 rounded-full bg-[#c59a6a]/20 blur-3xl" />
          <div className="absolute top-40 right-0 h-96 w-96 rounded-full bg-[#d34b4b]/10 blur-3xl" />
          <div className="absolute bottom-0 left-1/3 h-72 w-72 rounded-full bg-[#2a4d73]/15 blur-3xl" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(255,255,255,0.08),_transparent_38%),linear-gradient(180deg,_rgba(255,255,255,0.03),_transparent_22%)]" />
        </div>
        <div className="relative z-10">
          <Home />
          <Toast />
        </div>
      </div>
    </ErrorBoundary>
  )
}
