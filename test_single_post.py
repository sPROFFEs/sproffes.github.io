#!/usr/bin/env python3
"""
Script para probar la traducción de un solo post
"""

import sys
import os
from pathlib import Path

sys.path.append('.github/scripts')

from translate_posts import process_front_matter, translate_markdown_content
import frontmatter

def test_single_post():
    """Prueba la traducción de un solo post específico"""
    posts_dir = Path('_posts')

    # Tomar el primer post como ejemplo
    post_files = list(posts_dir.glob('*.md'))
    if not post_files:
        print("❌ No se encontraron posts para probar")
        return

    # Usar el post más reciente (último en la lista ordenada)
    test_post = sorted(post_files)[-1]
    print(f"🧪 Probando traducción con: {test_post.name}")

    try:
        # Leer el post original
        with open(test_post, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        print(f"📰 Título original: '{post.metadata.get('title', 'Sin título')}'")

        # Probar traducción del front matter solo a inglés para empezar
        print("🔤 Traduciendo front matter a inglés...")
        translated_fm = process_front_matter(post.metadata, 'en')
        print(f"📰 Título traducido: '{translated_fm.get('title', 'Sin título')}'")

        # Probar con un párrafo pequeño del contenido
        content_preview = post.content[:200]  # Solo los primeros 200 caracteres
        print(f"\n📄 Contenido original (preview): '{content_preview}...'")

        print("📝 Traduciendo contenido a inglés...")
        translated_content_preview = translate_markdown_content(content_preview, 'en')
        print(f"📄 Contenido traducido (preview): '{translated_content_preview}...'")

        print("✅ Prueba completada exitosamente!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_single_post()