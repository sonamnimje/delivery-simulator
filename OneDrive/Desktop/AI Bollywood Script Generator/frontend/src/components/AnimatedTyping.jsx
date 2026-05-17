import React, {useEffect, useState} from 'react'

export default function AnimatedTyping({phrases, speed=80}){
  const [idx, setIdx] = useState(0)
  const [pos, setPos] = useState(0)
  const [forward, setForward] = useState(true)

  useEffect(()=>{
    const p = phrases[idx]
    const t = setTimeout(()=>{
      if(forward){
        if(pos < p.length) setPos(pos+1)
        else setForward(false)
      } else {
        if(pos>0) setPos(pos-1)
        else { setForward(true); setIdx((idx+1)%phrases.length) }
      }
    }, speed)
    return ()=> clearTimeout(t)
  },[pos, idx, forward, phrases, speed])

  return <span>{phrases[idx].slice(0,pos)}<span className="blinking">|</span></span>
}
