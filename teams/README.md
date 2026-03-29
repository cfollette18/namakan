# Namakan Teams

Multi-agent team structure for autonomous operations.

## Overview

Teams of AI agents that work together to handle different domains.

## Teams

| Team | Focus |
|------|-------|
| `autonomous-agents/` | Background agents, schedulers, web scraping, data sync |
| `business/` | Business development, strategy, finance |
| `coding/` | Software engineering, devops |
| `customer-service/` | Support agents, FAQ, returns |
| `document-processing/` | OCR, parsing, document workflows |
| `hr/` | Recruiting, onboarding, employee management |
| `internal-llm/` | Internal AI tooling |
| `lead-qualification/` | Sales lead scoring and routing |
| `legal/` | Contract review, compliance |
| `meeting-agents/` | Calendar, scheduling, meeting prep |
| `product-pipeline/` | Product development |
| `research/` | Market research, competitive analysis |
| `social-media/` | Content creation, posting |

## Key Files

- `TEAMS.md` — Full team roster and structure

## Architecture

Teams follow Namakan's agentic workflow patterns:
- Supervisor agents delegate to specialist agents
- Each team has a team lead
- Cross-team coordination via shared state
