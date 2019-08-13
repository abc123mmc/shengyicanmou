# -*- coding: utf-8 -*-
#流量
#BusinessStaff>>BS
import sys, traceback#用于错误处理
import requests
import re,os,shutil
from selenium import webdriver
import time
from random import uniform
import pyperclip#剪切板
from selenium.webdriver.common.by import By#等待加载用
from selenium.webdriver.support.ui import WebDriverWait#等待加载用
from selenium.webdriver.support import expected_conditions as EC#等待加载
import pyautogui
import sqlite3#导入sqlite3数据库模块，python自带模块
from selenium.webdriver.common.action_chains import ActionChains #鼠标操作
from selenium.webdriver.common.keys import Keys#键盘事件
import currency#导入通用包
import xlrd


class BS_Flow(currency.BS_currency):#生意参谋_流量
    def __init__(self,driver):
        #super(BS_Flow,self).__init__(driver)
        super().__init__(driver)#和上一句效果一样

    def goToFlow(self):#进入浏量
        self.click1('ul[class="menu-list clearfix"]>li','流量')
        #['首页', '实时', '作战室', '', '流量', '品类', '交易', '内容', '服务', '营销', '物流', '财务', '', '市场', '竞争', '', '业务专区', '', '取数', '学院']
        try:
            for i in range(3):self.driver.find_element_by_css_selector('#flow-v3-new-guide>div>div>div>a').click()
        except:pass#对弹出流量纵横全新升级弹框的点击

    def shopSource(self):#店铺来源下载和保存
        self.click1('div>ul[class="menuList"] span','店铺来源')
        time.sleep(3)
        self.driver.find_element_by_xpath("//span[text()='1天']/..").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector('div.ebase-FaCommonFilter__right > div:nth-child(2)').click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[text()='PC端']").click()
        time.sleep(2)
        self.shopSource1('PC端')
        self.driver.find_element_by_css_selector('div.ebase-FaCommonFilter__right > div:nth-child(2)').click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[text()='无线端']").click()
        time.sleep(2)
        self.shopSource1('无线端')

    def shopSource1(self,pcwx):#店铺来源下载和保存
        self.driver.find_element_by_xpath("//a/span[text()='下载']").click()
        time.sleep(5)
        j='./xiazai'+'\\'+os.listdir('xiazai')[0]
        data = xlrd.open_workbook(j)
        table = data.sheets()[0]
        nrows = table.nrows
        table_title=table.row_values(5)#6行的列表
        li=[table.row_values(i) for i in range(6,nrows)]#6行后所有行的列表
        t='%s-%s-%s'%time.localtime()[:3]
        l01=[]
        for i in li:
            data={}
            for j in range(1,len(i)):
                if j==1:data['日期来源']=t+pcwx+''.join(i[:2])
                else:data[table_title[j]]=i[j]
            l01.append(data)
        l02=['日期来源','访客数','访客数变化','下单金额','下单金额变化','下单买家数','下单买家数变化','下单转化率','下单转化率变化',
             '支付金额','支付金额变化','支付买家数','支付买家数变化','支付转化率','支付转化率变化','客单价','客单价变化','UV价值',
             'uv价值变化','关注店铺买家数','关注店铺买家数变化','收藏商品买家数','收藏商品买家数变化','加购人数','加购人数变化',
             '新访客','新访客变化','收藏人数','收藏人数变化','跳失率','跳失率变化','浏览量','浏览量变化','人均浏览量','人均浏览量变化',
             '粉丝支付买家数','直接支付买家数','加购商品-支付买家数','收藏商品-支付买家数','访客数环比']
        b=currency.sqlite_weiwei()
        sql=b.sql01('Shop_Flow',l02)
        try:b.addDelUpd(sql)
        except:pass#首次创建表
        l03=[]
        for i in l01:
            l04=[]
            for j in l02:
                if j in i:l04.append(i[j])
                else:l04.append('')
            l03=l03+[l04]
        sql="insert into Shop_Flow values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        l03=[i for i in l03 if re.findall('[1-9]',str(i[1:]))]
        for i in l03:
            try:b.addDelUpd(sql,i)
            except:pass
        shutil.rmtree("xiazai")
        b.conn.close()

    def shuru1(self,i):
        i=str(i)
        self.driver.find_element_by_css_selector('div>div>span>span.ant-input-suffix>i').click()
        time.sleep(0.2)
        e=self.driver.find_element_by_css_selector('div>span>input')
        e.click()
        e.send_keys(i[:5])
        time.sleep(0.3)
        e.send_keys(i[5:])
        e.send_keys(Keys.ENTER)
        time.sleep(1)
        f=self.driver.find_element_by_css_selector('div.oui-typeahead-dropdown>div>span')
        if '暂无数据' in f.text:self.shuru1(i)
        else:f.click()

    def commoditySource(self):#商品来源
        self.click1('div>ul[class="menuList"] span','商品来源')
        time.sleep(3)
        self.driver.find_element_by_xpath("//span[text()='1天']/..").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector('div.ebase-FaCommonFilter__middle > div:nth-child(1) > div').click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[text()='PC端']").click()
        time.sleep(2)
        self.commoditySource1('PC端')
        self.driver.find_element_by_css_selector('div.ebase-FaCommonFilter__middle > div:nth-child(1) > div').click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[text()='无线端']").click()
        time.sleep(2)
        self.commoditySource1('无线端')        

    def commoditySource1(self,pcwx):#商品来源
        with open('parameter.txt','r') as ff:
            f=ff.readlines()
        b=eval(f[0])
        for i in b['流量商品来源id']:
            self.driver.find_element_by_css_selector('div>span[class*="sycm-common-select"]').click()
            time.sleep(0.5)
            self.shuru1(i)
            time.sleep(2)
            self.driver.find_element_by_xpath("//a/span[text()='下载']").click()
            time.sleep(5)
            j='./xiazai'+'\\'+os.listdir('xiazai')[0]
            data = xlrd.open_workbook(j)
            table = data.sheets()[0]
            nrows = table.nrows
            li=[table.row_values(i) for i in range(6,nrows)]#所有的数据行
            table_title=table.row_values(5)#表头行
            t='%s-%s-%s'%time.localtime()[:3]
            l01=[]#所有数据【｛｝，｛｝。。。】
            for k in li:
                data={}
                for j in range(len(k)):#i是一行数据
                    if j==0:data['日期来源']=t+pcwx+'【%s】'% i+k[j]
                    else:data[table_title[j]]=k[j]
                l01.append(data)
            l02=['日期来源','访客数','浏览量','浏览量占比','店内跳转人数','跳出本店人数','收藏人数','加购人数','下单买家数',
            '下单转化率','支付件数','支付买家数','支付金额','支付转化率','直接支付买家数','收藏商品-支付买家数',
            '粉丝支付买家数','加购商品-支付买家数']
            b=currency.sqlite_weiwei()
            sql=b.sql01('commodity_Flow',l02)
            try:b.addDelUpd(sql)
            except:pass#首次创建表
            l03=[]
            for k in l01:
                l04=[]
                for j in l02:
                    if j in k:l04.append(k[j])
                    else:l04.append('')
                l03=l03+[l04]
            sql="insert into commodity_Flow values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            l03=[i for i in l03 if re.findall('[1-9]',str(i[1:]))]
            for i in l03:
                try:b.addDelUpd(sql,i)
                except:pass
            shutil.rmtree("xiazai")
            b.conn.close()

    def mian(self):
        self.goToBS()
        self.goToFlow()
        self.shopSource()
        self.commoditySource()

if __name__=='__main__':
    driver=currency.starUpChrome()
    b=BS_Flow(driver.driver)
'''
if 1:
    conn = sqlite3.connect('BS_Data_qplxbqjd.db')
    cursor = conn.cursor()#创建游标
    sql="select * from commodity_Flow"
    f=cursor.execute(sql)#执行语句
    o=f.fetchall()
'''
