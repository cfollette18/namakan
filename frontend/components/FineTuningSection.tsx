'use client'

import { motion, useReducedMotion } from 'framer-motion'

export function FineTuningSection() {
  const prefersReducedMotion = useReducedMotion()

  return (
    <motion.section
      className="section section-finetuning"
      initial={prefersReducedMotion ? false : { opacity: 0, y: 32 }}
      whileInView={prefersReducedMotion ? {} : { opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.18 }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
    >
      <motion.div
        className="section-copy"
        initial={prefersReducedMotion ? false : { opacity: 0, y: 18 }}
        whileInView={prefersReducedMotion ? {} : { opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.25 }}
        transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1], delay: 0.06 }}
      >
        <span className="section-kicker">Fine-tuned models</span>
        <h2 className="section-title section-title-left">Teach the model how your business actually thinks.</h2>
        <p className="section-description">
          A fine-tuned model should not just "know documents." It should learn how your company classifies
          incidents, escalates risk, frames replies, and handles edge cases before retrieval or agents ever run.
        </p>
      </motion.div>

      <div className="hero-compare">
        <motion.article
          className="compare-card compare-card-generic"
          initial={prefersReducedMotion ? false : { opacity: 0, x: -24 }}
          whileInView={prefersReducedMotion ? {} : { opacity: 1, x: 0 }}
          viewport={{ once: true, amount: 0.22 }}
          transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1], delay: 0.08 }}
        >
          <div className="compare-card-header">
            <span className="compare-card-badge compare-card-badge-generic">Generic AI</span>
            <span className="compare-card-chip">Public model</span>
          </div>

          <div className="compare-thread">
            <div className="compare-bubble compare-bubble-user">
              Northforge Components has a field failure on forged valve assemblies used in washdown food-processing lines. The customer wants replacement parts shipped today, but the lot was produced on an older die set and the account is still inside the sanitation warranty window. Draft the response and tell ops what to do next.
            </div>
            <div className="compare-bubble compare-bubble-generic">
              Product issues like this usually require reviewing warranty terms, production history, and
              customer service policies before determining next steps.
            </div>
          </div>

          <div className="compare-list">
            <div className="compare-list-item compare-list-item-bad">No company-specific policy context</div>
            <div className="compare-list-item compare-list-item-bad">No citations or approved language</div>
            <div className="compare-list-item compare-list-item-bad">Unsafe for operational use</div>
          </div>

          <div className="compare-footer">Source: Unknown / internet priors</div>
        </motion.article>

        <motion.article
          className="compare-card compare-card-namakan"
          initial={prefersReducedMotion ? false : { opacity: 0, x: 24 }}
          whileInView={prefersReducedMotion ? {} : { opacity: 1, x: 0 }}
          viewport={{ once: true, amount: 0.22 }}
          transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1], delay: 0.14 }}
        >
          <div className="compare-card-header">
            <span className="compare-card-badge compare-card-badge-namakan">Namakan</span>
            <span className="compare-card-chip compare-card-chip-namakan">Fine-tuned model</span>
          </div>

          <div className="compare-thread">
            <div className="compare-bubble compare-bubble-user">
              Draft the customer reply and internal handoff for the Northforge washdown-line valve failure.
            </div>
            <div className="compare-bubble compare-bubble-namakan">
              Classify this as a sanitation-critical field issue. Pull the lot trace from the pre-May die set,
              open a same-day containment ticket, and release replacement assemblies only from the post-rework
              inventory tagged for washdown environments. In the customer reply, acknowledge the line-down risk,
              confirm expedited replacement under the sanitation warranty, and tell them quality is reviewing
              whether the older die-set lot needs broader recall action. Keep the tone direct, operational, and
              accountability-first, which is how Northforge handles plant-floor incidents.
            </div>
          </div>

          <div className="compare-list">
            <div className="compare-list-item compare-list-item-good">Learns Northforge's incident-handling logic</div>
            <div className="compare-list-item compare-list-item-good">Applies the company's plant-floor tone automatically</div>
            <div className="compare-list-item compare-list-item-good">Knows when to trigger QA and containment workflows</div>
          </div>

          <div className="compare-footer compare-footer-namakan">Fine-tuned on warranty playbooks, lot-trace procedures, QA escalations, and approved Northforge incident responses</div>
        </motion.article>
      </div>

      <div className="hero-foundation-grid">
        <motion.div
          className="hero-foundation-card hero-foundation-card-featured"
          initial={prefersReducedMotion ? false : { opacity: 0, y: 22 }}
          whileInView={prefersReducedMotion ? {} : { opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.25 }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1], delay: 0.1 }}
        >
          <span className="hero-signal-label">Why this comes first</span>
          <h2>Train the intelligence layer before you automate the workflow.</h2>
          <p>
            A fine-tuned model does more than search. It learns how your business classifies incidents,
            escalates risk, frames replies, and handles edge cases before retrieval or agents ever run.
          </p>
        </motion.div>

        <motion.div
          className="hero-foundation-card"
          initial={prefersReducedMotion ? false : { opacity: 0, y: 22 }}
          whileInView={prefersReducedMotion ? {} : { opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.25 }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1], delay: 0.16 }}
        >
          <span className="hero-signal-label">Training inputs</span>
          <p>Contracts, SOPs, ticket history, CRM notes, playbooks, taxonomies, and approved responses.</p>
        </motion.div>

        <motion.div
          className="hero-foundation-card"
          initial={prefersReducedMotion ? false : { opacity: 0, y: 22 }}
          whileInView={prefersReducedMotion ? {} : { opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.25 }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1], delay: 0.22 }}
        >
          <span className="hero-signal-label">Built after tuning</span>
          <p>RAG systems, workflow automation, and AI employees running on a model that actually knows the business.</p>
        </motion.div>
      </div>
    </motion.section>
  )
}
