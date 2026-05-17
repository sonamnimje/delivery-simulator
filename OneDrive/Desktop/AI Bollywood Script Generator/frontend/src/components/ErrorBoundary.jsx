import React from 'react'

export default class ErrorBoundary extends React.Component{
  constructor(props){ super(props); this.state = {error: null} }
  static getDerivedStateFromError(error){ return {error} }
  componentDidCatch(err, info){ console.error('ErrorBoundary', err, info) }
  render(){
    if(this.state.error){
      return <div className="p-6 bg-[#1b0b0b] text-red-300">Something went wrong.</div>
    }
    return this.props.children
  }
}
