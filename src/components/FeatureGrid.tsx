import { Brain, ListTodo, MessageCircle, Mail } from 'lucide-react'

const features = [
  { icon: Brain, title: 'Real-Time Hints', desc: 'Context-aware suggestions surface as the conversation unfolds — no lag, no tab-switching.', stat: '2.3s', statLabel: 'avg hint latency' },
  { icon: ListTodo, title: 'Action Items', desc: 'Automatically extracts commitments, owners, and deadlines from every exchange.', stat: '37%', statLabel: 'fewer missed tasks' },
  { icon: MessageCircle, title: 'Tone Coach', desc: 'Live feedback on pacing, filler words, and assertiveness. Sound like the best version of yourself.', stat: '4.1x', statLabel: 'confidence score gain' },
  { icon: Mail, title: 'Follow-Up Drafts', desc: 'Meeting ends, follow-up email is ready. Structured recap with next steps, sent in one click.', stat: '8 min', statLabel: 'saved per meeting' },
]

export default function FeatureGrid() {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <div className="mb-14">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-slate-900 mb-4">
            Built for the moments that matter most.
          </h2>
          <p className="text-slate-500 text-lg max-w-[55ch]">
            Four AI capabilities, one sidebar. Hintly runs silently until you need it.
          </p>
        </div>
        <div className="grid md:grid-cols-2 border border-slate-200 rounded-2xl overflow-hidden divide-y md:divide-y-0 divide-slate-200">
          {features.map(({ icon: Icon, title, desc, stat, statLabel }, i) => (
            <div key={title} className={`bg-white p-8 hover:bg-slate-50 transition-colors ${i % 2 === 0 ? 'md:border-r border-slate-200' : ''}`}>
              <div className="w-10 h-10 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center mb-5">
                <Icon size={20} className="text-indigo-600" strokeWidth={1.5} />
              </div>
              <h3 className="font-bold text-slate-900 text-lg mb-2">{title}</h3>
              <p className="text-slate-500 text-sm leading-relaxed mb-6">{desc}</p>
              <div className="border-t border-slate-100 pt-4 flex items-end gap-2">
                <span className="text-2xl font-bold text-slate-900 tabular-nums">{stat}</span>
                <span className="text-xs text-slate-400 mb-0.5">{statLabel}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
