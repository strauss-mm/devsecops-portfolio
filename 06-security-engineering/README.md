# Module 06: Security Engineering

Infrastructure-as-code security, policy-as-code with OPA/Rego, secrets management patterns, and zero-trust architecture design.

## Labs

| Lab | Focus | Difficulty | Status |
|-----|-------|-----------|--------|
| [lab-01](labs/lab-01-iac-security/) | Secure Terraform patterns + scanning | Senior | Planned |
| [lab-02](labs/lab-02-policy-as-code/) | Policy-as-code with OPA/Rego | Senior+ | Planned |
| [lab-03](labs/lab-03-secrets-management/) | Secrets management (rotation, Vault, Secrets Manager) | Principal | Planned |
| [lab-04](labs/lab-04-zero-trust/) | Zero-trust architecture for SaaS platforms | Principal | Planned |

## Writeups

- Terraform security at scale (multi-account, multi-region)
- Secrets in SaaS integration pipelines
- Building security platforms (not just tools)

## Reusable Modules

- [secure-ecs-service](modules/secure-ecs-service/) — Hardened ECS Fargate service module
- [secure-s3-bucket](modules/secure-s3-bucket/) — S3 bucket with encryption, logging, lifecycle
- [waf-standard](modules/waf-standard/) — Standard WAF rule set module

## Key Concepts

- **Security as code**: Version-controlled, reviewed, tested security configurations
- **Policy enforcement**: Automated guardrails that prevent misconfigurations
- **Secrets lifecycle**: Generation, rotation, distribution, revocation
- **Zero trust**: Never trust, always verify — network, identity, device

## Prerequisites

- Terraform fundamentals
- AWS services (IAM, VPC, ECS, S3, Secrets Manager)
- Understanding of PKI and identity management
