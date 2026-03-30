import Link from 'next/link'
import { Footer, Nav, ProductCard } from '../../components'
import { Reveal } from '../../components/Reveal'

export default function PricingPage() {
  const plans = [
    {
      tag: 'Sprint',
      title: 'Discovery and AI fit assessment',
      description:
        'For teams that need to identify the right use case, model strategy, and technical path before building.',
      features: [
        'Use-case selection and workflow mapping',
        'Data and document audit',
        'Architecture recommendation',
        'Delivery roadmap and scope'
      ],
      price: 'Starting at $3K'
    },
    {
      tag: 'Build',
      title: 'A production AI system for one workflow',
      description:
        'For companies ready to ship a focused model, retrieval, or workflow system that solves a real operational problem.',
      features: [
        'Fine-tuning or RAG implementation',
        'Workflow and tool integration',
        'Testing and iteration',
        'Launch support'
      ],
      price: 'Starting at $5K-$15K'
    },
    {
      tag: 'Retainer',
      title: 'Ongoing AI capability inside the business',
      description:
        'For operators that want continuous improvement, new workflows, and an AI partner embedded over time.',
      features: [
        'Monthly optimization and experiments',
        'New workflow and employee rollouts',
        'Performance reviews and reporting',
        'Priority support'
      ],
      price: 'Starting at $2K/mo'
    },
    {
      tag: 'Enterprise',
      title: 'Multi-team systems and deeper rollout',
      description:
        'For larger organizations that need multiple processes, tighter governance, and a broader deployment plan.',
      features: [
        'Cross-team AI system design',
        'Security and deployment planning',
        'Advanced integrations',
        'Custom commercial terms'
      ],
      price: 'Custom'
    }
  ]

  const notes = [
    'Every project is scoped around business complexity, data quality, and integration surface area.',
    'We can start with a single workflow and expand after proving value.',
    'If your use case is unusual, we will usually recommend a paid discovery sprint first.'
  ]

  return (
    <main className="min-h-screen bg-white">
      <Nav />

      <section className="section">
        <Reveal className="products-grid">
          {plans.map((plan) => (
            <ProductCard key={plan.title} {...plan} />
          ))}
        </Reveal>
      </section>

      <section className="section page-section-muted">
        <Reveal>
          <div className="section-copy">
            <span className="section-kicker">How pricing works</span>
            <h2 className="section-title section-title-left">We price for the system you need, not a fake template.</h2>
            <p className="section-description">
              The right scope depends on the number of workflows, the model approach, the quality of source
              data, and how deeply the system needs to plug into your existing tools.
            </p>
          </div>
        </Reveal>

        <div className="info-grid">
          {notes.map((note, index) => (
            <Reveal key={note} className="info-card" delay={index * 0.08}>
              <p>{note}</p>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="cta-section">
        <Reveal>
          <h2>Need a quote for your exact use case?</h2>
        </Reveal>
        <Reveal delay={0.08}>
          <Link href="/contact" className="cta">
            Contact Us
          </Link>
        </Reveal>
      </section>

      <Footer />
    </main>
  )
}