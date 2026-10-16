'use client'
import { useState } from 'react'

interface Segment { speaker: string; text: string; hint?: string; confidence?: number }

export default function TranscriptStream() {
  const [segments, setSegments] = useState<Segment[]>([])
  const [status, setStatus] = useState<'idle' | 'streaming' | 'done'>('idle')

  const start = () => {
    setSegments([])
    setStatus('streaming')
    const es = new EventSource('/api/demo/stream')
    es.onmessage = (e) => {
      const seg: Segment = JSON.parse(e.data)
      setSegments(prev => [...prev, seg])
    }
    es.onerror = () => { es.close(); setStatus('done') }
  }

  return (
    <div className="bg-slate-950 rounded-2xl overflow-hidden border border-slate-800">
      <div className="bg-slate-900 px-5 py-3 flex items-center justify-between border-b border-slate-800">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${status === 'streaming' ? 'bg-green-400 animate-pulse' : 'bg-slate-600'}`} />
          <span className="text-xs text-slate-400 font-medium">Live Transcript</span>
        </div>
        <button
          onClick={start}
          className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg transition-colors active:scale-[0.98]"
        >
          {status === 'idle' ? 'Start Demo' : 'Restart'}
        </button>
      </div>
      <div className="p-5 h-80 overflow-y-auto space-y-5">
        {segments.length === 0 && (
          <p className="text-slate-600 text-sm text-center mt-20">Click &quot;Start Demo&quot; to see a live meeting simulation.</p>
        )}
        {segments.map((seg, i) => (
          <div key={i} className="space-y-2">
            <div className="flex gap-3">
              <span className="text-xs font-semibold text-indigo-400 w-14 shrink-0 pt-0.5">{seg.speaker}</span>
              <p className="text-sm text-slate-300 leading-relaxed">{seg.text}</p>
            </div>
            {seg.hint && (
              <div className="ml-17 pl-3 border-l-2 border-indigo-600">
                <div className="bg-indigo-950/60 border border-indigo-800/50 rounded-xl px-4 py-3 ml-14">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-semibold text-indigo-400">Hintly</span>
                    <span className="text-xs text-green-400 tabular-nums">{seg.confidence}% confident</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">{seg.hint}</p>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
