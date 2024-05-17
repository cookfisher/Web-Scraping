"""
通过requests获取音频数据保存到本地
https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1646.mp3
https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1645.mp3
https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1643.mp3
https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1642.mp3
https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1641.mp3
"""

import requests
import threading

class ThreadSpider(threading.Thread):
    def __init__(self, url, file_path):
        super().__init__()
        self.url = url
        self.file_path = file_path

    def run(self):
        print(f'start download: {self.url} ')
        response = requests.get(self.url, timeout=10).content
        file_name = self.file_path + self.url.rsplit('/')[-1]
        with open(file_name, 'wb') as f:
            f.write(response)
            print('下载完成...')


url_list = [
        'https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1646.mp3',
        'https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1645.mp3',
        'https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1643.mp3',
        'https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1642.mp3',
        'https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1641.mp3'
    ]

for url in url_list:
    ts = ThreadSpider(url, file_path='.\\download_files\\')
    ts.start()

# import asyncio, requests
# from retrying import retry
#
#
# @retry(stop_max_attempt_number=3)
# async def download_file(loop, url, file_path='.\\download_files\\'):
#     print('start download:', url)
#     # requests不支持异步，使用线程池来辅助实现
#     fut = loop.run_in_executor(None, requests.get, url)
#     response = await fut
#     print('download completed:', url)
#     file_name = file_path + url.rsplit('/')[-1]
#     with open(file_name, 'wb') as f:
#         f.write(response.content)


# if __name__ == '__main__':
#     url_list = [
#         'https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1646.mp3',
#         'https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1645.mp3',
#         'https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1643.mp3',
#         'https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1642.mp3',
#         'https://downsc.chinaz.net/Files/DownLoad/sound1/202303/y1641.mp3'
#     ]
#
#     loop = asyncio.get_event_loop()
#
#     tasks = [loop.create_task(download_file(loop, url)) for url in url_list]
#     # loop.run_until_complete(asyncio.wait(tasks))
#
#     try:
#         loop.run_until_complete(asyncio.wait(tasks))
#     except Exception as e:
#         print('Exception throws:', e)
#     finally:
#         print('Normal')
