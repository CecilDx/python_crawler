import requests
from lxml import etree
import pymysql


class doubantop250(object):

    def __init__(self):
        self.url = 'https://movie.douban.com/top250'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

    # requests 获取网页
    def get_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def in_up_page(self, data):
        html = etree.HTML(data)
        detail_page = html.xpath('//*[@id="content"]/div/div[1]/ol/li//div[@class="pic"]/a/@href')
        try:
            next_url = self.url + html.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href')[0]
        except:
            next_url = None
        return next_url, detail_page

    # xpath 提取 elements
    def get_movie_detail(self, detail_page):
        el_list = []
        n = 0
        for i in detail_page:
            r = self.get_url(i)
            html = etree.HTML(r)
            xpath_sentence = {
                'title': '//*[@id="content"]/h1/span[1]/text()',
                'directors': '//*[@id="info"]/span[1]/span[2]/a/text()',
                'actors': '//div[@id="info"]/span[3]/span[@class="attrs"]/a[position()<4]/text()',
                'genre': '//*[@id="info"]/span[@property="v:genre"]/text()',
                'country': '//span[contains(./text(), "制片国家/地区:")]/following::text()[1]',
                'release_date': '//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()',
                'rating_in_douban': '//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()',
            }
            plain_list = []
            for value in xpath_sentence.values():
                el = html.xpath(value)
                plain_list.append(el)
            el_list.append(plain_list)
            n += 1
            print(f'正在打印第{n}部电影')
        print('25部电影打印成功')
        return el_list

    # 写入 mysql
    def write_into_mysql(self, data):
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='PHX1103p',
            database='requestsproject',
            charset='utf8'
        )
        cur = conn.cursor()
        sql = "insert into doubantop250scraper (title, directors, actors, genre, country, release_date, rating_in_douban) values (%s, %s, %s, %s, %s, %s, %s)"
        try:
            for movie_sum in data:
                cur.execute(sql, ('/'.join(movie_sum[0]),'/'.join(movie_sum[1]),'/'.join(movie_sum[2]),
                                  '/'.join(movie_sum[3]),'/'.join(movie_sum[4]),'/'.join(movie_sum[5]),'/'.join(movie_sum[6])))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    # 运行程序 + 解包
    def main(self):
        n = 0
        info_list = []
        next_url = self.url
        while True:
            if next_url == None:
                break
            else:
                n += 1
                print(f'正在打印第{n}页')
                r = self.get_url(next_url)
                next_url, detail_page = self.in_up_page(r)
                movie_list = self.get_movie_detail(detail_page)
                info_list.append(movie_list)
        unzipped_data = []
        for each in info_list:
            for eachmovie in each:
                unzipped_data.append(eachmovie)
        self.write_into_mysql(unzipped_data)


if __name__ == '__main__':
    infomation = doubantop250()
    print(infomation.main())