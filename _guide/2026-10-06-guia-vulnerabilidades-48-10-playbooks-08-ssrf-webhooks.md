---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Playbook: SSRF, URLs, webhooks y redirecciones"
toc: true
permalink: /guia/10-playbooks/08-ssrf-webhooks/
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

El servidor obtiene URLs, valida webhooks, importa recursos, genera vistas previas, convierte documentos o conecta integraciones.

## Preparación

Usa exclusivamente un receptor controlado y autorizado. Registra DNS y HTTP sin apuntar a loopback, redes internas, metadata cloud o terceros.

```bash
curl -isk "$BASE_URL/preview?url=https%3A%2F%2Freceptor-control.example.invalid%2Fcanary-7f3a"
curl -iskG "$BASE_URL/redirect" --data-urlencode 'next=https://example.invalid/control'
```

## Pruebas

- Esquemas y puertos aceptados.
- Validación antes y después de redirects.
- Resolución DNS y conexión contra la IP validada.
- Normalización de host, IPv4, IPv6 y credenciales en URL.
- Segmentación, timeouts, tamaño y redirects máximos.
- Firma, replay e idempotencia de webhooks.
- Open redirect en login, logout, OAuth y correos.

## Detención

No consultes metadata, loopback, paneles internos ni servicios ajenos sin autorización explícita.

## Referencias locales

- `hacktricks/src/pentesting-web/open-redirect.md`
- `hacktricks/src/pentesting-web/ssrf-server-side-request-forgery/`
