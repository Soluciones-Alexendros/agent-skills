# Box (Upstash) — Sandboxed Containers con Agentes IA

> **Submódulo de `upstash`** — Router: `upstash` → `references/box.md`. Skill independiente aspiracional: `entorno-aislado` (no existe en este repo)

---

## Instalación

```bash
npm install @upstash/box
npm install zod   # peer dependency para responseSchema / browser schemas
```

```typescript
import { Box, Agent, ClaudeCode, BoxApiKey } from "@upstash/box";

const box = await Box.create({
  name: "my-box",
  runtime: "node",           // "node" | "python" | "golang" | "ruby" | "rust" (+ "-alpine")
  size: "small",             // "small" (2CPU/4GB) | "medium" (4/8) | "large" (8/16)
  labels: ["beta", "x-team"], // max 5, ≤20 chars
  keepAlive: true,           // no idle-pause
  initCommand: "npm install && npm run dev", // solo keep-alive
  browser: true,             // headless Chromium
  agent: {
    harness: Agent.ClaudeCode,
    model: ClaudeCode.Sonnet_4_5,
    apiKey: BoxApiKey.UpstashKey, // Upstash-provided LLM key
  },
  git: { token: process.env.GITHUB_TOKEN, userName: "Bot", userEmail: "bot@example.com" },
  env: { DATABASE_URL: "..." },
  skills: ["upstash/qstash-js/qstash-js"],
  timeout: 600_000,
});
```

---

## Ciclo de Vida de la Box

```typescript
// Reconectar
const same = await Box.get(box.id, { gitToken: process.env.GITHUB_TOKEN });
const byName = await Box.getByName("my-box");
const all = await Box.list();
const beta = await Box.list({ label: "beta" });

// Pausar/Reanudar/Eliminar
await box.pause();    // throw en keep-alive
await box.resume();
await box.delete();   // irreversible

// Estado
const { status } = await box.getStatus();
// status: "running" | "paused" | "stopped" | "deleted"
```

---

## Agentes IA (Agent Runs)

```typescript
import { z } from "zod";

// Output estructurado con Zod
const run = await box.agent.run({
  prompt: "Review the code for security issues",
  responseSchema: z.object({
    verdict: z.enum(["approved", "changes_requested"]),
    findings: z.array(z.object({
      severity: z.enum(["high", "medium", "low"]),
      file: z.string(),
      issue: z.string(),
    })),
  }),
  timeout: 120_000,
  maxRetries: 2,
  options: { maxTurns: 20, maxBudgetUsd: 1.0, effort: "high" },
  onToolUse: (tool) => console.log(tool.name, tool.input),
});

// Streaming
const stream = await box.agent.stream({ prompt: "Build a REST API" });
for await (const chunk of stream) {
  if (chunk.type === "text-delta") process.stdout.write(chunk.text);
  if (chunk.type === "tool-call") console.log(chunk.toolName, chunk.input);
}

// Fire-and-forget con webhook
await box.agent.run({
  prompt: "Run tests",
  webhook: { url: "https://example.com/hook", headers: { Authorization: "Bearer ..." } }
});
```

**Harness soportados:** `Agent.ClaudeCode`, `Agent.Codex`, `Agent.OpenCode`, `Agent.Cursor`, `Agent.Custom`

---

## Shell / Code Execution

```typescript
// Comandos shell
const run = await box.exec.command("echo hello && ls -la");

// Code snippets
const run2 = await box.exec.code({ code: "console.log(1+1)", lang: "js", timeout: 10_000 });

// Streaming
const stream = await box.exec.stream("npm run build");
for await (const chunk of stream) {
  // chunk: { type: "output", data } | { type: "exit", exitCode, cpuNs }
}
```

### Live Sessions (PTY, WebSocket)

