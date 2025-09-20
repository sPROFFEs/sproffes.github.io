#!/usr/bin/env python3
"""
Script para traducir automáticamente posts de Jekyll de español a inglés
usando LibreTranslate (FOSS)
"""

import os
import re
import requests
import frontmatter
import yaml
from pathlib import Path
import json
import time

def translate_text(text, source_lang='es', target_lang='en'):
    """Traduce texto usando LibreTranslate API (gratuito y open source)"""
    # Lista de instancias públicas de LibreTranslate con sus configuraciones
    instances = [
        {
            "url": "https://translate.fedilab.app/translate",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"}
        },
        {
            "url": "https://libretranslate.com/translate",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"}
        },
        {
            "url": "https://libretranslate.de/translate",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"}
        }
    ]

    for instance in instances:
        try:
            # Dividir texto largo en chunks para evitar límites
            max_length = 1000
            if len(text) > max_length:
                # Dividir en oraciones
                sentences = re.split(r'(?<=[.!?])\s+', text)
                translated_parts = []

                for sentence in sentences:
                    if sentence.strip():
                        translated_part = translate_chunk(sentence, source_lang, target_lang, instance)
                        translated_parts.append(translated_part)
                        time.sleep(1)  # Pausa para no sobrecargar el servicio

                return ' '.join(translated_parts)
            else:
                return translate_chunk(text, source_lang, target_lang, instance)

        except Exception as e:
            print(f"Error con {instance['url']}: {e}")
            continue

    # Fallback: traducción simple con diccionario básico
    print(f"⚠️ LibreTranslate no disponible. Usando diccionario básico para {target_lang}.")
    return simple_translate(text, target_lang)

def translate_chunk(text, source_lang, target_lang, instance):
    """Traduce un chunk de texto usando una instancia específica de LibreTranslate"""

    # Usar form data en lugar de JSON
    data = {
        'q': text,
        'source': source_lang,
        'target': target_lang,
        'format': 'text'
    }

    response = requests.post(instance["url"], data=data, headers=instance["headers"], timeout=20)
    response.raise_for_status()

    result = response.json()
    return result['translatedText']

def simple_translate(text, target_lang='en'):
    """Traducción básica para casos de emergencia usando diccionario simple"""
    translations = {
        'en': {
            'análisis': 'analysis',
            'forense': 'forensic',
            'digital': 'digital',
            'herramientas': 'tools',
            'ciberseguridad': 'cybersecurity',
            'seguridad': 'security',
            'configuración': 'configuration',
            'instalación': 'installation',
            'tutorial': 'tutorial',
            'guía': 'guide',
            'introducción': 'introduction',
            'avanzado': 'advanced',
            'básico': 'basic',
            'comandos': 'commands',
            'sistema': 'system',
            'red': 'network',
            'administración': 'administration',
            'usuario': 'user'
        },
        'de': {
            'análisis': 'Analyse',
            'forense': 'forensisch',
            'digital': 'digital',
            'herramientas': 'Werkzeuge',
            'ciberseguridad': 'Cybersicherheit',
            'seguridad': 'Sicherheit',
            'configuración': 'Konfiguration',
            'instalación': 'Installation',
            'tutorial': 'Tutorial',
            'guía': 'Anleitung',
            'introducción': 'Einführung',
            'avanzado': 'fortgeschritten',
            'básico': 'grundlegend',
            'comandos': 'Befehle',
            'sistema': 'System',
            'red': 'Netzwerk',
            'administración': 'Verwaltung',
            'usuario': 'Benutzer'
        },
        'fr': {
            'análisis': 'analyse',
            'forense': 'légale',
            'digital': 'numérique',
            'herramientas': 'outils',
            'ciberseguridad': 'cybersécurité',
            'seguridad': 'sécurité',
            'configuración': 'configuration',
            'instalación': 'installation',
            'tutorial': 'tutoriel',
            'guía': 'guide',
            'introducción': 'introduction',
            'avanzado': 'avancé',
            'básico': 'basique',
            'comandos': 'commandes',
            'sistema': 'système',
            'red': 'réseau',
            'administración': 'administration',
            'usuario': 'utilisateur'
        }
    }

    # Obtener diccionario para el idioma destino
    lang_dict = translations.get(target_lang, translations['en'])

    # Traducir palabras conocidas
    words = text.lower().split()
    translated_words = []

    for word in words:
        # Limpiar signos de puntuación
        clean_word = re.sub(r'[^\w]', '', word)
        if clean_word in lang_dict:
            # Preservar capitalización original
            if word[0].isupper():
                translated_word = lang_dict[clean_word].capitalize()
            else:
                translated_word = lang_dict[clean_word]
            # Restaurar puntuación
            translated_word = word.replace(clean_word, translated_word)
            translated_words.append(translated_word)
        else:
            translated_words.append(word)

    return ' '.join(translated_words)

def should_translate_file(file_path):
    """Determina si un archivo debe ser traducido"""
    # Solo traducir archivos que no tengan sufijo de idioma
    if any(lang in file_path.name for lang in ['_en.md', '_es.md', '_de.md', '_fr.md']):
        return False

    # Verificar si ya existen todas las versiones traducidas
    target_langs = ['en', 'de', 'fr']
    for lang in target_langs:
        lang_version = file_path.parent / file_path.name.replace('.md', f'_{lang}.md')
        if not lang_version.exists():
            return True  # Si falta alguna traducción, debe traducirse

    return False  # Ya existen todas las traducciones

