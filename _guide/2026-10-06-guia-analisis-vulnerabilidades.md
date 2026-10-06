---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Guía modular de análisis de vulnerabilidades"
permalink: /guia-analisis-vulnerabilidades/
order: 90
toc: true
comments: false
math: false
mermaid: true
---

# Guía modular de análisis de vulnerabilidades

> **IMPORTANTE: Propósito**
> Evaluar cualquier producto de forma ordenada, determinando para cada familia si **aplica**, se ha **probado sin hallazgo**, existe un **hallazgo**, queda **bloqueada** o puede declararse **no aplicable con evidencia**.

## Inicio obligatorio

1. [Motor de decisión de aplicabilidad]({{ site.baseurl }}/guia/00-inicio/motor-de-aplicabilidad/)
2. [Inventario de capacidades del producto]({{ site.baseurl }}/guia/08-plantillas/inventario-capacidades/)
3. [Matriz de cobertura y aplicabilidad]({{ site.baseurl }}/guia/08-plantillas/matriz-cobertura/)
4. [Plantilla de caso de prueba]({{ site.baseurl }}/guia/08-plantillas/caso-de-prueba/)

## Recorrido secuencial

1. [Preparación y modelado]({{ site.baseurl }}/guia/01-preparacion/)
2. [Identidad, sesiones, autorización y negocio]({{ site.baseurl }}/guia/02-nucleo-web/)
3. [Entradas, navegador y APIs]({{ site.baseurl }}/guia/03-entradas-y-cliente/)
4. [Integraciones, datos, HTTP y supply chain]({{ site.baseurl }}/guia/04-integraciones-y-datos/)
5. [Operación y resiliencia]({{ site.baseurl }}/guia/05-operacion-y-resiliencia/)
6. [Red, cloud, clientes e IA]({{ site.baseurl }}/guia/06-plataformas/)
7. [Encadenamiento, cobertura y cierre]({{ site.baseurl }}/guia/07-cierre/)

## Catálogos y conservación

- [Catálogo local de técnicas y productos]({{ site.baseurl }}/guia/09-catalogos/catalogo-local-hacktricks/)
- [Mapa completo original archivado]({{ site.baseurl }}/guia/99-referencia/mapa-completo-original/)

## Principio de cobertura

La guía no promete una lista estática de “todas las vulnerabilidades posibles”. Su mecanismo de exhaustividad consiste en inventariar **todas las capacidades reales del producto**, asociarles familias de fallos, revisar tecnologías y versiones concretas, y dejar evidencia de toda decisión. Lo desconocido queda bloqueado o pendiente, nunca se convierte silenciosamente en “No aplica”.
