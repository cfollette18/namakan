import Link from 'next/link'

export function Nav() {
  return (
    <nav className="nav">
      <Link href="/" className="nav-logo">
        <span className="nav-logo-icon" aria-hidden="true" />
        <span className="nav-logo-wordmark" aria-hidden="true" />
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
