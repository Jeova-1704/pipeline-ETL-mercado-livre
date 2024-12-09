import scrapy

class MercadoLivreSpiderSpider(scrapy.Spider):
    name = "mercado_livre_spider"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_page_count = 10

    def parse(self, response):
        products = response.css('div.poly-card__content')
        
        for product in products:
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()
                
            yield {
                'marca': product.css('span.poly-component__brand::text').get(),
                'nome': product.css('h2.poly-box.poly-component__title a::text').get(),
                'preco_antigo': prices[0] if len(prices) > 1 else None,
                'centavos_antigo': cents[0] if len(cents) > 1 else None,
                'preco_atual': prices[1] if len(prices) > 1 else None,
                'centavos_atual': cents[1] if len(cents) > 1 else None,
                'avaliacao': product.css('span.poly-reviews__rating::text').get(),
                'quantidade_avaliacoes': product.css('span.poly-reviews__total::text').get(),
            }
        
        if self.page_count < self.max_page_count:
            next_page = response.css('li.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                print("Next page URL:", next_page)
                yield scrapy.Request(url=next_page, callback=self.parse)
