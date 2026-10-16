'use client'
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'

const data = [
  { week: 'W40', hints: 31, score: 79 },
  { week: 'W41', hints: 44, score: 83 },
  { week: 'W42', hints: 38, score: 81 },
  { week: 'W43', hints: 59, score: 88 },
  { week: 'W44', hints: 52, score: 91 },
]

const tooltipStyle = { borderRadius: 8, border: '1px solid #e2e8f0', fontSize: 12, boxShadow: '0 4px 12px rgba(0,0,0,0.06)' }

export default function AnalyticsChart() {
  return (
    <div className="grid md:grid-cols-2 gap-5">
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-5">Hints per Week</p>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={data} barSize={22}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
            <XAxis dataKey="week" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={tooltipStyle} cursor={{ fill: '#f8fafc' }} />
            <Bar dataKey="hints" fill="#4f46e5" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-5">Communication Score Trend</p>
        <ResponsiveContainer width="100%" height={180}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
            <XAxis dataKey="week" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
            <YAxis domain={[70, 100]} tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={tooltipStyle} />
            <Line type="monotone" dataKey="score" stroke="#4f46e5" strokeWidth={2} dot={{ r: 4, fill: '#4f46e5', strokeWidth: 0 }} activeDot={{ r: 5 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
