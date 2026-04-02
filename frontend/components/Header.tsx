export function Header() {
  return (
    <nav className="header">
      <div className="header-logo">
        <img src="/logo.png" alt="Namakan" width={28} height={28} style={{ borderRadius: '6px' }} />
        <span>AMAKAN</span>
      </div>
      <div className="header-links">
        <a href="/">Services</a>
        <a href="/">About</a>
        <a href="/">Pricing</a>
        <a href="mailto:clint@namakanai.com">Contact</a>
      </div>
      <a href="mailto:clint@namakanai.com" className="header-cta">Talk to Us</a>
    </nav>
  )
}

export function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-brand">
          <img src="/logo.png" alt="Namakan" width={24} height={24} style={{ borderRadius: '4px' }} />
          <span>AMAKAN</span>
          <p>Custom AI Engineering</p>
        </div>
        <div className="footer-links">
          <div className="footer-col">
            <h4>Services</h4>
            <a href="/">Fine-Tuned Models</a>
            <a href="/">RAG Pipelines</a>
            <a href="/">Agentic Workflows</a>
            <a href="/">Custom AI Employees</a>
          </div>
          <div className="footer-col">
            <h4>Company</h4>
            <a href="/">About</a>
            <a href="mailto:clint@namakanai.com">Contact</a>
          </div>
          <div className="footer-col">
            <h4>Contact</h4>
            <a href="mailto:clint@namakanai.com">clint@namakanai.com</a>
            <a href="tel:+16128672860">612-867-2860</a>
            <span>Minneapolis, MN</span>
          </div>
        </div>
      </div>
      <div className="footer-bottom">
        <p>© 2026 Namakan. All rights reserved.</p>
      </div>
    </footer>
  )
}
