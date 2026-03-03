require 'cgi'

module Jekyll
  module URLEncode
    def url_encode(url)
      return CGI.escape(url) if url
      nil
    end
  end
end

Liquid::Template.register_filter(Jekyll::URLEncode)
