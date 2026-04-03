import { Nav, Footer, Hero, ProductCard } from '../../components'
import { ContactModal } from '../../components/ContactModal'
import { FineTuningSection } from '../../components/FineTuningSection'
import { Reveal } from '../../components/Reveal'
import { WorkflowGraphic } from '../../components/WorkflowGraphic'

export default function Home() {
  const products = [
    {
      tag: 'Data → AI',
      title: 'Your CRM. Your database. Your AI.',
      description: "We connect to your existing data sources, clean it, and train a model that actually knows your business — not generic AI.",
      features: ['Pulls from your CRM, database, docs', 'Cleans and structures your data', 'Trains a 8B model on YOUR data', 'Model runs on your infrastructure'],
      price: 'Starting at $5K'
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
      description: 'A full-time worker dedicated to your business. Researches leads, drafts emails, updates your CRM, and keeps follow-ups moving — 24/7.',
      features: ['Handles repetitive tasks', 'Integrates with your tools', 'Reports productivity metrics', '20+ hours saved per week'],
      price: 'Starting at $2K/mo per employee'
    }
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

      <section className="section section-automation">
        <Reveal className="section-copy automation-copy">
          <span className="section-kicker">Agentic execution</span>
          <h2 className="section-title section-title-left">Now let your AI DO the work.</h2>
          <p className="section-description">
            Once your fine-tuned model knows your business, we build workflows and employees
            that act on that knowledge — autonomously, 24/7.
          </p>
        </Reveal>

        <div className="automation-grid">
          <Reveal className="graphic-card graphic-card-automation" delay={0.08}>
            <div className="graphic-copy">
              <span className="graphic-eyebrow">Agentic workflow</span>
              <h3 className="graphic-title">A workflow that can do the task, not just describe it</h3>
              <p className="graphic-description">
                Built around a manufacturing incident: triage the failure, validate the
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
                Processing field failures, preparing replacement comms, and handing
                only the highest-risk issues to the team.
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
          <h2 className="section-title">Three systems we build</h2>
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
          <h2>Give us your messy data. We'll build the AI.</h2>
        </Reveal>
        <Reveal delay={0.08}>
          <ContactModal className="cta" />
        </Reveal>
      </section>

      <Footer />
    </div>
  )
}
