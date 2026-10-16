import Link from 'next/link'

export default function LoginPage() {
  return (
    <main className="min-h-[100dvh] bg-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-indigo-600 flex items-center justify-center mx-auto mb-4">
            <span className="text-white text-xl font-bold">H</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Sign in to Hintly</h1>
          <p className="text-slate-500 text-sm mt-2">Access your meeting history and analytics.</p>
        </div>
        <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm shadow-slate-100">
          <a
            href="/api/auth/google"
            className="flex items-center justify-center gap-3 w-full py-3 px-4 border border-slate-200 rounded-xl text-slate-700 font-medium hover:bg-slate-50 transition-colors active:scale-[0.98]"
          >
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
              <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908C16.658 14.233 17.64 11.925 17.64 9.2z" fill="#4285F4"/>
              <path d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18z" fill="#34A853"/>
              <path d="M3.964 10.707A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.707V4.961H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.039l3.007-2.332z" fill="#FBBC05"/>
              <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.96L3.964 7.293C4.672 5.163 6.656 3.58 9 3.58z" fill="#EA4335"/>
            </svg>
            Continue with Google
          </a>
          <p className="text-center text-xs text-slate-400 mt-6">
            By continuing, you agree to Hintly&apos;s{' '}
            <Link href="/terms" className="text-indigo-600 hover:underline">Terms</Link>
            {' '}and{' '}
            <Link href="/privacy" className="text-indigo-600 hover:underline">Privacy Policy</Link>.
          </p>
        </div>
        <p className="text-center mt-6 text-sm text-slate-500">
          New to Hintly?{' '}
          <Link href="/install" className="text-indigo-600 font-medium hover:underline">Install the extension</Link>
        </p>
      </div>
    </main>
  )
}
