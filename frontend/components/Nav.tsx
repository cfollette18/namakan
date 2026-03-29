import Link from 'next/link'
import Image from 'next/image'

export function Nav() {
  return (
    <nav className="fixed top-0 left-0 right-0 h-16 flex items-center justify-between px-12 bg-white border-b border-slate-200 z-50">
      <Link href="/" className="flex items-center gap-2 text-slate-900 font-bold text-xl no-underline">
        <Image 
          src="/logo.png" 
          alt="Namakan" 
          width={28} 
          height={28}
          className="rounded"
        />
        <span>AMAKAN</span>
      </Link>
      <div className="flex gap-8">
        <Link href="/" className="text-slate-600 no-underline text-sm font-medium hover:text-slate-900">Services</Link>
        <Link href="/" className="text-slate-600 no-underline text-sm font-medium hover:text-slate-900">About</Link>
        <Link href="/" className="text-slate-600 no-underline text-sm font-medium hover:text-slate-900">Pricing</Link>
      </div>
      <Link href="/" className="bg-teal-600 text-white px-5 py-2.5 rounded-lg text-sm font-semibold no-underline hover:bg-teal-700">
        Talk to Us
      </Link>
    </nav>
  )
}