def process_front_matter(front_matter, target_lang='en'):
    """Procesa y traduce el front matter"""
    translated_fm = front_matter.copy()

    # Traducir campos específicos
    if 'title' in translated_fm:
        translated_fm['title'] = translate_text(translated_fm['title'], 'es', target_lang)

    # Añadir metadatos de idioma
    translated_fm['lang'] = target_lang
    translated_fm['original_lang'] = 'es'

    # Mantener categorías y tags técnicos sin traducir
    technical_terms = ['OSINT', 'CTF', 'Docker', 'AWS', 'Azure', 'Kubernetes', 'DevOps', 'CI/CD', 'API', 'JSON', 'XML', 'HTML', 'CSS', 'JavaScript']

    if 'categories' in translated_fm:
        translated_categories = []
        for cat in translated_fm['categories']:
            if cat in technical_terms:
                translated_categories.append(cat)
            else:
                translated_categories.append(translate_text(cat, 'es', target_lang))
        translated_fm['categories'] = translated_categories

    return translated_fm

def translate_markdown_content(content, target_lang='en'):
    """Traduce el contenido markdown preservando el formato"""
    # Dividir en párrafos para traducir por bloques
    paragraphs = content.split('\n\n')
    translated_paragraphs = []

    for paragraph in paragraphs:
        if not paragraph.strip():
            translated_paragraphs.append(paragraph)
            continue

        # No traducir bloques de código
        if paragraph.startswith('```') or paragraph.startswith('    '):
            translated_paragraphs.append(paragraph)
            continue

        # No traducir tablas markdown
        if '|' in paragraph and paragraph.count('|') > 2:
            translated_paragraphs.append(paragraph)
            continue

        # No traducir líneas que son principalmente código o comandos
        if re.match(r'^(\s*[`$#>]|\s*\|)', paragraph):
            translated_paragraphs.append(paragraph)
            continue

        # No traducir URLs solas
        if re.match(r'^https?://', paragraph.strip()):
            translated_paragraphs.append(paragraph)
            continue

        # Traducir párrafo normal
        try:
            translated = translate_text(paragraph, 'es', target_lang)
            translated_paragraphs.append(translated)
        except Exception as e:
            print(f"Error traduciendo párrafo: {e}")
            translated_paragraphs.append(paragraph)  # Mantener original si falla

    return '\n\n'.join(translated_paragraphs)

def main():
    """Función principal"""
    posts_dir = Path('_posts')
    target_languages = ['en', 'de', 'fr']  # Idiomas destino

    print("🔍 Buscando posts para traducir con LibreTranslate...")

    # Limitar a 3 posts por ejecución para evitar timeouts
    posts_to_process = []
    for post_file in posts_dir.glob('*.md'):
        if should_translate_file(post_file):
            posts_to_process.append(post_file)
        if len(posts_to_process) >= 3:
            break

    if not posts_to_process:
        print("✅ No hay posts nuevos para traducir.")
        return

    print(f"📊 Encontrados {len(posts_to_process)} posts para traducir")

    for post_file in posts_to_process:
        print(f"📝 Procesando: {post_file.name}")

        try:
            # Leer el post original
            with open(post_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            # Crear versión original marcada como español
            es_filename = post_file.name.replace('.md', '_es.md')
            es_path = posts_dir / es_filename

            if not es_path.exists():
                # Actualizar el front matter del original
                original_fm = post.metadata.copy()
                original_fm['lang'] = 'es'
                original_post = frontmatter.Post(post.content, **original_fm)

                with open(es_path, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(original_post))

                print(f"📁 Creado archivo español: {es_filename}")

            # Traducir a cada idioma destino
            for target_lang in target_languages:
                lang_filename = post_file.name.replace('.md', f'_{target_lang}.md')
                lang_path = posts_dir / lang_filename

                # Verificar si ya existe la traducción
                if lang_path.exists():
                    print(f"  ⏭️  Ya existe {lang_filename}, omitiendo...")
                    continue

                print(f"  🌍 Traduciendo a {target_lang.upper()}...")

                # Traducir front matter
                print(f"    🔤 Traduciendo front matter a {target_lang}...")
                translated_fm = process_front_matter(post.metadata, target_lang)

                # Traducir contenido
                print(f"    📄 Traduciendo contenido a {target_lang}...")
                translated_content = translate_markdown_content(post.content, target_lang)

                # Crear el post traducido
                translated_post = frontmatter.Post(translated_content, **translated_fm)

                # Guardar versión traducida
                with open(lang_path, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(translated_post))

                print(f"    ✅ Creado: {lang_filename}")
                print("    ⏱️  Pausa para no sobrecargar el servicio...")
                time.sleep(3)  # Pausa entre idiomas

            # Eliminar archivo original después de procesar todos los idiomas
            if post_file.exists():
                post_file.unlink()
                print(f"🗑️  Eliminado archivo original: {post_file.name}")

            print(f"🎉 Completado: {post_file.name}")

        except Exception as e:
            print(f"❌ Error procesando {post_file.name}: {e}")

if __name__ == "__main__":
    main()