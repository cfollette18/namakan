'use client'

import { useState } from 'react'

const workflowSteps = [
  {
    label: 'Research',
    summary:
      'Review the Northforge field-failure report, identify the affected forged valve assembly, and confirm whether the failure came from a washdown-line deployment.',
    items: [
      'Customer incident details collected from service intake',
      'Affected assembly and plant environment verified',
      'Initial failure context prepared for lot-trace review'
    ]
  },
  {
    label: 'Enrich',
    summary:
      'Pull lot history, warranty eligibility, prior service notes, and QA flags so the workflow uses actual Northforge operating context.',
    items: [
      'Lot trace matched against the pre-May die set',
      'Warranty window and distributor account history attached',
      'QA notes added to the incident brief'
    ]
  },
  {
    label: 'Draft',
    summary:
      'Generate the customer-facing reply using Northforge’s approved industrial tone, warranty language, and line-down escalation framing.',
    items: [
      'Replacement language selected from approved templates',
      'Line-down risk acknowledged in the response',
      'Fallback copy prepared if QA hold remains in place'
    ]
  },
  {
    label: 'Approve',
    summary:
      'Validate the action against margin rules, QA containment policy, and sanitation-warranty handling before release.',
    items: [
      'Containment requirements checked against SOP',
      'Escalation path confirmed for any recall risk',
      'Ready for service and operations review'
    ]
  },
  {
    label: 'Update CRM',
    summary:
      'Write the incident outcome back to systems so service, QA, and operations all see the same next action.',
    items: [
      'Case status logged with replacement disposition',
      'QA ticket and service follow-up date recorded',
      'Customer timeline updated for the account team'
    ]
  }
] as const

export function WorkflowGraphic() {
  const [activeStep, setActiveStep] = useState(0)
  const step = workflowSteps[activeStep]

  return (
    <div className="workflow-graphic">
      <div className="workflow-step-row" role="tablist" aria-label="Agentic workflow steps">
        {workflowSteps.map((item, index) => (
          <button
            key={item.label}
            type="button"
            role="tab"
            aria-selected={index === activeStep}
            className={`workflow-node ${index === activeStep ? 'workflow-node-active' : ''}`}
            onClick={() => setActiveStep(index)}
          >
            {item.label}
          </button>
        ))}
      </div>

      <div className="workflow-run-card">
        <div className="workflow-run-label">Current step</div>
        <strong>{step.label}</strong>
        <p className="workflow-run-summary">{step.summary}</p>
      </div>

      <div className="workflow-run-list">
        {step.items.map((item) => (
          <div key={item} className="workflow-run-item">
            {item}
          </div>
        ))}
      </div>
    </div>
  )
}
