import type { Metadata } from 'next'
import localFont from 'next/font/local'
import './globals.css'
import { ThemeProvider } from '@/components/ThemeProvider'

const satoshi = localFont({
  src: [
    {
      path: '../public/fonts/Satoshi-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../public/fonts/Satoshi-Medium.woff2',
      weight: '500',
      style: 'normal',
    },
    {
      path: '../public/fonts/Satoshi-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
    {
      path: '../public/fonts/Satoshi-Black.woff2',
      weight: '900',
      style: 'normal',
    },
  ],
  variable: '--font-satoshi',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Namakan AI Engineering — Custom AI Built on Your Data',
  description: 'Custom AI engineering for businesses with proprietary data — fine-tuned models, RAG pipelines, and agentic workflows.',
  openGraph: {
    title: 'Namakan AI Engineering',
    description: 'We build custom AI systems for businesses with proprietary data — fine-tuned models, RAG pipelines, and agentic workflows trained on YOUR data.',
    url: 'https://namakanai.com',
    siteName: 'Namakan AI Engineering',
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Namakan AI Engineering',
    description: 'Custom AI built on YOUR data — fine-tuned models, RAG pipelines, and agentic workflows.',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${satoshi.variable} font-satoshi antialiased`}>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
