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
    def goToFlow(self):#进入浏量
        self.click1('ul[class="menu-list clearfix"]>li','流量')
        #['首页', '实时', '作战室', '', '流量', '品类', '交易', '内容', '服务', '营销', '物流', '财务', '', '市场', '竞争', '', '业务专区', '', '取数', '学院']
        try:
            for i in range(3):self.driver.find_element_by_css_selector('#flow-v3-new-guide>div>div>div>a').click()
        except:pass#对弹出流量纵横全新升级弹框的点击

    def shopSource(self):#店铺来源
        self.click1('div>ul[class="menuList"] span','店铺来源')
        time.sleep(3)
        self.driver.find_element_by_xpath("//span[text()='1天']/..").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//a/span[text()='下载']").click()
        time.sleep(5)
        j='./xiazai'+'\\'+os.listdir('xiazai')[0]
        data = xlrd.open_workbook(j)
        table = data.sheets()[0]
        nrows = table.nrows
        li=[table.row_values(i) for i in range(6,nrows)]
        t='%s-%s-%s'%time.localtime()[:3]
        li=[[t+''.join(i[:2])]+i[2:] for i in li if re.findall('[1-9]',str(i[2:]))]
        b=currency.sqlite_weiwei('BS_Data_qplxbqjd.db')
        sql='''create table Shop_Flow (
        日期来源 primary key not null default "",
        访客数 text not null default "",
        访客数变化 text not null default "",
        下单金额 text not null default "",
        下单金额变化 text not null default "",
        下单买家数 text not null default "",
        下单买家数变化 text not null default "",
        下单转化率 text not null default "",
        下单转化率变化 text not null default "",
        支付金额 text not null default "",
        支付金额变化 text not null default "",
        支付买家数 text not null default "",
        支付买家数变化 text not null default "",
        支付转化率 text not null default "",
        支付转化率变化 text not null default "",
        客单价 text not null default "",
        客单价变化 text not null default "",
        UV价值 text not null default "",
        uv价值变化 text not null default "",
        关注店铺买家数 text not null default "",
        关注店铺买家数变化 text not null default "",
        收藏商品买家数 text not null default "",
        收藏商品买家数变化 text not null default "",
        加购人数 text not null default "",
        加购人数变化 text not null default "",
        新访客 text not null default "",
        新访客变化 text not null default "")'''
        try:b.zengShanGai(sql)
        except:pass#首次创建表
        sql="insert into Shop_Flow values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        for i in li:
            try:b.zengShanGai(sql,i)
            except:pass
        shutil.rmtree("xiazai")
        b.conn.close()

    def commoditySource(self):#商品来源
        self.click1('div>ul[class="menuList"] span','商品来源')
        time.sleep(3)
        self.driver.find_element_by_xpath("//span[text()='1天']/..").click()
        with open('parameter.txt','r') as ff:
            f=ff.readlines()
        b=eval(f[0])
        for i in b['流量商品来源id']:
            self.driver.find_element_by_css_selector('div>span[class*="sycm-common-select"]').click()
            time.sleep(1)
            e=self.driver.find_element_by_css_selector('div>span>input')
            e.click()
            time.sleep(0.5)
            e.send_keys(i)
            time.sleep(1)
            self.driver.find_element_by_css_selector('div.oui-typeahead-dropdown>div>span').click()
            time.sleep(2)
            self.driver.find_element_by_xpath("//a/span[text()='下载']").click()
            time.sleep(5)
            j='./xiazai'+'\\'+os.listdir('xiazai')[0]
            data = xlrd.open_workbook(j)
            table = data.sheets()[0]
            nrows = table.nrows
            li=[table.row_values(i) for i in range(6,nrows)]
            t='%s-%s-%s'%time.localtime()[:3]
            li=[[t+'[%s]'% i+j[0]]+j[1:] for j in li if re.findall('[1-9]',str(j[2:]))]
            b=currency.sqlite_weiwei('BS_Data_qplxbqjd.db')
            sql='''create table commodity_Flow (
            日期来源 primary key not null default "",
            访客数 text not null default "",
            浏览量 text not null default "",
            浏览量占比 text not null default "",
            店内跳转人数 text not null default "",
            跳出本店人数 text not null default "",
            收藏人数 text not null default "",
            加购人数 text not null default "",
            下单买家数 text not null default "",
            下单转化率 text not null default "",
            支付件数 text not null default "",
            支付买家数 text not null default "",
            支付金额 text not null default "",
            支付转化率 text not null default "")'''
            try:b.zengShanGai(sql)
            except:pass#首次创建表
            sql="insert into commodity_Flow values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            for i in li:
                try:b.zengShanGai(sql,i)
                except:pass
            shutil.rmtree("xiazai")
            b.conn.close()


    def mian(self):
        self.goToBS()
        self.goToFlow()
        self.shopSource()
        self.commoditySource()

