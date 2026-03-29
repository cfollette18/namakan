import Link from 'next/link'
import Image from 'next/image'

export function Nav() {
  return (
    <nav className="nav">
      <Link href="/" className="nav-logo">
        <Image 
          src="/logo.png" 
          alt="Namakan" 
          width={28} 
          height={28}
          className="nav-logo-mark"
        />
        <span>AMAKAN</span>
      </Link>
      <div className="nav-links">
        <Link href="/">Services</Link>
        <Link href="/">About</Link>
        <Link href="/">Pricing</Link>
      </div>
      <Link href="/" className="nav-cta">Talk to Us</Link>
    </nav>
  )
}
