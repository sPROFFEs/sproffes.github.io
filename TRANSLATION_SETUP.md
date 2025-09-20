# Configuración de Traducción Automática con LibreTranslate

Este sistema permite traducir automáticamente los posts de tu blog Jekyll de español a inglés usando **LibreTranslate** (completamente FOSS) sin necesidad de mantener contenido duplicado.

## Características

- ✅ Traducción automática usando **LibreTranslate** (100% gratuito y open source)
- ✅ Soporte para **4 idiomas**: Español (ES), Inglés (EN), Alemán (DE) y Francés (FR)
- ✅ Selector de idioma en el frontend con iconos de banderas
- ✅ URLs diferenciadas por idioma:
  - Español: `/posts/titulo/`
  - Inglés: `/en/posts/title/`
  - Alemán: `/de/posts/titel/`
  - Francés: `/fr/posts/titre/`
- ✅ Preservación del formato Markdown
- ✅ Traducción automática del front matter
- ✅ **Sin necesidad de API keys o configuración externa**

## Configuración Inicial

### ¡No necesitas configurar nada más!

A diferencia de Google Translate, LibreTranslate es completamente gratuito y no requiere:
- ❌ API keys
- ❌ Cuentas en servicios de pago
- ❌ Límites estrictos de uso
- ❌ Configuración de secrets en GitHub

El script ya está configurado para usar múltiples instancias públicas de LibreTranslate automáticamente.

### El selector de idioma se incluye automáticamente

No necesitas hacer nada adicional. El selector de idioma aparecerá automáticamente en la esquina superior derecha cuando tengas posts traducidos.

El selector es un dropdown simple y discreto que no interfiere con el tema Chirpy.

### Activar el plugin (si usas Jekyll local)

En tu `_config.yml`, asegúrate de que los plugins estén habilitados:

```yaml
plugins:
  - jekyll-feed
  - jekyll-sitemap
  # otros plugins...

# Permitir plugins personalizados
safe: false
```

## Cómo Funciona

### Proceso Automático

1. **Trigger**: Al hacer push de un nuevo post en `_posts/`
2. **Detección**: El script detecta posts sin traducir
3. **Traducción**: Usa LibreTranslate API para traducir:
   - Front matter (título, categorías)
   - Contenido del post (preservando código y formato)
4. **Generación**: Crea archivos `_es.md`, `_en.md`, `_de.md` y `_fr.md`
5. **Commit**: Hace commit automático de las traducciones

### Estructura de Archivos Resultante

```
_posts/
├── 2024-01-01-mi-post_es.md      # Post original en español
├── 2024-01-01-mi-post_en.md      # Traducción en inglés
├── 2024-01-01-mi-post_de.md      # Traducción en alemán
├── 2024-01-01-mi-post_fr.md      # Traducción en francés
└── ...
```

### URLs Generadas

- Español: `https://tudominio.com/posts/mi-post/`
- Inglés: `https://tudominio.com/en/posts/my-post/`
- Alemán: `https://tudominio.com/de/posts/mein-post/`
- Francés: `https://tudominio.com/fr/posts/mon-post/`

## Personalización

### Modificar idiomas soportados

En `_config.yml`:

```yaml
languages: ["es", "en", "de", "fr"]  # Idiomas soportados actualmente
default_lang: "es"
```

En `_data/locales/`, ya están disponibles archivos para:
- `es.yml` para español
- `en.yml` para inglés
- `de.yml` para alemán
- `fr.yml` para francés

### Excluir contenido de la traducción

El script automáticamente preserva:
- Bloques de código (```code```)
- Comandos shell
- URLs
- Nombres técnicos comunes (Docker, AWS, etc.)

Para excluir más contenido, modifica `translate_posts.py`:

```python
# No traducir términos específicos
EXCLUDED_TERMS = ['Metasploit', 'OSINT', 'CTF', 'Docker']
```

### Personalizar el selector de idioma

Edita `_includes/language-selector.html` para cambiar:
- Posición (top-right por defecto)
- Estilos CSS
- Iconos
- Comportamiento

## Uso Manual

Si prefieres traducir manualmente algunos posts:

1. Desactiva el workflow automático comentando el trigger en `.github/workflows/auto-translate.yml`
2. Ejecuta el script manualmente:

```bash
cd .github/scripts
python translate_posts.py
```

## Troubleshooting

### La traducción no funciona

1. Verifica que `GOOGLE_TRANSLATE_API_KEY` esté configurada correctamente
2. Revisa los logs del GitHub Action
3. Asegúrate de que la API de Google Translate esté habilitada

### Los links entre idiomas no funcionan

1. Verifica que el plugin `multilang.rb` esté cargándose
2. Confirma que `safe: false` esté en `_config.yml`
3. Para GitHub Pages, el plugin no funcionará (solo funciona localmente)

### Formato roto después de la traducción

El script preserva Markdown, pero si algo se rompe:
1. Revisa `translate_posts.py` en la función `translate_markdown_content`
2. Agrega más patrones de exclusión
3. Ajusta la lógica de detección de bloques de código

## Alternativas

Si no quieres usar la API de Google Translate:

### Opción 1: Traducción Offline
Reemplaza Google Translate con [Argos Translate](https://github.com/argosopentech/argos-translate) (gratuito, offline)

### Opción 2: Traducción Manual con Estructura
Usa solo la estructura de archivos multiidioma y traduce manualmente

### Opción 3: Cliente-side con JavaScript
Implementa traducción en el navegador usando librerías como Google Translate Widget

## Prueba Local

Para probar la traducción localmente antes de hacer commit:

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install requests pyyaml python-frontmatter

# Probar traducción
python3 test_translation.py
```

## Consideraciones

- ✅ **Gratuito**: Completamente gratuito usando LibreTranslate
- ✅ **Open Source**: Todo el código es FOSS
- ⚠️ **Calidad**: La traducción automática puede no ser perfecta para contenido técnico muy específico
- ✅ **SEO**: URLs diferenciadas por idioma (/es/ y /en/)
- ⚠️ **GitHub Pages**: Los plugins personalizados no funcionan en GitHub Pages (solo Jekyll themes oficiales)

## Instancias LibreTranslate Utilizadas

El script usa automáticamente estas instancias públicas:
1. `https://translate.fedilab.app/translate` (principal)
2. `https://libretranslate.com/translate` (respaldo)
3. `https://libretranslate.de/translate` (respaldo)

Si todas fallan, usa un diccionario básico de términos técnicos.

Para más detalles técnicos, revisa los archivos:
- `.github/workflows/auto-translate.yml` - GitHub Action principal
- `.github/scripts/translate_posts.py` - Script de traducción
- `_plugins/multilang.rb` - Plugin Jekyll para multiidioma
- `test_translation.py` - Script de pruebas locales