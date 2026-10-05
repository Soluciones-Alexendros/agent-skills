const fs = require("fs");
const path = require("path");

const SKILLS_DIR = path.join(
  "/home/alexendros/Aplicaciones/Fuentes/agent-skills",
  "skills"
);
const ISSUES = [];

function parseFrontmatter(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  const match = content.match(/^---[\s\S]*?^---$/m);
  if (!match) return null;
  const text = match[0];
  const lines = text.split("\n").slice(1, -1);
  const fm = {};
  for (const line of lines) {
    const colonIdx = line.indexOf(":");
    if (colonIdx === -1) continue;
    const key = line.substring(0, colonIdx).trim();
    const value = line.substring(colonIdx + 1).trim();
    fm[key] = value.replace(/^["]/, "").replace(/["]$/, "");
  }
  return fm;
}

function checkFrontmatter(fm, filePath) {
  if (!fm) {
    ISSUES.push(`${filePath}: Missing frontmatter`);
    return;
  }

  const required = ["name", "description", "license", "metadata"];
  for (const key of required) {
    if (!fm[key]) {
      ISSUES.push(`${filePath}: Missing frontmatter key '${key}'`);
    }
  }

  const metaRequired = ["author", "version", "domain", "type", "language"];
  for (const key of metaRequired) {
    if (!fm.metadata?.[key]) {
      ISSUES.push(`${filePath}: Missing metadata.key '${key}'`);
    }
  }

  if (fm.metadata && fm.metadata.language !== "en") {
    ISSUES.push(
      `${filePath}: language should be 'en', got '${fm.metadata.language}'`
    );
  }

  const validDomains = ["planning", "build", "verify", "operate", "design"];
  if (fm.metadata?.domain && !validDomains.includes(fm.metadata.domain)) {
    ISSUES.push(`${filePath}: Invalid domain '${fm.metadata.domain}'`);
  }

  const version = fm.metadata?.version;
  if (version) {
    const isReclassified =
      filePath.includes("build-design-system") ||
      filePath.includes("build-interface") ||
      filePath.includes("design-") ||
      filePath.includes("verify-") ||
      filePath.includes("operate-");
    const isNew = version === "1.0.0" && !isReclassified;
    const isTranslated =
      version === "2.0.0" || (version === "1.0.0" && isReclassified);

    if (isReclassified && version !== "2.0.0") {
      ISSUES.push(
        `${filePath}: Reclassified skill should have version '2.0.0', got '${version}'`
      );
    }
    if (isNew && version !== "1.0.0") {
      ISSUES.push(
        `${filePath}: New skill should have version '1.0.0', got '${version}'`
      );
    }
    if (isTranslated && parseFloat(version) < 2.0) {
      ISSUES.push(
        `${filePath}: Translated skill should have version >= 2.0, got '${version}'`
      );
    }
  }
}

function checkReferences(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  const matches = content.match(/\.\.\/\.\.\/references\/[^\s]+/g);
  if (matches) {
    const refDir = path.join(path.dirname(filePath), "references");
    if (!fs.existsSync(refDir)) {
      ISSUES.push(
        `${filePath}: Has reference paths but missing references/ directory`
      );
    }
  }
}

function checkSkillName(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  const nameMatch = content.match(/^name:[\s]*([^\s]+)/m);
  if (!nameMatch) {
    ISSUES.push(`${filePath}: Missing name in frontmatter`);
    return;
  }
  const name = nameMatch[1];
  const parts = name.split("-");
  if (parts.length < 2) {
    ISSUES.push(
      `${filePath}: Skill name '${name}' doesn't follow {domain}-{name} pattern`
    );
  }
}

const mdFiles = [];
function walkDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkDir(fullPath);
    } else if (entry.name.endsWith(".md")) {
      mdFiles.push(fullPath);
    }
  }
}

walkDir(SKILLS_DIR);

console.log(`Checking ${mdFiles.length} SKILL.md files...\n`);

for (const file of mdFiles) {
  checkFrontmatter(parseFrontmatter(file), file);
  checkReferences(file);
  checkSkillName(file);
}

console.log("===== ISSUES =====");
if (ISSUES.length === 0) {
  console.log("No issues found! All skills are valid.");
} else {
  for (const issue of ISSUES) {
    console.log(issue);
  }
}
console.log(`\nTotal issues: ${ISSUES.length}`);
