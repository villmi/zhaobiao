import scrapy
import mysql.connector
import time
import random
import datetime


class ZhaobiaoSpider(scrapy.Spider):
    name = "zhaobiao_getAll"

    def start_requests(self):
        url = 'http://www.bidchance.com/' \
              'freesearch.do?&filetype=&channel=gonggao&currentpage=441' \
              '&searchtype=sj&queryword=&displayStyle=title&pstate=&' \
              'field=all&leftday=&province=&bidfile=&project=&' \
              'heshi=&recommend=&field=all&jing=&starttime=&endtime=&' \
              'attachment='
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        conn = mysql.connector.connect(host='localhost', port='3306', user='vill', password='hao5jx', database='spider')
        cursor = conn.cursor()
        spans = response.xpath('//tr[@class = "datatr"]')
        line = 0
        tablename = 'zhaobiao_getall'
        for span in spans:
            title = span.xpath('//tr[@class = "datatr"]/td/a')
            title = title.xpath('string(.)').extract()[line]
            url = span.xpath('//tr[@class = "datatr"]/td/a//@href').extract()[line]
            location = span.xpath("//td[starts-with(@id,'prov')]")
            location = location.xpath('string(.)').extract()[line]
            channel = span.xpath("//td[starts-with(@id,'channel')]")
            channel = channel.xpath('string(.)').extract()[line]
            pubdate = span.xpath("//td[starts-with(@id,'pubdate')]")
            pubdate = pubdate.xpath('string(.)').extract()[line]
            line += 1
            sql = "insert into spider.`%s`(title,url,location,channel,pubdate) values" \
                  "('%s','%s','%s','%s','%s')" % (tablename, title, url, location, channel, pubdate)
            cursor.execute(sql)
            conn.commit()
        next_page = response.xpath(
                '//div[@class = "fy l"]/div[@class= "fynr"]/div[@id = "nextpage2"]/a/@href').extract_first()
        if next_page is not None:
            mlog = open("vill.log", "a")
            dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            mlog.write('[%s]_%s\n' % (str(dt), str(next_page)))
            s = random.randint(0, 15)
            print(s)
            time.sleep(s)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
