import scrapy
import os
import time
import re


class ZhaobiaoSpider(scrapy.Spider):
    name = "zhaobiao_spider"
    number = 0

    def start_requests(self):
        url = 'http://www.bidchance.com/search.do'
        tag = getattr(self, 'keyword', None)
        ss = str(tag).split(",")
        count = int(int(ss[1]) / 50) + 1
        querys = ss[0].split(".")
        query = ''
        for q in querys:
            query += " "
            query += q
        print(count)
        if tag is not None:
            yield scrapy.FormRequest(url=url, formdata={"queryword": query.encode("GBK"), }, callback=self.parse,
                                     meta={'number': int(ss[1]),
                                           'filename': ("zhaobiao_spider" + time.strftime("%Y%m%d%H%M%S",
                                                                                          time.localtime(
                                                                                              time.time())) + ".txt"),
                                           'line': 0,
                                           'count': count,
                                           'queryword': query})

    def parse(self, response):
        spans = response.xpath('//tr[@class = "datatr"]/td/a')
        os.chdir('/Users/vill/Desktop/')
        filename = response.meta['filename']
        line = response.meta['line']
        print(response.meta['count'])
        if int(response.meta['count']) > 1:
            for span in spans[0:51]:
                print(response.meta['queryword'] + "222222")
                querywords = str(response.meta['queryword']).split(" ")
                title = span.xpath('string(.)').extract()[0]
                flag = False
                for queryword in querywords:
                    if re.search(queryword, title) is not None:
                        flag = True
                if not flag:
                    break
                else:
                    with open(filename, "a+") as file:
                        line += 1
                        print(line)
                        file.write(str(line) + '.')
                        file.write(title)
                        file.write(span.xpath('//tr[@class = "datatr"]/td/a/@href').extract()[line % 50 - 1])
                        file.write("\n")
                        file.close()
            next_page = response.xpath(
                '//div[@class = "fy l"]/div[@class= "fynr"]/div[@id = "nextpage2"]/a/@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(url=next_page,
                                     meta={'number': response.meta['number'] - 50,
                                           'filename': filename,
                                           'line': line,
                                           'count': int(int(response.meta['count']) - 1),
                                           'queryword': response.meta['queryword']},
                                     callback=self.parse)
        elif response.meta['count'] == 1:
            for span in spans[0:response.meta['number']]:
                print(response.meta['queryword'] + '22222222')
                querywords = str(response.meta['queryword']).split(" ")
                title = span.xpath('string(.)').extract()[0]
                flag = False
                for queryword in querywords:
                    if re.search(queryword, title) is not None:
                        flag = True
                if not flag:
                    break
                else:
                    with open(filename, "a+") as file:
                        line += 1
                        print(line)
                        file.write(str(line) + '.')
                        file.write(span.xpath('string(.)').extract()[0])
                        file.write(span.xpath('//tr[@class = "datatr"]/td/a//@href').extract()[line % 50 - 1])
                        file.write("\n")
                        file.close()
