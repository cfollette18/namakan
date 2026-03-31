import { Header, Footer, Hero, ProductCard } from '../components'
import Link from 'next/link'

export default function Home() {
  const products = [
    {
      tag: 'Fine-Tuned Models',
      title: 'AI trained on YOUR data',
      description: 'Generic AI doesn\'t know your business. We train AI models on your contracts, policies, and knowledge. It learns your voice. Your rules. Your domain.',
      features: ['Trained on your documents', 'Knows your brand voice', 'Cites your sources', '40-60% accuracy improvement'],
      price: 'Starting at $5K–$15K'
    },
    {
      tag: 'RAG Pipelines',
      title: 'AI that knows YOUR documents',
      description: 'Your AI searches your entire knowledge base before answering. Contracts, CRM, emails, databases — all indexed and accessible in seconds.',
      features: ['Searches 100s of documents instantly', 'Always cites the source', 'Real-time data, not training data', 'No hallucinations on your data'],
      price: 'Starting at $5K + $500/mo'
    },
    {
      tag: 'Agentic Workflows',
      title: 'AI that actually DOES the work',
      description: 'Multi-step tasks completed autonomously. Research leads, enrich data, draft emails, update CRM — all without human intervention.',
      features: ['Multi-step task automation', 'Integrates with your tools', '0 human approvals needed', 'Completes in seconds'],
      price: 'Starting at $5K per workflow'
    },
    {
      tag: 'Custom AI Employees',
      title: 'AI that NEVER sleeps',
      description: 'Runs around the clock on repeatable work. Researches leads, drafts emails, updates your CRM, and keeps follow-ups moving without constant human input.',
      features: ['Handles repetitive tasks', 'Integrates with your tools', 'Reports productivity metrics', '20+ hours saved per week'],
      price: 'Starting at $2K/mo per employee'
    }
  ]

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      <Hero />

      {/* Products Section */}
      <section className="section">
        <h2 className="section-title">Four ways we help companies stop losing to generic AI</h2>
        <div className="products-grid">
          {products.map((product, index) => (
            <ProductCard key={index} {...product} />
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-12 text-center border-t border-slate-200">
        <h2 className="text-3xl font-bold mb-6">Stop guessing. Start knowing.</h2>
        <Link href="/contact" className="cta">
          Contact Us
        </Link>
      </section>

      <Footer />
    </div>
  )
}
