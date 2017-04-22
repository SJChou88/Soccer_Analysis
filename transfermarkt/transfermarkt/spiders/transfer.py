#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:15:06 2017

@author: stephenchou
"""

import scrapy

class TransferSpider(scrapy.Spider):
    name = "transfer"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN":2,
        "BOT_NAME":'inv',
        "ROBOTSTXT_OBEY":False}

#scrapy shell -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' 'http://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1?saison_id=2014'
#scrape seasons for leagues, make list of leagues like, premier, bundesliga...
#start with only premier league. scrape tables for positions. premier league can just scroll through season ids.

    def start_requests(self):
        league_list = ('GB1','L1','ES1','IT1','FR1')
        
        beg_url = 'http://www.transfermarkt.com/premier-league/tabelle/wettbewerb/{}'
        end_url = '?saison_id={}'
        season_template_url = 'http://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1?saison_id={}'
        seasons = range(1992, 2017)
        for league in league_list:
            for season in seasons:
                start_url = beg_url.format(league)+end_url.format(season)
                yield scrapy.Request(url=start_url, callback = self.getTeams)

    def getTables(self, response):
        tablename = response.xpath('//div[@id="main"]//div[@class="large-8 columns"]//div[@class="table-header"]/text()').extract_first()
        for trow in response.xpath('//div[@id="main"]//div[@class="large-8 columns"]//div[@class="responsive-table"]//tbody/tr'):
            try:
                position=trow.xpath('.//td[@class="rechts hauptlink"]/text()').extract_first()
                teamname=trow.xpath('.//td[@class="no-border-links hauptlink"]/a[contains(@class,"vereinprofil")]/text()').extract_first()
                matches=trow.xpath('.//td[@class="zentriert"]/a/text()').extract()[0]
                wins=trow.xpath('.//td[@class="zentriert"]/a/text()').extract()[1]
                draws=trow.xpath('.//td[@class="zentriert"]/a/text()').extract()[2]
                losses=trow.xpath('.//td[@class="zentriert"]/a/text()').extract()[3]
                goals=trow.xpath('.//td[@class="zentriert"]/text()').extract()[0]
                plusminus=trow.xpath('.//td[@class="zentriert"]/text()').extract()[1]
                pts=trow.xpath('.//td[@class="zentriert"]/text()').extract()[2]
                tablekey = tablename + " " +teamname
                yield {tablekey: [tablename, position, teamname, matches, wins, draws, losses, goals, plusminus,pts]}
            except:
                continue
        
    def getTeams(self, response):
        for link in response.xpath('//div[@class="large-8 columns"]//div[@class="responsive-table"]/table//tr//a[contains(@class,"verein")]/@href').extract():
            yield scrapy.Request(url='http://www.transfermarkt.com/'+link, callback=self.getTeamTransfersAll)

    def getTeamTransfersAll(self, response):
        transferlink = response.xpath('//div[@class="large-12 columns"]//ul[@class="megamenu"]//div[contains(@class,"fullwidth")]//a[contains(@href,"alletransfers")]/@href').extract()[0]
        yield scrapy.Request(url='http://www.transfermarkt.com/'+transferlink, callback=self.getTransfers)

    def getTransfers(self, response):
        clubname = response.xpath('//div[@class="row"]//div[@class="dataName"]/h1[contains(@itemprop,"name")]/b/text()').extract()[0]
        for i in response.xpath('//div[contains(@class,"large-6 columns")]'):
            try:
                for box in i.xpath('.//div[@class="box"]'):
                    try:
                        category = box.xpath('.//div[contains(@class,"table-header")]/text()').extract_first().replace('\n','').replace('\t','').replace('\r','')
                        for j in box.xpath('.//table//tr'): #.extract():
                            try:
                                print(j.xpath('.//td[contains(@class,"hauptlink")]/a[contains(@class,"spiel")]/text()').extract_first())
                                name = j.xpath('.//td[contains(@class,"hauptlink")]/a[contains(@class,"spiel")]/text()').extract_first()
                                longfromclub = j.xpath('.//td[contains(@class,"zentriert")]//a[contains(@class,"verein")]/img/@alt').extract_first()
                                fromclub = j.xpath('.//td[contains(@class,"no-border-links")]//a[contains(@class,"verein")]/text()').extract_first()
                                fee = j.xpath('.//td[contains(@class,"rechts")]/text()').extract_first()
                                key = category + " " + clubname + " " + name
                                yield {key: [category, clubname, name, longfromclub, fromclub, fee]}

                            except:
                                continue
                    except:
                        continue
            except:
                continue