import requests
import pandas as pd
import time
from fake_useragent import UserAgent


class xhspgy_crawler(object):

    def __init__(self, pagenum=None, contentTag=None, location=None, gender=None, personalTags=None, cookies=None):
        self.url = 'https://pgy.xiaohongshu.com/api/solar/cooperator/blogger/v2'
        self.cookies = cookies
        self.payload = {
            'contentTag': contentTag,
            'location': location,
            'gender': gender,
            'personalTags': personalTags
        }
        self.headers = {
                'Origin': 'https://pgy.xiaohongshu.com',
                'Referer': 'https://pgy.xiaohongshu.com/solar/pre-trade/note/kol'
        }
        self.page_num = pagenum
        self.columns = ['userId', 'name', 'gender', 'fansNum', 'redId', 'location', 'personalTags', 'businessNoteCount',
                       'picturePrice', 'videoPrice', 'featureTags', 'tradeType', 'clickMidNum', 'interMidNum',
                       'pictureReadCost', 'videoReadCost', 'pictureClickMidNum', 'pictureInterMidNum', 'videoClickMidNum',
                       'videoFinishRate', 'videoInterMidNum', 'fans30GrowthRate', 'fans30GrowthNum', 'fansActiveIn28dLv',
                       'fansEngageNum30dLv', 'hundredLikePercent30', 'thousandLikePercent30', 'pictureHundredLikePercent30',
                       'pictureThousandLikePercent30', 'videoHundredLikePercent30', 'videoThousandLikePercent30',
                       'sellerRealIncomeAmt90d', 'mEngagementNum', 'mEngagementNumMcn']

    def get_page_data(self):
        data_df = pd.DataFrame(columns=self.columns)

        for i in range(1, self.page_num + 1):
            self.headers['user-agent'] = str(UserAgent().Chrome)
            self.payload['pageNum'] = i

            print(f'开始请求第 {i} 页')
            response = requests.post(self.url, headers=self.headers, cookies=self.cookies, json=self.payload)
            print(f'第 {i} 页请求状态为: {response.status_code}')

            response_json = response.json()
            per_page_data_list = response_json['data']['kols']
            per_page_data_parse = self.parse_data(per_page_data_list, i)
            data_df = pd.concat([data_df, per_page_data_parse], ignore_index=True)
            print(f'第 {i} 页数据收集完成')
            time.sleep(2)

        return data_df

    def parse_data(self, data_list, pagenum):
        df = pd.DataFrame(columns=self.columns)
        for i, item in enumerate(data_list):
            print(f'正在处理第 {pagenum} 页的第 {i + 1} 个博主数据')
            new_item_row = {col: f'{item[col]}' for col in self.columns}
            new_df_row = pd.DataFrame(new_item_row, index=[(pagenum - 1) * 20 + i + 1])
            new_df_row['location'] = new_df_row['location'].apply(
                lambda row: ','.join(row.split(' '))
            )
            new_df_row['tradeType'] = new_df_row['tradeType'].apply(
                lambda row: ','.join(row.split(' '))
            )
            new_df_row['personalTags'] = new_df_row['personalTags'].apply(
                lambda row: ','.join(map(lambda x: x.replace("'", ''), row.strip('[]').split(',')))
            )
            new_df_row['featureTags'] = new_df_row['featureTags'].apply(
                lambda row: ','.join(map(lambda x: x.replace("'", ''), row.strip('[]').split(',')))
            )
            df = pd.concat([df, new_df_row], ignore_index=True)
        print(f'该页第一条数据的博主名称为：{df.iloc[0, 1]}')
        print(f'第 {pagenum} 页处理完成')

        return df

    def main(self):
        data_list = self.get_page_data()
        res = pd.concat([data_list])
        res.to_csv('./df.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    pagenum = 1  # 指定爬取几页
    contentTag = ["出行旅游"]  # 指定爬取某个内容类目的博主
    location = ["中国 江苏 南京"]  # 指定爬取某个位置的博主
    gender = '女'  # 指定爬取某个性别的博主
    personalTags = ["摄影师"]  # 指定爬取某个职业的博主
    cookies = {None}  # 登陆后，使用 json 格式的 cookies 替换
    crawler = xhspgy_crawler(pagenum=pagenum,
                             contentTag=contentTag,
                             location=location,
                             gender=gender,
                             personalTags=personalTags,
                             cookies=cookies)
    crawler.main()