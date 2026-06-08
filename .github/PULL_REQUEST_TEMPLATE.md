## Summary

<!-- Brief description of changes -->

## Type

- [ ] New lab content
- [ ] New tool / shipped code
- [ ] Detection rule (Sigma/YARA/KQL)
- [ ] Documentation / writeup
- [ ] Infrastructure (Terraform/K8s/Docker)
- [ ] CI/CD workflow change
- [ ] Bug fix

## Security Checklist

- [ ] No secrets, API keys, or credentials in code
- [ ] No proprietary/internal information exposed
- [ ] Dependencies pinned to specific versions
- [ ] Input validation present where applicable
- [ ] Error messages don't leak sensitive information
- [ ] Terraform/IaC follows least-privilege principle
- [ ] Docker images use non-root user where possible

## Testing

- [ ] Lab code runs successfully end-to-end
- [ ] Unit tests pass (if applicable)
- [ ] Detection rules validated against test cases
- [ ] Documentation reviewed for accuracy

## Module Impact

<!-- Which module(s) does this affect? -->

---

*Security scan results will appear as PR checks above.*
