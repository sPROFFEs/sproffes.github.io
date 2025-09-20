#!/usr/bin/env python3
"""
Script de prueba para testear la traducción con LibreTranslate localmente
"""

import sys
import os
sys.path.append('.github/scripts')

from translate_posts import translate_text

def test_libretranslate():
    """Prueba básica de LibreTranslate"""

    print("🧪 Probando LibreTranslate...")

    # Textos de prueba
    test_texts = [
        "Hola mundo",
        "Este es un texto de prueba para verificar que LibreTranslate funciona correctamente.",
        "Análisis forense digital",
        "Herramientas de ciberseguridad"
    ]

    # Idiomas de prueba
    target_languages = [
        ('en', 'inglés'),
        ('de', 'alemán'),
        ('fr', 'francés')
    ]

    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Prueba {i}: '{text}'")

        for lang_code, lang_name in target_languages:
            try:
                translated = translate_text(text, 'es', lang_code)
                print(f"  ✅ {lang_name.capitalize()}: '{translated}'")
            except Exception as e:
                print(f"  ❌ Error {lang_name}: {e}")

    print("\n🎉 Pruebas completadas!")

def test_with_post():
    """Prueba con un post real"""
    from pathlib import Path
    import frontmatter
    from translate_posts import process_front_matter, translate_markdown_content

    posts_dir = Path('_posts')
    post_files = list(posts_dir.glob('*.md'))

    if not post_files:
        print("❌ No se encontraron posts para probar")
        return

    # Tomar el primer post como ejemplo
    test_post = post_files[0]
    print(f"\n🧪 Probando con post: {test_post.name}")

    try:
        with open(test_post, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # Probar traducción del título
        if 'title' in post.metadata:
            print(f"📰 Título original: '{post.metadata['title']}'")
            translated_title = translate_text(post.metadata['title'])
            print(f"📰 Título traducido: '{translated_title}'")

        # Probar con un párrafo del contenido
        paragraphs = post.content.split('\n\n')
        for paragraph in paragraphs[:3]:  # Solo los primeros 3 párrafos
            if paragraph.strip() and not paragraph.startswith('#') and not paragraph.startswith('```'):
                print(f"\n📄 Párrafo original: '{paragraph[:100]}...'")
                translated_paragraph = translate_text(paragraph)
                print(f"📄 Párrafo traducido: '{translated_paragraph[:100]}...'")
                break

    except Exception as e:
        print(f"❌ Error probando con post: {e}")

if __name__ == "__main__":
    test_libretranslate()

    # Preguntar si quiere probar con un post real
    response = input("\n¿Quieres probar con un post real? (y/n): ")
    if response.lower() in ['y', 'yes', 's', 'si']:
        test_with_post()