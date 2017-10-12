#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/16 16:57
# @Author  : Conan
# @Function: get image from uestc
import requests
import threadpool

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=C2DA8E66445DFFDC27CF74A1021AC7DD; __utma=108824541.1856663078.1500194228.1504672805.1505364276.5; __utmz=108824541.1505364276.5.5.utmcsr=idas.uestc.edu.cn|utmccn=(referral)|utmcmd=referral|utmcct=/authserver/login; UM_distinctid=15e41572e5c9-0d85ba8c874ceb8-40544130-15f900-15e41572e5d168; iPlanetDirectoryPro=AQIC5wM2LY4SfcwEbLQyY7RfjphR6SQclTTGQYl2D6CqnXs%3D%40AAJTSQACMDE%3D%23',
    'Host': 'yjsjy.uestc.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
}


# 创建一个student_id生成器
def generate_student_id(grade='2017', institute='2206', iclass='0522', count=99):
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
        print i
        pic = requests.get(baseurl + i, headers=headers,timeout=3)
        if len(pic.content)<=4*1024: 
            continue
        temp_dir = mkdir_for_pic(grade, institute, iclass)
        print temp_dir + '/' + i + '.jpg'
        temp_pic_file = open(temp_dir + '/' + i + '.jpg', 'wb')
        # print pic.content
        temp_pic_file.write(pic.content)
        temp_pic_file.close()

if __name__ == '__main__':
    prefix=['52','21','22']
    institute=['01','02','03','04','05','06','07','08','09','10','11','12','13','16','17','18','19','21','22','24','26','31']

    prefix_institute=[i+j for i in prefix for j in institute]

    # 01 通信 02 电工 03 威固 04 物电 05 光电 06 计算机 07 自动化 08 机电 09 生命 10 数学 11经管 12 征管 13 外国语 16 马原 17能源 18 资环 19 航空 21 医学院 22 信软 24 电科 26抗干扰 31 基础
    iclass = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11','12','13','14','15','16','17','18','19','20']

    pool=threadpool.ThreadPool(10)
    par_list=[('2017',None),(prefix_institute,None),(iclass,None)]
    thread_requests = threadpool.makeRequests(work, par_list) 
    [pool.putRequest(req) for req in requests] 
    pool.wait()

    # for i in prefix_institute:
    #     for j in iclass:
    #         work(grade='2017', institute=i, iclass=j)
