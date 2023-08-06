#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : RyanSu
# @Filename : __init__.py
# @Mailto   : i@suruifu.com
# @Website  : https://www.suruifu.com/
import re
import json
from urllib.parse import unquote
import os
import sys
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import utils
import requests


class Book:
    """图书馆图书"""
    item_prefix = ["cov", "bok", "leg", "fow", "!", "", "att", "cov"]
    item_description = ["封面", "书名", "版权", "前言", "目录", "正文", "附录", "封底"]
    zeros_number = [3, 3, 3, 3, 5, 6, 3, 3]

    def __init__(self, isbn=None, marc_no=None):
        """设置isbn"""
        try_time = 0
        while True:
            try:
                if not isbn:
                    url_detail = 'http://202.119.70.22:888/opac/item.php?marc_no=%s' % marc_no
                    doc_detail = self.request_url_until_200(url_detail).text
                    regex = r"ISBN=(.*)?';"
                    self.isbn = re.findall(regex, doc_detail)[0]
                else:
                    self.isbn = isbn
                bid = self.get_bid(self.isbn)
                url_reader = self.get_reader_url(bid)
                meta_data = self.get_meta_from_reader(url_reader)
                self.title = meta_data[0]
                self.url_base = meta_data[1]
                self.page_number = meta_data[2]
                break
            except:
                try_time = try_time + 1
                if try_time > 3:
                    break
                else:
                    continue

    def download(self):
        """下载所有图片"""
        # 清理先前的遗留文件
        if not os.path.exists('downloads'):
            os.mkdir('downloads')
        directory = 'downloads/' + self.title
        os.mkdir(directory)

        for item in range(8):
            if self.page_number[item] == '0':
                print('下载：%s页\t0/0' % self.item_description[item])
            else:
                for page in range(1, int(self.page_number[item]) + 1):
                    page_name = self.item_prefix[item] + str(page).zfill(self.zeros_number[item]) + '.jpg'
                    page_uri = self.url_base + page_name
                    with open(os.path.join(directory, page_name), 'ab') as f:
                        while True:
                            binary = self.request_url_until_200(page_uri).content
                            if len(binary) > 400:
                                break
                        f.write(binary)
                    f.close()
                    sys.stdout.write("\r下载：{}页\t{}/{}".
                                     format(self.item_description[item], str(page), self.page_number[item]))
                sys.stdout.write("\n")
        print("本书下载完成")

    def generate_pdf(self, grid=False, line_width=1.0, line_color='#a3b7d3', grid_length=24):
        width, height = landscape(A3)
        if grid:
            width = width * 3 / 4
        c = canvas.Canvas("%s.pdf" % self.title, pagesize=(width, height))
        for item in range(8):
            if self.page_number[item] == '0':
                print('转换：%s页\t0/0' % self.item_description[item])
            else:
                for page in range(1, int(self.page_number[item]) + 1):
                    # 绘制方格
                    if grid:
                        x, y = 0, 0
                        c.setLineWidth(line_width)
                        c.setStrokeColor(line_color)
                        while x <= width:
                            c.line(x, 0, x, height)
                            x = x + grid_length
                        while y <= height:
                            c.line(0, y, width, y)
                            y = y + grid_length
                    # 绘制图片
                    file_name = self.item_prefix[item] + str(page).zfill(self.zeros_number[item]) + '.jpg'
                    directory = 'downloads/' + self.title
                    image_path = os.path.join(directory, file_name)
                    image = utils.ImageReader(image_path)
                    image_width, image_height = image.getSize()
                    aspect = image_height / float(image_width)
                    c.drawImage(image, 0, 0, height / aspect, height)
                    c.showPage()
                    sys.stdout.write("\r转换：{}页\t{}/{}".
                                     format(self.item_description[item], str(page), self.page_number[item]))
                sys.stdout.write("\n")
        c.save()
        print("PDF转换完成")

    def get_bid(self, isbn):
        """根据isbn获取BID"""
        url_bid = 'http://202.119.70.51:8088/servlet/isExitJson?&isbn=%s' % isbn
        jsonstr_bid = self.request_url_until_200(url_bid).text[5:-3]
        json_bid = json.loads(jsonstr_bid)
        return json_bid['ssid']

    def get_reader_url(self, bid):
        """根据bid获取阅读界面url"""
        url_get_cookie = "http://202.119.70.51:8088/markbook/guajie.jsp?BID=%s" % bid
        JSESSIONID = self.request_url_until_200(url_get_cookie).cookies['JSESSIONID']
        url_get_reader = 'http://202.119.70.51:8088/getbookread?' \
                         'BID=%s&ReadMode=0&jpgread=0' \
                         '&displaystyle=0&NetUser=&page=' % bid
        doc_get_reader = self.request_url_until_200(url_get_reader, {"JSESSIONID": JSESSIONID}).text
        return 'http://202.119.70.51:8088' + unquote(doc_get_reader)

    def get_meta_from_reader(self, url_reader):
        """在阅读界面获得图书元信息"""
        doc_reader = self.request_url_until_200(url_reader).text
        # URL模板
        url_base = re.findall(r"var str='(.*)';", doc_reader)[0]
        # 各部分的页数
        page_number_content = re.findall(r"epage = (.*);", doc_reader)[0]
        page_number_temp = re.findall(r"pages :(.*)?,", doc_reader)[0]
        page_number = re.findall(r"\[.*?,(.*?)]", page_number_temp)
        page_number[5] = page_number_content
        # 标题
        title = re.findall(r"<title>(.*?)</title>", doc_reader)[0]
        return [title, url_base, page_number]

    @staticmethod
    def request_url_until_200(url, cookies={}):
        while True:
            try:
                return requests.get(url, cookies=cookies)
            except:
                continue

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
