---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Playbooks operativos"
toc: true
permalink: /guia/10-playbooks/00-indice/
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

- [Autenticación, recuperación y MFA]({{ '/guia/10-playbooks/01-autenticacion-recuperacion-mfa/' | relative_url }})
- [Sesiones, cookies, JWT y CSRF]({{ '/guia/10-playbooks/02-sesiones-cookies-jwt-csrf/' | relative_url }})
- [Autorización, IDOR y multitenancy]({{ '/guia/10-playbooks/03-autorizacion-idor-multitenancy/' | relative_url }})
- [Inyecciones del servidor]({{ '/guia/10-playbooks/04-inyecciones-servidor/' | relative_url }})
- [Navegador, XSS, CORS y clickjacking]({{ '/guia/10-playbooks/05-navegador-xss-cors/' | relative_url }})
- [API REST, GraphQL, gRPC y SOAP]({{ '/guia/10-playbooks/06-api/' | relative_url }})
- [Archivos, rutas y subidas]({{ '/guia/10-playbooks/07-archivos-rutas/' | relative_url }})
- [SSRF, URLs, webhooks y redirecciones]({{ '/guia/10-playbooks/08-ssrf-webhooks/' | relative_url }})
- [Lógica de negocio, concurrencia y límites]({{ '/guia/10-playbooks/09-logica-race-rate-limit/' | relative_url }})
- [OAuth, OIDC, SAML y SSO]({{ '/guia/10-playbooks/10-oauth-oidc-saml/' | relative_url }})
- [HTTP, proxies, caché y desync]({{ '/guia/10-playbooks/11-http-proxy-cache/' | relative_url }})
- [Red, servicios, cloud y contenedores]({{ '/guia/10-playbooks/12-red-cloud-contenedores/' | relative_url }})
- [Dependencias, secretos y CI/CD]({{ '/guia/10-playbooks/13-dependencias-cicd/' | relative_url }})
- [Móvil, escritorio y extensiones]({{ '/guia/10-playbooks/14-clientes/' | relative_url }})
- [LLM, RAG, MCP y agentes]({{ '/guia/10-playbooks/15-llm-rag-agentes/' | relative_url }})
