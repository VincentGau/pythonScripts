#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
给win10锁屏壁纸文件夹下的所有文件加上jpg后缀名，并保存；
"""

import os
import shutil
import getpass
from PIL import Image

# assets原始地址
assets_path = r'C:\Users\%s\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets' % getpass.getuser()
# 临时存放地址
temp_dir = r'C:\Users\%s\Desktop\AssetsTmp' % getpass.getuser()
# 最终保存图片的地址
pic_zone = r'C:\Wallpaper'
# 不保存小于save_size（KB）的图片
save_size = 400


def copy_to_temp():
    """
    将Assets文件夹复制到临时路径

    :return:
    """
    if os.path.exists(temp_dir):
        print(f'{temp_dir} 临时文件夹已存在，先删除')
        shutil.rmtree(temp_dir)

    print("开始复制文件夹")
    shutil.copytree(assets_path, temp_dir)
    print("复制文件夹完成")


def rename():
    """
    对临时文件夹中的文件增加jpg后缀

    :return:
    """
    for parent, dirname, filenames in os.walk(temp_dir):
        print(len(filenames))
        for filename in filenames:
            print(os.path.join(parent, filename), parent)
            s = Image.open(os.path.join(parent, filename)).size
            print(s[0], s[1])
            new_name = filename + '.jpg'
            if s[0] < s[1]:
                new_name = 'm_' + new_name
            os.rename(os.path.join(parent, filename), os.path.join(parent, new_name))


def del_temp():
    """
    删除临时文件夹

    :return:
    """
    shutil.rmtree(temp_dir)
    print("删除临时文件夹")


def filter_by_size():
    """
    临时文件夹中大于400KB的图片复制到图片文件夹

    :return:
    """
    for parent, dirname, filenames in os.walk(temp_dir):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            print(file_path)
            print(os.path.getsize(file_path)/1024)
            if os.path.getsize(file_path)/1024 > save_size:
                shutil.copy(file_path, pic_zone)


copy_to_temp()
rename()
filter_by_size()
del_temp()
