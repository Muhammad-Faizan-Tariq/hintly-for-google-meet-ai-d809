import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import TranscriptStream from '@/components/TranscriptStream'
import HintCard from '@/components/HintCard'

const SAMPLE_HINTS = [
  { suggestion: 'The prospect mentioned budget constraints twice — now is the right moment to present the ROI data.', confidence: 89, type: 'action' as const },
  { suggestion: 'Speaking pace is above 165 wpm. Slow down slightly to improve comprehension and project confidence.', confidence: 94, type: 'tone' as const },
]

export default function DemoPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-[100dvh] bg-slate-50 pt-24 pb-16">
        <div className="max-w-7xl mx-auto px-6">
          <div className="mb-12">
            <p className="text-xs font-semibold text-indigo-600 uppercase tracking-widest mb-3">Interactive Demo</p>
            <h1 className="text-4xl font-bold tracking-tight text-slate-900 mb-3">See Hintly in action.</h1>
            <p className="text-slate-500 text-lg max-w-[55ch]">
              A simulated sales call. Watch AI hints surface in real time as the conversation unfolds.
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-8 items-start">
            <TranscriptStream />
            <div className="space-y-4">
              <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Example Hints</h2>
              {SAMPLE_HINTS.map((h, i) => <HintCard key={i} {...h} />)}
              <div className="mt-6 p-5 bg-white border border-slate-200 rounded-2xl">
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">What Hintly detects</p>
                <ul className="space-y-2 text-sm text-slate-600">
                  {['Unanswered questions from earlier in the call', 'Budget and authority signals', 'Filler words and passive voice', 'Missing next steps and commitments'].map(item => (
                    <li key={item} className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 flex-shrink-0" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