```typescript
const session = await box.exec.session({
  cmd: "sort",
  cwd: "/workspace/home",
  env: ["LOG_LEVEL=debug"],
  onStdout: (bytes) => process.stdout.write(bytes),
  onStderr: (bytes) => process.stderr.write(bytes),
});

session.write("input\n");
session.endStdin();
const exitCode = await session.wait();
session.close();

// Interactive / TUI
const shell = await box.exec.session({ argv: ["bash", "-i"], tty: true, rows: 40, cols: 120 });
shell.resize(50, 160);
shell.kill("INT");
```

---

## Filesystem

```typescript
// Read/Write
await box.files.write({ path: "/workspace/home/app.js", content: "console.log('hi')" });
const content = await box.files.read("/workspace/home/app.js");

// Binary (base64)
await box.files.write({ path: "/workspace/home/img.png", content: base64Str, encoding: "base64" });
const b64 = await box.files.read("/workspace/home/img.png", { encoding: "base64" });

// Range read (capped 8MB)
const head = await box.files.read("/workspace/home/big.log", { length: 64 * 1024 });
const slice = await box.files.read("/workspace/home/big.log", { offset: 1024, length: 512 });

// List/Stat
const entries = await box.files.list("/workspace/home");
const stat = await box.files.stat("/workspace/home/app.js"); // lstat por default
const target = await box.files.stat("/workspace/home/link", { follow: true });

// Directories
await box.files.mkdir("build/cache", { parents: true });
await box.files.rename("draft.md", "docs/final.md");
await box.files.remove("build/cache", { recursive: true });

// Upload/Download
await box.files.upload([{ path: "./local/file.txt", destination: "/workspace/home/file.txt" }]);
await box.files.download({ folder: "src" }); // → ./src local
```

---

## Git (Dentro de la Box)

```typescript
await box.git.clone({ repo: "github.com/org/repo", branch: "main", depth: 1 });
await box.cd("repo");

const status = await box.git.status();
const diff = await box.git.diff();

await box.git.commit({ message: "fix: bug", authorName: "Bot", authorEmail: "bot@example.com" });
await box.git.push({ branch: "feature/fix" });

const pr = await box.git.createPR({ title: "Fix bug", body: "...", base: "main" });
// pr: { url, number, title, base }
```

---

## Schedules (Cron en la Box)

```typescript
// Shell cron
await box.schedule.exec({
  cron: "* * * * *",
  command: ["bash", "-c", "date >> /workspace/home/cron.log"],
  webhookUrl: "https://example.com/hook",
});

// Agent cron
await box.schedule.agent({
  cron: "0 9 * * *",
  prompt: "Run test suite and fix failures",
  folder: "/workspace/home/repo",
  model: "anthropic/claude-sonnet-5",
  options: { maxBudgetUsd: 1.0, effort: "high" },
  timeout: 300_000,
});

await box.schedule.pause(id);
await box.schedule.resume(id);
await box.schedule.delete(id);
```

---

## Snapshots (Checkpoints)

```typescript
// Crear snapshot
const snap = await box.snapshot({ name: "after-setup" });

// Restaurar desde snapshot (nueva box)
const restored = await Box.fromSnapshot(snap.id, {
  size: "medium",
  keepAlive: true,
  git: { token: process.env.GITHUB_TOKEN, userName: "Bot", userEmail: "bot@example.com" },
  env: { DATABASE_URL: "..." },
});

await box.deleteSnapshot(snap.id);
```

---

## Browser (Headless Chromium)

```typescript
const box = await Box.create({ browser: true, agent: { harness: Agent.ClaudeCode } });

const tab = await box.browser.tab.create("https://example.com", { waitUntil: "load", timeout: 30_000 });

// AI operations (metered)
const data = await tab.extract("Top story", z.object({ title: z.string(), points: z.number() }));
const { elements } = await tab.observe("What can I click?");
const acted = await tab.act("Click first headline");

// Replay sin LLM (no tokens)
await tab.act(elements[0]);

// CDP para Playwright/Puppeteer
const cdpUrl = await box.browser.cdpUrl();
const remote = await chromium.connectOverCDP(cdpUrl);

// Grabaciones HLS/MP4
const handle = await box.browser.recordings.start({ maxDurationSeconds: 600 });
const recording = await handle.stop();
await box.browser.recordings.download(recording.id, { path: "./demo.mp4" });
```

