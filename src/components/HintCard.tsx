interface HintCardProps {
  suggestion: string
  confidence: number
  type: 'action' | 'tone' | 'info'
}

const typeStyles = {
  action: { border: 'border-indigo-200', bg: 'bg-indigo-50', badge: 'bg-indigo-100 text-indigo-700', label: 'Action' },
  tone: { border: 'border-amber-200', bg: 'bg-amber-50', badge: 'bg-amber-100 text-amber-700', label: 'Tone' },
  info: { border: 'border-slate-200', bg: 'bg-slate-50', badge: 'bg-slate-100 text-slate-700', label: 'Info' },
}

export default function HintCard({ suggestion, confidence, type }: HintCardProps) {
  const s = typeStyles[type]
  return (
    <div className={`border ${s.border} ${s.bg} rounded-2xl p-5`}>
      <div className="flex items-center justify-between mb-3">
        <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${s.badge}`}>{s.label}</span>
        <span className="text-xs text-slate-400 font-medium tabular-nums">{confidence}% confident</span>
      </div>
      <p className="text-slate-700 text-sm leading-relaxed">{suggestion}</p>
    </div>
  )
}
