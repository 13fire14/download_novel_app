# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 12:05:54 2023

@author: bianca
"""

#%% 爬取小说平台

import streamlit as st
import requests
from lxml import etree
import time
import re
from tqdm import tqdm
import os
st.title('小说免费下载平台')
st.subheader("长篇小说需要一定的下载时间，请耐心等候")
name=st.text_input('请输入小说名字的拼音')
list_name=os.listdir('D:\\novel')
if f'{name}.txt' in list_name:
    st.write('已下载完成，无须再下载')
else:
    # file_name=st.text_input("请输入即将存放的地址")
    # if not file_name:
    #     st.warning('Please input a file.')
    #     st.stop()
    # st.success(f'Thank you for inputting a file. {file_name}\{name}')
    # name='douluodalu'
    #获取小说第一章网址
    novel_url=f'https://www.51shucheng.net/{name}'
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
    resp=requests.get(novel_url,headers=headers)
    resp.encoding='utf_8'
    try:
        url_all=re.findall('<li>.*<a href="(.*)" title=.*</a>',resp.text)
        url=url_all[0]
        st.subheader("当前书城中存在此小说，正在下载")
        for i in tqdm(range(len(url_all))):
            #伪装自己
            headers={
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
            #发出请求访问
            resp=requests.get(url,headers=headers)
            #保证不乱码
            resp.encoding='utf_8'
            #打印网页源代码
            e=etree.HTML(resp.text)
            title=e.xpath('/html/body/div[1]/div[4]/h1/text()')[0]
            info='\n'.join(e.xpath('/html/body/div[1]/div[4]/div[3]/p/text()'))
            
            #获取下一章网址
            url=e.xpath('/html/body/div[1]/div[6]/div[1]/a/@href')[0]
            st.write(f'{i}/{len(url_all)}:{title}')
            time.sleep(0.2)
            # print(info)
            with open(f'D:\\novel\\{name}.txt','a',encoding='utf-8') as f:
                f.write(title+'\n\n'+info+'\n\n')
    except:
        st.write(f"当前书城并没有收录该小说,网址为{novel_url},可查看")
    