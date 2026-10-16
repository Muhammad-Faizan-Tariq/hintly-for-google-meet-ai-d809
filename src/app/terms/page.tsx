import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'

const sections = [
  {
    title: 'Acceptance',
    body: 'By installing Hintly or using any Hintly service, you agree to these Terms. If you do not agree, uninstall the extension and cease use of Hintly services.',
  },
  {
    title: 'Permitted use',
    body: 'Hintly is licensed for personal and professional use within the constraints of your subscription plan. You may not reverse-engineer, redistribute, or use Hintly AI outputs to train competing machine learning models.',
  },
  {
    title: 'Subscriptions and billing',
    body: 'Pro and Team plans are billed monthly or annually. You may cancel at any time; your plan remains active until the end of the billing period. No partial refunds are issued for unused time.',
  },
  {
    title: 'Limitation of liability',
    body: 'Hintly provides AI-generated suggestions which may contain errors. Hintly is not liable for decisions made based on AI output. Apply professional judgment at all times.',
  },
  {
    title: 'Contact',
    body: 'Legal inquiries: legal@hintly.ai',
  },
]

export default function TermsPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-[100dvh] bg-white pt-28 pb-24">
        <div className="max-w-3xl mx-auto px-6">
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 mb-2">Terms of Service</h1>
          <p className="text-slate-400 text-sm mb-14">Last updated: October 16, 2026</p>
          <div className="space-y-10">
            {sections.map(s => (
              <section key={s.title}>
                <h2 className="text-lg font-bold text-slate-900 mb-3">{s.title}</h2>
                <p className="text-slate-600 leading-relaxed text-sm">{s.body}</p>
              </section>
            ))}
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
