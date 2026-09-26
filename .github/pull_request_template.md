## Qué cambia y por qué

## Skills afectadas (bump de `metadata.version` si cambian instrucciones)

## Validación local

- [ ] `bash run-validation.sh` en verde
- [ ] `python3 tools/version/bump.py --check --auto --base origin/main` en verde
- [ ] CHANGELOG.md actualizado
- [ ] Sin trailing whitespace
- [ ] Sin residuos (`__pycache__/`, `.pytest_cache/`, `.archivado-*`)
- [ ] Tests añadidos/actualizados si scripts cambiaron
- [ ] Smoke test añadido/actualizado si scripts cambiaron
- [ ] Cuerpo < 500 líneas
