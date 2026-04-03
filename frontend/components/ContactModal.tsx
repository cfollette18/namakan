'use client'

import * as Dialog from '@radix-ui/react-dialog'
import { useState } from 'react'

type ContactModalProps = {
  className?: string
  label?: string
}

export function ContactModal({ className, label = 'Contact Us' }: ContactModalProps) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    inquiryType: 'general',
    message: ''
  })

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
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button type="button" className={className}>
          {label}
        </button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay className="contact-modal-overlay" />
        <Dialog.Content className="contact-modal-content">
          <div className="contact-modal-header">
            <div>
              <Dialog.Title className="contact-modal-title">Contact Us</Dialog.Title>
              <Dialog.Description className="contact-modal-description">
                Tell us about the workflow, team, and business problem you want to solve.
              </Dialog.Description>
            </div>
            <Dialog.Close asChild>
              <button type="button" className="contact-modal-close" aria-label="Close contact modal">
                ×
              </button>
            </Dialog.Close>
          </div>

          <form onSubmit={handleSubmit} className="contact-form">
            <div className="form-grid">
              <div className="field-group">
                <label htmlFor="modal-name">Full name</label>
                <input
                  id="modal-name"
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
                <label htmlFor="modal-email">Email</label>
                <input
                  id="modal-email"
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
              <label htmlFor="modal-company">Company</label>
              <input
                id="modal-company"
                name="company"
                type="text"
                value={formData.company}
                onChange={handleChange}
                className="field-input"
                placeholder="Your company"
              />
            </div>

            <div className="field-group">
              <label htmlFor="modal-inquiryType">Inquiry type</label>
              <select
                id="modal-inquiryType"
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
              <label htmlFor="modal-message">What do you need?</label>
              <textarea
                id="modal-message"
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
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}
