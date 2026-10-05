# Actualizaciones agrupadas: Renovate (canon) y sintaxis Dependabot groups

Usar en Fase C de `operate-release`. El bot de version-updates de la flota es Renovate; Dependabot `version-updates` sigue prohibido. Este documento fija cómo agrupar en Renovate y deja la sintaxis `groups` de Dependabot solo como referencia de migración.

## Renovate agrupado (canon)

Base `.github/renovate.json` (recortar `packageRules` al stack del repo):

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "schedule": ["before 4am on monday"],
  "timezone": "Europe/Madrid",
  "labels": ["dependencies"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "matchManagers": ["npm", "pip_requirements", "cargo", "gomod", "github-actions"],
      "groupName": "minor + patch (CI verde)",
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "groupName": "major (revisión humana)",
      "automerge": false
    }
  ],
  "github-actions": {
    "pinDigests": true
  }
}
```

Reglas:

- Automerge solo `patch`+`minor` con CI verde; `major` siempre con revisión humana y sin automerge.
- Un grupo por riesgo, no un PR por dependencia: menos ruido, misma señal.
- Los pins de Actions se mantienen a SHA completo + comentario de versión (`pinDigests`).
- Prerrequisito humano: la GitHub App Renovate instalada en la org o habilitada en el repo; sin ella el JSON no genera PRs.
- Las alertas de seguridad de Dependabot pueden quedar activadas aunque `version-updates` esté eliminado.

## Sintaxis `groups` de Dependabot (solo referencia)

Si un repo aún tiene `.github/dependabot.yml` pendiente de migrar, sus grupos se leen así y se traducen a `packageRules` Renovate antes de eliminar el fichero:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      minor-patch:
        update-types:
          - "minor"
          - "patch"
```

Eliminar el bloque `version-updates` en el mismo PR que añade Renovate. No desactivar Dependabot Alerts.
