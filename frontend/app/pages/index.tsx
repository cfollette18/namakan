import { Nav, Footer, Hero, ProductCard } from '../../components'
import { ContactModal } from '../../components/ContactModal'
import { FineTuningSection } from '../../components/FineTuningSection'
import { Reveal } from '../../components/Reveal'
import { WorkflowGraphic } from '../../components/WorkflowGraphic'

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
      title: 'AI that NEVER sleeps',
      description: 'Runs around the clock on repeatable work. Researches leads, drafts emails, updates your CRM, and keeps follow-ups moving without constant human input.',
      features: ['Handles repetitive tasks', 'Integrates with your tools', 'Reports productivity metrics', '20+ hours saved per week'],
      price: 'Starting at $2K/mo per employee'
    }
  ]
  const ragSources = [
    'washdown_warranty_policy_v3.pdf',
    'forged_valve_lot_trace_may.csv',
    'qa_containment_playbook.docx',
    'field_failures_q2_2026.xlsx'
  ]

  const employeeTimeline = [
    '08:42 AM — Reviewed three new field failure tickets from distributor accounts',
    '08:47 AM — Matched two incidents to the pre-May die-set lot trace',
    '08:51 AM — Drafted plant-floor replacement updates for customer service',
    '08:56 AM — Escalated one washdown-line case to QA and operations'
  ]

  return (
    <div className="min-h-screen bg-white">
      <Nav />
      <Hero />
      <FineTuningSection />

      <section className="section section-rag">
        <Reveal className="graphic-card graphic-card-wide">
          <div className="graphic-copy">
            <span className="graphic-eyebrow">RAG pipeline</span>
            <h3 className="graphic-title">Private retrieval before the answer is written</h3>
            <p className="graphic-description">
              For [Client], retrieval means searching warranty rules, lot traces, and QA procedures
              before anyone answers a field-failure question.
            </p>
          </div>

          <div className="rag-graphic">
            <div className="rag-docs">
              {ragSources.map((source) => (
                <div key={source} className="rag-doc">
                  <span className="rag-doc-check">✓</span>
                  <span>{source}</span>
                </div>
              ))}
            </div>

            <div className="rag-answer">
              <div className="rag-answer-badge">Retrieved from 847 documents</div>
              <div className="rag-answer-question">Which lots are eligible for same-day replacement under the washdown warranty?</div>
              <div className="rag-answer-body">
                Based on the warranty policy, lot-trace file, and field-failure history: only the post-rework
                lots tagged for washdown environments qualify for immediate replacement, while pre-May die-set
                inventory requires QA hold and containment review before release.
              </div>
              <div className="rag-answer-meta">
                <span>Vector match: 0.94</span>
                <span>Chunks retrieved: 12</span>
                <span>Sources verified: 3</span>
              </div>
            </div>
          </div>
        </Reveal>
      </section>

      <section className="section section-automation">
        <Reveal className="section-copy automation-copy">
          <span className="section-kicker">Agentic execution</span>
          <h2 className="section-title section-title-left">Workflows and AI employees belong in their own operating layer.</h2>
          <p className="section-description">
            Once the model and retrieval stack are right, Namakan can turn that intelligence into systems that
            execute tasks, move work across tools, and keep humans focused on the highest-risk decisions.
          </p>
        </Reveal>

        <div className="automation-grid">
          <Reveal className="graphic-card graphic-card-automation" delay={0.08}>
            <div className="graphic-copy">
              <span className="graphic-eyebrow">Agentic workflow</span>
              <h3 className="graphic-title">A workflow that can do the task, not just describe it</h3>
              <p className="graphic-description">
                Here the workflow is built around a manufacturing incident: triage the failure, validate the
                lot, draft the response, and move ops forward without losing control of risk.
              </p>
            </div>

            <WorkflowGraphic />
          </Reveal>

          <Reveal className="graphic-card graphic-card-automation" delay={0.14}>
            <div className="graphic-copy">
              <span className="graphic-eyebrow">AI employee</span>
              <h3 className="graphic-title">A task-running system with throughput and accountability</h3>
              <p className="graphic-description">
                The AI employee example is also manufacturing-specific: processing field failures, preparing
                replacement comms, and handing only the highest-risk issues to the team.
              </p>
            </div>

            <div className="employee-graphic">
              <div className="employee-topline">
                <div>
                  <span className="employee-name">[Client] Service Ops AI</span>
                  <span className="employee-status">Active</span>
                </div>
                <div className="employee-metrics">
                  <span>17 incident tasks today</span>
                  <span>5.8 hours saved</span>
                </div>
              </div>

              <div className="employee-timeline">
                {employeeTimeline.map((entry) => (
                  <div key={entry} className="employee-timeline-item">
                    <span className="employee-timeline-dot" />
                    <span>{entry}</span>
                  </div>
                ))}
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* Products Section */}
      <section className="section">
        <Reveal>
          <h2 className="section-title">Four systems we build after the model foundation is right</h2>
        </Reveal>
        <Reveal className="products-grid" delay={0.08}>
          {products.map((product, index) => (
            <ProductCard key={index} {...product} />
          ))}
        </Reveal>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <Reveal>
          <h2>Stop guessing. Start knowing.</h2>
        </Reveal>
        <Reveal delay={0.08}>
          <ContactModal className="cta" />
        </Reveal>
      </section>

      <Footer />
    </div>
  )
}
