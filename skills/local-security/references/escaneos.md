# Escaneos — uso correcto y trampas

## ClamAV (antivirus de firmas)

```bash
systemctl status clamav-daemon clamav-freshclam   # firmas al día es lo esencial
freshclam --stdout | tail -1                      # versión de base de firmas
clamscan -r -i --exclude-dir='^/proc|^/sys' /home/usuario/Directorio
```
- `-i` muestra solo infectados; sin él el log es inmanejable.
- PUA (possibly unwanted apps) dan falsos positivos en herramientas de red/admin: validar antes de cuarentena.

## rkhunter (rootkits)

```bash
rkhunter --check --sk --rwo          # solo warnings
rkhunter --propupd                   # OBLIGATORIO tras cada upgrade de paquetes
```
- Sus "warnings" tras un upgrade son casi siempre binarios cambiados legítimamente: `--propupd` los resetea. Sin propupd, rkhunter llora cada día.
- No ejecutar `--propupd` sin saber que el sistema está sano (consolidaría un compromiso).

## AIDE (integridad de ficheros)

```bash
systemctl list-timers --all | grep aide          # dailyaidecheck.timer diario ~02:29
aide --check --config=/etc/aide/aide.conf | grep -A20 'Changed entries'
aideinit                                          # regenerar DB (pregunta overwrite; validar sistema sano antes)
```
- La DB vive en `/var/lib/aide/aide.db` (gzip; inspección con `zgrep`).
- Regla de oro: **todo cambio reportado debe tener explicación** (paquete actualizado, edición propia documentada). Un cambio sin explicación = P0 hasta demostrar lo contrario.
- Ruido conocido a excluir mentalmente: `/swap.img`, `~/.config` (apps escribiendo), mtimes de directorios con sockets (`~/.gnupg`).

## debsums (integridad de paquetes)

```bash
debsums -s    # solo discrepancias contra los hashes del paquete
```
Binarios de paquetes modificados localmente aparecen aquí: distinguir "yo lo edité" de "alguien lo editó".

## Lynis (auditoría CIS)

```bash
lynis audit system --quick    # sin pausa interactiva
```
Salida a `/var/log/lynis.log` + report.dat. Sus "suggestions" no son hallazgos: filtrar por lo aplicable al contexto (escritorio vs servidor).

## Regla transversal

Todo escáner produce candidatos, no veredictos. La entrega al usuario separa: **validados** (confirmados por segunda vía) / **descartados** (con el motivo) / **indeterminados** (qué falta para decidir).
