'use client'

import Link from 'next/link'
import { motion, useReducedMotion } from 'framer-motion'

export function Hero() {
  const prefersReducedMotion = useReducedMotion()

  return (
    <section className="hero hero-top">
      <motion.div
        className="hero-copy"
        initial={prefersReducedMotion ? false : { opacity: 0, y: 28 }}
        animate={prefersReducedMotion ? {} : { opacity: 1, y: 0 }}
        transition={{ duration: 0.65, ease: [0.22, 1, 0.36, 1] }}
      >
        <div className="hero-eyebrow">Private AI systems</div>
        <h1 className="hero-headline">Generic AI was trained on everyone. Yours should be built for you.</h1>
        <p className="hero-subtext">
          Namakan engineers private AI systems around your contracts, policies, historical decisions,
          terminology, and approved language, then turns that intelligence into retrieval, workflows, and
          agents that can do real work inside your business.
        </p>

        <div className="hero-proof-row">
          <div className="hero-proof-pill">Private data and policies</div>
          <div className="hero-proof-pill">Fine-tuned reasoning layer</div>
          <div className="hero-proof-pill">Retrieval, workflows, and agents</div>
        </div>

        <div className="cta-wrapper">
          <Link href="/contact" className="cta">
            Contact Us
          </Link>
        </div>
      </motion.div>
    </section>
  )
}