**Nota:** `tab.run()` removido en 0.7.0. Usar loop `observe` + `act(action)` + `extract`, o agent in-box, o CDP.

---

## EphemeralBox (Ligeras, máx 3 días)

```typescript
import { EphemeralBox } from "@upstash/box";

const ebox = await EphemeralBox.create({
  name: "scratch-box",
  runtime: "python",
  size: "small",
  ttl: 3600, // segundos, max 259200 (3 días)
  env: { API_KEY: "..." },
  networkPolicy: { mode: "deny-all" },
});

await ebox.exec.command("python -c 'print(1+1)'");
await ebox.files.write({ path: "/workspace/home/data.json", content: "{}" });
await ebox.schedule.exec({ cron: "* * * * *", command: ["bash", "-c", "date"] });
const snap = await ebox.snapshot({ name: "checkpoint" });
```

**No soporta:** agent, git, skills, browser, public URLs. Sí: exec, files, schedule, snapshots.

---

## Public URLs (Exponer Puertos)

```typescript
const publicURL = await box.getPublicURL(3000);
// { url: "https://{id}-3000.preview.box.upstash.com", port }

const authed = await box.getPublicURL(3000, { bearerToken: true });
const basic = await box.getPublicURL(3000, { basicAuth: true });
```

---

## Skills (Context7 Registry)

```typescript
const box = await Box.create({ skills: ["upstash/qstash-js/qstash-js"] });
await box.skills.add("upstash/workflow-js/workflow-js");
await box.skills.remove("upstash/workflow-js/workflow-js");
```

---

## Network Policy & Outbound Headers

```typescript
const box = await Box.create({
  networkPolicy: {
    mode: "custom",           // "allow-all" | "deny-all" | "custom"
    allowedDomains: ["api.example.com"],
    allowedCidrs: ["203.0.113.0/24"],
    deniedCidrs: ["10.0.0.0/8"],
  },
  attachHeaders: {
    "api.stripe.com": { Authorization: "Bearer sk_live_..." },
    "*.example.com": { "X-Custom-Token": "secret123" },
  },
});
```

---

## MCP Servers

```typescript
const box = await Box.create({
  agent: { harness: Agent.ClaudeCode, model: ClaudeCode.Sonnet_4_5 },
  mcpServers: [
    { name: "fs", package: "@modelcontextprotocol/server-filesystem", args: [] },
    { name: "custom", url: "<mcp-url>", headers: { Authorization: "..." } },
  ],
});
```

---

## SSH Directo

```bash
ssh <box-id>@us-east-1.box.upstash.com
# Password = Box API Key
```

---

## Gotchas Clave

- `box.cd()` = tracking client-side, valida path pero no cambia shell cwd
- No `box.fork()` — usar snapshot + `Box.fromSnapshot()`
- `EphemeralBox` sin agent/git/skills/browser/public URLs
- `run.exitCode` = `null` para agent runs
- `files.download({ folder })` → path DENTRO de la box, output en `./<basename>`
- `files.stat()` = lstat por default (`follow: true` para dereferenciar)
- `exec.session()` = Node-only, handle owns process, no reattach
- `tab.run()` removido → usar loop `observe`+`act`+`extract`, agent in-box, o CDP
- `getInitCommand`/`setInitCommand` requieren `keepAlive: true`
- `box.delete()` irreversible — snapshot primero

---

## Recursos

- [Documentación Oficial](https://upstash.com/docs/box)
- [GitHub @upstash/box](https://github.com/upstash/box-js)
- [Python SDK](https://pypi.org/project/upstash-box/)