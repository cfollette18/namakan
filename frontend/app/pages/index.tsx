import { Header, Footer } from '../../components/Header'

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
      <Header />

      {/* Hero Section */}
      <section className="hero">
        <h1 className="hero-headline">Your AI has no idea who your customers are.</h1>
        <p className="hero-subtext">We fix that.</p>

        <div className="comparison">
          {/* Generic AI */}
          <div className="card card-generic">
            <div className="card-label card-label-generic">Generic AI</div>
            <div className="chat">
              <div className="bubble bubble-user">What&apos;s our return policy for enterprise clients?</div>
              <div className="bubble bubble-ai-generic">Our standard enterprise return policy typically follows industry norms of 30-90 days. We aim to accommodate all customer needs on a case-by-case basis.</div>
            </div>
            <div className="status-list">
              <div className="status status-error">✗ No company data</div>
              <div className="status status-error">✗ Generic response</div>
              <div className="status status-error">✗ No citations</div>
            </div>
            <div className="source">Source: Unknown</div>
          </div>

          {/* Namakan */}
          <div className="card card-namakan">
            <div className="card-label card-label-namakan">Namakan</div>
            <div className="chat">
              <div className="bubble bubble-user">What&apos;s our return policy for enterprise clients?</div>
              <div className="bubble bubble-ai-namakan">Based on your Contract Template v2.3 Section 4.2: Enterprise clients receive a 2-week acceptance period, followed by 90-day warranty. After warranty, credits are issued at management discretion.</div>
            </div>
            <div className="status-list">
              <div className="status status-success">✓ From Contract v2.3</div>
              <div className="status status-success">✓ Exact policy cited</div>
              <div className="status status-success">✓ Your brand voice</div>
            </div>
            <div className="source source-namakan">Source: Your Knowledge Base</div>
          </div>
        </div>

        <div className="cta-wrapper">
          <button className="cta">Talk to Us →</button>
        </div>
      </section>

      {/* Products Section */}
      <section className="section">
        <h2 className="section-title">Four ways we help companies stop losing to generic AI</h2>
        <div className="products-grid">
          {products.map((product, index) => (
            <div key={index} className="product-card">
              <span className="product-tag">{product.tag}</span>
              <h3 className="product-title">{product.title}</h3>
              <p className="product-desc">{product.description}</p>
              <div className="product-features">
                {product.features.map((feature, i) => (
                  <div key={i} className="product-feature">
                    <span className="product-feature-check">✓</span>
                    <span>{feature}</span>
                  </div>
                ))}
              </div>
              <div className="product-price">{product.price}</div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <h2 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '24px' }}>Stop guessing. Start knowing.</h2>
        <button className="cta">Talk to Us →</button>
      </section>

      <Footer />
    </div>
  )
}
