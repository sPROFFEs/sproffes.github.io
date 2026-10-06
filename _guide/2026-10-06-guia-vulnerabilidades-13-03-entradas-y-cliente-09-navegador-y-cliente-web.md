---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Fase 9. Navegador y cliente web"
permalink: /guia/03-entradas-y-cliente/09-navegador-y-cliente-web/
order: 309
toc: true
comments: false
math: false
mermaid: true
---

# Fase 9. Navegador y cliente web

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

- [ ] XSS por contexto y recorridos source-to-sink.
- [ ] DOM clobbering y prototype pollution cuando el JavaScript lo permita.
- [ ] CSP efectiva, no solo presente.
- [ ] Clickjacking en acciones sensibles.
- [ ] CSRF en toda operación con credenciales automáticas.
- [ ] CORS con orígenes reflejados, null, subdominios y credenciales.
- [ ] postMessage: origin exacto, source, formato y datos sensibles.
- [ ] Open redirect y su encadenamiento con OAuth, SSO o phishing.
- [ ] Reverse tabnabbing y enlaces externos.
- [ ] Service workers: alcance, cache, actualización y registro.
- [ ] localStorage/sessionStorage/IndexedDB sin secretos innecesarios.
- [ ] Source maps y JavaScript revelan rutas, claves o lógica privilegiada.
- [ ] WebSockets: autenticación, autorización por mensaje, Origin, sesión y límites.
- [ ] Cache deception/poisoning y claves de cache inconsistentes.

---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
