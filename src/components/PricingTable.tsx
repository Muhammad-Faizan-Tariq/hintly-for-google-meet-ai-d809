import Link from 'next/link'
import { Check } from 'lucide-react'

const plans = [
  {
    name: 'Free', price: '$0', period: 'forever',
    desc: 'For individuals trying Hintly for the first time.',
    cta: 'Install Free', href: '/install', primary: false,
    features: ['5 meetings / month', 'Real-time hints', 'Post-meeting summary', 'Chrome extension'],
  },
  {
    name: 'Pro', price: '$12', period: 'per month',
    desc: 'For professionals who live in back-to-back meetings.',
    cta: 'Start 14-day Trial', href: '/install', primary: true,
    features: ['Unlimited meetings', 'Tone coaching', 'Action item tracking', 'Follow-up email drafts', 'Meeting history dashboard', 'Priority support'],
  },
  {
    name: 'Team', price: '$9', period: 'per seat / mo',
    desc: 'For teams that need alignment and shared analytics.',
    cta: 'Contact Sales', href: 'mailto:sales@hintly.ai', primary: false,
    features: ['Everything in Pro', 'Shared team dashboard', 'Manager analytics', 'SSO / SAML', 'Custom onboarding', 'SLA support'],
  },
]

export default function PricingTable() {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-slate-900 text-center mb-4">Pricing</h2>
        <p className="text-slate-500 text-center mb-14 max-w-[44ch] mx-auto">Start free. Upgrade when your meetings demand it.</p>
        <div className="grid md:grid-cols-3 gap-5">
          {plans.map(plan => (
            <div key={plan.name} className={`rounded-2xl p-8 border ${plan.primary ? 'bg-indigo-600 border-indigo-500' : 'bg-white border-slate-200'}`}>
              <p className={`text-xs font-semibold uppercase tracking-widest mb-1 ${plan.primary ? 'text-indigo-200' : 'text-slate-400'}`}>{plan.name}</p>
              <div className="flex items-end gap-1 mb-2">
                <span className={`text-4xl font-bold ${plan.primary ? 'text-white' : 'text-slate-900'}`}>{plan.price}</span>
                <span className={`text-sm mb-1 ${plan.primary ? 'text-indigo-200' : 'text-slate-400'}`}>/{plan.period}</span>
              </div>
              <p className={`text-sm mb-7 ${plan.primary ? 'text-indigo-200' : 'text-slate-500'}`}>{plan.desc}</p>
              <ul className="space-y-3 mb-8">
                {plan.features.map(f => (
                  <li key={f} className={`flex items-center gap-2.5 text-sm ${plan.primary ? 'text-indigo-100' : 'text-slate-600'}`}>
                    <Check size={14} className={plan.primary ? 'text-indigo-300' : 'text-indigo-600'} strokeWidth={2.5} />
                    {f}
                  </li>
                ))}
              </ul>
              <Link href={plan.href} className={`block w-full text-center py-3 rounded-xl font-semibold text-sm transition-all active:scale-[0.98] ${plan.primary ? 'bg-white text-indigo-600 hover:bg-indigo-50' : 'bg-indigo-600 text-white hover:bg-indigo-700'}`}>
                {plan.cta}
              </Link>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
