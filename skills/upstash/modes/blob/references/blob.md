# Blob Storage S3-Compatible (Upstash Blob) — Referencia Completa

> **Submódulo de `upstash`** — Modo interno de `upstash` (`modes/blob/MODE.md`)

---

## Instalación

```bash
npm install @upstash/blob
```

```typescript
import { Bucket } from "@upstash/blob";

const bucket = Bucket.fromEnv(); // Lee UPSTASH_BLOB_TOKEN
// O explícito:
const bucket = new Bucket({ token: process.env.UPSTASH_BLOB_TOKEN! });
```

**Bucket público vs privado:**
- **Público**: objetos tienen URL accesible directamente
- **Privado**: sin URL pública, lecturas via `signedReadUrl()`

---

## Escritura (Upload)

```typescript
// Upload básico
const blob = await bucket.put("reports/q3.pdf", pdfBuffer, {
  contentType: "application/pdf",
  cache: "immutable",           // Cache-Control header
  metadata: { author: "user-123" }, // x-amz-meta-*
  allowOverwrite: true,         // false = error si existe
  ifUnchanged: "etag-value",    // Optimistic locking
  multipart: "16mb",            // Threshold multipart
});

// Respuesta
blob.url;           // URL pública (undefined en bucket privado)
blob.versionedUrl;  // URL con ?v=<etag> (cambia si bytes cambian)
blob.etag;          // Para ifUnchanged
```

**Tipos de body aceptados:** `Blob`/`File`, `ArrayBuffer`, typed arrays, `string`, `ReadableStream`, `Request`

**Paths únicos (evitar colisiones):**
```typescript
import { uniquePath } from "@upstash/blob";

const path = uniquePath`${userId}/${fileName}`; // 'u7/photo-3xK9mBqR.png'
```

---

## Lectura

```typescript
// Get (stream)
const res = await bucket.get("reports/q3.pdf");
// { path, etag, contentType, cacheControl, metadata, body: ReadableStream }

// Info (HEAD - sin bytes)
const info = await bucket.info("reports/q3.pdf");

// Exists (boolean)
const exists = await bucket.exists("avatars/u7.png");

// List (paginado)
const page = await bucket.list({ prefix: "avatars/", limit: 1000 });
// { cursor, blobs: [{ path, etag, size, uploadedAt }] }

// Leer stream como texto
const text = await new Response((await bucket.get("notes/1.md")).body).text();
```

---

## URLs Firmadas (Private Buckets)

```typescript
// URL firmada para lectura temporal
const { url, expiresAt } = await bucket.signedReadUrl("private/report.pdf", {
  expiresIn: "2m",              // 2 minutos
  downloadAs: "Report Q3.pdf"   // Content-Disposition filename
});

// Cachear hasta expiresAt (nunca compute deadline tú mismo)
```

---

## Subidas desde Navegador (Direct Browser Upload)

```typescript
// lib/uploads.ts (server-only)
import { uploadHandler, uniquePath, BlobError } from "@upstash/blob";
import { getUser } from "@/lib/auth";
import { db } from "@/lib/db";

export const uploads = uploadHandler({
  constraints: { maxSize: "20mb", contentTypes: ["image/*", "application/pdf"] },

  onBeforeUpload: async ({ request, file }) => {
    const user = await getUser(request);
    if (!user) throw new BlobError("unauthorized");
    return {
      path: uniquePath`${user.id}/${file.name}`,
      metadata: { owner: user.id }
    };
  },

  onUploadComplete: async ({ uploadId, path, url, metadata }) => {
    if (!metadata.owner) throw new BlobError("unauthorized");
    await db.files.upsert({ id: uploadId, owner: metadata.owner, path, url });
    return { path }; // Devuelto al cliente
  },
});
```

```typescript
// app/api/upload/route.ts
export const { GET, POST } = uploads;
```

