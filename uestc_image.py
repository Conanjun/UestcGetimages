#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/16 16:57
# @Author  : Conan
# @Function: get image from uestc
import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Cookie': 'input your cookie here',
    'Host': 'yjsjy.uestc.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
}


# 创建一个student_id生成器
def generate_student_id(grade='2017', institute='2206', iclass='0522', count=50):
    """
    :param grade 
    :param institute
    :param iclass
    :return: a student id
    """
    current_count = 1
    while current_count <= count:
        yield grade + institute + iclass + "%02d" % current_count
        current_count = current_count + 1


# 根据grade institute iclass创建文件夹
import os

current_dir_path = os.path.dirname(os.path.abspath(__file__))


def mkdir_for_pic(grade='2017', institute='2206', iclass='05'):
    """
    :param grade
    :param institute
    :param iclass
    :return: dir path
    """
    if os.path.exists(current_dir_path + '/images/' + grade):
        if os.path.exists(current_dir_path + '/images/' + grade + '/' + institute):
            if os.path.exists(current_dir_path + '/images/' + grade + '/' + institute + '/' + iclass):
                return current_dir_path + '/images/' + grade + '/' + institute + '/' + iclass
            else:
                os.mkdir(current_dir_path + '/images/' + grade + '/' + institute + '/' + iclass)
                return current_dir_path + '/images/' + grade + '/' + institute + '/' + iclass
        else:
            os.mkdir(current_dir_path + '/images/' + grade + '/' + institute)
            os.mkdir(current_dir_path + '/images/' + grade + '/' + institute + '/' + iclass)
            return current_dir_path + '/images/' + grade + '/' + institute + '/' + iclass
    else:
        os.mkdir(current_dir_path + '/images/' + grade)
        os.mkdir(current_dir_path + '/images/' + grade + '/' + institute)
        os.mkdir(current_dir_path + '/images/' + grade + '/' + institute + '/' + iclass)
        return current_dir_path + '/images/' + grade + '/' + institute + '/' + iclass


def work(baseurl='http://yjsjy.uestc.edu.cn/pyxx/grxx/xszphd/zp/xj/', grade='2017', institute='2206', iclass='05'):
    for i in generate_student_id(grade, institute, iclass):
        pic = requests.get(baseurl + i, headers=headers)
        if len(pic.content)<=4*1024:
            continue
        temp_dir = mkdir_for_pic(grade, institute, iclass)
        print temp_dir + '/' + i + '.jpg'
        temp_pic_file = open(temp_dir + '/' + i + '.jpg', 'wb')
        # print pic.content
        temp_pic_file.write(pic.content)
        temp_pic_file.close()

if __name__ == '__main__':
    # 11经管 12政管 13外国语 06计院 01通信
    institutes = ['2101','2201','2211', '2111', '2213', '2113', '2206', '2126', '2226', '2126','2212','2112']
    iclass = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']
    for i in institutes:
        for j in iclass:
            work(grade='2017', institute=i, iclass=j)
