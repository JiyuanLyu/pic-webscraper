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
    
    def parse_full_credits(self, response):
        """
        This function yield a `scrapy.Request` for the page of 
        each actor listed on the `Cast & Crew` page.
        Call the method `parse_actor_page(self_response)` when
        reaching the actors' pages.
        """

        # Click the actors' pictures using the hint
        actors = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        # For each actor, yield a request
        for actor in actors:
            actor_page = "https://www.imdb.com/" + actor
            yield scrapy.Request(actor_page,
                                 callback = self.parse_actor_page)
    
    def parse_actor_page(self, response):
        """
        This function yield a dictionary of two key-value pairs as
        {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}
        from the page of the actor.
        """

        # Get the first value in the dictionary: actor_name
        actor_name = response.css("span.itemprop::text").get()

        # Get the second value in the dictionary: movie_or_TV_name

        # Get all the filmography of this actor using the hint
        all_shows = response.css("div.filmo-row").css("a::text").getall()
        for movie in all_shows:
            yield {"actor": actor_name,
                   "movie_or_TV_name": movie}

