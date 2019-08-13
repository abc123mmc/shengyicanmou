# -*- coding: utf-8 -*-
#market Ranking#市场排行
#BusinessStaff>>BS生意参谋
#类：首字母大写，每个单词首字母大写（大驼峰命名法）
#方法：首字母小写，之后每个单词首字母都大写(小驼峰法命名法)
#变量b_variableName :b_加首字母小写，之后每个单词首字母都大写
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


class BS_Compete(currency.BS_currency):#生意参谋_市场
    def __init__(self,driver):
        #super(BS_Flow,self).__init__(driver)
        super().__init__(driver)#和上一句效果一样

    def goToCompete(self):#进入市场
        self.click1('ul[class="menu-list clearfix"]>li','市场')
        #['首页', '实时', '作战室', '', '流量', '品类', '交易', '内容', '服务', '营销', '物流', '财务', '', '市场', '竞争', '', '业务专区', '', '取数', '学院']
        try:
            for i in range(3):
                self.driver.find_element_by_css_selector('#flow-v3-new-guide>div>div>div>a').click()
        except:pass#对弹出流量纵横全新升级弹框的点击

    def competitionAnalysis(self):#市场分析competitionAnalysis
        self.click1('div>ul[class="menuList"] span','市场排行')
        time.sleep(3)
        li=self.getCategory()
        for i in li:
            self.driver.find_element_by_css_selector('.ebase-FaCommonFilter__top>div:nth-child(1)>div').click()
            input1=self.driver.find_element_by_css_selector('.ebase-FaCommonFilter__top input')
            input1.send_keys(i)
            time.sleep(2)
            input1.send_keys(Keys.ENTER)
            time.sleep(5)
            self.shopHighTrading(i)#店铺高交易
            self.shopHighFlow(i)#店铺高流量
            self.highCommodityTrading(i)#商品高交易
            self.highCommodityFlow(i)#商品高流量
            self.highCommodityIntention(i)#商品高意向
            self.brandHighTrading(i)#品牌高交易
            self.brandHighFlow(i)#品牌高流量

    def getCategory(self):#获取类目
        dl=self.driver.find_elements_by_css_selector('.ebase-FaCommonFilter__top ul:nth-child(2)>li')
        li=[]
        for j in range(len(dl)):
            self.driver.find_element_by_css_selector('.ebase-FaCommonFilter__top>div:nth-child(1)>div').click()
            self.driver.find_elements_by_css_selector('.ebase-FaCommonFilter__top ul:nth-child(2)>li')[j].click()
            self.driver.find_element_by_css_selector('.ebase-FaCommonFilter__top>div:nth-child(1)>div').click()
            li+=self.driver.find_element_by_css_selector('.common-picker-menu ul').text.split('\n')
            self.driver.find_elements_by_css_selector('.ebase-FaCommonFilter__top ul:nth-child(2)>li')[j].click()
            time.sleep(2)
        return li

    def shopHighTrading(self,i):#店铺高交易
        self.click1('.ebase-FaCommonFilter__bottom .ebase-Switch__item','店铺')
        self.click1('span.oui-tab-switch>span','高交易')
        time.sleep(5)
        self.driver.find_element_by_css_selector('#showPage').click()#一键转化
        time.sleep(1)
        self.driver.find_element_by_css_selector('#demo_wrapper  button[class*="csv"]').click()#导出
        time.sleep(2)
        self.driver.find_element_by_css_selector(' span> a[class*="close"]').click()#关闭
        j='./xiazai'+'\\'+os.listdir('xiazai')[0]
        data =open(j,encoding='utf-8')
        data=[eval(i[:-1]) if '\n' in i[-1] else eval(i) for i in data.readlines()[1:]]
        data=[[j[2]+i+j[1],j[0]]+list(j[3:]) for j in data]
        t='%s-%s-%s'%time.localtime()[:3]
        l02=['排名类目日期','店铺信息', '交易金额','交易增长幅度','支付转化率']
        b=currency.mysqlwei()
        sql=b.sql01('shopHighTrading',l02)
        try:b.addDelUpd(sql)
        except:pass
        sql="insert into shopHighTrading values(%s,%s,%s,%s,%s)"
        for l03 in data:
            try:b.addDelUpd(sql,l03)
            except:print(l03)
        shutil.rmtree("xiazai")
        b.con.close()

    def shopHighFlow(self,i):#店铺高流量
        self.click1('.ebase-FaCommonFilter__bottom .ebase-Switch__item','店铺')
        self.click1('span.oui-tab-switch>span','高流量')
        time.sleep(3)
        self.driver.find_element_by_css_selector('#showPage').click()#一键转化
        time.sleep(1)
        self.driver.find_element_by_css_selector('#demo_wrapper  button[class*="csv"]').click()#导出
        time.sleep(2)
        self.driver.find_element_by_css_selector(' span> a[class*="close"]').click()#关闭
        j='./xiazai'+'\\'+os.listdir('xiazai')[0]
        data =open(j,encoding='utf-8')
        data=[eval(i[:-1]) if '\n' in i[-1] else eval(i) for i in data.readlines()[1:]]
        data=[[j[2]+i+j[1],j[0]]+list(j[3:]) for j in data]
        t='%s-%s-%s'%time.localtime()[:3]
        l02=['排名类目日期','店铺信息','访客人数','搜索人数','搜索占比','交易金额','uv价值']
        b=currency.mysqlwei()
        sql=b.sql01('shopHighFlow',l02)
        try:b.addDelUpd(sql)
        except:pass
        sql="insert into shopHighFlow values(%s,%s,%s,%s,%s,%s,%s)"
        for l03 in data:
            try:b.addDelUpd(sql,l03)
            except:print(l03)
        shutil.rmtree("xiazai")
        b.con.close()

    def highCommodityTrading(self,i):#商品高交易
        self.click1('.ebase-FaCommonFilter__bottom .ebase-Switch__item','商品')
        self.click1('span.oui-tab-switch>span','高交易')
        time.sleep(3)
        self.driver.find_element_by_css_selector('#showPage').click()#一键转化
        time.sleep(1)
        self.driver.find_element_by_css_selector('#demo_wrapper  button[class*="csv"]').click()#导出
        time.sleep(2)
        self.driver.find_element_by_css_selector(' span> a[class*="close"]').click()#关闭
        j='./xiazai'+'\\'+os.listdir('xiazai')[0]
        data =open(j,encoding='utf-8')
        data=[eval(i[:-1]) if '\n' in i[-1] else eval(i) for i in data.readlines()[1:]]
        data=[[j[4]+i+j[3],j[1],j[2]]+list(j[5:]) for j in data]
        t='%s-%s-%s'%time.localtime()[:3]
        l02=['排名类目日期','店铺名','商品ID','交易金额','交易增长幅度','支付转化率']
        b=currency.mysqlwei()
        sql=b.sql01('highCommodityTrading',l02)
        try:b.addDelUpd(sql)
        except:pass
        sql="insert into highCommodityTrading values(%s,%s,%s,%s,%s,%s)"
        for l03 in data:
            try:b.addDelUpd(sql,l03)
            except:print(l03)
        shutil.rmtree("xiazai")
        b.con.close()

    def highCommodityFlow(self,i):#商品高流量
        self.click1('.ebase-FaCommonFilter__bottom .ebase-Switch__item','商品')
        self.click1('span.oui-tab-switch>span','高流量')
        time.sleep(3)
        self.driver.find_element_by_css_selector('#showPage').click()#一键转化
        time.sleep(1)
        self.driver.find_element_by_css_selector('#demo_wrapper  button[class*="csv"]').click()#导出
        time.sleep(2)
        self.driver.find_element_by_css_selector(' span> a[class*="close"]').click()#关闭
        j='./xiazai'+'\\'+os.listdir('xiazai')[0]
        data =open(j,encoding='utf-8')
        data=[eval(i[:-1]) if '\n' in i[-1] else eval(i) for i in data.readlines()[1:]]
        data=[[j[4]+i+j[3],j[1],j[2]]+list(j[5:]) for j in data]
        t='%s-%s-%s'%time.localtime()[:3]
        l02=['排名类目日期','店铺名','商品ID','访客人数','搜索人数','搜索占比','交易金额','uv价值']
        b=currency.mysqlwei()
        sql=b.sql01('highCommodityFlow',l02)
        try:b.addDelUpd(sql)
        except:pass
        sql="insert into highCommodityFlow values(%s,%s,%s,%s,%s,%s,%s,%s)"
        for l03 in data:
            try:b.addDelUpd(sql,l03)
            except:print(l03)
        shutil.rmtree("xiazai")
        b.con.close()

    def highCommodityIntention(self,i):#商品高意向
        self.click1('.ebase-FaCommonFilter__bottom .ebase-Switch__item','商品')
        self.click1('span.oui-tab-switch>span','高意向')
        time.sleep(3)
        self.driver.find_element_by_css_selector('#showPage').click()#一键转化
        time.sleep(1)
        self.driver.find_element_by_css_selector('#demo_wrapper  button[class*="csv"]').click()#导出
        time.sleep(2)
        self.driver.find_element_by_css_selector(' span> a[class*="close"]').click()#关闭
        j='./xiazai'+'\\'+os.listdir('xiazai')[0]
        data =open(j,encoding='utf-8')
        data=[eval(i[:-1]) if '\n' in i[-1] else eval(i) for i in data.readlines()[1:]]
        data=[[j[4]+i+j[3],j[1],j[2]]+list(j[5:]) for j in data]
        t='%s-%s-%s'%time.localtime()[:3]
        l02=['排名类目日期','店铺名','商品ID','收藏人数','加购人数','交易金额']
        b=currency.mysqlwei()
        sql=b.sql01('highCommodityIntention',l02)
        try:b.addDelUpd(sql)
        except:pass
        sql="insert into highCommodityIntention values(%s,%s,%s,%s,%s,%s)"
        for l03 in data:
            try:b.addDelUpd(sql,l03)
            except:print(l03)
        shutil.rmtree("xiazai")
        b.con.close()

    def brandHighTrading(self,i):#品牌高交易
        self.click1('.ebase-FaCommonFilter__bottom .ebase-Switch__item','品牌')
        self.click1('span.oui-tab-switch>span','高交易')
        time.sleep(3)
        self.driver.find_element_by_css_selector('#showPage').click()#一键转化
        time.sleep(1)
        self.driver.find_element_by_css_selector('#demo_wrapper  button[class*="csv"]').click()#导出
        time.sleep(2)
        self.driver.find_element_by_css_selector(' span> a[class*="close"]').click()#关闭
        j='./xiazai'+'\\'+os.listdir('xiazai')[0]
        data =open(j,encoding='utf-8')
        data=[eval(i[:-1]) if '\n' in i[-1] else eval(i) for i in data.readlines()[1:]]
        data=[[j[2]+i+j[1],j[0]]+list(j[3:]) for j in data]
        t='%s-%s-%s'%time.localtime()[:3]
        l02=['排名类目日期','品牌信息','交易金额','交易增长幅度','支付转化率']
        b=currency.mysqlwei()
        sql=b.sql01('brandHighTrading',l02)
        try:b.addDelUpd(sql)
        except:pass
        sql="insert into brandHighTrading values(%s,%s,%s,%s,%s)"
        for l03 in data:
            try:b.addDelUpd(sql,l03)
            except:print(l03)
        shutil.rmtree("xiazai")
        b.con.close()

    def brandHighFlow(self,i):#品牌高流量
        self.click1('.ebase-FaCommonFilter__bottom .ebase-Switch__item','品牌')
        self.click1('span.oui-tab-switch>span','高流量')
        time.sleep(3)
        self.driver.find_element_by_css_selector('#showPage').click()#一键转化
        time.sleep(1)
        self.driver.find_element_by_css_selector('#demo_wrapper  button[class*="csv"]').click()#导出
        time.sleep(2)
        self.driver.find_element_by_css_selector(' span> a[class*="close"]').click()#关闭
        j='./xiazai'+'\\'+os.listdir('xiazai')[0]
        data =open(j,encoding='utf-8')
        data=[eval(i[:-1]) if '\n' in i[-1] else eval(i) for i in data.readlines()[1:]]
        data=[[j[2]+i+j[1],j[0]]+list(j[3:]) for j in data]
        t='%s-%s-%s'%time.localtime()[:3]
        l02=['排名类目日期','品牌信息','访客人数','搜索人数','搜索占比','交易金额','uv价值']	
        b=currency.mysqlwei()
        sql=b.sql01('brandHighFlow',l02)
        try:b.addDelUpd(sql)
        except:pass
        sql="insert into brandHighFlow values(%s,%s,%s,%s,%s,%s,%s)"
        for l03 in data:
            try:b.addDelUpd(sql,l03)
            except:print(l03)
        shutil.rmtree("xiazai")
        b.con.close()

    def mian(self):
        self.goToBS()
        self.goToCompete()
        self.competitionAnalysis()

if __name__=='__main__':
    driver=currency.starUpChrome()
    b=BS_Compete(driver.driver)
    #b.mian()
    pass

'''
if 1:
    #s='shopHighTrading'#店铺高交易
    #s='shopHighFlow'#店铺高流量
    #s='highCommodityTrading'#商品高交易
    s='highCommodityFlow'#商品高流量
    #s='highCommodityIntention'#商品高意向
    #s='brandHighTrading'#品牌高交易
    #s='brandHighFlow'#品牌高流量
    e=currency.mysqlwei()
    e.cur.execute('desc %s'%s)
    lie=e.cur.fetchall()[0][0]#第一列名
    sql="select * from %s where %s like '%%2019-07-%%'  order by %s+0 desc"%(s,lie,lie)
    #sql="select * from %s where %s like '%%2019-07-%%'"%(s,lie)
    hang=e.sel(sql)
    print(len(hang))
    for i1 in hang[0]:
        print(i1)
'''
#e.cur.execute('drop database bs_data_qplxbqjd')
    

