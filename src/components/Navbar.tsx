'use client'
import Link from 'next/link'
import { useState } from 'react'
import { Menu, X } from 'lucide-react'

export default function Navbar() {
  const [open, setOpen] = useState(false)
  return (
    <nav className="fixed top-0 w-full z-50 bg-white/90 backdrop-blur border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center">
            <span className="text-white text-xs font-bold tracking-tight">H</span>
          </div>
          <span className="font-bold text-slate-900 tracking-tight">Hintly</span>
        </Link>
        <div className="hidden md:flex items-center gap-8 text-sm text-slate-600">
          <Link href="/demo" className="hover:text-slate-900 transition-colors">Demo</Link>
          <Link href="/install" className="hover:text-slate-900 transition-colors">Install</Link>
          <Link href="/dashboard" className="hover:text-slate-900 transition-colors">Dashboard</Link>
        </div>
        <div className="hidden md:flex items-center gap-3">
          <Link href="/login" className="text-sm text-slate-600 hover:text-slate-900 transition-colors">Sign in</Link>
          <Link href="/install" className="px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 transition-colors active:scale-[0.98]">
            Add to Chrome
          </Link>
        </div>
        <button className="md:hidden p-1" onClick={() => setOpen(!open)} aria-label="Toggle menu">
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>
      {open && (
        <div className="md:hidden bg-white border-t border-slate-100 px-6 py-4 flex flex-col gap-4 text-sm text-slate-700">
          <Link href="/demo" onClick={() => setOpen(false)}>Demo</Link>
          <Link href="/install" onClick={() => setOpen(false)}>Install</Link>
          <Link href="/dashboard" onClick={() => setOpen(false)}>Dashboard</Link>
          <Link href="/login" onClick={() => setOpen(false)}>Sign in</Link>
          <Link href="/install" onClick={() => setOpen(false)} className="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg text-center">Add to Chrome</Link>
        </div>
      )}
    </nav>
  )
}
