const meetings = [
  { id: '1', title: 'Q4 Strategy Review', date: 'Oct 14, 2026', duration: '52 min', hints: 14, score: 87 },
  { id: '2', title: 'Engineering Standup', date: 'Oct 13, 2026', duration: '18 min', hints: 4, score: 92 },
  { id: '3', title: 'Product Roadmap Walkthrough', date: 'Oct 12, 2026', duration: '61 min', hints: 21, score: 78 },
  { id: '4', title: 'Client Onboarding — Meridian Group', date: 'Oct 11, 2026', duration: '34 min', hints: 11, score: 83 },
  { id: '5', title: 'Design Review: Dashboard v3', date: 'Oct 9, 2026', duration: '41 min', hints: 9, score: 89 },
]

export default function MeetingHistoryTable() {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-200">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 border-b border-slate-200">
          <tr>
            {['Meeting', 'Date', 'Duration', 'Hints', 'Score'].map(h => (
              <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wide">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {meetings.map(m => (
            <tr key={m.id} className="hover:bg-slate-50 transition-colors cursor-pointer">
              <td className="px-4 py-3 font-medium text-slate-900">{m.title}</td>
              <td className="px-4 py-3 text-slate-500">{m.date}</td>
              <td className="px-4 py-3 text-slate-500 tabular-nums">{m.duration}</td>
              <td className="px-4 py-3">
                <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-indigo-50 text-indigo-700 font-medium tabular-nums text-xs">{m.hints}</span>
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-2">
                  <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${m.score}%` }} />
                  </div>
                  <span className="text-slate-700 tabular-nums text-xs font-medium">{m.score}</span>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
