# Seguridad — canon repo-standard

### Propósito de este documento

- **Objetivos:** Fijar la línea mínima de seguridad no negociable de la flota: escaneo de secretos, pinning de Actions con SHA, permisos mínimos, anti script-injection y supply chain. Solo lectura: la auditoría la ejecuta `operar-release` (Fase D) con `operar-release/references/actions-security.md` como procedimiento.
- **Estructura:** Esta meta-sección → Línea mínima (bloqueos) → Secret scanning → Pinning → Permisos → Script injection → Supply chain/OIDC → Incidentes de referencia.
- **Contenido a integrar según contexto:** En un producto, aplicar la línea mínima sin excepciones por tamaño; el gate proporcional (`operar-release/assets/checklist-readiness.md`) decide qué avisos suben a bloqueo en repos críticos.

## Línea mínima (siempre bloquea)

- Secreto en el árbol o en el historial reciente que el escaneo señale.
- `uses:` de terceros sin SHA completo de 40 hex verificado (en repo crítico, también `actions/*` y `github/*`).
- Workflow sin `permissions:` explícito.
- Job sin `timeout-minutes`.
- Entrada no confiable interpolada en `run:` o en `github-script`.
- `pull_request_target` o `workflow_run` que haga checkout y ejecute código no confiable.
- Runtime fuera de soporte confirmado por el calendario oficial del lenguaje, sin plan.
- `actionlint` en rojo cuando existen workflows.
- Required checks de lint/tests/build en rojo cuando el repo tiene CI.

Nunca hacer commit de un `uses:` con tag flotante (`@v*`, `@main`, `@master`) ni de un placeholder de pin.

## Secret scanning

- Gitleaks en cada pull request y en cada push a la rama por defecto, con historial completo (`fetch-depth: 0`) y sin filtro `paths` (un required check que no aparece en el PR no protege la rama).
- Comentarios del escáner solo en `pull_request` (ese job pide `pull-requests: write`). Los push escanean sin comentar.
- No subir SARIF como artefacto si puede incluir el secreto: hallazgos en el log y el resumen del job, no en un descargable.
- `gitleaks-action` v3 exige `GITLEAKS_LICENSE` en cuentas de organización y la omite en cuentas personales. No inventar ni commitear la licencia; si falta, el ítem queda `[PENDIENTE]`.
- Un secreto en el historial está comprometido: rotar el valor. No dejarlo en cachés, logs ni artefactos. Rotación y purga de historial solo con autorización explícita.
- Secretos de despliegue en `environment` con protection rules cuando el riesgo lo justifique. No cachear `~/.aws`, `~/.ssh` ni tokens.

## Pinning de Actions (procedimiento resumido)

Procedimiento completo en `operar-release/references/actions-security.md`; antes de citarlo, abrir las fuentes oficiales:

- `https://docs.github.com/en/actions/reference/security/secure-use`
- `https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/`
- `https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases`

1. Fijar owner, repo y tag de la release (`actions/checkout`, `v7.0.1`).
2. `gh api repos/OWNER/REPO` — si `fork` es true, descartar el pin.
3. `gh api repos/OWNER/REPO/git/ref/tags/TAG` → SHA del objeto.
4. Si es tag anotado, resolver `git/tags/OBJECT_SHA` hasta el commit.
5. Confirmar `gh api repos/OWNER/REPO/commits/COMMIT_SHA --jq .sha`.
6. Escribir `uses: owner/repo@COMMIT # vX.Y.Z`.
7. Mantener con Renovate (`github-actions`) en PRs revisables.

Los SHA de `operar-release/assets/` se verificaron el 2026-09-23: repetir el procedimiento antes de copiarlos. Si un paso falla, `[PENDIENTE]` y no reutilizar el pin.

## Permisos mínimos

- Defecto del workflow: `contents: read`. Un job que fija `permissions` reemplaza las del workflow (lo no indicado queda en `none`).
- Subir el ámbito solo en el job que lo usa: `contents: write` (publicar release), `pull-requests: write` (comentar en PR), `actions: write` (subir artefactos), `id-token: write` + `attestations: write` (attestations, con `contents: read` en ese mismo job).
- `persist-credentials: false` en `actions/checkout` cuando el token no hace falta tras el clon. `gh` recibe `GH_TOKEN: ${{ github.token }}` solo en el paso que lo usa.
- `SECURITY.md` con camino de divulgación es `BLOCK` si el repo es público y `WARN` si es privado no crítico. `CODEOWNERS` cubriendo `.github/workflows/` es aviso salvo repo crítico.

## Script injection

- No interpolar en `run:` títulos, cuerpos, nombres de rama, `github.head_ref` ni mensajes de tag. Pasar el valor por `env:` y leerlo desde el script; validar el formato (p. ej. SemVer del tag) y rechazar multilínea.
- En `actions/github-script`, leer `process.env`; no meter `${{ }}` dentro de template literals de JavaScript.
- Separar el workflow sin privilegios (produce artefactos evaluados) del workflow con privilegios (comenta o etiqueta) en triggers `pull_request_target` / `workflow_run`. Un entorno con required reviewers es complemento, no sustituto.

## Supply chain y OIDC

- Cada Action es una dependencia: pin, revisión y actualización en PR. Immutable releases evitan mover tags/assets publicados, pero el workflow sigue referenciando el pin a commit; no existe interruptor nativo que obligue a consumir solo immutable releases.
- Sustituir claves cloud de larga duración por OIDC (`id-token: write` solo en el job que asume el rol, subject limitado a repo/rama/entorno). Para npm/PyPI, trusted publishing en lugar de token persistente.
- Instalación de `actionlint`: asset de una release concreta con SHA-256 de `actionlint_<version>_checksums.txt` de esa misma release (no `curl | bash` contra `main`). Complemento: `gh attestation verify --repo rhysd/actionlint <archivo>`.
- Self-hosted runners: prohibidos en repos públicos; en privados, efímeros, sin workspace reutilizado y egress restringido.

## Incidentes de referencia

Comprobar el relato en la guía de secure use o el aviso del proyecto antes de repetir detalles.

- **tj-actions/changed-files (marzo 2025):** un tag mutable pasó a apuntar a un commit que filtraba secretos por los logs. El pin a SHA completo habría seguido en el commit anterior.
- **reviewdog / trivy-action (marzo 2025):** compromiso encadenado de acciones de terceros.
