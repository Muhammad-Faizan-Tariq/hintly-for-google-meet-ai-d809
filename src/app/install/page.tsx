import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import InstallSteps from '@/components/InstallSteps'
import Link from 'next/link'
import { Chrome, Lock, ShieldCheck } from 'lucide-react'

export default function InstallPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-[100dvh] bg-white pt-24 pb-16">
        <div className="max-w-4xl mx-auto px-6">
          <div className="text-center mb-14">
            <p className="text-xs font-semibold text-indigo-600 uppercase tracking-widest mb-3">Chrome Extension</p>
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-slate-900 mb-4">Install Hintly</h1>
            <p className="text-slate-500 text-lg mb-8">Four steps, under two minutes. No credit card required.</p>
            <Link
              href="https://chrome.google.com/webstore"
              className="inline-flex items-center gap-2 px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition-all duration-200 active:scale-[0.98]"
            >
              <Chrome size={20} />
              Add to Chrome — Free
            </Link>
          </div>
          <div className="bg-slate-50 rounded-2xl p-10 border border-slate-100 mb-10">
            <InstallSteps />
          </div>
          <div className="grid md:grid-cols-2 gap-5">
            <div className="flex gap-4 p-6 bg-slate-50 rounded-xl border border-slate-100">
              <Lock size={20} className="text-indigo-600 flex-shrink-0 mt-0.5" strokeWidth={1.5} />
              <div>
                <h3 className="font-semibold text-slate-900 mb-1">Permissions explained</h3>
                <p className="text-slate-500 text-sm leading-relaxed">
                  Hintly only accesses meet.google.com. It reads on-screen captions rendered by Meet — it never touches your microphone, camera, or raw audio stream.
                </p>
              </div>
            </div>
            <div className="flex gap-4 p-6 bg-slate-50 rounded-xl border border-slate-100">
              <ShieldCheck size={20} className="text-indigo-600 flex-shrink-0 mt-0.5" strokeWidth={1.5} />
              <div>
                <h3 className="font-semibold text-slate-900 mb-1">Chrome Web Store verified</h3>
                <p className="text-slate-500 text-sm leading-relaxed">
                  Hintly is reviewed and published in the Chrome Web Store. Enterprise security reviews available on request for Team plans.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
