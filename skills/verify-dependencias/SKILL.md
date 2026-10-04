---
name: verify-dependencias
description: >-
  Dependency audit (SCA/CVE): multi-language pipeline (npm/pip/cargo/go/maven/gradle/composer/gem)
  to detect vulnerabilities, malware, typosquatting, unused dependencies and outdated. Use when
  performing dependency audit, SCA, CVE scanning, supply chain security or SBOM generation. Not for code security review (→ verify-owasp) nor web compliance audits (→ verify-compliance).
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "2.3.0"
  domain: verify
  type: atomic
  language: en
---

# Verify Dependencies

## Overview

Dependency audit (SCA/CVE): multi-language pipeline (npm/pip/cargo/go/maven/gradle/composer/gem)
to detect vulnerabilities, malware, typosquatting, unused dependencies and outdated. Use when
performing dependency audit, SCA, CVE scanning, supply chain security or SBOM generation.

## When to Use

- When dependency audit is requested
- For SCA (Software Composition Analysis)
- For CVE (Common Vulnerabilities and Exposures) scanning
- For supply chain security
- For SBOM (Software Bill of Materials) generation

## Not for:

- Code OWASP review (→ verify-owasp)
- OS hardening (→ operate-seguridad)
- Disk cleanup (→ operate-mantenimiento)

## Supported Pipeline

| Language                                   | Dependency File                              |
| ------------------------------------------ | -------------------------------------------- |
| npm/pip/cargo/go/maven/gradle/composer/gem | package.json, requirements.txt, go.mod, etc. |

## What It Detects

- Vulnerabilities (CVE)
- Malware
- Typosquatting
- Outdated dependencies
- Unused dependencies

## SBOM Generation

- Complete list of all dependencies
- Exact versions
- Licenses
- Metadata for each package
