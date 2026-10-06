---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Fase 1. Comprender el producto antes de atacar"
permalink: /guia/01-preparacion/01-comprender-el-producto-antes-de-atacar/
order: 101
toc: true
comments: false
math: false
mermaid: true
---

# Fase 1. Comprender el producto antes de atacar

> **RESUMEN: Navegación**
> [Mapa principal]({{ site.baseurl }}/) · [Índice del bloque]({{ site.baseurl }}/guia/)

## Protocolo obligatorio de aplicabilidad

> **IMPORTANTE: No descartar por ausencia de explotación**
> Una prueba fallida no demuestra que la vulnerabilidad no aplique. El evaluador debe demostrar primero si existe la precondición técnica y después verificar el control.

Para cada familia o control de esta sección:

1. **Identificar la capacidad**: comprobar si el producto implementa el componente, flujo, parser, protocolo, intérprete, almacén, frontera de confianza o privilegio relacionado.
2. **Localizar la superficie**: enumerar endpoints, parámetros, mensajes, ficheros, jobs, interfaces, roles, tenants y dependencias que utilizan esa capacidad.
3. **Trazar entrada a destino**: determinar de dónde procede el dato, qué transformaciones recibe, qué componente toma la decisión y dónde termina.
4. **Revisar controles**: verificar validación, autorización, aislamiento, canonicalización, límites, integridad, configuración y logging en la capa que realmente ejecuta la acción.
5. **Diseñar casos**: preparar un caso positivo válido, un caso negativo, un caso de límite y, cuando proceda, comparación entre usuarios, roles o tenants.
6. **Probar de forma segura**: usar marcadores únicos y el mínimo impacto suficiente. Evitar datos reales, persistencia, agotamiento y acciones destructivas.
7. **Confirmar por dos señales**: por ejemplo, respuesta más cambio de estado; petición más log; diferencia de identidad más acceso al objeto.
8. **Clasificar y justificar** mediante uno de estos estados:
   - **Aplica, pendiente de prueba**: existe la precondición o superficie.
   - **Hallazgo**: el control puede eludirse y existe evidencia reproducible.
   - **Probado sin hallazgo**: la superficie existe, se cubrió una muestra definida y el control resistió.
   - **No aplica**: no existe la capacidad o precondición. Debe indicarse cómo se comprobó.
   - **Bloqueado**: no fue posible decidir por falta de acceso, información, entorno o por riesgo operativo.
9. **Registrar cobertura residual**: indicar endpoints no probados, roles ausentes, integraciones inaccesibles y diferencias respecto de producción.

### Evidencia mínima para descartar

Solo puede marcarse **No aplica** si queda registrada al menos una evidencia verificable, como arquitectura confirmada, configuración, inventario, revisión de código, especificación de API o entrevista técnica contrastada. La ausencia de un parámetro visible o el fallo de un payload no es evidencia suficiente.


---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false

## 1.1 Ficha del producto

- [ ] Propósito y procesos de negocio críticos.
- [ ] Tipos de usuarios, roles, organizaciones y tenants.
- [ ] Datos tratados: públicos, internos, personales, credenciales, financieros, salud, secretos.
- [ ] Canales: navegador, API, móvil, escritorio, CLI, webhooks, importaciones, correo.
- [ ] Arquitectura: frontend, gateway, backend, colas, bases de datos, almacenamiento, proveedores.
- [ ] Tecnologías y versiones confirmadas.
- [ ] Dependencias, plugins y servicios SaaS.
- [ ] Autenticación: local, LDAP, SAML, OAuth/OIDC, passkeys, certificados, API keys.
- [ ] Despliegue: on-premise, IaaS, PaaS, Kubernetes, serverless, CDN/WAF.
- [ ] Operaciones privilegiadas y procesos irreversibles.

## 1.2 Diagrama de flujo de datos y fronteras de confianza

Dibujar al menos:

1. Actores externos e internos.
2. Entradas y salidas.
3. Procesos y almacenes.
4. Servicios de terceros.
5. Fronteras entre Internet, edge, aplicación, administración, datos y cloud.
6. Flujos de secretos y tokens.

## 1.3 Modelado de amenazas

Aplicar STRIDE por componente:

- **S, suplantación**: robo de sesión, credenciales, tokens, identidad federada.
- **T, manipulación**: parámetros, objetos, archivos, mensajes, builds, webhooks.
- **R, repudio**: acciones sin trazabilidad o logs manipulables.
- **I, divulgación**: datos, errores, backups, metadatos, secretos.
- **D, denegación**: recursos caros, colas, regex, cargas, bloqueos.
- **E, elevación**: rol, tenant, plano de administración, host o cloud.

### Preguntas de negocio obligatorias

- [ ] ¿Qué acción produce dinero, crédito, privilegios o pérdida irreversible?
- [ ] ¿Qué operación confía en datos suministrados por el cliente?
- [ ] ¿Qué flujo requiere varias etapas y puede saltarse o repetirse?
- [ ] ¿Qué separación debe existir entre usuarios, organizaciones o regiones?
- [ ] ¿Qué callback, webhook o integración cambia el estado de una operación?
- [ ] ¿Qué sucede si dos peticiones válidas llegan simultáneamente?

### Puerta G1

No empezar fuzzing general hasta disponer de arquitectura, actores, activos críticos y fronteras de confianza. Sin ello se prueban payloads, no riesgos.

---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
