import time
import requests
import json
import jsonpath
import pymysql

class intangible_cultural_heritage(object):

    def __init__(self, pagenum):
        self.url = 'https://www.ihchina.cn/getProject.html?province=&rx_time=&type=&cate=&keywords=&category_id=16&limit=10&p={}'.format(pagenum)
        self.headers = {'User-Agent':' '} # 输入浏览器 f12 中的 user-agent
        self.query = ['$..list..title', '$..list..type', '$..list..protect_unit', '$..list..province']

    def get_url(self):
        response = requests.get(self.url, headers=self.headers)
        response.encoding = 'utf8'
        data_dict = json.loads(response.content.decode())
        data_raw = [jsonpath.jsonpath(data_dict, i) for i in self.query]
        return data_raw

    def parse_data(self, data_raw):
        group = zip(data_raw[0], data_raw[1], data_raw[2], data_raw[3])
        return [i for i in group]

    def write_to_mysql(self,data):
        conn = pymysql.connect(
            host='',
            port=,
            user='',
            password='',
            database='',
            charset='utf8'
        )
        try:
            cur = conn.cursor()
            for i in data:
                sql = "insert into intangible_cultural_heritage (title, type, protect_unit, province) values (%s, %s, %s, %s)"
                cur.execute(sql, (i[0], i[1], i[2], i[3]))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def main(self):
        data = self.get_url()
        result = self.parse_data(data)
        self.write_to_mysql(result)
        time.sleep(0.1)


if __name__ == '__main__':
    for i in range(1, 362):
        feiyi = intangible_cultural_heritage(i)
        feiyi.main()
        print(f'正在写入第{i}页')
