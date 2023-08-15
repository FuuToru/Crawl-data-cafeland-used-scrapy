import scrapy
import re

#Tạo class Item để khởi tạo các trường dữ liệu để khi đổ dữ liệu vô thì nó sẽ đổ vào mấy trường vừa tạo.
class Item(scrapy.Item):
    LoaiDuAn = scrapy.Field()
    TenDuAn = scrapy.Field()
    ChuDauTu = scrapy.Field()
    ViTriToaDo = scrapy.Field()
    DienTich = scrapy.Field()

#Khởi tạo class cào dữ liệu, tạo vòng for để duyệt qua 10 trang đầu tiên
class crawling_data(scrapy.Spider):
    name = "test"
    def start_requests(self):
        url = "https://cafeland.vn/du-an"
        yield scrapy.Request(url=url, callback=self.parse)
        for i in range(2, 11):
            concat_url = url + "/page-" + str(i)
            yield scrapy.Request(url=concat_url, callback=self.parse)

    def parse(self, response):
        for quote in response.xpath('//div/h3/a/@href').getall():
            yield scrapy.Request(
                url=response.urljoin(quote),
                callback=self.parse_author,
            )
    #Cào chi tiết các dữ liệu muốn lấy, do mỗi trường dữ liệu ở mỗi trang có xpath khác nhau nên hiện tại vẫn chưa có hướng giải quyết tốt hơn
    def parse_author(self, response):
        item = Item()
        item['DienTich'] = response.xpath('//tr[1]/td[2]/p/span/span/span[2]/span/span/text()').get()

        if response.xpath('//tr[3]/td[1]/p/span/span/span/span/span/span/text()').get():
            s = response.xpath('//tr[3]/td[1]/p/span/span/span/span/span/span/text()').get()
            item['LoaiDuAn'] = s.replace(": ", "")
        elif response.xpath('//tr[3]/td[1]/p/span/span/span/span/span/span/span/text()').get():
            s = response.xpath('//tr[3]/td[1]/p/span/span/span/span/span/span/span/text()').get()
            item['LoaiDuAn'] = s.replace(": ", "")
        elif response.xpath('// tr[3] / td[1] / p / text()').get():
            s = response.xpath('// tr[3] / td[1] / p / text()').get()
            item['LoaiDuAn'] = s.replace(": ", "")
        elif response.xpath('  // tr[3] / td[1] / p / span / span / text()').get():
            s = response.xpath('  // tr[3] / td[1] / p / span / span / text()').get()
            item['LoaiDuAn'] = s.replace("&nbsp; ", "")
        elif response.xpath('// tr[3] / td[1] / p / span / span / span / span /text()').get():
            s = response.xpath('// tr[3] / td[1] / p / span / span / span / span /text()').get()
            item['LoaiDuAn'] = s.replace(": ", "")
        else:
            s = response.xpath('// tr[3] / td[1] / p / span / span / span / span / span/text()').get()
            item['LoaiDuAn'] = s.replace(": ", "")
        if response.xpath('//tr[4]/td[1]/p/span/span/span/span/text()').get():
            s = response.xpath('//tr[4]/td[1]/p/span/span/span/span/text()').get()
            item['ChuDauTu'] = s.replace(": ", "")
        elif response.xpath('//tr[4]/td[1]/p/span/span/span[2]/span/text()').get():
            s = response.xpath('//tr[4]/td[1]/p/span/span/span[2]/span/text()').get()
            item['ChuDauTu'] = s.replace(": ", "")
        elif response.xpath('//tr[4]/td[1]/p/span/span/span[2]/span/span/text()').get():
            s = response.xpath('//tr[4]/td[1]/p/span/span/span[2]/span/span/text()').get()
            item['ChuDauTu'] = s.replace(": ", "")
        elif response.xpath(' //  tr[4] / td[1] / p[3] / span / span / span / span / span/text()').get() and response.xpath('// tr[4] / td[1] / p[2] / span / span / span / span / span ').get():
            s = response.xpath(' //  tr[4] / td[1] / p[3] / span / span / span / span / span/text()').get()
            item['ChuDauTu'] = s.replace(": ", "")
            s = response.xpath('// tr[4] / td[1] / p[2] / span / span / span / span / span/text() ').get()
            item['ChuDauTu'] += s.replace(": ", "")

        if response.xpath('//tr[1]/td[1]/p/span/span/span/span/span/text()').get():
            s = response.xpath('//tr[1]/td[1]/p/span/span/span/span/span/text()').get()
            item['TenDuAn'] = s.replace(": ", "")
        elif response.xpath('//tr[1]/td[1]/p/span/span/span/span/text()').get() :
            s = response.xpath('//tr[1]/td[1]/p/span/span/span/span/text()').get()
            item['TenDuAn'] = s.replace(": ", "")
        elif response.xpath('//tr[1]/td[1]/p/span/span/text()').get():
            s = response.xpath('//tr[1]/td[1]/p/span/span/text()').get()
            item['TenDuAn'] = s.replace(": ", "")
        s = response.xpath('// *[ @ id = "tab-duan-1"] / div[1] / a/@href').get()
        t = re.findall(r'[0-9]+\.[0-9]+\/[0-9]+\.[0-9]+', s)
        item['ViTriToaDo'] = t[0].replace("/", "-")
        yield item






