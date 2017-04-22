#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 17:15:51 2017

@author: stephenchou
"""


import scrapy

class TableSpider(scrapy.Spider):
    name = "table"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN":2,
        "BOT_NAME":'inv',
        "ROBOTSTXT_OBEY":False}

#    def start_requests(self):
 #       urls = [
  #              'http://www.basketball-reference.com/leagues/NBA_2017_advanced.html',
#            'http://stats.nba.com/league/player/#!/bio/?Season=1998-99&SeasonType=Regular%20Season',
 #           'http://quotes.toscrape.com/page/2/',
 #       ]
  #      for url in urls:
   #         yield scrapy.Request(url=url, callback=self.getPlayers)

#==============================================================================
#     class PlayerYear(scrapy.Item):
#         category = scrapy.Field()
#         name = scrapy.Field()
#         fromclub = scrapy.Field()
#         fee = scrapy.Field()
#==============================================================================

#scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' 'http://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1?saison_id=2014'
#scrape seasons for leagues, make list of leagues like, premier, bundesliga...
#start with only premier league. scrape tables for positions. premier league can just scroll through season ids.

    def start_requests(self):
        league_list = ('GB1','L1','ES1','IT1','FR1')
        
        beg_url = 'http://www.transfermarkt.com/premier-league/tabelle/wettbewerb/{}'
        end_url = '?saison_id={}'
        season_template_url = 'http://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1?saison_id={}'
#        bundesliga_url = http://www.transfermarkt.com/1-bundesliga/tabelle/wettbewerb/L1?saison_id=2009
#        laliga_url = http://www.transfermarkt.com/laliga/tabelle/wettbewerb/ES1?saison_id=1992
#        italy_url = http://www.transfermarkt.com/serie-a/tabelle/wettbewerb/IT1/saison_id/2016
#        ligue1_url = http://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1/plus/?saison_id=2011
        seasons = range(1992, 2017)
        for league in league_list:
            for season in seasons:
                #start_url = season_template_url.format(season)
                start_url = beg_url.format(league)+end_url.format(season)
                #yield scrapy.Request(url=start_url, callback = self.getTeams)
                yield scrapy.Request(url=start_url, callback = self.getTables)

    def getTables(self, response):
        tablename = response.xpath('//div[@id="main"]//div[@class="large-8 columns"]//div[@class="table-header"]/text()').extract_first()
        for trow in response.xpath('//div[@id="main"]//div[@class="large-8 columns"]//div[@class="responsive-table"]//tbody/tr'):
            try:
                position=trow.xpath('.//td[@class="rechts hauptlink"]/text()').extract_first()
                longteamname=trow.xpath('.//td[@class="zentriert no-border-rechts"]//img/@alt').extract_first()
                teamname=trow.xpath('.//td[@class="no-border-links hauptlink"]/a[contains(@class,"vereinprofil")]/text()').extract_first()
                matches=trow.xpath('.//td[@class="zentriert"]/a/text()').extract()[0]
                wins=trow.xpath('.//td[@class="zentriert"]/a/text()').extract()[1]
                draws=trow.xpath('.//td[@class="zentriert"]/a/text()').extract()[2]
                losses=trow.xpath('.//td[@class="zentriert"]/a/text()').extract()[3]
                goals=trow.xpath('.//td[@class="zentriert"]/text()').extract()[0]
                plusminus=trow.xpath('.//td[@class="zentriert"]/text()').extract()[1]
                pts=trow.xpath('.//td[@class="zentriert"]/text()').extract()[2]
                tablekey = tablename + " " +teamname
                yield {tablekey: [tablename, position, longteamname, teamname, matches, wins, draws, losses, goals, plusminus,pts]}
            except:
                continue