#'commodity_Flow','日期来源','2019'
def chashuju(tableName,field,condition):
    b=currency.sqlite_weiwei('BS_Data_qplxbqjd.db')
    sql="select * from %s where %s like '%%%s%%'"%(tableName,field,condition)#%%感觉有点类似转义
    #sql="select * from commodity_Flow where 日期来源 like '%%%s%%'"% riqi
    c=b.chaXun(sql)
    sql='pragma table_info(%s)'% tableName
    bt=[i[1] for i in b.chaXun(sql)]
    b.conn.close()
    return c,bt

if __name__=='__main__':
    #b=BS_Flow()
    #b.starUpChrome()
    #b.mian()
    #e=chashuju('commodity_Flow','日期来源','2019')
    #e=chashuju('Shop_Flow','日期来源','2019')
    #e[1][:6]  ;e[0][0][:6]#调中间的0，和末尾的6即可
    #e=chashuju('commodity_Flow','日期来源','直通车')
    pass


'''
    def unfold(self):#点击展开数据详细
        css='tbody>tr:not([data-row-key*="."])[data-row-key]>td>span:nth-child(2)'
        e=self.driver.find_elements_by_css_selector(css)#流量来源
        for i in e[1:]:
            i.click()
        print('llly01,点击展开数据完成')
        d=self.driver.find_elements_by_css_selector('tbody[class|="ant"] tr')
        for i in d:
            t=i.text
            print(t)

'''

























'''

    def Get_headers(self):
        #生成请求头
        self.headers={'Accept':'*/*' ,
        'Accept-Encoding':'gzip, deflate' ,
        'Accept-Language':'zh-CN,zh;q=0.8' ,
        'Connection':'keep-alive' ,'Content-Length':'163' ,'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8' ,
        'Host':'www.guanyierp.com' ,'Origin':'http://www.guanyierp.com' ,
        'Referer':'http://www.guanyierp.com/tc/trade/trade_order_approve' ,
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36' ,
        'X-Requested-With':'XMLHttpRequest'}
        cookies=self.driver.get_cookies()
        cookieslist = []
        for i in cookies:
            name = i['name']
            value = i['value']
            if i['name'] == '_tb_token_':
                token = i['value']
            cookieslist.append(name + '=' + value + '; ')
            self.headers['Cookie']=''.join(cookieslist)
    def get_cookies(self):
        cookieslist=[]
        cookies=self.driver.get_cookies()
        for i in cookies:
            name = i['name']
            value = i['value']
            cookieslist.append(name + '=' + value + '; ')
        return cookieslist

    def get_beiZhu_danHao(self):
        self.Get_headers()
        url='http://www.guanyierp.com/tc/trade/trade_order_approve/data/list?_dc=1541861951441'
        data={'memo':'w' ,'page':'1' ,'start':'0' ,'limit':'100'}
        req=requests.post(url,data=data,headers=self.headers).json()
        dinDan=req['rows']
        req['rows'][0]['id']
        return dinDan
    def diqu001(self,beizu):#获取地区编码
        data = xlrd.open_workbook(r'地区.xls')
        table0= data.sheets()[0]#通过索引顺序获取
        shengFeng1=table0.col_values(1)#表0里的1列,省份
        shengFeng=list(set(shengFeng1))
        shengFeng.sort(key=shengFeng1.index)
        chengShi=table0.col_values(2)#表0里的2列，城市
        diQu3=table0.col_values(3)#表0里的3列，地区
        li=[]
        for i, val in enumerate(diQu3):
            if val in beizu:
                li=li+[table0.row_values(i)]
        if not li:
            print('地址不符合要求')
            return False
        li1=[]
        for i in li:
            if i[2] in beizu:
                li1=li1+[i]
        if not li1:
            print('地址不符合要求')
            return False
        if len(li1)==1:
            print(li1[0])
            li1=li1[0]
            return li1

def data_headers(a):#得到头或者数据
    for i in a.splitlines():
        print(''.join(["'",i.split(':',1)[0],"'",':',"'",i.split(':',1)[1],"'"]),',')



'''






