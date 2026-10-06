---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Playbook: HTTP, proxies, caché y desync"
toc: true
permalink: /guia/10-playbooks/11-http-proxy-cache/
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

Hay CDN, balanceador, reverse proxy, WAF, caché, gateway, HTTP/2 o múltiples capas de parsing.

## Pruebas iniciales

```bash
curl -isk "$BASE_URL/" -H 'Cache-Control: no-cache'
curl -isk "$BASE_URL/" -H 'X-Forwarded-Host: control.example.invalid'
curl -isk "$BASE_URL/" -H 'X-Original-URL: /control-nonexistent'
```

Observa `Age`, `Vary`, claves de caché, host reflejado, enlaces, redirects y diferencias entre frontend y backend.

## Cobertura

- Cache poisoning y cache deception con contenido inocuo.
- Cabeceras hop-by-hop y de reescritura.
- Host header en recuperación y enlaces.
- Normalización divergente de rutas y encoding.
- Request smuggling o desync solo en ventana autorizada.

## Detención

No pruebes desync contra producción compartida sin autorización específica. Puede afectar solicitudes de terceros.

## Referencias locales

- `hacktricks/src/pentesting-web/abusing-hop-by-hop-headers.md`
- `hacktricks/src/pentesting-web/http-connection-request-smuggling.md`
- `hacktricks/src/pentesting-web/http-response-smuggling-desync.md`
