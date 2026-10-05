// Canon repo-standard — configuración commitlint (conventional-commits).
// Solo lectura: copiar al producto y adaptar `scopes` si el dominio lo exige.
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      ["feat", "fix", "docs", "chore", "refactor", "test", "ci", "revert"],
    ],
    "subject-case": [
      2,
      "never",
      ["sentence-case", "start-case", "pascal-case", "upper-case"],
    ],
    "header-max-length": [2, "always", 100],
  },
};
