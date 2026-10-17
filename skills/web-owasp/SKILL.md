---
name: web-owasp
description: "Code security review (OWASP): injection, XSS, authn/authz, cryptography, SSRF, secrets and misconfiguration. Use when performing security review, OWASP or searching for vulnerabilities in this code. Not for dependency CVEs (→ project-libraries) nor web compliance (→ web-compliance)."
license: MIT
metadata:
  author: Soluciones-Alexendros (adapted)
  version: 4.0.1
  domain: web
  type: atomic
  language: en
  keywords: web-owasp
compatibility: opencode, codex, cursor, copilot
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Web OWASP

## Overview

Code security review (OWASP): injection, XSS, authn/authz, cryptography, SSRF, secrets
and misconfiguration. Use when performing security review, OWASP or searching for vulnerabilities
in this code.

## When to Use

- When security review is requested
- To search for vulnerabilities in code
- OWASP security review

## Not for:

- OS hardening (→ local-security)
- Release closure (→ project-publish)
- Dependency audit/SCA (→ project-libraries)

## OWASP Categories

### A01: Injection

- SQL, NoSQL, OS injection
- Prevention: parametrized queries, input validation

### A02: Broken Authentication

- Session handling
- Weak credentials
- Prevention: multi-factor authentication

### A03: Cross-Site Scripting (XSS)

- Input sanitization
- Output encoding

### A05: Security Misconfiguration

- Default credentials
- Informative error messages
- Security patches

### A09: Identification and Authentication Failures

- Password management
- Account lockout

## Best Practices

- Input validation everywhere
- Output escaping
- Security headers (CSP, HSTS)
- Secure secret management