```tsx
// Client component
"use client";
import { useUpload } from "@/lib/upload-hooks";

export function UploadForm() {
  const { start, upload, accept } = useUpload();
  return (
    <>
      <input type="file" accept={accept} onChange={e => start({ file: e.target.files?.[0] })} />
      {upload?.pending && <progress value={upload.percent} max={100} />}
      {upload?.status === "done" && <a href={upload.blob.url}>{upload.blob.data.path}</a>}
      {upload?.status === "error" && <p>{upload.error.message}</p>}
    </>
  );
}
```

**Reglas críticas:**
- `onUploadComplete` puede ejecutarse más de una vez (reintentos browser) → upsert por `uploadId`
- Throw en `onUploadComplete` **elimina el objeto** → catch errores BD propios

---

## Multipart & Large Files (>16MB)

```typescript
// Configurar multipart en handler
const uploads = uploadHandler({
  constraints: { maxSize: "100mb" },
  multipart: true, // Fuerza multipart para todos
  // ...
});

// Cleanup uploads multipart incompletos (cron diario)
await bucket.abortStaleMultipartUploads({ olderThan: "1d" });
```

**Features multipart:** pause/resume, retry por parte, resume tras recarga navegador.

---

## Cache Headers (Cache-Control)

```typescript
await bucket.put("asset.png", data, {
  cache: "immutable"    // public, max-age=31536000, immutable
  // cache: "revalidate"   // public, max-age=0, must-revalidate
  // cache: "no-store"     // no-store
  // cache: "15m"          // public, max-age=900
});
```

**immutable** requiere path que cambie al cambiar bytes (`uniquePath` o `versionedUrl`).

---

## Copy / Move / Update JSON

```typescript
// Copy
await bucket.copy("from/path.png", "to/path.png", { contentType, cache, metadata });

// Move (rename)
await bucket.move("old/path.png", "new/path.png", { contentType, cache, metadata });

// Update JSON atómico (read-modify-write con retry)
await bucket.updateJson("config/app.json", (current) => ({
  ...current,
  featureFlags: { ...current.featureFlags, newFeature: true }
}), { maxAttempts: 6 });
```

---

## Eliminación

```typescript
// Un archivo
await bucket.del("avatars/me.png");

// Array (batched 1000)
await bucket.del(["a.png", "b.png"]);

// Prefix (todo bajo prefijo)
await bucket.del({ prefix: "tmp/" });

// del({ prefix: '' }) requiere all: true
```

---

## S3 Client (AWS SDK Compatible)

```typescript
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

const config = bucket.s3(); // { bucket, endpoint, credentials: async providers }
const s3 = new S3Client(config);

await s3.send(new GetObjectCommand({
  Bucket: config.bucket,
  Key: "reports/q3.pdf"
}));

// Útil para: byte ranges, conditional GETs, tagging, operaciones no wrappedas
```

---

## Errores (BlobError)

```typescript
import { BlobError } from "@upstash/blob";

if (BlobError.is(e)) {
  switch (e.code) {
    case "not_found": return null;
    case "already_exists": return "conflict";
    case "too_large": return "size limit";
    case "unauthorized": return "auth required";
    case "partial_delete": return e.failed; // array de fallidos
    // ...
  }
}
```

**Siempre usar `BlobError.is()`**, no `instanceof` (ESM/CJS diferentes clases).

---

## Mejores Prácticas

1. **uniquePath** para paths de usuario → evita colisiones
2. **Uploads directos browser** → bytes no pasan por tu servidor
3. **Private bucket + signedReadUrl** → control de acceso granular
4. **Multipart para >16MB** → pause/resume, retry, resume tras reload
5. **Cache headers en upload** → inmutable para assets, revalidate para docs
6. **onUploadComplete upsert** → maneja reintentos browser
6. **Catch errores BD en onUploadComplete** → throw elimina objeto

---

## Recursos

- [Documentación Oficial](https://upstash.com/docs/blob)
- [GitHub @upstash/blob](https://github.com/upstash/blob-js)
- [Browser Uploads Guide](https://upstash.com/docs/blob/browser-uploads)