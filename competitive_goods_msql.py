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

    def competitionAnalysis(self):#竟品分析competitionAnalysis
        self.click1('div>ul[class="menuList"] span','竞品分析')
        time.sleep(3)
        self.driver.find_element_by_xpath("//button/span[text()='日']/..").click()
        time.sleep(2)
        with open('parameter.txt','r') as ff:
            f=ff.readlines()
        b=eval(f[2])
        for i in b['竟品']:
            self.driver.find_elements_by_css_selector('#itemAnalysisSelect> div> span > div')[1].click()#d点击选择竟品
            time.sleep(0.5)
            self.driver.find_element_by_css_selector('div>div>span>span.ant-input-suffix>i').click()
            time.sleep(0.2)
            e=self.driver.find_element_by_css_selector('div>span>input')
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
            time.sleep(1)
            self.driver.find_element_by_xpath("//body").send_keys(Keys.HOME)

            self.goodsCruxIndex(i)#竟品关键指标
            time.sleep(1)
            self.drainageKeywords(i)#关键词
            time.sleep(1)
            self.goodsSourceOfEntry(i)#竟品入店来源
            time.sleep(0.5)
            self.driver.find_element_by_xpath("//body").send_keys(Keys.HOME)
            time.sleep(1)
            for j in range(50):self.driver.find_element_by_xpath("//body").send_keys(Keys.UP)

    def goodsCruxIndex(self,i):#竟品关键指标
        b_cruxIndex=self.driver.find_elements_by_css_selector('div>div.alife-one-design-sycm-indexes-trend-index-container>div>div')
        b_cruxIndex1=[i.text.split('\n') for i in b_cruxIndex]
        b_cruxIndex1={i[0]:i[2] for i in b_cruxIndex1}
        time.sleep(1)
        try:self.driver.find_element_by_css_selector('div>div>i[class*="right"]').click()
        except:self.driver.find_element_by_css_selector('div>div>i[class*="left"]').click()
        time.sleep(1)
        b_cruxIndex=self.driver.find_elements_by_css_selector('div>div.alife-one-design-sycm-indexes-trend-index-container>div>div')
        b_cruxIndex=[i.text.split('\n') for i in b_cruxIndex]
        for j in b_cruxIndex:b_cruxIndex1[j[0]]=j[2]#b_cruxIndex1为各指数为键，数值为值的字段
        t='%s-%s-%s'%time.localtime()[:3]
        l02=['日期商品id','交易指数','流量指数','搜索人气','收藏人气','加购人气','支付转化指数']
        b=currency.sqlite_weiwei()
        sql=b.sql01('goodsCruxIndex',l02)
        try:b.addDelUpd(sql)
        except:pass
        l03=[]
        for j in l02:
            if j=='日期商品id':
                l03+=[t+'  '+i]
            else:
                l03+=[b_cruxIndex1[j]]
        sql="insert into goodsCruxIndex values(?,?,?,?,?,?,?)"
        try:b.addDelUpd(sql,l03)
        except:pass
        b.con.close()

    def drainageKeywords(self,i):#引流关键词
        llrx=self.driver.find_element_by_css_selector('#itemAnalysisKeyword')#定位入店搜索词
        self.driver.execute_script('(arguments[0]).scrollIntoView()',llrx)#滚动到指定元素
        for j in range(5):self.driver.find_element_by_xpath("//body").send_keys(Keys.UP)
        time.sleep(2)
        l02=['日期来源商品id词','访客数']
        b=currency.sqlite_weiwei()
        sql=b.sql01('drainageKeywords',l02)#引流关键词
        try:b.addDelUpd(sql)
        except:pass
        self.driver.find_element_by_xpath("//*[@id='itemAnalysisKeyword']//span[text()='引流关键词']").click()
        time.sleep(1)
        li=self.shopSearchWords(i)
        sql="insert into drainageKeywords values(?,?)"
        for j in li:
            try:b.addDelUpd(sql,j)
            except:pass

        l02=['日期来源商品id词','交易指数']
        sql=b.sql01('transactionKeywords',l02)#成交关键词
        try:b.addDelUpd(sql)
        except:pass
        self.driver.find_element_by_xpath("//*[@id='itemAnalysisKeyword']//span[text()='成交关键词']").click()
        time.sleep(1)
        li=self.shopSearchWords(i)
        sql="insert into transactionKeywords values(?,?)"
        for j in li:
            try:b.addDelUpd(sql,j)
            except:pass
        b.con.close()
        
    def shopSearchWords(self,i):#入店搜索词,被drainageKeywords调用
        t='%s-%s-%s'%time.localtime()[:3]
        self.driver.find_element_by_css_selector('#itemAnalysisKeyword   div.oui-card-header>div> div').click()
        time.sleep(2)
        self.driver.find_element_by_css_selector('div[data-reactroot]>div:not([class*="hidden"])>div>ul>li:nth-child(2)').click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='itemAnalysisKeyword']//span[text()='淘宝']").click()
        time.sleep(1)
        tr=self.driver.find_elements_by_css_selector('#itemAnalysisKeyword tbody tr')
        li=[i.text.split('\n') for i in tr]#无线淘宝
        li=[[t+'无线淘宝'+i+j[0],j[-1]] for j in li]
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='itemAnalysisKeyword']//span[text()='天猫']").click()
        time.sleep(1)
        tr=self.driver.find_elements_by_css_selector('#itemAnalysisKeyword tbody tr')
        li1=[i.text.split('\n') for i in tr] #无线天猫
        li1=[[t+'无线天猫'+i+j[0],j[-1]] for j in li1]

        self.driver.find_element_by_css_selector('#itemAnalysisKeyword   div.oui-card-header>div> div').click()
        time.sleep(2)
        self.driver.find_element_by_css_selector('div[data-reactroot]>div:not([class*="hidden"])>div>ul>li:nth-child(1)').click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='itemAnalysisKeyword']//span[text()='淘宝']").click()
        time.sleep(1)
        tr=self.driver.find_elements_by_css_selector('#itemAnalysisKeyword tbody tr')
        li2=[i.text.split('\n') for i in tr]#PC淘宝
        li2=[[t+'PC淘宝'+i+j[0],j[-1]] for j in li2]
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='itemAnalysisKeyword']//span[text()='天猫']").click()
        time.sleep(1)
        tr=self.driver.find_elements_by_css_selector('#itemAnalysisKeyword tbody tr')
        li3=[i.text.split('\n') for i in tr] #PC天猫
        li3=[[t+'PC淘宝'+i+j[0],j[-1]] for j in li3]
        return li+li1+li2+li3

    def goodsSourceOfEntry(self,i):#竟品入店来源
        llrx=self.driver.find_element_by_css_selector('#sycm-mc-flow-analysis')#定位入店来源
        self.driver.execute_script('(arguments[0]).scrollIntoView()',llrx)#滚动到指定元素
        for j in range(5):self.driver.find_element_by_xpath("//body").send_keys(Keys.UP)
        time.sleep(3)
        t='%s-%s-%s'%time.localtime()[:3]
        li=['访客数','客群指数','支付转化指数','交易指数']
        self.driver.find_element_by_css_selector('#sycm-mc-flow-analysis   div.oui-card-header>div> div').click()
        time.sleep(2)
        self.driver.find_element_by_css_selector('div[data-reactroot]>div:not([class*="hidden"])>div>ul>li:nth-child(2)').click()
        time.sleep(2)
        data=self.sourceOfEntry1()
        li1=[]
        for j in data:
            li2=[t+'无线端'+i+j]
            for p in li:
                if p in data[j]:li2+=[data[j][p]]
                else:li2+=['0']
            li1+=[li2]
        
        self.driver.find_element_by_css_selector('#sycm-mc-flow-analysis   div.oui-card-header>div> div').click()
        time.sleep(2)
        self.driver.find_element_by_css_selector('div[data-reactroot]>div:not([class*="hidden"])>div>ul>li:nth-child(1)').click()
        time.sleep(2)
        data=self.sourceOfEntry1()
        for j in data:
            li2=[t+'PC端'+i+j]
            for p in li:
                if p in data[j]:li2+=[data[j][p]]
                else:li2+=['0']
            li1+=[li2]
        l02=['日期来源商品id项目']+li
        b=currency.sqlite_weiwei()
        sql=b.sql01('goodssourceOfEntry',l02)#引流关键词
        try:b.addDelUpd(sql)
        except:pass
        sql="insert into goodssourceOfEntry values(?,?,?,?,?)"
        for j in li1:
            try:b.addDelUpd(sql,j)
            except:pass
        b.con.close()


    def sourceOfEntry1(self):#入店来源
        data={}
        try:self.driver.find_element_by_css_selector('#sycm-mc-flow-analysis li[title="1"]').click()
        except:pass
        time.sleep(1)
        while 1:
            for j in range(4):
                self.driver.find_elements_by_css_selector('#sycm-mc-flow-analysis input')[j].click()
                time.sleep(2)
                tr=self.driver.find_elements_by_css_selector('#sycm-mc-flow-analysis tbody tr')
                li=[l.text.split('\n') for l in tr]
                for l in li:
                    if l[0] not in data:data[l[0]]={}
                    xm=self.driver.find_elements_by_css_selector('#sycm-mc-flow-analysis li:not([title])')[j].text
                    data[l[0]][xm]=l[1]
            try:self.driver.find_element_by_css_selector('li[title="下一页"][aria-disabled="false"]').click()
            except:break
        return data

    def mian(self):
        self.goToBS()
        self.goToCompete()
        self.competitionAnalysis()
        #self.commoditySource()

if __name__=='__main__':
    driver=currency.starUpChrome()
    b=BS_Compete(driver.driver)
    #b.mian()
    pass
    print(123)

    

'''
if 1:
    #s='goodsCruxIndex'#竟品关键指标
    #s='drainageKeywords'#引流关键词
    #s='transactionKeywords'#交易关键词
    s='goodsSourceOfEntry'#竟品入店来源
    e=currency.sqlite_weiwei()
    e.cur.execute('desc %s'%s)
    lie=[i[0] for i in e.cur.fetchall()]#表头
    sql="select * from %s where %s regexp '2019-7-'"%(s,lie[0])
    hang=e.sel(sql)
    print(len(hang))
    for i1 in hang[0]:
        print(i1)

'''
 
