import Link from 'next/link'
import { ContactModal } from './ContactModal'

export function Nav() {
  return (
    <nav className="nav">
      <Link href="/" className="nav-logo">
        <span className="nav-logo-icon" aria-hidden="true" />
        <span className="nav-logo-wordmark" aria-hidden="true" />
      </Link>
      <div className="nav-actions">
        <div className="nav-links">
          <Link href="/services">Services</Link>
          <Link href="/pricing">Pricing</Link>
          <Link href="/templates">Templates</Link>
          <Link href="/about">About</Link>
        </div>
        <ContactModal className="nav-cta" />
      </div>
    </nav>
  )
}
