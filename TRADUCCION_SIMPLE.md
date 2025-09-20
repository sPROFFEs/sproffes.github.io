# 🌐 Sistema de Traducción Automática

Sistema **simple y local** para traducir automáticamente tus posts de Jekyll a 4 idiomas usando **deep-translator**.

## ✅ Características

- 🇪🇸 **Español** (idioma original)
- 🇬🇧 **Inglés**
- 🇩🇪 **Alemán**
- 🇫🇷 **Francés**
- 🆓 **100% gratuito**
- 🏠 **Completamente local** (sin GitHub Actions)
- 📝 **Traduce contenido completo** (títulos, párrafos, listas, headers)
- 🛡️ **Preserva código** y formato markdown
- ⚡ **Rápido** y confiable

## 🚀 Uso Simple

### 1. Configuración inicial (solo una vez)

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install python-frontmatter deep-translator
```

### 2. Traducir posts

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar traducción (traduce contenido completo)
python3 translate_simple.py
```

### 3. Publicar

```bash
# Revisar archivos generados
git status

# Hacer commit
git add .
git commit -m "Nuevas traducciones de posts"

# Publicar
git push
```

## 🎯 Cómo Funciona

1. **Escribes** tu post en español como siempre
2. **Ejecutas** `python3 translate_simple.py`
3. **Se traduce completamente** el contenido usando deep-translator (Google Translate)
4. **Se generan** automáticamente 4 versiones:
   - `post_es.md` (español)
   - `post_en.md` (inglés)
   - `post_de.md` (alemán)
   - `post_fr.md` (francés)

## 🌐 URLs Resultantes

- Español: `https://tudominio.com/posts/titulo/`
- Inglés: `https://tudominio.com/posts/titulo-en/`
- Alemán: `https://tudominio.com/posts/titulo-de/`
- Francés: `https://tudominio.com/posts/titulo-fr/`

## 🔄 Selector de Idioma

**Nuevo selector mejorado estilo Polyglot:**
- Dropdown elegante en la esquina superior derecha
- Funciona en posts y writeups
- Soporte para modo oscuro/claro
- Responsive y optimizado para móviles
- Aparece automáticamente cuando hay traducciones disponibles

## 📝 Qué se Traduce

- ✅ **Títulos** de los posts
- ✅ **Categorías** (Reconocimiento → Reconnaissance, etc.)
- ✅ **Headers** del contenido (## Título → ## Title)
- ✅ **Contenido completo** (párrafos, listas, texto)
- ✅ **Preserva formato** (código, URLs, imágenes, tablas)

## ⚠️ Notas Importantes

- ✅ **Sistema local**: No usa GitHub Actions ni servicios externos
- ✅ **Traducción completa**: Usa deep-translator con Google Translate
- ⚡ **1 post por ejecución** para máxima estabilidad
- 🔄 **Ejecuta varias veces** si tienes muchos posts
- 📁 **Archivos originales** se renombran a `_es.md`
- 🌐 **Selector automático** aparece en posts traducidos

## 🔧 Archivos del Sistema

- `translate_simple.py` - Script principal de traducción (posts y writeups)
- `_includes/polyglot-lang-selector.html` - Selector de idioma mejorado
- `_includes/footer.html` - Integración con tema Chirpy
- `_config.yml` - Configuración de permalinks multiidioma
- `TRADUCCION_SIMPLE.md` - Esta documentación