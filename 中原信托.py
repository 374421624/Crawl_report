# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 14:20:24 2018

@author: 崔
"""



# 爬取目录页面-公告对应的网址
from urllib import request
from bs4 import BeautifulSoup
import re
import time
import os


# 使用代理解析页面函数
def gethtmltext(url):
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    req = request.Request(url, headers = head)
    response = request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, 'lxml')
    return soup

# 爬取内容存入文件
def input_file(download_soup_texts,f,each_company):
    print('正在保存的报告————>' + each_company['name'])
    f.write(download_soup_texts)

def file_exist():
    #创建文本文件夹
    if not os.path.exists('F:/中原信托管理报告'):
        os.mkdir('F:/中原信托管理报告')
    with open('F:/中原信托管理报告/num.txt','a',encoding = 'utf-8') as a: # 初次运行，创建页面记录文件，方便下次运行
        a.write("")
    with open('F:/中原信托管理报告/num.txt','r',encoding = 'utf-8') as a:
        out_num = a.read()
    if out_num == '':
        out_num = 0
    out_num = int(out_num) 
    # 读取页面记录
    if (int(out_num)>=n):  # 走到最后一页，跳回第一页，方便检查更新
        out_num = 0
        print('检查前三页是否存在更新：')
    out_num = int(out_num) # 将读出页面值字符串化为整形
    return out_num   

# 输出报告到文件函数
def output(before,num):
    for every_page in range(before,num):
        print('正在保存第'+str(every_page+1)+'页：')
        # 报告目录对应网址
        url = 'http://www.zyxt.com.cn/product.php?fid=25&fup=3&pageid='+str(every_page+1)
        soup = gethtmltext(url)
        # 找到报告对应标签并爬取所有的报告
        soup_texts = soup.find('ul',class_='jList fadeUp')
        soup_texts = soup_texts.find_all('a')
        # 报告网址字典
        report_urls = {}
        # 对报告目录页循环访问并打印名称及网址
        for each in range(0,len(soup_texts),2):
            # 每个报告对应网址
            download_url = 'http://www.zyxt.com.cn/'+soup_texts[each].get('href')
            download_soup = gethtmltext(download_url)
            each_company = {}
            # 获取每个报告标题
            each_company['name'] = soup_texts[each].get_text()
            #print(each_company['name'])
            # 筛选出管理报告形成报告标题列表
            report_name = re.findall(r'.*?管理报告.*?',each_company['name'])
            #print(report_name)
            # 报告列表不空，将报告网址存入网址记录文件
            if report_name!=[]:
                tilte_files = open('F:/中原信托管理报告/网址记录.txt','a+',encoding = 'utf-8')
                tilte_files.seek(0) # 回到文件开头
                tilte_files_urls = tilte_files.read() #读取文件每一行
                report_urls['url'] = download_url
                # 匹配网址记录文件中已有网址，若没有则爬取并添加新的网址至网址文件
                if report_urls['url'] not in tilte_files_urls:
                    tilte_files.write(report_urls['url'])
                    tilte_files.write('\n')
                    tilte_files.close()
                    # 获取文本发布时间
                    # download_time = download_soup.find('h5')
                    # download_time = download_time.get_text()
                    # 获取文本内容
                    download_soup_texts = download_soup.find('div',class_ = 'article')
                    download_soup_texts = download_soup_texts.get_text()
                    #打开文件，并以报告名称命名
                    report_files = open('F:/中原信托管理报告/'+ each_company['name'] +'.txt','w',encoding = 'utf-8')
                    # 存入文件函数
                    input_file(download_soup_texts,report_files,each_company)
                    report_files.close()
                    time.sleep(0)
        with open('F:/中原信托管理报告/num.txt','w',encoding = 'utf-8') as f: # 每次把爬取的当前页码存到页面记录文件中
            f.write(str(every_page+1)) 

# 主函数
if __name__ == '__main__':
    # 目录页数
    n=478
    out_num = file_exist()
    output(out_num,n)
    print('请将主函数中n值改为3，方便检查是否存在更新，若已是3，请不必更改！')
    print('请将主函数中n值改为3，方便检查是否存在更新，若已是3，请不必更改！')
    print('请将主函数中n值改为3，方便检查是否存在更新，若已是3，请不必更改！')
