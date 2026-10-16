import { Download, ShieldCheck, ToggleRight, Video } from 'lucide-react'

const steps = [
  { icon: Download, step: '01', title: 'Click "Add to Chrome"', desc: 'Visit the Chrome Web Store and install Hintly. Takes under 30 seconds — no account required.' },
  { icon: ShieldCheck, step: '02', title: 'Grant permissions', desc: 'Hintly requests access to meet.google.com only. It reads on-screen captions — never audio or video.' },
  { icon: ToggleRight, step: '03', title: 'Pin the extension', desc: 'Click the puzzle piece icon in the Chrome toolbar and pin Hintly for one-click access.' },
  { icon: Video, step: '04', title: 'Join any meeting', desc: 'Start a Google Meet call. The Hintly sidebar opens automatically and begins listening.' },
]

export default function InstallSteps() {
  return (
    <div className="grid sm:grid-cols-2 gap-8">
      {steps.map(({ icon: Icon, step, title, desc }) => (
        <div key={step} className="flex gap-4">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center flex-shrink-0">
            <Icon size={18} className="text-white" strokeWidth={1.5} />
          </div>
          <div>
            <p className="text-xs font-mono text-indigo-500 mb-1">{step}</p>
            <h3 className="font-semibold text-slate-900 mb-1.5">{title}</h3>
            <p className="text-slate-500 text-sm leading-relaxed">{desc}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
