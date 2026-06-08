# Module 04: SDLC Security

Shift-left security integration — PR review automation, dependency scanning, sprint regression tracking, and CI/CD security gates.

## Labs

| Lab | Focus | Difficulty | Status |
|-----|-------|-----------|--------|
| [lab-01](labs/lab-01-pr-review-automation/) | AI-assisted PR security reviewer | Senior+ | Planned |
| [lab-02](labs/lab-02-dependency-analysis/) | Deep dependency analysis (beyond surface CVEs) | Senior | Planned |
| [lab-03](labs/lab-03-sprint-regression-tracker/) | Sprint regression tracker with Jira integration | Principal | Planned |
| [lab-04](labs/lab-04-security-gates/) | CI/CD security gate engine (policy-based) | Principal | Planned |

## Writeups

- Understanding platform PRs from a security perspective
- Shift-left without slowing down developers
- Regression patterns in enterprise software releases

## Tools

- [pr-security-linter](tools/pr-security-linter/) — GitHub Action for PR security linting

## Key Concepts

- **Security champions**: Embedding security knowledge in dev teams
- **Gate vs advisory**: When to block vs when to warn
- **Regression tracking**: Identifying reintroduced vulnerabilities across sprints
- **Dependency depth**: Transitive vulnerabilities that scanners miss
- **Sprint cadence integration**: Timing security activities around release cycles

## Prerequisites

- Git and GitHub workflows
- CI/CD concepts (GitHub Actions)
- Understanding of dependency management (pip, npm, Maven)
- Python 3.11+
