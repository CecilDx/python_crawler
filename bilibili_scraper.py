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
                       'User-Agent':''}
        self.cookies = {"Cookie":""}

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


