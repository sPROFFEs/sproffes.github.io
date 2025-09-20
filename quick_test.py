#!/usr/bin/env python3
"""
Script rápido para traducir solo 1 post como prueba
"""

import sys
from pathlib import Path

sys.path.append('.github/scripts')

from translate_posts import process_front_matter, translate_markdown_content, should_translate_file
import frontmatter

def quick_translate():
    """Traduce solo el primer post encontrado"""
    posts_dir = Path('_posts')

    # Encontrar el primer post que necesite traducción
    for post_file in posts_dir.glob('*.md'):
        if should_translate_file(post_file):
            print(f"🚀 Traduciendo rápidamente: {post_file.name}")

            try:
                # Leer el post original
                with open(post_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)

                # Solo traducir a inglés para la prueba
                print("📝 Traduciendo a inglés...")

                # Traducir front matter
                translated_fm = process_front_matter(post.metadata, 'en')

                # Traducir solo los primeros 500 caracteres del contenido para ir rápido
                content_preview = post.content[:500]
                translated_content = translate_markdown_content(content_preview, 'en')

                # Crear el post traducido
                translated_post = frontmatter.Post(translated_content + "\n\n[Traducción parcial para prueba]", **translated_fm)

                # Guardar versión en inglés
                en_filename = post_file.name.replace('.md', '_en.md')
                en_path = posts_dir / en_filename

                with open(en_path, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(translated_post))

                # Crear versión en español
                es_filename = post_file.name.replace('.md', '_es.md')
                es_path = posts_dir / es_filename

                if not es_path.exists():
                    original_fm = post.metadata.copy()
                    original_fm['lang'] = 'es'
                    original_post = frontmatter.Post(post.content, **original_fm)

                    with open(es_path, 'w', encoding='utf-8') as f:
                        f.write(frontmatter.dumps(original_post))

                # Eliminar archivo original
                post_file.unlink()

                print(f"✅ Creados: {es_filename} y {en_filename}")
                print("🎉 Prueba rápida completada!")
                return

            except Exception as e:
                print(f"❌ Error: {e}")
                return

    print("ℹ️ No hay posts nuevos para traducir")

if __name__ == "__main__":
    quick_translate()