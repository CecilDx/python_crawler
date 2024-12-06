import requests
import pandas as pd
import time
from fake_useragent import UserAgent


class xhspgy_crawler(object):

    def __init__(self, pagenum=None, contentTag=None, location=None, gender=None, personalTags=None, cookies=None):
        self.url = 'https://pgy.xiaohongshu.com/api/solar/cooperator/blogger/v2'
        self.cookies = cookies
        self.payload = {
            'contentTag': contentTag,  # 指定爬取的博主笔记类目
            'location': location,  # 指定爬取的博主位置
            'gender': gender,  # 指定爬取的博主性别
            'personalTags': personalTags  # 指定爬取的博主职业
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
        # return res


if __name__ == '__main__':
    pagenum = 1
    contentTag = ["出行旅游"]
    location = ["中国 江苏 南京"]
    gender = '女'
    personalTags = ["摄影师"]
    cookies = {
        "abRequestId": "745969b4-ffa3-5749-a572-8ba7aa1d9922",
        "a1": "190ea2f4d1chaxg5y9nn9z6rhlvjek10kiwb9oo0450000878572",
        "webId": "9ab412cf1a04a8794d50ce2b5f81b4ad",
        "gid": "yj8d0Ji2q8TKyj8d0Ji4f3llySx0Ck2vjIIjE84uKFx1hD28VdTy8j888YWY2WJ8J8Di40qW",
        "web_session": "040069b767298a4e05dded170a354bb9ee1a63",
        "xsecappid": "ratlin",
        "customerClientId": "857418022489424",
        "acw_tc": "0a0d0eb817334707270374496e544835a976e583a368e1c4f62e25eb32d5f6",
        "websectiga": "8886be45f388a1ee7bf611a69f3e174cae48f1ea02c0f8ec3256031b8be9c7ee",
        "sec_poison_id": "873d0317-95e9-413d-8127-e084b2d4abac",
        "customer-sso-sid": "68c517445206141335896043e14f5784c5ed09fa",
        "x-user-id-pgy.xiaohongshu.com": "673488414f00000000000001",
        "solar.beaker.session.id": "1733472139484095230738",
        "access-token-pgy.xiaohongshu.com": "customer.pgy.AT-68c5174452061456247382654kztbcfpsr1kuav8",
        "access-token-pgy.beta.xiaohongshu.com": "customer.pgy.AT-68c5174452061456247382654kztbcfpsr1kuav8"
    }
    crawler = xhspgy_crawler(pagenum=pagenum,
                             contentTag=contentTag,
                             location=location,
                             gender=gender,
                             personalTags=personalTags,
                             cookies=cookies)
    crawler.main()
    # content = crawler.main()
    # print(content)