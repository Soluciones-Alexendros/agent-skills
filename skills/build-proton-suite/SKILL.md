---
name: build-proton-suite
description: >-
  Proton Mail (Proton Mail Bridge IMAP/SMTP local, MCP Mail) and Proton Pass secrets
  (pass-cli v2.3+ with JSON output, MCP Pass). Use when the operator requests reading,
  searching, sending or classifying Proton Mail, or obtaining tokens, passwords and API keys
  stored in Proton Pass. Do not use for other email providers or CI/GitHub secrets.
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "2.0.0"
  domain: build
  type: atomic
  language: en
---
# Build Proton Suite

## Overview

Proton Mail (Proton Mail Bridge IMAP/SMTP local, MCP Mail) and Proton Pass secrets
(pass-cli v2.3+ with stable JSON output, MCP Pass). Use when the operator requests reading,
searching, sending or classifying Proton Mail, or obtaining tokens, passwords and API keys
stored in Proton Pass. Do not use for other email providers or CI/GitHub secrets.

## When to Use

- When reading Proton Mail emails
- To search messages by sender or organization
- To classify email by case (court, registry, TGSS, notary, SMAC)
- To obtain tokens, passwords and API keys from Proton Pass
- To send emails from the Proton account

## Not for:

- Other email providers
- CI/GitHub secrets

## Workflow

```text
Read email
       │
       ▼
Search by sender
       │
       ▼
Classify by case
       │
       ▼
Obtain secrets
       │
       ▼
Send email
```
