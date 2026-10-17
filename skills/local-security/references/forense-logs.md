# Forense ligero de registros — cookbook

Objetivo: reconstruir "quién hizo qué, cuándo y con qué resultado" sin herramientas de IR pesadas.

## Fuentes y para qué sirve cada una

| Fuente | Contenido | Acceso |
|---|---|---|
| `journalctl` | servicios, sudo, systemd | usuario (adm) |
| `/var/log/audit/audit.log` + `ausearch` | AVC/AppArmor, vigilancias -w, syscalls regladas | root/adm |
| `/var/log/auth.log` | SSH, sudo, PAM | adm |
| `/var/log/apparmor/denials.log` | denegaciones MAC cosechadas a diario | root |
| `~/.bash_history`, `last`, `lastlog` | actividad de cuentas | adm |

## Recetas frecuentes

### Autenticación sospechosa
```bash
journalctl _COMM=sshd --since "24 hours ago" | grep -iE 'failed|accepted'
last -f /var/log/wtmp | head -20
ausearch -m USER_LOGIN -ts today 2>/dev/null | grep -v success
```

### Uso de sudo/privilegios
```bash
journalctl _COMM=sudo --since today | grep -E 'COMMAND|user'
ausearch -m USER_START -ts today | grep 'op=PAM:session_open'
```

### Denegaciones AppArmor (auditd intercepta: SIEMPRE ausearch, no journalctl -k)
```bash
ausearch -m avc -ts today | grep 'apparmor="DENIED"' | grep -oP 'profile="[^"]+"' | sort | uniq -c | sort -rn
ausearch -m avc -ts recent | tail -20        # lo último, con contexto
```
Tormentas: un mismo perfil con miles de eventos en minutos = perfil roto, no ataque. Ver playbook §8.

### Vigilancia de rutas concretas (auditd -w)
```bash
auditctl -l                                   # claves disponibles
ausearch -k terminal_canon -ts today          # actividad sobre ~/Terminal
ausearch -k identity -ts today                # /etc/passwd, shadow, group...
```

### Cronología de un PID o binario
```bash
ausearch -p <pid> -ts today
journalctl _PID=<pid> --since today
```

## Reglas de interpretación

1. **Hora del sistema primero**: `timedatectl` — un reloj roto invalida toda cronología.
2. **Distinguir ruido de señal**: rotaciones de log, timers systemd y maintainers de paquetes generan eventos legítimos masivos. Filtrar por lo que CAMBIA respecto al patrón.
3. **Nunca concluir "intrusión" con un solo evento**: buscar la cadena (login → sudo → proceso → escritura).
4. **Guardar evidencia**: copiar los extractos relevantes a un fichero con timestamp antes de remediar nada.
