---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Playbook: API REST, GraphQL, gRPC y SOAP"
toc: true
permalink: /guia/10-playbooks/06-api/
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

Existe una API directa, OpenAPI, GraphQL, gRPC, WSDL/SOAP, cliente móvil o interfaz que consuma servicios.

## Inventario inicial

```bash
curl -isk "$BASE_URL/openapi.json"
curl -isk "$BASE_URL/swagger.json"
curl -isk "$BASE_URL/graphql" -H 'Content-Type: application/json'   --data '{"query":"query { __typename }"}'
```

No asumas que la documentación enumera todas las rutas. Compara tráfico del cliente, versiones, métodos y hosts.

## Pruebas

- Autenticación y autorización por operación, objeto y campo.
- Métodos alternativos, content types y versiones.
- Mass assignment y campos de solo lectura.
- Paginación, filtros, búsquedas, exportación y límites.
- GraphQL: autorización en resolvers, aliases, batching, profundidad y coste.
- gRPC: metadatos, reflexión, método y mensajes inesperados.
- SOAP: SOAPAction, esquemas, XXE y autorización por operación.

## Señales

Operación no documentada accesible, campo sensible expuesto, límites eludibles o autorización diferente entre transportes.

## Referencias locales

- `hacktricks/src/pentesting-web/grpc-web-pentest.md`
- `hacktricks/src/pentesting-web/json-xml-yaml-hacking.md`
- `hacktricks/src/pentesting-web/soap-jax-ws-threadlocal-auth-bypass.md`
