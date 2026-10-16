import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="border-t border-slate-100 bg-white">
      <div className="max-w-7xl mx-auto px-6 py-12 flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-md bg-indigo-600 flex items-center justify-center">
            <span className="text-white text-xs font-bold">H</span>
          </div>
          <span className="font-bold text-slate-900">Hintly</span>
          <span className="text-slate-400 text-sm">— AI Meeting Assistant</span>
        </div>
        <nav className="flex flex-wrap justify-center gap-6 text-sm text-slate-500">
          <Link href="/demo" className="hover:text-slate-900 transition-colors">Demo</Link>
          <Link href="/install" className="hover:text-slate-900 transition-colors">Install</Link>
          <Link href="/dashboard" className="hover:text-slate-900 transition-colors">Dashboard</Link>
          <Link href="/privacy" className="hover:text-slate-900 transition-colors">Privacy</Link>
          <Link href="/terms" className="hover:text-slate-900 transition-colors">Terms</Link>
        </nav>
        <p className="text-xs text-slate-400">2026 Hintly, Inc.</p>
      </div>
    </footer>
  )
}
