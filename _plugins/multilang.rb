# Plugin para soporte multiidioma en Jekyll
# Permite acceso a traducciones desde templates Liquid

module Jekyll
  class MultiLangTag < Liquid::Tag
    def initialize(tag_name, key, tokens)
      super
      @key = key.strip
    end

    def render(context)
      site = context.registers[:site]
      page = context.registers[:page]

      # Determinar idioma actual
      current_lang = page['lang'] || site.config['default_lang'] || 'es'

      # Obtener traducciones
      locales = site.data['locales']
      return '' unless locales && locales[current_lang]

      # Navegar por la clave (ej: 'commons.recent_posts')
      keys = @key.split('.')
      translation = locales[current_lang]

      keys.each do |k|
        translation = translation[k] if translation
      end

      translation || @key
    end
  end

  # Filtro para obtener posts por idioma
  module MultiLangFilters
    def posts_by_lang(posts, lang)
      posts.select { |post| post.data['lang'] == lang }
    end

    def default_lang_posts(posts)
      site = @context.registers[:site]
      default_lang = site.config['default_lang'] || 'es'
      posts.select { |post| post.data['lang'] == default_lang || post.data['lang'].nil? }
    end

    def translate_url(url, target_lang)
      site = @context.registers[:site]
      default_lang = site.config['default_lang'] || 'es'

      if target_lang == default_lang
        # Remover prefijo de idioma si es el idioma por defecto
        url.gsub(/^\/en\//, '/')
      else
        # Agregar prefijo de idioma
        "/#{target_lang}#{url}"
      end
    end

    def find_translation(post, target_lang)
      site = @context.registers[:site]
      posts = site.posts.docs

      # Buscar post traducido basado en la fecha y título similar
      base_name = File.basename(post.path, '.md').gsub(/_[a-z]{2}$/, '')
      target_name = "#{base_name}_#{target_lang}.md"

      posts.find { |p| File.basename(p.path).include?(target_name) } || post
    end
  end
end

# Registrar el tag y filtros
Liquid::Template.register_tag('t', Jekyll::MultiLangTag)
Liquid::Template.register_filter(Jekyll::MultiLangFilters)