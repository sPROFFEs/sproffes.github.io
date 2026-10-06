---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Fase 6. Autorización y aislamiento"
permalink: /guia/02-nucleo-web/06-autorizacion-y-aislamiento/
order: 206
toc: true
comments: false
math: false
mermaid: true
---

# Fase 6. Autorización y aislamiento

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

> **PELIGRO: Prioridad máxima**
> Probar siempre con al menos dos usuarios equivalentes, dos roles distintos y, si existe multitenancy, dos organizaciones diferentes.

## 6.1 Matriz de autorización

| Función/objeto | Anónimo | Usuario A | Usuario B | Admin tenant A | Admin global | Servicio |
|---|---:|---:|---:|---:|---:|---:|
| Leer objeto propio | | | | | | |
| Leer objeto ajeno | | | | | | |
| Modificar objeto | | | | | | |
| Exportar/borrar | | | | | | |

## 6.2 Pruebas

- [ ] Acceso forzado a rutas sin autenticación.
- [ ] IDOR/BOLA al cambiar ID, UUID, slug, nombre, ruta o referencia indirecta.
- [ ] Escalada horizontal entre usuarios.
- [ ] Escalada vertical entre roles.
- [ ] Aislamiento entre tenants en lectura, escritura, búsqueda, exportación, archivos y cache.
- [ ] Autorización en backend, no solo ocultación de interfaz.
- [ ] Métodos alternativos y versiones antiguas mantienen controles.
- [ ] Operaciones batch verifican autorización por cada objeto.
- [ ] Mass assignment no permite cambiar rol, owner, tenant, precio o estado.
- [ ] Recursos hijos no heredan acceso indebidamente.
- [ ] WebSockets, webhooks y jobs asíncronos aplican la misma autorización.
- [ ] URLs firmadas limitan recurso, acción, usuario y tiempo.
- [ ] Búsquedas, contadores y mensajes no filtran existencia de objetos ajenos.

---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
