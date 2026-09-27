# Modo Blob (ES)

> Modo interno de la skill `upstash` (no es skill separada). Router: `upstash` → este modo
> ante S3, blob, upload, presigned URL, multipart o subida directa desde navegador.

## Cubre

Almacenamiento de objetos S3-compatible (`Bucket` en servidor, `uploadHandler` + hooks
React para subir desde el navegador sin pasar por la app), URLs firmadas, multipart,
lecturas firmadas y cabeceras de caché.

## Referencias propias

Guía principal (ES): `references/blob.md`.

| Fichero | Contenido |
|---|---|
| `references/blob.md` | guía principal ES |
| `references/overview.md` | visión general del SDK `@upstash/blob` |

## Ejemplos

Ver `ejemplos.md` (subida en servidor, subida directa desde navegador, URL firmada).

## Dependencias

Ninguna. El token es bearer del bucket: solo en servidor (ver `../../core/config.md`).
Errores y resume multipart: `../../core/errores.md`.
