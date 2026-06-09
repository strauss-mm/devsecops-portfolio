# Existing Production Systems

These are production systems referenced throughout this portfolio. They demonstrate real-world application of the concepts taught in each module.

## CVE Intake MCP Server

**Stack**: Python, AWS (Lambda, Fargate, DynamoDB, S3, Cognito), Terraform, Slack, Jira, Wiz

Serverless vulnerability intake pipeline processing 500+ CVEs/month for enterprise customers. Features automated classification (OS vs application-level responsibility), Wiz enrichment, SLA calculation, and Jira ticket creation.

**Demonstrates**: Module 01 (vuln management at scale), Module 07 (MCP server architecture)

## Pentest Red Team MCP Server

**Stack**: Python, FastMCP, 44 security tools (Nmap, Nuclei, Nikto, ZAP, Trivy, Hydra, kubectl)

Comprehensive penetration testing toolkit with structured playbooks for network, web app, K8s, and cloud assessments. Includes chain-of-custody evidence collection and OWASP Top 10 mapping.

**Demonstrates**: Module 03 (pentest methodology), Module 05 (K8s security), Module 07 (tool orchestration)

## CTI Grafana Dashboard

**Stack**: Terraform, EKS, PostgreSQL, Grafana, Python collectors, Docker

Kubernetes-hosted threat intelligence dashboard aggregating 10+ data sources (NVD, CISA KEV, EPSS, Wiz, Shodan, GreyNoise, OTX). Production-grade with Okta authentication and CloudFront CDN.

**Demonstrates**: Module 02 (threat intel aggregation), Module 06 (IaC at scale)

## AppSec RAG Agent

**Stack**: Python, FastAPI, ChromaDB, Claude API (Bedrock), boto3, Google Cloud

RAG-as-a-Service for multi-cloud security inventory. Collects AWS + GCP resources into vector store, answers natural language security queries via Claude with tool use.

**Demonstrates**: Module 07 (agentic AI patterns, RAG for security)

## Groundplex Scan Pipeline

**Stack**: ECS Fargate, Trivy, WizCLI, Maven analyzer, Python, SES

Automated monthly vulnerability scanning of containerized SaaS platform including runtime-loaded components (snap packs) that standard scanners miss.

**Demonstrates**: Module 01 (scanning beyond surface), Module 05 (container security)
