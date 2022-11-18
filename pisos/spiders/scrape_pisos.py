import scrapy


class ScrapePisosSpider(scrapy.Spider):
    name = 'scrape-pisos'
    allowed_domains = ['www.pisos.com']
    start_urls = ['https://www.pisos.com/venta/pisos-barcelona/fecharecientedesde-desc/']
    max_pages_to_crawl = 10


    def parse(self, response):

        wrapper = response.css("div.grid__wrapper")

        for entrada in wrapper.css('.ad-preview'):
            doc = {}
            doc['url'] = 'https://' + self.allowed_domains[0] + entrada.css('*::attr(data-lnk-href)').extract_first()
            doc['title'] = entrada.css('div:nth-child(2) > a *::text').extract_first()
            doc['direccion'] = entrada.css('div:nth-child(2) > p *::text').extract_first()
            doc['nHabitaciones'] = entrada.css('div:nth-child(3) > div > p:nth-child(1) *::text').extract_first()
            doc['nBanyos'] = entrada.css('div:nth-child(3) > div > p:nth-child(2) *::text').extract_first()
            doc['metrosCuadrados'] = entrada.css('div:nth-child(3) > div > p:nth-child(3) *::text').extract_first()
            doc['planta'] = entrada.css('div:nth-child(3) > div > p:nth-child(4) *::text').extract_first()
            doc['descripcion'] = entrada.css('div.ad-preview__section.u-hide > p *::text').extract_first()
            doc['descuento'] = entrada.css('div.ad-preview__info > div:nth-child(1) > div > span.ad-preview__drop *::text').extract_first()
            doc['imgPreview'] = entrada.css('div.carousel > div.carousel__container > div:nth-child(2) > div *::attr(data-bg)').extract_first()
            doc['precio'] = entrada.css('div.ad-preview__bottom > div.ad-preview__info > div:nth-child(1) > div > span *::text').extract_first()
            yield scrapy.Request(doc['url'], callback=self.parse_piso, meta=doc)

        # Next page
        path = response.css('div.pagination__content > div.pagination__next.border-l > a *::attr(href)').extract_first()
        if path is None:
            path = response.css('div.pagination__content > div > a *::attr(href)').extract_first()
        next_page = 'https://' + self.allowed_domains[0] + path
        if next_page is not None and self.max_pages_to_crawl > 0:
            self.max_pages_to_crawl -= 1
            yield scrapy.Request(next_page, callback=self.parse)
        

    def parse_piso(self, response):
        detail = response.meta

        detail['superficieConstruida'] = None
        detail['planta'] = None
        detail['antiguedad'] = None
        detail['referencia'] = None
        detail['superficieUtil'] = None
        detail['conservacion'] = None
        

        basic_info = response.css("#characteristics > div:nth-child(1) > div.charblock-right > ul")

        for item in basic_info.css("li"):
            key = item.css('span:nth-child(1) *::text').extract_first()
            value = item.css('span:nth-child(2) *::text').extract_first()
            if key == 'Superficie construida':
                detail['superficieConstruida'] = value
            elif key == 'Planta':
                detail['planta'] = value
            elif key == 'Antigüedad':
                detail['antiguedad'] = value
            elif key == 'Referencia':
                detail['referencia'] = value
            elif key == 'Superficie útil':
                detail['superficieUtil'] = value
            elif key == 'Conservación':
                detail['conservacion'] = value

        detail['certificado_energetico'] = response.css("li.charblock-element.element-with-bullet.certificate-emissions > div > .sel *::text").extract_first()

        # Clean keys
        for key in detail:
            if detail[key] is not None and isinstance(detail[key], str):
                if key != 'url' and key != 'imgPreview':
                    detail[key] = detail[key].encode('utf-8').decode('utf-8').replace(':', '').strip()
                else:
                    detail[key] = detail[key].encode('utf-8').decode('utf-8').strip()

        yield detail
