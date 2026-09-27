# Release — canon repo-standard

### Propósito de este documento

- **Objetivos:** Fijar versionado, changelog, publicación y provenance (SLSA/sigstore) de la flota. Solo lectura: la ceremonia de cierre la ejecuta `operar-release` (Fases B y F).
- **Estructura:** Esta meta-sección → Esquema de versión → Changelog → Publicación → Provenance → Yank.
- **Contenido a integrar según contexto:** En un producto, elegir SemVer o CalVer una vez y no mezclarlos. Las notas de release salen siempre del changelog, nunca se redactan aparte.

## Esquema de versión

- Por defecto **SemVer 2.0.0** (`https://semver.org/spec/v2.0.0.html`): `MAJOR.MINOR.PATCH` con tags anotados `vX.Y.Z`.
- Si el repo ya es **CalVer**, no convertirlo: la versión es la fecha del esquema vigente y el changelog sigue siendo obligatorio. No derivar bumps SemVer de commits `feat`/`fix` en un repo CalVer.
- Coherencia verificada antes de publicar: último tag == sección del changelog == manifiesto real (`package.json`, `pyproject.toml`, `Cargo.toml`; en Go el tag es la versión del módulo). Un desfase en modo publicación es `BLOCK`. Sin manifiesto reconocible: `[PENDIENTE]`, no dar la coherencia por buena.
- Regla de bump (solo SemVer + Conventional Commits tras el último tag): `fix` → PATCH, `feat` → MINOR, `BREAKING CHANGE` o `type!:` → MAJOR. Revisar además diffs de API, firmas públicas y esquemas: un breaking no marcado bloquea la publicación.

## Changelog (Keep a Changelog 1.1.0)

Fuente: `https://keepachangelog.com/en/1.1.0/`. Plantilla en `operar-release/assets/CHANGELOG.md`.

- Una sección por release: `## [X.Y.Z] - AAAA-MM-DD`, la más reciente arriba, justo bajo `[Unreleased]`.
- Grupos canónicos: Added / Changed / Deprecated / Removed / Fixed / Security. Omitir grupos vacíos en una release real.
- Breaking: prefijo `**Breaking:**` al inicio de la entrada + bump MAJOR obligatorio.
- Enlaces de comparación al pie con owner y repo reales.
- `CHANGELOG.md` no lleva la meta-sección larga de otros markdown: un párrafo breve al inicio o ninguno.

## Publicación

1. Promover `[Unreleased]` al formato de la plantilla. El changelog es la fuente de las notas: extraer la sección exacta, no redactar notas que diverjan (ver `reusable-release.yml` / `assets/workflows/release.yml`).
2. Si la release viaja en PR: mergear ese PR con merge-watch (Fase F) **antes** del tag.
3. Tag anotado `vX.Y.Z` y `gh release create` solo tras sí explícito de esa acción. Nunca reutilizar un número publicado.
4. `gh release create "${GITHUB_REF_NAME}" --notes-file notes.md --verify-tag`, con notas extraídas del changelog y validadas como no vacías.
5. Idioma del informe: el del usuario. Labels, workflows, commits y nombres de checks, en inglés técnico.

## Provenance: SLSA, attestations, sigstore

- Exigibles solo en repo crítico (público con consumidores externos, despliega a producción) o si el usuario las pide. En el resto son aviso, no bloqueo.
- El job que atestigua lleva exactamente `id-token: write`, `contents: read` y `attestations: write` en ese job (no en el workflow entero) y usa `actions/attest-build-provenance` (o `actions/attest`) con SHA verificado. Separarlo del job con `contents: write` de la publicación cuando sea posible.
- En repos privados hace falta un plan que incluya attestations; si la API lo rechaza, es `N/A` justificado, no un SHA inventado.
- Firmas sigstore/cosign siguen la misma regla de proporcionalidad: solo en crítico o a petición.

## Yank y versiones retiradas

- Sección marcada `[YANKED]` con motivo: `## [X.Y.Z] - AAAA-MM-DD [YANKED]`. Nunca reutilizar ese número.
- Publicar sobre un número yanked o con sección yanked es `BLOCK`.
- Un breaking sin marcar en el changelog o sin bump MAJOR es `BLOCK` en modo publicación.
