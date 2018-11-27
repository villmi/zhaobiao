import scrapy
import mysql.connector
import time
import random
import datetime
import traceback

"this is a dictionary of chinese province"
d = {
    110000: "beijing",
    120000: "tianjing",
    310000: "shanghai",
    500000: "chongqing",
    130000: "hebei",
    410000: "henan",
    530000: "yunnan",
    210000: "liaoning",
    230000: "heilongjiang",
    430000: "hunan",
    340000: "anhui",
    370000: "shandong",
    650000: "xinjiang",
    320000: "jiangsu",
    330000: "zhejiang",
    360000: "jiangxi",
    420000: "hubei",
    450000: "guangxi",
    620000: "gansu",
    140000: "shan1xi",
    150000: "neimeng",
    620000: "shan3xi",
    220000: "jilin",
    350000: "fujian",
    520000: "guizhou",
    440000: "guangdong",
    630000: "qinghai",
    540000: "xizang",
    510000: "sichuan",
    640000: "ningxia",
    460000: "hainan"
}


class ZhaobiaoSpider(scrapy.Spider):
    name = "zhaobiao_getAll"

    def start_requests(self):
        url = 'http://www.bidchance.com/' \
              'freesearch.do?&filetype=&channel=gonggao&currentpage=1' \
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
            try:
                cursor.execute(sql)
            except :
                mlog = open("error_vill_zhaobiao.log", "a")
                dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                mlog.write('[%s]\n' % dt)
                traceback.print_exc(file=mlog)
                mlog.write('\n')
            conn.commit()
        next_page = response.xpath(
            '//div[@class = "fy l"]/div[@class= "fynr"]/div[@id = "nextpage2"]/a/@href').extract_first()
        if next_page is not None:
            mlog = open("vill.log", "a")
            dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            mlog.write('[%s]_%s\n' % (str(dt), str(next_page)))
            s = random.randint(10, 20)
            print(s)
            time.sleep(s)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            mlog = open("vill.log", "a")
            dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            mlog.write('[%s]_province_ _is_over\n' % (str(dt), str(next_page)))
