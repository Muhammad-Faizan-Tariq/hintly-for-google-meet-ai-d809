import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'

const sections = [
  {
    title: 'What data Hintly collects',
    body: 'Hintly accesses closed-caption text rendered on screen by Google Meet. This text is processed and sent to Hintly servers only when you choose to save a meeting summary. We do not record audio, video, or raw microphone input at any point.',
  },
  {
    title: 'How we use your data',
    body: 'Caption data is used exclusively to generate AI hints in real time. Summaries you save are stored securely and linked to your Google account. We never sell, share, or license your meeting data to third parties.',
  },
  {
    title: 'Data retention',
    body: 'Meeting summaries are retained for 12 months or until you delete them. You can export or permanently delete all your data at any time from Dashboard settings.',
  },
  {
    title: 'Security',
    body: 'All data in transit is encrypted with TLS 1.3. At-rest data is encrypted with AES-256. We undergo annual SOC 2 Type II audits.',
  },
  {
    title: 'Contact',
    body: 'Questions or data requests? Email privacy@hintly.ai — we respond within 48 hours.',
  },
]

export default function PrivacyPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-[100dvh] bg-white pt-28 pb-24">
        <div className="max-w-3xl mx-auto px-6">
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 mb-2">Privacy Policy</h1>
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
