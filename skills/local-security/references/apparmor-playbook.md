# AppArmor playbook — lecciones de trabajo real (Ubuntu 26.04, kernel 7.0)

Leer ANTES de tocar perfiles. Todo aquí está verificado en batalla, no en documentación.

## 1. `aa-enforce /etc/apparmor.d/*` reescribe los archivos

`aa-enforce`/`aa-complain` editan el archivo del perfil y **eliminan `flags=(unconfined)`** de la cabecera. Ubuntu 26.04 usa ese flag en ~90 perfiles "allows everything" (brave, firefox, thunderbird, Discord, Electron en general) cuyo único propósito es dar nombre al proceso y conceder `userns`. Un enforce masivo los convierte en default-deny con solo `userns,` → apps rotas al instante.

- Antes de un enforce masivo, guardar baseline (`aa-status`) y, tras él, verificar que los perfiles con comentario *"This profile allows everything"* conservan su flag; restaurar con sed si hace falta.
- Ojo a perfiles que ya tienen otros flags (sbuild: `attach_disconnected, mediate_deleted`): añadir un segundo `flags=()` es error de sintaxis.

## 2. Semántica de deny que NO es la que esperas

- **`deny` sin `audit` no se loguea** (al menos con regla allow coexistente en este kernel). Para credenciales usar `audit deny` — bloquea Y audita.
- **En modo complain los deny NO bloquean**: complain permite todo y solo loguea (incluidos los deny). La protección de credenciales solo es efectiva al pasar a enforce. No vender el soak como protección activa.

## 3. auditd secuestra el canal

Con auditd instalado, los eventos AppArmor van a `/var/log/audit/audit.log` y **journalctl -k queda ciego**. Recolectores y `aa-notify` deben leer de audit.log (aa-notify lo hace por defecto). `ausearch -m avc -ts recent` es la herramienta.

## 4. aa-notify: demonio correcto

- Sale limpio sin `-m` (modo merge con backoff exponencial) y se daemoniza sin `-F`.
- Unidad systemd de usuario correcta: `ExecStart=/usr/bin/aa-notify -p -m -F --display :0`. El paquete trae autostart XDG de "una pasada al login"; para vigilancia continua hace falta la unidad.

## 5. Attachments y rutas

- Los binarios symlink resuelven al destino real: perfilar la **ruta resuelta** (p. ej. `/usr/bin/head` → `/usr/lib/cargo/bin/coreutils/head` en uutils). Verificar con `readlink -f`.
- Espacios en rutas: el parser de kernel acepta `"/opt/Command Code/x"` en la cabecera pero NO en reglas; la toolchain perl (aa-logprof) rechaza el escape `\ `. Solución compatible con ambos: glob `?` → `/opt/Command?Code/**`.
- AppImages: el binario real vive en `/tmp/.mount_<nombre>*/...`. Attachment con glob funciona: `profile app "/tmp/.mount_*/usr/share/cursor/cursor"`. El ejecutable que pide userns suele ser el binario principal, no chrome-sandbox — mirar el `comm=` del DENIED.

## 6. Hijes de procesos perfilados

Por defecto, un hijo sin perfil genera subperfiles `null-` (ruido masivo en aa-status; se limpian al reiniciar). Para CLIs de agentes que deben lanzar herramientas sin confinar (diseño: confinar el agente, no los intérpretes): `/** ux,`. OJO: entra en conflicto con reglas exec de `abstractions/base` y con el `mr` propio ("merged rule with conflicting x modifiers") — en perfiles mínimos de soak, quitar esas reglas y dejar solo `userns,` + `/** ux,` + denies.

## 7. flags=(unconfined) en kernel nuevo

En kernels recientes el "true unconfined" se emula como default_allow: permite todo, mantiene reglas deny efectivas y concede `userns`. Es el mecanismo oficial para que Electron funcione con `kernel.apparmor_restrict_unprivileged_userns=1`. NO bajar el sysctl a 0 como atajo.

## 8. Tormentas de denegaciones

Un perfil de fábrica incompleto (caso real: vivaldi) puede generar 40k+ denegaciones/min, saturar el backlog de audit (`audit_lost`), rotar audit.log cada minuto y enterrar los eventos legítimos. Respuesta: `aa-disable` inmediato (vuelta al estado efectivo previo) y perfil dedicado con `aa-genprof` en sesión aparte. Nunca dejar una tormenta en complain "para el soak": en complain loguea todo igualmente.

## 9. Verificación de que un perfil adjunta

- `cat /proc/<pid>/attr/current` en un proceso longevo.
- Sin proceso longevo: `aa-exec --profile='<nombre>' -- cat /proc/self/attr/current`.
- Denegación de prueba rápida: perfil temporal sobre un binario concreto con `audit deny` a un fichero legible → EACCES en un fichero world-readable solo puede venir del MAC.

## 10. Ciclo correcto para agentes CLI

genprof/autodep → complain → **soak de días de uso real** → `aa-logprof` → enforce. Con `audit deny` de credenciales desde el día 1 (se activan solas al enforce). La toolchain perl (logprof) debe poder parsear el archivo: validar antes con `echo F | aa-logprof` y comprobar que no dice "skipping unparseable".
