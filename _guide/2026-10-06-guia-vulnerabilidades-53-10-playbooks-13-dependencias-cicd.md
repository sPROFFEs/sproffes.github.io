---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Playbook: dependencias, secretos y CI/CD"
toc: true
permalink: /guia/10-playbooks/13-dependencias-cicd/
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

Hay repositorios, paquetes, artefactos, pipelines, registries, plugins, actualizadores o infraestructura como código.

## Inventario seguro

```bash
find . -maxdepth 4 -type f \( -name 'package-lock.json' -o -name 'requirements.txt'   -o -name 'pom.xml' -o -name 'go.sum' -o -name 'Dockerfile' \) -print
git log --oneline -n 20
```

## Pruebas

- Dependencias directas, transitivas, fuentes y bloqueo.
- Nombres internos susceptibles a dependency confusion.
- Firmas, checksums y promoción de artefactos.
- Secretos en código, historial, logs, imágenes y artefactos.
- Permisos de runners, tokens, forks y entornos protegidos.
- Scripts de instalación y acciones fijadas por commit o digest.
- Actualización y rollback autenticados.

No publiques paquetes señuelo en registros públicos ni actives pipelines ajenos. Valida dependency confusion por configuración o en un registro privado de laboratorio.

## Referencias locales

- `hacktricks/src/pentesting-web/dependency-confusion.md`
- `owasp-top10/docs/es/A03_2025-Software_Supply_Chain_Failures.md`
- `owasp-top10/docs/es/A08_2025-Software_or_Data_Integrity_Failures.md`
