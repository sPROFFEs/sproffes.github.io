#!/usr/bin/env python3
"""
Script simple y funcional para traducir posts con deep-translator
"""

import frontmatter
from pathlib import Path
from deep_translator import GoogleTranslator
import time

def translate_text(text, target_lang='en'):
    """Traduce texto usando GoogleTranslator"""
    try:
        translator = GoogleTranslator(source='es', target=target_lang)
        result = translator.translate(text)
        print(f"    ✅ '{text[:40]}...' → '{result[:40]}...'")
        return result
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return text

def should_translate_file(file_path):
    """Determina si un archivo debe ser traducido"""
    if any(lang in file_path.name for lang in ['_en.md', '_es.md', '_de.md', '_fr.md']):
        return False

    # Verificar si ya existen todas las traducciones
    base_name = file_path.stem
    for lang in ['en', 'de', 'fr']:
        lang_file = file_path.parent / f"{base_name}_{lang}.md"
        if not lang_file.exists():
            return True
    return False

def translate_markdown_content(content, target_lang):
    """Traduce contenido markdown preservando código y formato"""
    import re

    # Dividir en párrafos
    paragraphs = content.split('\n\n')
    translated_paragraphs = []

    in_code_block = False

    for paragraph in paragraphs:
        # Verificar si estamos en un bloque de código
        if paragraph.strip().startswith('```'):
            in_code_block = not in_code_block
            translated_paragraphs.append(paragraph)  # No traducir código
            continue

        if in_code_block:
            translated_paragraphs.append(paragraph)  # No traducir código
            continue

        # No traducir párrafos vacíos
        if not paragraph.strip():
            translated_paragraphs.append(paragraph)
            continue

        # No traducir líneas que son principalmente código
        if paragraph.strip().startswith(('    ', '\t')) or '`' in paragraph and paragraph.count('`') >= 2:
            translated_paragraphs.append(paragraph)
            continue

        # No traducir URLs solas
        if re.match(r'^https?://', paragraph.strip()):
            translated_paragraphs.append(paragraph)
            continue

        # No traducir tablas markdown
        if '|' in paragraph and paragraph.count('|') > 2:
            translated_paragraphs.append(paragraph)
            continue

        # Traducir párrafo normal
        lines = paragraph.split('\n')
        translated_lines = []

        for line in lines:
            line_stripped = line.strip()

            # No traducir líneas vacías
            if not line_stripped:
                translated_lines.append(line)
                continue

            # Traducir headers
            if line_stripped.startswith('#'):
                header_match = re.match(r'^(#+)\s*(.*)', line_stripped)
                if header_match:
                    level, title = header_match.groups()
                    if title.strip():
                        translated_title = translate_text(title, target_lang)
                        translated_lines.append(f"{level} {translated_title}")
                    else:
                        translated_lines.append(line)
                else:
                    translated_lines.append(line)

            # Traducir listas
            elif line_stripped.startswith(('- ', '* ', '+ ')) or re.match(r'^\d+\.\s', line_stripped):
                # Extraer prefijo de lista
                list_match = re.match(r'^(\s*(?:[-*+]|\d+\.)\s*)(.*)', line)
                if list_match:
                    prefix, content = list_match.groups()
                    if content.strip():
                        translated_content = translate_text(content, target_lang)
                        translated_lines.append(f"{prefix}{translated_content}")
                    else:
                        translated_lines.append(line)
                else:
                    translated_lines.append(line)

            # No traducir líneas con mucho código inline
            elif line.count('`') >= 4:
                translated_lines.append(line)

            # Traducir texto normal
            else:
                if line_stripped:
                    translated_line = translate_text(line_stripped, target_lang)
                    # Preservar indentación original
                    indent = line[:len(line) - len(line.lstrip())]
                    translated_lines.append(f"{indent}{translated_line}")
                else:
                    translated_lines.append(line)

        translated_paragraphs.append('\n'.join(translated_lines))

    return '\n\n'.join(translated_paragraphs)

def main():
    """Función principal"""
    print("🚀 Traduciendo posts con deep-translator...")

    # Buscar en ambos directorios: _posts y _writeups
    directories_to_check = [Path('_posts'), Path('_writeups')]
    target_languages = [
        ('en', 'inglés'),
        ('de', 'alemán'),
        ('fr', 'francés')
    ]

    # Buscar posts para traducir en ambos directorios
    posts_to_process = []
    for directory in directories_to_check:
        if not directory.exists():
            continue

        # Buscar archivos markdown de forma recursiva
        for post_file in directory.rglob('*.md'):
            if should_translate_file(post_file):
                posts_to_process.append(post_file)
                break  # Solo 1 post por vez

        if posts_to_process:  # Si encontramos algo, salir del bucle
            break

    if not posts_to_process:
        print("✅ No hay posts nuevos para traducir.")
        return

    for post_file in posts_to_process:
        print(f"\n📝 Procesando: {post_file.name}")

        try:
            # Leer post original
            with open(post_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            # Crear versión en español
            es_filename = post_file.stem + '_es.md'
            es_path = post_file.parent / es_filename

            if not es_path.exists():
                original_fm = post.metadata.copy()
                original_fm['lang'] = 'es'
                original_post = frontmatter.Post(post.content, **original_fm)

                with open(es_path, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(original_post))
                print(f"📁 Creado: {es_filename}")

            # Traducir a cada idioma
            for lang_code, lang_name in target_languages:
                lang_filename = post_file.stem + f'_{lang_code}.md'
                lang_path = post_file.parent / lang_filename

                if lang_path.exists():
                    print(f"  ⏭️ Ya existe {lang_filename}")
                    continue

                print(f"  🌍 Traduciendo a {lang_name}...")

                # Preparar front matter traducido
                translated_fm = post.metadata.copy()
                translated_fm['lang'] = lang_code
                translated_fm['original_lang'] = 'es'

                # Traducir título si existe
                if 'title' in translated_fm and translated_fm['title'].strip():
                    print(f"  📰 Traduciendo título...")
                    translated_fm['title'] = translate_text(translated_fm['title'], lang_code)

                # Traducir categorías
                if 'categories' in translated_fm:
                    print(f"  📂 Traduciendo categorías...")
                    translated_categories = []
                    for cat in translated_fm['categories']:
                        # No traducir términos técnicos
                        if cat.upper() in ['OSINT', 'CTF', 'DOCKER', 'AWS', 'AZURE']:
                            translated_categories.append(cat)
                        else:
                            translated_cat = translate_text(cat, lang_code)
                            translated_categories.append(translated_cat)
                    translated_fm['categories'] = translated_categories

                # Traducir contenido completo pero preservando formato
                print(f"  📄 Traduciendo contenido completo...")
                translated_content = translate_markdown_content(post.content, lang_code)

                # Crear post traducido
                translated_post = frontmatter.Post(translated_content, **translated_fm)

                # Guardar
                with open(lang_path, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(translated_post))

                print(f"    ✅ Creado: {lang_filename}")
                time.sleep(2)  # Pausa entre idiomas

            # Eliminar archivo original
            post_file.unlink()
            print(f"🗑️ Eliminado archivo original: {post_file.name}")

            print(f"🎉 ¡Completado! Archivos generados:")
            print(f"   - {es_filename}")
            for lang_code, _ in target_languages:
                lang_filename = post_file.stem + f'_{lang_code}.md'
                print(f"   - {lang_filename}")

        except Exception as e:
            print(f"❌ Error procesando {post_file.name}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()