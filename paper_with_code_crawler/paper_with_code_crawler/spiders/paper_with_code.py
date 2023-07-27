import scrapy

base = "https://paperswithcode.com/"
class PaperWithCodeSpider(scrapy.Spider):
    name = 'papers'
    start_urls = [
        base
    ]

    def parse(self, response):
        for quote in response.css("div.item-content"):
            a =  quote.css("h1 a::text").get()
            b = quote.css("p.author-section span.item-github-link a").attrib['href']
            yield {
                "paper_name": quote.css("h1 a::text").get(),
                "github_link": quote.css("p.author-section span.item-github-link a").attrib['href'],
                "paper_link": quote.css("h1 a").attrib['href'],
                "paper_date": quote.css("p.author-section span.item-date-pub::text").get(),
                "paper_abstract": quote.css("p.item-strip-abstract::text").get(),
                # "tag": quote.css("div.tags a.tag::text").getall()
            }
        
        link = response.css("a.infinite-more-link::attr(href)").get()
        if link is not None:
            next_link = base + link
            yield scrapy.Request(next_link, callback=self.parse)
        else:
            print("============END STATE================================")