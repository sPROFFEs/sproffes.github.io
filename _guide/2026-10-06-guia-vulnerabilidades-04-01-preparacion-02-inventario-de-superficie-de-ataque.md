---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Fase 2. Inventario de superficie de ataque"
permalink: /guia/01-preparacion/02-inventario-de-superficie-de-ataque/
order: 102
toc: true
comments: false
math: false
mermaid: true
---

# Fase 2. Inventario de superficie de ataque

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

## 2.1 Descubrimiento pasivo

- [ ] Dominios, subdominios, ASN/IP autorizadas y certificados.
- [ ] DNS: A/AAAA, CNAME, MX, TXT, NS, CAA y delegaciones.
- [ ] Tecnologías expuestas en headers, HTML, JavaScript, iconos y errores.
- [ ] Repositorios, paquetes, documentación, Swagger/OpenAPI, GraphQL y SDK públicos.
- [ ] Historial de endpoints, archivos y subdominios retirados.
- [ ] Secretos o configuraciones publicados accidentalmente.
- [ ] Dependencias de terceros y riesgo de subdomain takeover.

## 2.2 Descubrimiento activo controlado

- [ ] Hosts, puertos y protocolos autorizados.
- [ ] Virtual hosts, redirects, aliases y rutas base.
- [ ] Directorios, ficheros, backups, source maps y endpoints ocultos.
- [ ] Métodos HTTP y tipos de contenido aceptados.
- [ ] Parámetros en URL, body, JSON, XML, multipart, cookies y headers.
- [ ] WebSockets, SSE, gRPC, webhooks y canales asíncronos.
- [ ] Paneles de administración, health, metrics, debug y observabilidad.
- [ ] Funciones accesibles tras autenticación por cada rol.

## 2.3 Matriz de superficie

| ID | Componente | Entrada | Actor mínimo | Datos | Frontera | Tecnología | Criticidad | Módulos aplicables |
|---|---|---|---|---|---|---|---|---|
| SURF-001 | Ejemplo API pagos | `POST /api/payments` | usuario | financiero | Internet → API | REST/JSON | crítica | authz, lógica, race, inyección |

### Puerta G2

Cada endpoint o función crítica debe tener actor, dato, frontera y módulos de prueba asociados. Lo no inventariado no puede considerarse cubierto.

---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
