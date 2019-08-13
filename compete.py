# -*- coding: utf-8 -*-
#compete竞争
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


class BS_Compete(currency.BS_currency):#生意参谋_竞争
    def __init__(self,driver):
        #super(BS_Flow,self).__init__(driver)
        super().__init__(driver)#和上一句效果一样

    def goToCompete(self):#进入竞争
        self.click1('ul[class="menu-list clearfix"]>li','竞争')
        #['首页', '实时', '作战室', '', '流量', '品类', '交易', '内容', '服务', '营销', '物流', '财务', '', '市场', '竞争', '', '业务专区', '', '取数', '学院']
        try:
            for i in range(3):
                self.driver.find_element_by_css_selector('#flow-v3-new-guide>div>div>div>a').click()
        except:pass#对弹出流量纵横全新升级弹框的点击

    def analysisOfCompetitiveShop(self):#竟店分析AnalysisOfCompetitiveShop
        self.click1('div>ul[class="menuList"] span','竞店分析')
        time.sleep(3)
        self.driver.find_element_by_xpath("//button/span[text()='日']/..").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//body").send_keys(Keys.END)
        time.sleep(5)
        li=['淘内免费','付费流量','自主访问','淘外网站','淘外APP','其它来源']
        for j in li:self.driver.find_element_by_xpath("//tr/td/span[text()='%s']/../span[2]"% j).click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//body").send_keys(Keys.HOME)
        for j in range(50):self.driver.find_element_by_xpath("//body").send_keys(Keys.UP)
        with open('parameter.txt','r') as ff:
            f=ff.readlines()
        b=eval(f[1])
        for i in b['竟店']:
            self.driver.find_elements_by_css_selector('#shopAnalysisSelect > div> span > div')[1].click()#d点击选择竟店
            time.sleep(0.5)
            self.driver.find_element_by_css_selector('div[mode="vertical"]>span>span.ant-input-suffix>i').click()
            time.sleep(0.2)
            e=self.driver.find_element_by_css_selector('div[mode="vertical"]>span>input')
            e.click()
            e.send_keys(i[:3])
            time.sleep(0.3)
            e.send_keys(i[3:])
            e.send_keys(Keys.ENTER)
            time.sleep(1)
            f=self.driver.find_element_by_css_selector('div.oui-typeahead-dropdown>div>span')
            if '暂无数据' in f.text:print('暂无数据')
            else:f.click()
            time.sleep(0.5)
            self.driver.find_element_by_xpath("//body").send_keys(Keys.END)
            time.sleep(2)
            self.driver.find_element_by_xpath("//body").send_keys(Keys.HOME)
            try:self.cruxIndex(i)#关键指标
            except:currency.Ri_zhi()
            time.sleep(1)
            try:self.commodityList(i)#TOP商品榜
            except:currency.Ri_zhi()
            time.sleep(1)
            try:self.transactionComposition(i)#交易构成
            except:currency.Ri_zhi()
            time.sleep(1)
            try:self.sourceOfEntry(i)#入店来源
            except:currency.Ri_zhi()
            time.sleep(0.5)
            self.driver.find_element_by_xpath("//body").send_keys(Keys.HOME)
            time.sleep(1)
            

    def cruxIndex(self,i):#关键指标
        b_cruxIndex=self.driver.find_elements_by_css_selector('div>div.alife-one-design-sycm-indexes-trend-index-container>div>div')
        b_cruxIndex1=[i.text.split('\n') for i in b_cruxIndex]
        try:self.driver.find_element_by_css_selector('div>div>i[class*="right"]').click()
        except:self.driver.find_element_by_css_selector('div>div>i[class*="left"]').click()
        time.sleep(1)
        b_cruxIndex=self.driver.find_elements_by_css_selector('div>div.alife-one-design-sycm-indexes-trend-index-container>div>div')
        b_cruxIndex=[i.text.split('\n') for i in b_cruxIndex]
        b_cruxIndex=b_cruxIndex1+b_cruxIndex
        t='%s-%s-%s'%time.localtime()[:3]
        b_data={j[0]:[j[2],j[4]] for j in b_cruxIndex}#数据转为字典
        l02=['店铺日期','交易指数','流量指数','搜索人气','收藏人气','加购人气',
             '预售定金交易指数','预售支付商品件数','上新商品数','支付转化指数','客群指数']
        b=currency.sqlite_weiwei()
        sql=b.sql01('cruxIndex',l02)
        try:b.addDelUpd(sql)
        except:pass
        bd=self.driver.find_element_by_css_selector('span.ebase-Selector__title').text#本店名称
        l03,l04=[],[]
        for j in l02:
            if j=='店铺日期':
                l03+=[t+bd]
                l04+=[t+i]
            else:
                try:l03+=[b_data[j][0]]
                except: return
                l04+=[b_data[j][1]]
        sql="insert into cruxIndex values(?,?,?,?,?,?,?,?,?,?,?)"
        try:b.addDelUpd(sql,l03)
        except:pass
        try:b.addDelUpd(sql,l04)
        except:currency.Ri_zhi()
        b.cursor.close()

    def commodityList(self,i):#TOP商品榜
        t='%s-%s-%s'%time.localtime()[:3]
        l02=['店铺日期商品id项目','top排名','指数','较前一日']
        b=currency.sqlite_weiwei()
        sql=b.sql01('commodityList',l02)
        try:b.addDelUpd(sql)
        except:pass#首次创建表
        llrx=self.driver.find_elements_by_css_selector('#shopAnalysisItems div>div>div>span>span')#定位浏览热销
        self.driver.execute_script('(arguments[0]).scrollIntoView()',llrx[0])#滚动到指定元素
        time.sleep(1)
        for j in range(5):self.driver.find_element_by_xpath("//body").send_keys(Keys.UP)
        time.sleep(0.5)
        for j in range(2):
            if j==0:rl='热销'
            else:rl='流量'
            self.driver.find_elements_by_css_selector('#shopAnalysisItems div>div>div>span>span')[j].click()#定位浏览热销
            time.sleep(2)
            # 店铺top前十
            sql="insert into commodityList values(?,?,?,?)"
            td1=self.driver.find_elements_by_css_selector('#shopAnalysisItems>div>div>div:nth-child(1) tbody td:nth-child(1)')
            td2=self.driver.find_elements_by_css_selector('#shopAnalysisItems>div>div>div:nth-child(1) tbody td:nth-child(2)')
            bd=self.driver.find_element_by_css_selector('span.ebase-Selector__title').text#本店名称
            num=1
            for td in zip(td1,td2):
                id1=re.findall('id=(\d+)" target',td[0].get_attribute("outerHTML"))[0]
                ourShop=[t+bd+id1+rl]#时间店铺id项目
                zhsh=td[1].text
                ourShop+=[str(num)]+zhsh.split('\n')
                num+=1
                try:b.addDelUpd(sql,ourShop)
                except:pass
            # 竟店top前十
            td1=self.driver.find_elements_by_css_selector('#shopAnalysisItems>div>div>div:nth-child(2) tbody td:nth-child(1)')
            td2=self.driver.find_elements_by_css_selector('#shopAnalysisItems>div>div>div:nth-child(2) tbody td:nth-child(2)')
            num=1
            for td in zip(td1,td2):
                id1=re.findall('id=(\d+)" target',td[0].get_attribute("outerHTML"))[0]
                competitiveStores=[t+i+id1+rl]#时间店铺id项目
                zhsh=td[1].text
                competitiveStores+=[str(num)]+zhsh.split('\n')
                num+=1
                try:b.addDelUpd(sql,competitiveStores)
                except:pass
        b.cursor.close()

    def transactionComposition(self,i):#交易构成
        t='%s-%s-%s'%time.localtime()[:3]
        l02=['日期店铺排名','类目','支付金额占比']
        b=currency.sqlite_weiwei()
        sql=b.sql01('transactionComposition',l02)
        try:b.addDelUpd(sql)
        except:pass#首次创建表
        b_jygc=self.driver.find_element_by_css_selector('#shopAnalysisTrade>div.oui-card-content')#交易构成
        self.driver.execute_script('(arguments[0]).scrollIntoView()',b_jygc)#滚动到指定元素
        for j in range(5):
            self.driver.find_element_by_xpath("//body").send_keys(Keys.DOWN)
        time.sleep(1)
        
        css01='#shopAnalysisTrade>div.oui-card-content>div:nth-child(%s)>div:nth-child(%s) tr'
        b_lmzbbd=self.driver.find_elements_by_css_selector(css01%(1,1))#类目占比本店
        b_lmzbjd=self.driver.find_elements_by_css_selector(css01%(1,2))#类目占比竟店
        b_jgdzbbd=self.driver.find_elements_by_css_selector(css01%(2,1))#价格带占比本店
        b_jgdzbjd=self.driver.find_elements_by_css_selector(css01%(2,2))#价格带占比竟店
        bd=self.driver.find_element_by_css_selector('span.ebase-Selector__title').text#本店名称
        sql="insert into transactionComposition values(?,?,?)"
        for j in range(len(b_lmzbbd)):
            if j==0:continue
            data=b_lmzbbd[j].text
            data=data.split('\n')
            try:b.addDelUpd(sql,[t+bd+data[0],data[1],data[2]])
            except:pass 
        for j in range(len(b_lmzbjd)):
            if j==0:continue
            data=b_lmzbjd[j].text
            data=data.split('\n')
            try:b.addDelUpd(sql,[t+i+data[0],data[1],data[2]])
            except:pass

        l02=['日期店铺编号','价格带','支付金额占比']
        sql=b.sql01('price_band',l02)
        try:b.addDelUpd(sql)
        except:pass#首次创建表
        sql="insert into price_band values(?,?,?)"
        for j in range(len(b_jgdzbbd)):
            if j==0:continue
            data=b_jgdzbbd[j].text
            data=data.split('\n')
            try:b.addDelUpd(sql,[t+bd+str(j),data[0],data[1]])
            except:pass 
        for j in range(len(b_jgdzbjd)):
            if j==0:continue
            data=b_jgdzbjd[j].text
            data=data.split('\n')
            try:b.addDelUpd(sql,[t+i+str(j),data[0],data[1]])
            except:pass
        b.cursor.close()

    def sourceOfEntry(self,i):#入店来源
        t='%s-%s-%s'%time.localtime()[:3]
        l02=['日期店铺来源','流量指数','客群指数','支付转化指数','交易指数','访客数','支付买家数','支付转化率','支付金额']
        b=currency.sqlite_weiwei()
        sql=b.sql01('sourceOfEntry',l02)
        try:b.addDelUpd(sql)
        except:pass#首次创建表
        li=self.driver.find_elements_by_css_selector('#sycm-mc-flow-analysis li')
        self.driver.execute_script('(arguments[0]).scrollIntoView()',li[0])#滚动到指定元素
        for j in range(5):self.driver.find_element_by_xpath("//body").send_keys(Keys.UP)
        time.sleep(1)
        
        bd=self.driver.find_element_by_css_selector('span.ebase-Selector__title').text#本店名称
        Li=[{},{}]
        for j in range(len(li)):
            self.driver.find_elements_by_css_selector('#sycm-mc-flow-analysis input')[j].click()
            time.sleep(3)
            xm=li[j].text
            tbody=self.driver.find_element_by_css_selector('#sycm-mc-flow-analysis tbody').text
            tbody=[i.split('\n') for i in tbody.split('\n趋势\n')]
            for k in tbody:
                if k[0] not in Li[0]:Li[0][k[0]]={}
                if k[0] not in Li[1]:Li[1][k[0]]={}
                Li[0][k[0]][xm]=k[1]
                Li[1][k[0]][xm]=k[2]
                Li[0][k[0]][xm]=k[1]
                Li[1][k[0]][xm]=k[2]
                if '流量' in xm:
                    Li[0][k[0]]['访客数']=k[3]
                    Li[1][k[0]]['访客数']=''
                elif '客群' in xm:
                    Li[0][k[0]]['支付买家数']=k[3]
                    Li[1][k[0]]['支付买家数']=''
                elif '支付' in xm:
                    Li[0][k[0]]['支付转化率']=k[3]
                    Li[1][k[0]]['支付转化率']=''
                elif '交易' in xm:
                    Li[0][k[0]]['支付金额']=k[3]
                    Li[1][k[0]]['支付金额']=''
        sql="insert into sourceOfEntry values(?,?,?,?,?,?,?,?,?)"
        for o in Li[0]:#Li[0]是字段，o是字段的键
            bdli=[t+bd+o]
            for u in l02[1:]:#u是字典Li[0][o] 的键，也是字段名
               bdli+=[Li[0][o][u]]
            if re.findall('[1-9]',str(bdli[1:])):
                try:b.addDelUpd(sql,bdli)
                except:pass
        for o in Li[1]:#Li[0]是字段，o是字段的键
            jdli=[t+i+o]
            for u in l02[1:]:#u是字典Li[0][o] 的键，也是字段名
               jdli+=[Li[1][o][u]]
            if re.findall('[1-9]',str(jdli[1:])):
                try:b.addDelUpd(sql,jdli)
                except:pass
        b.cursor.close()

    def mian(self):
        self.goToBS()
        self.goToCompete()
        self.analysisOfCompetitiveShop()
        #self.commoditySource()

if __name__=='__main__':
    driver=currency.starUpChrome()
    b=BS_Compete(driver.driver)
    #b.mian()
    pass
    print(123)

'''
if 1:
    #s='cruxIndex'#关键指标
    s='commodityList'#TOP商品榜
    #s='transactionComposition'#交易构成
    #s='price_band'#价格带占比
    #s='sourceOfEntry'#入店来源
    e=currency.mysqlwei()
    e.cur.execute('desc %s'%s)
    lie=[i[0] for i in e.cur.fetchall()]#表头
    sql="select * from %s where %s regexp '(?=.*18)(?=.*手淘).*'"%(s,lie[0])
    hang=e.sel(sql)
    print(len(hang))
    for i1 in hang[0]:
        print(i1)

'''

