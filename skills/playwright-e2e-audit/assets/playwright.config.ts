import { defineConfig, devices } from '@playwright/test';

/**
 * Config de referencia para la auditoría E2E.
 * TARGET_URL se inyecta por entorno: TARGET_URL=https://ejemplo.com npx playwright test
 */
export default defineConfig({
  timeout: 60_000,
  retries: 1,
  use: {
    baseURL: process.env.TARGET_URL,
    // storageState: 'auth.json', // descomentar tras login de usuario_logueado
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    actionTimeout: 10_000,
    navigationTimeout: 30_000,
  },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 900 } } },
    { name: 'tablet', use: { ...devices['Desktop Chrome'], viewport: { width: 768, height: 1024 } } },
    { name: 'mobile', use: { ...devices['iPhone 13'], viewport: { width: 390, height: 844 } } },
  ],
  reporter: [['list'], ['html', { outputFolder: 'output/playwright-report' }]],
});
