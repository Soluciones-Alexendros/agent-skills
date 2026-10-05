# hardening-baseline.md — STUB (legado)

> Baseline canónico: ../operate-security/references/hardening-baseline.md

Este fichero es un stub. El baseline activo de hardening (servidor completo
CIS Nivel 1/2/3 + controles de escritorio, niveles R1/R2 y rollback) vive en
`operate-security`. Esta skill **no** verifica hardening puro
(SSH/KR/FS-05–08/AU/UA/CR): eso lo evalúa `operate-security`
(`harden_plan.py`, `postura_seguridad.sh`).

## Subconjunto de higiene verificado por esta skill

`audit_quick.py` / `audit_full.py` solo verifican estos controles
(ver `references/audit-checklist.md` para el detalle de cada ID):

| ID     | Control                                                     | Criticidad | Dónde       |
| ------ | ----------------------------------------------------------- | ---------- | ----------- |
| PKG-01 | Actualizaciones de seguridad pendientes                     | P1         | quick, full |
| PKG-03 | Kernel running vs installed (reboot pendiente)              | P1         | quick, full |
| PKG-04 | Firmware actualizable (fwupd)                               | P2         | full        |
| PKG-05 | Paquetes huérfanos                                          | P3         | quick, full |
| PKG-06 | Paquetes foráneos (AUR/manuales)                            | P3         | full        |
| PKG-07 | Configs pendientes (.pacnew/.dpkg-new/.rpmnew, pacdiff/ucf) | P2         | quick, full |
| PKG-09 | Tamaño de caché de paquetes                                 | P4         | full        |
| ARC-07 | Sin actualizaciones parciales (Arch)                        | P1         | full        |
| DEB-04 | unattended-upgrades activo (Debian/Ubuntu)                  | P2         | full        |
| FS-09  | Symlinks rotos en /etc, /usr, /boot                         | P3         | full        |
| FS-10  | Uso de disco crítico (≥ 80/90%)                             | P1/P2      | quick, full |
| FS-11  | Uso de inodos (≥ 80/90%)                                    | P2/P3      | full        |
| LOG-06 | Errores en journal 24h (prioridad 0–3)                      | P2–P4      | quick, full |
| LOG-08 | Fallos de arranque (`journalctl -b`)                        | P2–P4      | full        |
| SRV-02 | Servicios systemd fallidos                                  | P1         | quick, full |
| NET-04 | SSH expuesto en todas las interfaces                        | P0         | quick, full |

Todo lo demás (SSH-_, KR-_, FS-05–08, AU-_, UA-_, CR-_, FW-_, SD-*) → baseline canónico.
