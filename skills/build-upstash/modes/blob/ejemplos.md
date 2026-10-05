# Ejemplos Blob (ES)

> Ejemplos mínimos del modo `blob`. Detalle en `references/blob.md`.

## Subida en servidor

```typescript
import { Bucket } from "@upstash/blob";
const bucket = Bucket.fromEnv();

await bucket.put("facturas/2026-001.pdf", pdfBytes, {
  contentType: "application/pdf",
});
```

## Subida directa desde navegador (sin pasar por la app)

```typescript
// app/api/upload/route.ts
import { uploadHandler } from "@upstash/blob/nextjs";

export const POST = uploadHandler({ bucket: "mi-bucket" });
```

```tsx
// cliente
import { useUpload } from "@upstash/blob/react";
const { upload } = useUpload();
await upload({ file, pathname: `avatares/${file.name}` });
```

## URL firmada de lectura

```typescript
const url = await bucket.getSignedUrl("facturas/2026-001.pdf", {
  expiresIn: 3600,
});
```
