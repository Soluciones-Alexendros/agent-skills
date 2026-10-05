> **Nota (ES):** documento original del SDK (inglés). La guía del modo en español está en `../MODE.md`.

# QStash JavaScript SDK

QStash is an HTTP-based messaging and scheduling solution for serverless and edge runtimes. This skill helps you use the QStash JS SDK effectively.

## When to use this skill

Use this skill when:

- Publishing HTTP messages to endpoints or URL groups
- Creating scheduled or delayed message delivery
- Managing FIFO queues with configurable parallelism
- Verifying incoming webhook signatures from QStash
- Implementing callbacks, DLQ handling, or message deduplication

## Quick Start

### Installing the SDK

```bash
npm install @upstash/qstash
```

### Basic Publishing

```typescript
import { Client } from "@upstash/qstash";

const client = new Client({
  token: process.env.QSTASH_TOKEN!,
});

const result = await client.publishJSON({
  url: "https://my-api.example.com/webhook",
  body: { event: "user.created", userId: "123" },
});
```

## Core Concepts

For fundamental QStash operations, see:

- [Publishing Messages](publishing-messages.md)
- [Schedules](schedules.md)
- [Queues and Flow Control](queues-and-flow-control.md)
- [URL Groups](url-groups.md)
- [Local Development](local-development.md) — automatic dev server via `devMode: true`

For verifying incoming messages:

- [Receiver Verification](receiver.md) - Core signature verification with the Receiver class
- Platform-Specific Verifiers:
  - [Next.js](nextjs.md) - App Router, Pages Router, and Edge Runtime

For advanced features:

- [Callbacks](callbacks.md)
- [Dead Letter Queue (DLQ)](dlq.md)
- [Message Deduplication](deduplication.md)
- [Region migration & multi-region support](multi-region-summary.md)
  - If needed, [multi-region env variable setup verification script](../examples/verify-multi-region-setup.ts). Can be run without arguments

## Platform Support

QStash JS SDK works across various platforms:

- Next.js (App Router and Pages Router)
- Cloudflare Workers
- Deno
- Node.js (v18+)
- Vercel Edge Runtime
- SvelteKit, Nuxt, SolidJS, and other frameworks

> **Note on Workflow SDK:** For building complex durable workflows that chain multiple QStash messages together, consider using the separate QStash Workflow SDK (`@upstash/workflow`). The Workflow SDK empowers you to orchestrate multi-step processes with automatic state management, retries, and fault tolerance. This Skills file focuses on the core QStash messaging SDK.

## Best Practices

- Always verify incoming QStash messages using the Receiver class
- Use environment variables for tokens and signing keys
- Set appropriate retry counts and timeouts for your use case
- Use queues for ordered processing with controlled parallelism
- Implement DLQ handling for failed message recovery
