import Link from 'next/link'
import { Chrome, ArrowRight, CheckCircle2 } from 'lucide-react'

const BADGES = ['Real-time hints', 'Action items', 'Tone coaching', 'Follow-up drafts']

export default function Hero() {
  return (
    <section className="min-h-[100dvh] flex items-center bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 pt-16">
      <div className="max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-2 gap-16 items-center w-full">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-indigo-500/10 border border-indigo-500/20 rounded-full text-indigo-400 text-xs font-medium mb-6">
            <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />
            Chrome Extension — Free to install
          </div>
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-white leading-tight mb-6">
            Think faster in<br />
            <span className="text-indigo-400">every meeting.</span>
          </h1>
          <p className="text-lg text-slate-400 leading-relaxed max-w-[52ch] mb-8">
            Hintly runs alongside Google Meet and delivers AI-powered hints, action items, and tone coaching in real time — so you stay sharp without missing a beat.
          </p>
          <div className="flex flex-wrap gap-x-6 gap-y-2 mb-10">
            {BADGES.map(b => (
              <div key={b} className="flex items-center gap-1.5 text-xs text-slate-400">
                <CheckCircle2 size={13} className="text-indigo-400" />
                {b}
              </div>
            ))}
          </div>
          <div className="flex flex-wrap gap-3">
            <Link href="/install" className="flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl transition-all duration-200 active:scale-[0.98]">
              <Chrome size={18} />
              Add to Chrome — Free
            </Link>
            <Link href="/demo" className="flex items-center gap-2 px-6 py-3 border border-slate-700 text-slate-300 hover:border-slate-500 hover:text-white rounded-xl transition-all duration-200">
              See live demo <ArrowRight size={16} />
            </Link>
          </div>
        </div>
        <div className="relative hidden md:block">
          <div className="bg-slate-800 rounded-2xl overflow-hidden border border-slate-700 shadow-2xl shadow-black/40">
            <div className="bg-slate-900 px-4 py-2.5 flex items-center gap-2 border-b border-slate-700">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/60" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/60" />
                <div className="w-3 h-3 rounded-full bg-green-500/60" />
              </div>
              <span className="text-slate-500 text-xs ml-2 font-mono">meet.google.com/rqw-bxkp-zna</span>
            </div>
            <div className="p-4 grid grid-cols-3 gap-2">
              {['AK', 'ML', 'TR', 'SJ'].map((init, i) => (
                <div key={init} className={`${i === 0 ? 'col-span-2' : ''} aspect-video bg-slate-700 rounded-lg flex items-center justify-center`}>
                  <div className="w-9 h-9 rounded-full bg-indigo-600/40 border border-indigo-500/30 text-indigo-300 flex items-center justify-center text-xs font-bold">{init}</div>
                </div>
              ))}
            </div>
            <div className="mx-4 mb-4 bg-indigo-950/60 border border-indigo-800/40 rounded-xl p-4">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
                <span className="text-indigo-300 text-xs font-semibold">Hintly Hint</span>
                <span className="ml-auto text-xs text-green-400 font-medium tabular-nums">94% confident</span>
              </div>
              <p className="text-slate-200 text-xs leading-relaxed">
                Ask about Q4 budget allocation — the client mentioned constraints twice and has not addressed the decision timeline yet.
              </p>
            </div>
          </div>
          <div className="absolute -bottom-6 -right-6 w-32 h-32 bg-indigo-600/15 rounded-full blur-3xl pointer-events-none" />
        </div>
      </div>
    </section>
  )
}
