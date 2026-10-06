---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Playbooks operativos"
toc: true
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

# Playbooks operativos

Esta sección convierte la metodología en comprobaciones cortas, reproducibles y de bajo impacto. Los playbooks se utilizan después del motor de aplicabilidad, nunca como una lista de payloads ejecutada a ciegas.

## Flujo obligatorio

1. Confirmar alcance, ventana y activos autorizados.
2. Activar una familia solo si existe su precondición técnica.
3. Preparar actores, objetos, estados y datos sintéticos.
4. Capturar una petición legítima de control.
5. Modificar una sola variable cada vez.
6. Comparar código, cuerpo, tamaño, tiempo y efecto persistente.
7. Confirmar cualquier anomalía mediante una segunda señal.
8. Detener la prueba al demostrar el impacto mínimo.
9. Registrar resultado, evidencia, limitaciones y cobertura residual.

## Variables recomendadas

```bash
export BASE_URL='https://producto.example'
export TARGET='producto.example'
export TOKEN_A='token-de-prueba-a'
export TOKEN_B='token-de-prueba-b'
export ID_A='objeto-controlado-a'
export ID_B='objeto-controlado-b'
```

## Índice

- [Autenticación, recuperación y MFA]({% post_url 2026-02-11-10-playbooks-01-autenticacion-recuperacion-mfa %})
- [Sesiones, cookies, JWT y CSRF]({% post_url 2026-02-12-10-playbooks-02-sesiones-cookies-jwt-csrf %})
- [Autorización, IDOR y multitenancy]({% post_url 2026-02-13-10-playbooks-03-autorizacion-idor-multitenancy %})
- [Inyecciones del servidor]({% post_url 2026-02-14-10-playbooks-04-inyecciones-servidor %})
- [Navegador, XSS, CORS y clickjacking]({% post_url 2026-02-15-10-playbooks-05-navegador-xss-cors %})
- [API REST, GraphQL, gRPC y SOAP]({% post_url 2026-02-16-10-playbooks-06-api %})
- [Archivos, rutas y subidas]({% post_url 2026-02-17-10-playbooks-07-archivos-rutas %})
- [SSRF, URLs, webhooks y redirecciones]({% post_url 2026-02-18-10-playbooks-08-ssrf-webhooks %})
- [Lógica de negocio, concurrencia y límites]({% post_url 2026-02-19-10-playbooks-09-logica-race-rate-limit %})
- [OAuth, OIDC, SAML y SSO]({% post_url 2026-02-20-10-playbooks-10-oauth-oidc-saml %})
- [HTTP, proxies, caché y desync]({% post_url 2026-02-21-10-playbooks-11-http-proxy-cache %})
- [Red, servicios, cloud y contenedores]({% post_url 2026-02-22-10-playbooks-12-red-cloud-contenedores %})
- [Dependencias, secretos y CI/CD]({% post_url 2026-02-23-10-playbooks-13-dependencias-cicd %})
- [Móvil, escritorio y extensiones]({% post_url 2026-02-24-10-playbooks-14-clientes %})
- [LLM, RAG, MCP y agentes]({% post_url 2026-02-25-10-playbooks-15-llm-rag-agentes %})
