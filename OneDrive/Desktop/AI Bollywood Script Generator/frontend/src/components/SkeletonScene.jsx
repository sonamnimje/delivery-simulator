import React from 'react'

export default function SkeletonScene(){
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4 animate-pulse">
      <div className="h-4 w-1/3 rounded-full bg-white/10 mb-3"></div>
      <div className="h-3 w-full rounded-full bg-white/8 mb-2"></div>
      <div className="h-3 w-5/6 rounded-full bg-white/8 mb-2"></div>
      <div className="h-3 w-2/3 rounded-full bg-white/8"></div>
    </div>
  )
}
