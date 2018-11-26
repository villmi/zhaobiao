import scrapy
import time
import re
import mysql.connector
import sys

print(sys.version)
print('just test')


class ZhaobiaoSpider(scrapy.Spider):
    name = "zhaobiao"
    number = 0

    def start_requests(self):
        conn = mysql.connector.connect(host='localhost', port='3306', user='vill', password='hao5jx', database='spider')
        url = 'http://www.bidchance.com/search.do'
        tag = getattr(self, 'keyword', None)
        ss = str(tag).split(",")
        count = int(int(ss[1]) / 50) + 1
        querys = ss[0].split(".")
        query = ''
        for q in querys:
            query += q
            query += " "
        query = query[:-1]
        print(query)
        cursor = conn.cursor()
        name = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        sql = "insert into spider.query (word,tablename,state,completed,total) values ('%s','%s',%d,%d,%d)" % (
            query, name, 0, 0, int(ss[1]))
        cursor.execute(sql)
        conn.commit()
        sql = "CREATE TABLE `spider`.`%s` " \
              "(`id` INT NOT NULL AUTO_INCREMENT," \
              "`title` VARCHAR(200) NOT NULL,`url` VARCHAR(200) NOT NULL," \
              "`location` VARCHAR(200) NOT NULL," \
              "`channel` VARCHAR(200) NOT NULL," \
              "`pubdate` VARCHAR(200) NOT NULL," \
              "PRIMARY KEY (`id`));" % name
        cursor.execute(sql)
        if tag is not None:
            yield scrapy.FormRequest(url=url, formdata={"queryword": query.encode("GBK"), "field": "title"},
                                     callback=self.parse,
                                     meta={'number': int(ss[1]),
                                           'filename': ("zhaobiao_spider" + time.strftime("%Y%m%d%H%M%S",
                                                                                          time.localtime(
                                                                                              time.time())) + ".txt"),
                                           'line': 0,
                                           'count': count,
                                           'queryword': query,
                                           'connect': conn,
                                           'tablename': name,
                                           "total": int(ss[1])})

    def parse(self, response):
        spans = response.xpath('//tr[@class = "datatr"]')
        filename = response.meta['filename']
        line = response.meta['line']
        conn = response.meta['connect']
        cursor = conn.cursor()
        tablename = response.meta['tablename']
        if int(response.meta['count']) > 1:
            for index, span in enumerate(spans[0:51]):
                line += 1
                querywords = str(response.meta['queryword']).split(" ")
                title = span.xpath('//tr[@class = "datatr"]/td/a')
                title = title.xpath('string(.)').extract()[line % 50 - 1]
                flag = False
                url = span.xpath('//tr[@class = "datatr"]/td/a//@href').extract()[line % 50 - 1]
                location = span.xpath("//td[starts-with(@id,'prov')]")
                location = location.xpath('string(.)').extract()[line % 50 - 1]
                channel = span.xpath("//td[starts-with(@id,'channel')]")
                channel = channel.xpath('string(.)').extract()[line % 50 - 1]
                pubdate = span.xpath("//td[starts-with(@id,'pubdate')]")
                pubdate = pubdate.xpath('string(.)').extract()[line % 50 - 1]
                for queryword in querywords:
                    if re.search(queryword, title) is not None:
                        flag = True
                if not flag:
                    break
                else:
                    sql = "insert into spider.`%s` (title,url,location,channel,pubdate) values " \
                          "('%s','%s','%s','%s','%s')" % (tablename, title, url, location, channel, pubdate)
                    cursor.execute(sql)
                    conn.commit()
                    sql = "update query set completed=completed+1 where tablename='%s'" % tablename
                    cursor.execute(sql)
                    conn.commit()
                if ((index + 1 == len(spans)) and (index != 49)) or line == int(response.meta['total']):
                    sql = "update query set state=1 where tablename='%s'" % tablename
                    cursor.execute(sql)
                    conn.commit()
            next_page = response.xpath(
                '//div[@class = "fy l"]/div[@class= "fynr"]/div[@id = "nextpage2"]/a/@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(url=next_page,
                                     meta={'number': response.meta['number'] - 50,
                                           'filename': filename,
                                           'line': line,
                                           'count': int(int(response.meta['count']) - 1),
                                           'queryword': response.meta['queryword'],
                                           'connect': conn,
                                           'tablename': tablename,
                                           'total': int(response.meta['total'])},
                                     callback=self.parse)
        elif response.meta['count'] == 1:
            for span in spans[0:response.meta['number']]:
                line += 1
                querywords = str(response.meta['queryword']).split(" ")
                title = span.xpath('//tr[@class = "datatr"]/td/a')
                title = title.xpath('string(.)').extract()[line % 50 - 1]
                flag = False
                url = span.xpath('//tr[@class = "datatr"]/td/a//@href').extract()[line % 50 - 1]
                location = span.xpath("//td[starts-with(@id,'prov')]")
                location = location.xpath('string(.)').extract()[line % 50 - 1]
                channel = span.xpath("//td[starts-with(@id,'channel')]")
                channel = channel.xpath('string(.)').extract()[line % 50 - 1]
                pubdate = span.xpath("//td[starts-with(@id,'pubdate')]")
                pubdate = pubdate.xpath('string(.)').extract()[line % 50 - 1]
                print(location)
                tablename = response.meta['tablename']
                for queryword in querywords:
                    if re.search(queryword, title) is not None:
                        flag = True
                if not flag:
                    break
                else:
                    sql = "insert into spider.`%s` (title,url,location,channel,pubdate) values " \
                          "('%s','%s','%s','%s','%s')" % (tablename, title, url, location, channel, pubdate)
                    cursor.execute(sql)
                    conn.commit()
                    sql = "update query set completed=completed+1 where tablename='%s'" % tablename
                    cursor.execute(sql)
                    conn.commit()
                if line == int(response.meta['total']):
                    sql = "update query set state=1 where tablename='%s'" % tablename
                    cursor.execute(sql)
                    conn.commit()
