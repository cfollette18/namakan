import Link from 'next/link'

import { Footer, Nav, ProductCard } from '../../components'
import { Reveal } from '../../components/Reveal'

export default function ServicesPage() {
  const services = [
    {
      tag: 'Fine-Tuned Models',
      title: 'Models trained on your operating logic',
      description:
        'We train models on your contracts, SOPs, historical decisions, approved language, and domain terms so the model behaves like your business.',
      features: [
        'Private training data preparation',
        'Evaluation and behavior testing',
        'Company-specific tone and escalation logic',
        'Deployment guidance for production use'
      ],
      price: '$5K–$15K per project'
    },
    {
      tag: 'RAG Systems',
      title: 'Private retrieval for grounded answers',
      description:
        'We build retrieval systems that search the right policies, documents, notes, and records before an answer is generated.',
      features: [
        'Source-aware retrieval pipelines',
        'Chunking and indexing for business knowledge',
        'Citation-ready answer experiences',
        'Document and system connectors'
      ],
      price: '$5K–$15K + $500/mo'
    },
    {
      tag: 'Agentic Workflows',
      title: 'Workflows that actually complete the task',
      description:
        'Research, enrich, draft, approve, and update systems in a controlled flow so work gets done instead of just described.',
      features: [
        'Multi-step task execution',
        'Tool and CRM integrations',
        'Approval and exception logic',
        'Operational guardrails and auditability'
      ],
      price: 'From $5K per workflow'
    },
    {
      tag: 'AI Employees',
      title: 'Persistent systems for repeatable operations',
      description:
        'For high-volume recurring work, we build AI employees that operate within your process, report activity, and hand off only what needs a human.',
      features: [
        'Role-specific automation design',
        'Task queues and reporting',
        'Human handoff rules',
        'Ongoing optimization and support'
      ],
      price: 'From $2K per month'
    }
  ]

  const process = [
    {
      title: 'Understand the business',
      description: 'We map the language, systems, decisions, and failure cases that make your operation unique.'
    },
    {
      title: 'Build the intelligence layer',
      description: 'We fine-tune, retrieve, and test against real scenarios before automating anything important.'
    },
    {
      title: 'Ship the operational system',
      description: 'We connect the model to the workflow, tools, and review process your team actually uses.'
    }
  ]

  return (
    <main className="min-h-screen bg-white">
      <Nav />

      <section className="section">
        <Reveal>
          <div className="section-copy">
            <span className="section-kicker">What we build</span>
            <h2 className="section-title section-title-left">Each layer is useful on its own. Together, they become a system.</h2>
            <p className="section-description">
              Fine-tuning gives the model business-specific behavior. Retrieval grounds answers in private
              data. Workflows execute the process. AI employees keep recurring operations moving.
            </p>
          </div>
        </Reveal>

        <Reveal className="products-grid" delay={0.08}>
          {services.map((service) => (
            <ProductCard key={service.title} {...service} />
          ))}
        </Reveal>
      </section>

      <section className="section page-section-muted">
        <div className="info-grid info-grid-3">
          {process.map((item, index) => (
            <Reveal key={item.title} className="info-card" delay={index * 0.08}>
              <span className="info-card-index">0{index + 1}</span>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="cta-section">
        <Reveal>
          <h2>Need a system tailored to your operation?</h2>
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
