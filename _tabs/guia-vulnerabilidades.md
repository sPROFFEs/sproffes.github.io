---
title: Guía de vulnerabilidades
icon: fas fa-shield-halved
order: 3
permalink: /guia-vulnerabilidades/
---

# Guía de análisis de vulnerabilidades

Esta sección reúne la metodología completa para evaluar productos de forma ordenada, justificar qué familias de vulnerabilidades aplican y registrar evidencias, limitaciones y cobertura residual.

> La guía está orientada exclusivamente a evaluaciones autorizadas. Las pruebas deben realizarse con el mínimo impacto necesario y dentro del alcance acordado.

## Empezar

- [Abrir el mapa principal]({{ site.baseurl }}/guia-analisis-vulnerabilidades/)
- [Motor de decisión de aplicabilidad]({{ site.baseurl }}/guia/00-inicio/motor-de-aplicabilidad/)
- [Inventario de capacidades]({{ site.baseurl }}/guia/08-plantillas/inventario-capacidades/)
- [Matriz de cobertura]({{ site.baseurl }}/guia/08-plantillas/matriz-cobertura/)
- [Índice de playbooks]({{ site.baseurl }}/guia/10-playbooks/00-indice/)

## Recorrido recomendado

{% assign guide_posts = site.guide | sort: "order" %}
{% assign sections = "Inicio y aplicabilidad|Preparación|Núcleo web|Entradas, cliente y APIs|Integraciones y datos|Operación y resiliencia|Plataformas|Cierre|Plantillas|Playbooks operativos|Catálogo y referencia" | split: "|" %}

{% for section in sections %}
### {{ section }}

{% assign found = false %}
{% for post in guide_posts %}
  {% assign path = post.path | downcase %}
  {% assign include_post = false %}
  {% case section %}
    {% when "Inicio y aplicabilidad" %}{% if path contains "00-inicio" or post.url == "/guia-analisis-vulnerabilidades/" %}{% assign include_post = true %}{% endif %}
    {% when "Preparación" %}{% if path contains "01-preparacion" %}{% assign include_post = true %}{% endif %}
    {% when "Núcleo web" %}{% if path contains "02-nucleo-web" %}{% assign include_post = true %}{% endif %}
    {% when "Entradas, cliente y APIs" %}{% if path contains "03-entradas-y-cliente" %}{% assign include_post = true %}{% endif %}
    {% when "Integraciones y datos" %}{% if path contains "04-integraciones-y-datos" %}{% assign include_post = true %}{% endif %}
    {% when "Operación y resiliencia" %}{% if path contains "05-operacion-y-resiliencia" %}{% assign include_post = true %}{% endif %}
    {% when "Plataformas" %}{% if path contains "06-plataformas" %}{% assign include_post = true %}{% endif %}
    {% when "Cierre" %}{% if path contains "07-cierre" %}{% assign include_post = true %}{% endif %}
    {% when "Plantillas" %}{% if path contains "08-plantillas" %}{% assign include_post = true %}{% endif %}
    {% when "Playbooks operativos" %}{% if path contains "10-playbooks" %}{% assign include_post = true %}{% endif %}
    {% when "Catálogo y referencia" %}{% if path contains "09-catalogos" or path contains "99-referencia" %}{% assign include_post = true %}{% endif %}
  {% endcase %}
  {% if include_post %}
- [{{ post.title }}]({{ post.url | relative_url }}){% if post.description %}: {{ post.description | strip_html | strip_newlines }}{% endif %}
    {% assign found = true %}
  {% endif %}
{% endfor %}
{% unless found %}
- Sección pendiente de publicación.
{% endunless %}

{% endfor %}

## Todos los documentos

La lista siguiente se actualiza automáticamente cuando se publica un nuevo post dentro de la colección **guide**.

{% for post in guide_posts %}
1. [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
