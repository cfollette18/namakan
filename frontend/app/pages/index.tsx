import { Nav, Footer, Hero, ProductCard } from '../../components/Nav'

export default function Home() {
  const products = [
    {
      tag: 'Fine-Tuned Models',
      title: 'AI trained on YOUR data',
      description: "Generic AI doesn't know your business. We train AI models on your contracts, policies, and knowledge. It learns your voice. Your rules. Your domain.",
      features: ['Trained on your documents', 'Knows your brand voice', 'Cites your sources', '40-60% accuracy improvement'],
      price: 'Starting at $10K per project'
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
      title: 'A full-time worker that never sleeps',
      description: "AI that actually does the work. Researches leads, drafts emails, updates your CRM, schedules follow-ups. It's an employee that works 24/7.",
      features: ['Handles repetitive tasks', 'Integrates with your tools', 'Reports productivity metrics', '20+ hours saved per week'],
      price: 'Starting at $2K/mo per employee'
    }
  ]

  return (
    <div className="min-h-screen bg-white">
      <Nav />
      <Hero />

      {/* Products Section */}
      <section className="py-20 px-12 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12 text-slate-900">
          Four ways we help companies stop losing to generic AI
        </h2>
        <div className="grid grid-cols-2 gap-8">
          {products.map((product, index) => (
            <ProductCard key={index} {...product} />
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-12 text-center border-t border-slate-200">
        <h2 className="text-3xl font-bold mb-6 text-slate-900">Stop guessing. Start knowing.</h2>
        <button className="bg-teal-600 text-white text-base font-semibold px-8 py-4 rounded-lg hover:bg-teal-700 hover:-translate-y-0.5 transition-all cursor-pointer">
          Talk to Us →
        </button>
      </section>

      <Footer />
    </div>
  )
}
