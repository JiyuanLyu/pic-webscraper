# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0241527/']

    def parse(self, response):
        """
        This function navigates to the `Cast & Crew` page
        from the starting movie page, and then calls the function
        `parse_full_credits(self, response)`.
        """

        # Navigates to the `Cast & Crew` page
        castcrew = response.urljoin("fullcredits")

        # Call function in the `callback` argument to 
        # a yielded `scrapy.Request`
        yield scrapy.Request(castcrew,
                             callback = self.parse_full_credits)
