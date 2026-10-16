import type { Metadata } from 'next'
import { Plus_Jakarta_Sans } from 'next/font/google'
import './globals.css'

const jakarta = Plus_Jakarta_Sans({
  subsets: ['latin'],
  variable: '--font-jakarta',
  weight: ['400', '500', '600', '700', '800'],
})

export const metadata: Metadata = {
  title: 'Hintly — AI Meeting Assistant for Google Meet',
  description: 'Real-time AI hints, action items, and tone coaching during your Google Meet calls.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${jakarta.variable} font-sans bg-white text-slate-900 antialiased`}>
        {children}
      </body>
    </html>
  )
}
