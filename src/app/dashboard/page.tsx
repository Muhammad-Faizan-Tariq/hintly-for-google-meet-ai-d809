import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import MeetingHistoryTable from '@/components/MeetingHistoryTable'
import AnalyticsChart from '@/components/AnalyticsChart'
import Link from 'next/link'

const stats = [
  { label: 'Meetings this month', value: '23', delta: '+4 vs last month' },
  { label: 'Total hints received', value: '341', delta: '+67 vs last month' },
  { label: 'Avg. score', value: '86.4', delta: '+3.1 vs last month' },
  { label: 'Hours in meetings', value: '18.7', delta: 'this month' },
]

export default function DashboardPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-[100dvh] bg-slate-50 pt-24 pb-16">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between mb-10">
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-slate-900">Dashboard</h1>
              <p className="text-slate-500 mt-1 text-sm">Meeting intelligence for the past 30 days.</p>
            </div>
            <Link href="/install" className="px-4 py-2 bg-indigo-600 text-white text-sm font-semibold rounded-lg hover:bg-indigo-700 transition-colors">
              Get the extension
            </Link>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {stats.map(s => (
              <div key={s.label} className="bg-white rounded-xl border border-slate-200 p-5">
                <p className="text-xs text-slate-500 mb-2">{s.label}</p>
                <p className="text-2xl font-bold text-slate-900 tabular-nums mb-1">{s.value}</p>
                <p className="text-xs text-slate-400">{s.delta}</p>
              </div>
            ))}
          </div>
          <div className="mb-6">
            <AnalyticsChart />
          </div>
          <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h2 className="text-sm font-semibold text-slate-900 mb-5">Recent Meetings</h2>
            <MeetingHistoryTable />
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
