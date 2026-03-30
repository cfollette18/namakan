/* eslint-disable react/no-unescaped-entities */
'use client'

import { motion, useReducedMotion } from 'framer-motion'

export function FineTuningSection() {
  const prefersReducedMotion = useReducedMotion()

  const genericBullets = [
    'Generic answer based on public priors',
    'No internal customer or contract context',
    'Not safe to send without manual review'
  ]

  const namakanBullets = [
    'Uses approved enterprise return policy',
    'Understands contract-specific exception windows',
    'Ready for retrieval and workflow handoff'
  ]

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

      <motion.div
        className="finetuning-stage-card"
        initial={prefersReducedMotion ? false : { opacity: 0, y: 24 }}
        whileInView={prefersReducedMotion ? {} : { opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.2 }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1], delay: 0.08 }}
      >
        <div className="finetuning-stage-visual">
          <div className="finetuning-stage-split">
            <div className="finetuning-panel finetuning-panel-generic">
              <div className="finetuning-panel-head">
                <span className="finetuning-panel-label">Generic model</span>
                <span className="finetuning-panel-chip">No private context</span>
              </div>

              <div className="finetuning-shell">
                <div className="finetuning-thread">
                  <div className="finetuning-message-row finetuning-message-row-user">
                    <div className="finetuning-message finetuning-message-user">
                      What&apos;s our return policy for enterprise clients?
                    </div>
                  </div>

                  <div className="finetuning-message-row">
                    <div className="finetuning-message finetuning-message-generic">
                      Enterprise return policies usually vary by provider and can differ depending on the
                      contract, customer tier, and support agreement.
                    </div>
                  </div>
                </div>

                <div className="finetuning-composer">
                  <button type="button" className="finetuning-composer-add" aria-label="Add context">
                    +
                  </button>
                  <div className="finetuning-composer-input">Message the model...</div>
                </div>
              </div>

              <div className="finetuning-status-list">
                {genericBullets.map((item) => (
                  <div key={item} className="finetuning-status finetuning-status-bad">
                    <span className="finetuning-status-icon" aria-hidden="true">
                      x
                    </span>
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="finetuning-panel finetuning-panel-namakan">
              <div className="finetuning-panel-head">
                <span className="finetuning-panel-label finetuning-panel-label-namakan">Trained model</span>
                <span className="finetuning-panel-chip finetuning-panel-chip-namakan">Policy-aware</span>
              </div>

              <div className="finetuning-shell finetuning-shell-namakan">
                <div className="finetuning-thread">
                  <div className="finetuning-message-row finetuning-message-row-user">
                    <div className="finetuning-message finetuning-message-user">
                      What&apos;s our return policy for enterprise clients?
                    </div>
                  </div>

                  <div className="finetuning-message-row">
                    <div className="finetuning-message finetuning-message-namakan">
                      Based on Contract Template v2.3 and the enterprise returns clause library: Northforge
                      enterprise accounts receive a 14-day acceptance period followed by a 90-day warranty
                      window. Replacement or credit terms after that require account-level approval and must use
                      the approved exception language.
                    </div>
                  </div>
                </div>

                <div className="finetuning-composer">
                  <button type="button" className="finetuning-composer-add" aria-label="Add context">
                    +
                  </button>
                  <div className="finetuning-composer-input">Message the model...</div>
                </div>
              </div>

              <div className="finetuning-status-list">
                {namakanBullets.map((item) => (
                  <div key={item} className="finetuning-status finetuning-status-good">
                    <span className="finetuning-status-icon" aria-hidden="true">
                      ✓
                    </span>
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </motion.div>

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
