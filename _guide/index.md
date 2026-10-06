---
layout: page
title: Guía de análisis de vulnerabilidades
description: Metodología ordenada y playbooks operativos para evaluar la seguridad de productos web, APIs, infraestructura, clientes e integraciones.
permalink: /guia/
icon: fas fa-shield-halved
order: 1
toc: true
comments: false
---

Esta colección reúne el mapa completo de análisis de vulnerabilidades, el motor de aplicabilidad, las fases de evaluación, las plantillas de evidencias y los playbooks operativos.

## Punto de entrada

{% assign principal = site.guide | where_exp: "item", "item.url contains '/guia-analisis-vulnerabilidades/'" | first %}
{% if principal %}
- [Abrir el mapa principal]({{ principal.url | relative_url }})
{% endif %}

## Todos los documentos

{% assign guide_docs = site.guide | where_exp: "item", "item.url != '/guia/'" | sort: "order" %}
{% for item in guide_docs %}
- [{{ item.title }}]({{ item.url | relative_url }})
{% endfor %}
