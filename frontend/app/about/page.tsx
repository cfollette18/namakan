import Link from 'next/link'
import { Footer, Nav } from '../../components'
import { Reveal } from '../../components/Reveal'

export default function AboutPage() {
  const principles = [
    'Private by default, not public by default.',
    'Model behavior matters as much as model accuracy.',
    'AI should fit the business, not force the business to fit the AI.'
  ]

  const workingStyle = [
    {
      title: 'Close to operations',
      description: 'We spend time with the documents, decisions, exceptions, and real edge cases that shape day-to-day work.'
    },
    {
      title: 'Evaluation before polish',
      description: 'We test whether the system behaves correctly before we worry about slick demos or generic interfaces.'
    },
    {
      title: 'Systems over slogans',
      description: 'The goal is not to sound intelligent. The goal is to complete work with the right context and control.'
    }
  ]

  return (
    <main className="min-h-screen bg-white">
      <Nav />

      <section className="section">
        <div className="page-two-column">
          <Reveal className="info-card info-card-large">
            <span className="section-kicker">Why Namakan exists</span>
            <h2 className="page-section-title">Most AI fails inside companies for predictable reasons.</h2>
            <p className="page-paragraph">
              Public models are broad, generic, and detached from the actual rules that govern a business.
              They can sound plausible while missing policy nuance, brand tone, operational constraints, and
              exception handling.
            </p>
            <p className="page-paragraph">
              Namakan exists to close that gap. We build AI around private business context so the system can
              do work in a way that is grounded, controlled, and genuinely useful to the team.
            </p>
          </Reveal>

          <Reveal className="info-card" delay={0.08}>
            <span className="section-kicker">Principles</span>
            <div className="stack-list">
              {principles.map((item) => (
                <div key={item} className="stack-list-item">
                  <span className="stack-list-mark">✓</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </Reveal>
        </div>
      </section>

      <section className="section page-section-muted">
        <div className="info-grid info-grid-3">
          {workingStyle.map((item, index) => (
            <Reveal key={item.title} className="info-card" delay={index * 0.08}>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="cta-section">
        <Reveal>
          <h2>Want to see how Namakan would approach your business?</h2>
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