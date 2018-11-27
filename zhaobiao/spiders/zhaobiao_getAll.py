import scrapy
import mysql.connector
import time
import random
import datetime
import traceback

"this is a dictionary of chinese province"
provinces = {
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

provinces_index = [
    110000,
    120000,
    310000,
    500000,
    130000,
    410000,
    530000,
    210000,
    230000,
    430000,
    340000,
    370000,
    650000,
    320000,
    330000,
    360000,
    420000,
    450000,
    620000,
    140000,
    150000,
    620000,
    220000,
    350000,
    520000,
    440000,
    630000,
    540000,
    510000,
    640000,
    460000
]


class ZhaobiaoSpider(scrapy.Spider):
    name = "zhaobiao_getAll"

    def start_requests(self):
        province_index = 0
        url = 'http://www.bidchance.com/' \
              'freesearch.do?&filetype=&channel=gonggao&currentpage=1' \
              '&searchtype=sj&queryword=&displayStyle=title&pstate=&' \
              'field=all&leftday=&province=%d&bidfile=&project=&' \
              'heshi=&recommend=&field=all&jing=&starttime=&endtime=&' \
              'attachment=' % provinces_index[province_index]
        yield scrapy.Request(url=url, callback=self.parse,
                             meta={'province_index': province_index,
                                   'currentPage': 1})

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
            except:
                mlog = open("error_vill_zhaobiao.log", "a")
                dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                mlog.write('>>>>>[%s]\n' % dt)
                traceback.print_exc(file=mlog)
                mlog.write('\n')
                mlog.write("the url of the worn page is \n%s\n" % url)
                mlog.close()
            conn.commit()
        next_page = response.xpath(
            '//div[@class = "fy l"]/div[@class= "fynr"]/div[@id = "nextpage2"]/a/@href').extract_first()
        currentPage = int(response.meta['currentPage'])
        if (currentPage == 500) or (next_page is None):
            province_index = int(response.meta["province_index"])
            mlog = open("vill.log", "a")
            dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            mlog.write('[%s]province %s is over\n' % (str(dt), provinces[provinces_index[province_index]]))
            mlog.close()
            province_index += 1
            url = 'http://www.bidchance.com/' \
                  'freesearch.do?&filetype=&channel=gonggao&currentpage=1' \
                  '&searchtype=sj&queryword=&displayStyle=title&pstate=&' \
                  'field=all&leftday=&province=%d&bidfile=&project=&' \
                  'heshi=&recommend=&field=all&jing=&starttime=&endtime=&' \
                  'attachment=' % provinces_index[province_index]
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={'province_index': province_index,
                                       'currentPage': 1})
        elif next_page is not None:
            mlog = open("vill.log", "a")
            dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            mlog.write('[%s]currentPage is %s\n url of next page is %s\n' % (str(dt), currentPage, str(next_page)))
            mlog.close()
            s = random.randint(10, 20)
            print('sleep:%s' % s)
            province_index = int(response.meta["province_index"])
            print('province index is %d' % province_index)
            time.sleep(s)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse,
                                 meta={'province_index': response.meta['province_index'],
                                       'currentPage': (int(response.meta['currentPage']+1))})
