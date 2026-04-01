import Link from 'next/link'
import Image from 'next/image'

export function Header() {
  return (
    <nav className="nav">
      <Link href="/" className="nav-logo">
        <Image 
          src="/logo.png" 
          alt="Namakan Logo" 
          width={28} 
          height={28}
          className="nav-logo-mark"
          style={{ borderRadius: '6px' }}
        />
        <span>NAMAKAN</span>
      </Link>
      <div className="nav-links">
        <Link href="/services">Services</Link>
        <Link href="/about">About</Link>
        <Link href="/pricing">Pricing</Link>
      </div>
      <Link href="/contact" className="nav-cta">Contact Us</Link>
    </nav>
  )
}

export function Footer() {
  return (
    <footer className="footer">
      <p>Namakan — Custom AI Engineering</p>
    </footer>
  )
}

export function Hero() {
  return (
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
        <Link href="/contact" className="cta">Contact Us</Link>
      </div>
    </section>
  )
}
