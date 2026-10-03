---
name: build-upstash
description: >-
  Upstash ecosystem router: Redis, Vector/RAG, Search, QStash/Workflows, Ratelimit, Blob, Box
  with 7 internal modes. Use when the operator requests Upstash, serverless Redis, managed
  embeddings/RAG, QStash or rate limiting. Not for Postgres nor other relational databases.
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "2.0.0"
  domain: build
  type: atomic
  language: en
---
# Build Upstash

## Overview

Upstash ecosystem router (Redis, Vector/RAG, Search, QStash/Workflows, Ratelimit, Blob, Box)
with 7 internal modes. Use when the operator requests Upstash, serverless Redis, managed
embeddings/RAG, QStash or rate limiting. Not for Postgres nor other relational databases.

## When to Use

- When Upstash is requested
- For serverless Redis
- For managed embeddings/RAG
- For QStash queues or workflows
- For rate limiting

## Not for:

- Postgres or other relational databases

## Internal Modes

| Mode | Description |
|------|-------------|
| Redis | Cache, sessions, KV store |
| Vector | Embeddings, semantic search, RAG |
| Search | Full-text, typo-tolerant, facets |
| QStash | Queues, cron, workflows |
| Ratelimit | Rate limiting integration |
| Blob | S3-compatible storage |
| Box | Sandboxed containers |
