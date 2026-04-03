'use client'

import Link from 'next/link'
import { useState } from 'react'

import { Footer, Nav } from '../../components'
import { Reveal } from '../../components/Reveal'

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    inquiryType: 'general',
    message: ''
  })

  const contactMethods = [
    {
      title: 'General inquiries',
      description: 'Questions about Namakan, partnerships, or where to start.',
      contact: 'hello@namakanai.com'
    },
    {
      title: 'Project scoping',
      description: 'For teams exploring a fine-tuned model, RAG system, or workflow automation.',
      contact: 'Share the workflow, team, and source systems involved'
    },
    {
      title: 'Pricing conversations',
      description: 'Need a quote for one workflow or a broader rollout?',
      contact: 'We scope around complexity, data quality, and integration needs'
    },
    {
      title: 'Response window',
      description: 'You should hear back quickly with next steps or follow-up questions.',
      contact: 'Typical response within 1 business day'
    }
  ]

  function handleChange(
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) {
    const { name, value } = event.target
    setFormData((current) => ({ ...current, [name]: value }))
  }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const subject = encodeURIComponent(
      `${formData.inquiryType} inquiry - ${formData.company || formData.name}`
    )
    const body = encodeURIComponent(
      [
        `Name: ${formData.name}`,
        `Email: ${formData.email}`,
        `Company: ${formData.company || 'N/A'}`,
        `Inquiry Type: ${formData.inquiryType}`,
        '',
        formData.message
      ].join('\n')
    )

    window.location.href = `mailto:hello@namakanai.com?subject=${subject}&body=${body}`
  }

  return (
    <main className="min-h-screen bg-white">
      <Nav />

      <section className="page-hero">
        <Reveal className="page-hero-copy">
          <span className="section-kicker">Contact</span>
          <h1 className="page-title">Tell us what you want the system to do.</h1>
          <p className="page-description">
            If you already know the workflow, great. If not, describe the team, the process, the tools, and
            the operational friction. We can help decide whether the right answer is fine-tuning, retrieval,
            workflows, or a larger rollout.
          </p>
          <div className="page-actions">
            <a href="mailto:hello@namakanai.com" className="cta">
              Email hello@namakanai.com
            </a>
            <Link href="/services" className="cta cta-secondary">
              View Services
            </Link>
          </div>
        </Reveal>
      </section>

      <section className="section">
        <div className="info-grid info-grid-2">
          {contactMethods.map((method, index) => (
            <Reveal key={method.title} className="info-card" delay={index * 0.08}>
              <h3>{method.title}</h3>
              <p>{method.description}</p>
              <div className="contact-detail">{method.contact}</div>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="section page-section-muted">
        <div className="contact-layout">
          <Reveal className="contact-form-card">
            <span className="section-kicker">Message us</span>
            <h2 className="page-section-title">Contact form</h2>
            <p className="page-paragraph">
              Submitting this opens your email client with the details pre-filled so you can send the message
              directly.
            </p>

            <form onSubmit={handleSubmit} className="contact-form">
              <div className="form-grid">
                <div className="field-group">
                  <label htmlFor="name">Full name</label>
                  <input
                    id="name"
                    name="name"
                    type="text"
                    required
                    value={formData.name}
                    onChange={handleChange}
                    className="field-input"
                    placeholder="Jane Smith"
                  />
                </div>

                <div className="field-group">
                  <label htmlFor="email">Email</label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    className="field-input"
                    placeholder="jane@company.com"
                  />
                </div>
              </div>

              <div className="field-group">
                <label htmlFor="company">Company</label>
                <input
                  id="company"
                  name="company"
                  type="text"
                  value={formData.company}
                  onChange={handleChange}
                  className="field-input"
                  placeholder="Your company"
                />
              </div>

              <div className="field-group">
                <label htmlFor="inquiryType">Inquiry type</label>
                <select
                  id="inquiryType"
                  name="inquiryType"
                  value={formData.inquiryType}
                  onChange={handleChange}
                  className="field-input"
                >
                  <option value="general">General</option>
                  <option value="pricing">Pricing</option>
                  <option value="fine-tuning">Fine-tuning</option>
                  <option value="rag">RAG</option>
                  <option value="workflow">Workflow automation</option>
                </select>
              </div>

              <div className="field-group">
                <label htmlFor="message">What do you need?</label>
                <textarea
                  id="message"
                  name="message"
                  required
                  rows={6}
                  value={formData.message}
                  onChange={handleChange}
                  className="field-input field-textarea"
                  placeholder="Describe the workflow, team, data, tools, and business problem."
                />
              </div>

              <button type="submit" className="cta">
                Contact Us
              </button>
            </form>
          </Reveal>

          <Reveal className="info-card info-card-large" delay={0.08}>
            <span className="section-kicker">What to include</span>
            <h2 className="page-section-title">The more operational detail you share, the better we can help.</h2>
            <div className="stack-list">
              <div className="stack-list-item">
                <span className="stack-list-mark">1</span>
                <span>Which team owns the process and what work is being done today?</span>
              </div>
              <div className="stack-list-item">
                <span className="stack-list-mark">2</span>
                <span>What sources of truth matter: docs, CRM, tickets, databases, or policies?</span>
              </div>
              <div className="stack-list-item">
                <span className="stack-list-mark">3</span>
                <span>Where is the biggest bottleneck: quality, speed, repetition, or inconsistency?</span>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      <Footer />
    </main>
  )
}
