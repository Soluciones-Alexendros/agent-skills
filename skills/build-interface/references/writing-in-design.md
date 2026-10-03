# Copy como Material de Diseño (Writing in Design)

## Principios Fundamentales

### 1. Escribe desde el Lado del Usuario
- **Nombra por lo que la gente controla**, no por cómo está construido el sistema
- ❌ "Webhook configuration" → ✅ "Manage notifications"
- ❌ "Database settings" → ✅ "Data & storage"
- ❌ "API endpoints" → ✅ "Integrations"

### 2. Describe Qué Hace, No Lo Vendas
- ❌ "Streamline your workflow with our powerful automation"
- ✅ "Automate repetitive tasks"
- ❌ "Unlock the full potential of your data"
- ✅ "Export your data to CSV, JSON, or Excel"

### 3. Voz Activa por Defecto
- ❌ "Your request has been processed"
- ✅ "We processed your request"
- ❌ "Changes will be saved"
- ✅ "Save changes"

### 4. Consistencia de Vocabulario
Una acción = un nombre en todo el flujo:
- Botón: "Publish" → Toast: "Published" → Email subject: "Your post was published"
- Botón: "Save" → Toast: "Saved" → Confirmación: "Save changes?"
- Botón: "Delete" → Modal: "Delete permanently?" → Toast: "Deleted"

### 5. Sentence Case, Sin Relleno
- ✅ "Save changes"
- ✅ "Delete account"
- ✅ "Copy link"
- ❌ "Save Changes"
- ❌ "Delete Account Permanently"
- ❌ "Click Here to Copy Link"

## Estados de Error y Vacío (Error & Empty States)

### Errores: Qué pasó + Cómo arreglar
```tsx
// ❌ MALO
"Error 500: Something went wrong"

// ✅ BUENO
"Couldn't save your changes. The server timed out. Try again in a moment."
// O para validación:
"Email invalid. Format: name@domain.com"
```

### Pantallas Vacías: Invitación a Actuar
```tsx
// ❌ MALO
"No data found"

// ✅ BUENO
"No projects yet. Create your first project to get started."
[Create Project] [Import from GitHub]
```

## Microcopy Patterns

### Botones (Buttons)
| Acción | Texto | Contexto |
|--------|-------|----------|
| Primaria | Save / Create / Publish / Continue | Acción principal |
| Secundaria | Cancel / Skip / Maybe later | Alternativa |
| Destructiva | Delete / Remove / Leave | Irreversible |
| Ghost | View details / Learn more | Navegación suave |

### Formularios (Forms)
```tsx
// Labels: Sustantivo, sentence case
<label htmlFor="email">Email address</label>

// Placeholders: Ejemplo, no instrucción
<input placeholder="name@company.com" />

// Help text: Contexto, no regla
<span id="password-hint">At least 8 characters</span>

// Error: Qué + cómo arreglar
<span role="alert">Password too short. Minimum 8 characters.</span>
```

### Navegación (Navigation)
```tsx
// Breadcrumbs: Ubicación actual
Home / Projects / "Project Alpha" / Settings

// Tabs: Sustantivo plural o categoría
Projects / Team / Settings / Billing

// Pagination: Contexto
Showing 1-20 of 147 results
Previous / 1 / 2 / 3 / Next
```

## Tonality (Tono)

### Por Contexto
| Contexto | Tono | Ejemplo |
|----------|------|---------|
| Onboarding | Amable, alentador | "Welcome! Let's set up your workspace." |
| Error crítico | Directo, útil | "We couldn't connect. Check your internet." |
| Confirmación destructiva | Serio, claro | "This will permanently delete 47 files." |
| Éxito | Breve, satisfactorio | "Published! Your changes are live." |
| Empty state | Invitador | "No messages yet. Start a conversation." |

### Evitar
- ❌ "Oops!" / "Whoops!" (infantil)
- ❌ "Successfully..." (redundante)
- ❌ "Please note that..." (relleno)
- ❌ "In order to..." → "To"
- ❌ "Should you have any questions..." → "Questions? Contact us."

## Checklist de Copy
- [ ] Cada botón usa voz activa
- [ ] Vocabulario consistente en todo el flujo
- [ ] Errores explican qué pasó + cómo arreglar
- [ ] Empty states invitan a actuar
- [ ] Sentence case en todo (no Title Case)
- [ ] Sin "please", "kindly", "oops", "successfully"
- [ ] Tono apropiado al contexto