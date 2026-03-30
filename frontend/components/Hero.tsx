'use client'

import { motion, useReducedMotion } from 'framer-motion'
import { ContactModal } from './ContactModal'

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
        <h1 className="hero-headline">Your business isn&apos;t &quot;standard.&quot; Why is your AI?</h1>
        <p className="hero-subtext">
          Public models are trained on the average of the internet. But your advantage lives in your specifics:
          your proprietary language, your approval workflows, your operating logic, and your hard-won decisions.
          Namakan turns that internal context into a private AI operating system with fine-tuned models, RAG
          pipelines grounded in your data, autonomous workflows, and AI employees that work within your safety
          rails and speak your language.
        </p>

        <div className="cta-wrapper">
          <ContactModal className="cta" />
        </div>
      </motion.div>
    </section>
  )
}
