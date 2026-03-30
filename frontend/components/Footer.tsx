import Link from 'next/link'

export function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div>
          <p className="footer-brand">Namakan</p>
          <p className="footer-copy">Private AI systems built around your language, logic, and operations.</p>
        </div>

        <div className="footer-links">
          <Link href="/services">Services</Link>
          <Link href="/about">About</Link>
          <Link href="/pricing">Pricing</Link>
          <Link href="/templates">Templates</Link>
          <Link href="/contact">Contact</Link>
        </div>
      </div>
    </footer>
  )
}
