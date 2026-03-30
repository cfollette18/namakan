'use client'

import { useState } from 'react'

const workflowSteps = [
  {
    label: 'Research',
    summary:
      'Gather context on the incoming request — identify the request type, relevant parties, and any prior history that affects how to handle it.',
    items: [
      'Request details collected and classified',
      'Relevant prior cases and context attached',
      'Initial summary prepared for next steps'
    ]
  },
  {
    label: 'Enrich',
    summary:
      'Pull additional data from connected systems — account records, policy documents, prior interactions, and any external context needed to act accurately.',
    items: [
      'Account and policy data retrieved',
      'Prior history matched and attached',
      'Context window assembled for action phase'
    ]
  },
  {
    label: 'Draft',
    summary:
      'Generate the response or action using client-specific language, approved templates, and the tone appropriate to the situation.',
    items: [
      'Response drafted from approved templates',
      'Tone and terminology aligned to client brand',
      'Fallback path prepared for edge cases'
    ]
  },
  {
    label: 'Approve',
    summary:
      'Validate the action against business rules, compliance requirements, and risk thresholds before release.',
    items: [
      'Business rules checked',
      'Escalation path confirmed for high-risk items',
      'Ready for release or human review'
    ]
  },
  {
    label: 'Update CRM',
    summary:
      'Write the outcome back to all connected systems so every team sees the same current state and no follow-up falls through.',
    items: [
      'Case status and disposition recorded',
      'Follow-up tasks and dates scheduled',
      'Timeline updated for all stakeholders'
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