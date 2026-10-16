import HintCard from './HintCard'

const HINTS = [
  { suggestion: 'Budget approval threshold was mentioned — confirm the decision-maker authority before closing.', confidence: 91, type: 'action' as const },
  { suggestion: 'Tone alert: your last 3 responses used passive voice. Try "We will deliver by Friday" instead.', confidence: 85, type: 'tone' as const },
]

export default function MeetMockup() {
  return (
    <section className="py-24 bg-slate-50 border-y border-slate-100">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid md:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-slate-900 mb-4">
              Runs inside your meeting. Stays out of the way.
            </h2>
            <p className="text-slate-500 leading-relaxed mb-8 max-w-[50ch]">
              A collapsible sidebar pins to the right of Meet. Hints appear, you act, they fade. No switching apps, no taking notes mid-sentence.
            </p>
            <ul className="space-y-4">
              {[
                'Invisible to other participants',
                'Works with any Google Workspace account',
                'Zero audio or video data leaves your device',
              ].map(item => (
                <li key={item} className="flex items-center gap-3 text-sm text-slate-600">
                  <div className="w-5 h-5 rounded-full bg-indigo-100 flex items-center justify-center flex-shrink-0">
                    <div className="w-2 h-2 rounded-full bg-indigo-600" />
                  </div>
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div className="space-y-3">
            {HINTS.map((hint, i) => (
              <HintCard key={i} {...hint} />
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
