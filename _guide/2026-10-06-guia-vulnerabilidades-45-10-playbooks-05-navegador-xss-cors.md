---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Playbook: navegador, XSS, CORS y clickjacking"
toc: true
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

La aplicación representa contenido controlable, emplea JavaScript, iframes, CORS, `postMessage`, service workers, WebSockets o almacenamiento local.

## Pruebas

- Traza cada entrada hasta su contexto: HTML, atributo, URL, JavaScript, CSS o plantilla.
- Empieza con la marca inerte `XSS-CONTROL-7F3A`.
- Revisa `innerHTML`, `document.write`, `eval` y construcción dinámica de URL.
- Comprueba CORS con origen no confiable y con o sin credenciales.
- Revisa CSP `frame-ancestors` y `X-Frame-Options`.
- Valida origen, tipo y estructura en `postMessage`.

```bash
curl -isk "$BASE_URL/api/me" -H 'Origin: https://origen-control.example.invalid'
curl -isk "$BASE_URL/" | grep -iE 'content-security-policy|x-frame-options|access-control-allow'
```

Usa una prueba de ejecución inocua solo cuando la reflexión y el contexto la justifiquen.

## Señales

Contenido interpretado en contexto ejecutable, CORS con credenciales para origen no confiable, framing de acciones sensibles o mensajes aceptados desde origen arbitrario.

## Referencias locales

- `hacktricks/src/pentesting-web/cors-bypass.md`
- `hacktricks/src/pentesting-web/clickjacking.md`
- `hacktricks/src/pentesting-web/client-side-template-injection-csti.md`
- `hacktricks/src/pentesting-web/websocket-attacks.md`
