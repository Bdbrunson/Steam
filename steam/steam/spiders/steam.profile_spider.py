from steam.items import steamItem
import scrapy
import random


class steamProfile_Spider(object):
	"""docstring for steamProfile_Spider"""
	name = "steamProfile_Spider"
	allowed_urls: ['http://steamcommunity.com']
	start_urls = ['http://steamcommunity.com/profiles/76561197960265729/games/?tab=all']

	def parse(self, response):
		urlstart = random.randrange(76561197960265729, 76561198100989000, 1)
		pageurl = ['http://steamcommunity.com/profiles/' + l + '/games/?tab=all' for l in urlstart]

		for url in pageurl:
            yield scrapy.Request(url, callback=self.parse_top)

    def parse_top(self, response):
    	accountname = response.xpath('//div[@id="games_list_rows"]//@class="gameListRowItemName ellipsis "]/text()').extract()
    	gamenames = 
    	timePlayed = 

//*[@id="game_8930"]/div[2]/div[1]

class="gameListRowItemName ellipsis "



#urlstart =random.randrange(76561199160265729, 76561198346202659, 1)
#urlpage = ['http://steamcommunity.com/profiles/' + l for l in urlstart + '/games/?tab=all']

#http://steamcommunity.com/profiles/76561197960265729/games/?tab=all #starting website for first steam profile
#~175 million users give or take
#let's try 140,723,264. somewhere in the last 35 million users they changed account
#numbers to be randomly generated. created a new account and mine is 76561198436040338
# which actually precedes the random sequences. X.X
