import os
import re
import time

import requests
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue


def download_img(url, download_path):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    img_list = soup.find_all('img', class_='ui image lazy')

    for img in img_list:
        img_url = img.get('data-original')
        img_title = img.get('title')
        print(img_url)
        try:
            with open(download_path + filter_file_name(img_title) + os.path.splitext(img_url)[-1], 'wb') as f:
                f.write(requests.get(img_url).content)
        except Exception as e:
            print(f"Failed. {url}\n{str(e)}")


def filter_file_name(filename):
    return re.sub('[\\\/:\*\?<>|]', '-', filename)


class DownloadThread(Thread):
    def __init__(self, queue, download_path):
        Thread.__init__(self)
        self.queue = queue
        self.download_path = download_path
        if not os.path.exists(download_path):
            os.makedirs(download_path)

    def run(self):
        while True:
            url = self.queue.get()
            try:
                download_img(url, self.download_path)
            finally:
                self.queue.task_done()


if __name__ == '__main__':
    base_url = 'https://fabiaoqing.com/biaoqing/lists/page/{page}.html'
    urls = (base_url.format(page=page) for page in range(1, 201))

    start = time.time()

    queue = Queue()
    download_path = r'D:/emoji/'
    for _ in range(10):
        worker = DownloadThread(queue, download_path)
        worker.daemon = True
        worker.start()

    for url in urls:
        print(url)
        queue.put(url)

    queue.join()

    print(f"共耗时：{time.time() - start}")