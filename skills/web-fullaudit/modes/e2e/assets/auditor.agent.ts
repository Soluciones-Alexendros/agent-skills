// Auditor Agent v2.1 — Loop autónomo de referencia (recolectar → pensar → actuar)
// Endurecido sobre la versión original: captura de red, evidencias con screenshot,
// formularios triple pasada y límites de seguridad (no seguir logout ni submits reales).
import { Page, Locator } from '@playwright/test';
import * as fs from 'fs';

export interface CheckEntry {
  id: string; url: string; category: string; check: string;
  method: string; status: 'PASS' | 'FAIL' | 'WARN' | 'N/A';
  severity: 'Crítica' | 'Alta' | 'Media' | 'Baja';
  evidence: { locator?: string; screenshot?: string; console?: string[]; network?: string[] };
  recommendation?: string; wcag_ref?: string;
}

const EVIDENCE_DIR = 'output/evidence';

export async function auditPage(page: Page, url: string, checklist: CheckEntry[]) {
  fs.mkdirSync(EVIDENCE_DIR, { recursive: true });
  const consoleErrors: string[] = [];
  const failedRequests: string[] = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 200)); });
  page.on('pageerror', e => consoleErrors.push('PAGEERROR: ' + e.message.slice(0, 200)));
  page.on('response', r => { if (r.status() >= 400) failedRequests.push(`${r.status()} ${r.url()}`); });

  await page.goto(url, { waitUntil: 'networkidle' });

  // 1. RECOLECTAR: snapshot accesible + mediciones (assets/measure.js)
  const ariaSnapshot = await page.locator('body').ariaSnapshot();
  const measureSnippet = fs.readFileSync('assets/measure.js', 'utf-8');
  const measurements = await page.evaluate(measureSnippet);

  // 2. FUNCIONAL: click en todo lo clicable visible (con self-healing)
  const clickables = await page
    .getByRole('button').or(page.getByRole('link')).or(page.getByRole('combobox')).all();
  for (const el of clickables.slice(0, 60)) {
    const desc = await safeDescribe(el);
    try {
      if (!(await el.isVisible())) continue;
      await el.click({ timeout: 3000, trial: true }); // trial: no ejecuta, verifica accionabilidad
      checklist.push({ id: 'FN-01', url, category: 'Funcional', check: `Elemento accionable: ${desc}`,
        method: 'trial-click', status: 'PASS', severity: 'Crítica',
        evidence: { locator: desc } });
    } catch {
      const shot = `${EVIDENCE_DIR}/fn01-${Date.now()}.png`;
      await el.screenshot({ path: shot }).catch(() => {});
      checklist.push({ id: 'FN-01', url, category: 'Funcional', check: `Elemento no accionable: ${desc}`,
        method: 'trial-click', status: 'FAIL', severity: 'Crítica',
        evidence: { locator: desc, screenshot: shot, console: consoleErrors },
        recommendation: 'Revisar handler, overlay que intercepta el click o estado deshabilitado' });
    }
  }

  // 3. FORMULARIOS: triple pasada (vacío → inválido → válido con datos contextuales)
  for (const form of await page.locator('form').all()) {
    await auditForm(page, form, url, checklist);
  }

  // 4. RED: requests fallidos
  if (failedRequests.length) {
    checklist.push({ id: 'FN-02', url, category: 'Funcional', check: 'Requests >=400 durante navegación',
      method: "page.on('response')", status: 'FAIL', severity: 'Alta',
      evidence: { network: failedRequests.slice(0, 10) },
      recommendation: 'Corregir endpoints/recursos rotos' });
  }

  return { measurements, consoleErrors, failedRequests, ariaSnapshot };
}

async function auditForm(page: Page, form: Locator, url: string, checklist: CheckEntry[]) {
  const desc = (await form.getAttribute('aria-label')) || (await form.getAttribute('id')) || 'form';
  // Pasada A: vacío — debe mostrar validación visible
  const submit = form.getByRole('button', { name: /enviar|submit|continuar|registrar|comprar/i }).first();
  if (await submit.count()) {
    await submit.click({ timeout: 3000 }).catch(() => {});
    const invalid = await form.locator('[aria-invalid="true"], :invalid').count();
    checklist.push({ id: 'FM-01', url, category: 'Formularios',
      check: `Validación visible en submit vacío (${desc})`, method: 'triple-pasada/A',
      status: invalid > 0 ? 'PASS' : 'FAIL', severity: 'Crítica',
      evidence: { locator: `form#${desc}` }, wcag_ref: '3.3.1',
      recommendation: 'Mostrar errores en texto asociados con aria-describedby' });
  }
  // Pasadas B/C requieren datos contextuales (faker + LLM) y cuidado:
  // nunca ejecutar submits con efectos reales (pagos, emails) en producción.
}

async function safeDescribe(el: Locator): Promise<string> {
  try {
    const role = await el.getAttribute('role');
    const text = (await el.innerText({ timeout: 500 })).slice(0, 40);
    const testid = await el.getAttribute('data-testid');
    return `${role || 'elemento'} "${text.trim()}"${testid ? ` [testid=${testid}]` : ''}`;
  } catch {
    return 'elemento sin describir';
  }
}
