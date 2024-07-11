import os
import time
import requests
import re
import json
from moviepy.editor import *


class bilibili_scraper(object):

    def __init__(self, BV):
        self.url = 'https://www.bilibili.com/video/{}/'.format(BV)
        self.header = {'Referer': self.url,
                       'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
        self.cookies = {"Cookie":"buvid3=F197ADA4-DFCC-39C6-4A45-ECC55DEDF34256889infoc; b_nut=1720098956; CURRENT_FNVAL=4048; _uuid=DC83F5FE-35BB-1A102-8642-DFB4BED27B6656472infoc; buvid_fp=29ebe4633dfaa6f047f91621a71d937e; buvid4=CD951564-0156-5A11-E409-17BFF06FCDB457565-024070413-pehBMGu8tP8BJvPpPsBS9w%3D%3D; rpdid=|(u))|lkYYY)0J'u~k||m)ml); b_lsid=E95253C5_190A0EC35FA; bsource=search_bing; bmg_af_switch=1; bmg_src_def_domain=i2.hdslb.com; enable_web_push=DISABLE; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1707-932; SESSDATA=5dc797bb%2C1736238770%2C7b5ec%2A72CjCiNZ_WhfY53Hfd2Uk2aQFdpH5eQhynkxmpzrJU-EKz2D_kVDR_9nUDP7KWkf39jPMSVm8zSzVzVTJLOFlDYWdRRVhUR09nLWpkc3phS0w1LXNnaFlaczFNZ1JHVkY4RlJxaFRBRzlXN2U1czNZT0cxVjd6Zk9xbnlXWnNSWkhCdGtxU3NtZEZBIIEC; bili_jct=d66e9e1232a99556e2cbeeb812caf443; DedeUserID=4422245; DedeUserID__ckMd5=eea32aadb5496aea; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA5NDU5NzgsImlhdCI6MTcyMDY4NjcxOCwicGx0IjotMX0.ojpTrwPmp8PWJ0JaO4RVk9l0ByX0qSmalaZ4hEl8JaY; bili_ticket_expires=1720945918; sid=6d53dg8c"}

    def get_url(self):
        html = requests.get(self.url, headers=self.header, cookies=self.cookies)
        html.encoding = 'utf8'
        return html.content.decode()

    def parse_html(self, html_content):
        post_re_data = re.findall(r'window\.__playinfo__\s*=\s*(.*?)</script>', html_content)[0]
        title = re.findall(r'<title data-vue-meta="true">(.*?)</title>', html_content)[0]
        html_dict = json.loads(post_re_data)
        return html_dict, title

    def get_video(self, json_dict, title):
        video_url = json_dict['data']['dash']['video'][0]["baseUrl"]
        audio_url = json_dict['data']['dash']['audio'][0]["baseUrl"]
        time.sleep(3)
        print('开始下载视频')
        video = requests.get(video_url, headers=self.header, cookies=self.cookies).content
        print('视频下载成功')
        time.sleep(3)
        print('开始下载音频')
        audio = requests.get(audio_url, headers=self.header, cookies=self.cookies).content
        print('音频下载成功')
        with open(title + '.mp4', 'wb') as videof:
            videof.write(video)
        with open(title + '.mp3', 'wb') as audiof:
            audiof.write(audio)
        videoclip = VideoFileClip('{}.mp4'.format(title))
        audioclip = AudioFileClip('{}.mp3'.format(title))
        complete_video = videoclip.set_audio(audioclip)
        complete_video.write_videofile(title + 'bilibili' + '.mp4')
        os.remove('{}.mp4'.format(title))
        os.remove('{}.mp3'.format(title))

    def main(self):
        html_data = self.get_url()
        resource_json, video_title = self.parse_html(html_data)
        self.get_video(resource_json, video_title)


if __name__ == '__main__':
    BV = input('请输入视频 BV 号：')
    wait_to_scraper = bilibili_scraper(BV)
    wait_to_scraper.main()


