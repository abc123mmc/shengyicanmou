import sqlite3#导入sqlite3数据库模块，python自带模块
from selenium import webdriver
import os  
import xlrd  
import xlwt  
from xlutils.copy import copy
import time
from selenium.webdriver.common.keys import Keys
import re
import win32api,win32con  #弹出框
from tkinter import * #界面
import threading #线程
import sys, traceback#用于错误处理
import requests
import json
from selenium.webdriver.common.action_chains import ActionChains


def excelwrite(sheet1,L):
    '''#在excel的最后一行写入列表L，如果excel文件不存在的话会自动创建'''
    if L is None:  
        L = []   
    yr=time.strftime('%m%d%H')
    filename='竟店信息.xls' #导出数据名       
    try:
        workbook = xlrd.open_workbook(filename, formatting_info=True)        
    except:
        workbook=xlwt.Workbook()
        table=workbook.add_sheet(sheet1)
        li01=['日期','店铺','交易指数','流量指数','搜索人气','收藏人气','加购人气','手淘搜索','淘内免费其他','手淘微淘',
              '手淘首页','手淘问大家','手淘旺信','手淘我的评价','手淘消息中心','手淘其他店铺商品详情','猫客搜索',
              '手淘淘宝直播','手淘其他店铺','手淘找相似','猫客其他店铺','我的淘宝','购物车','直接访问']
        for i in range(len(li01)):
            table.write(0,i,li01[i])
        workbook.save(filename)
        workbook = xlrd.open_workbook(filename, formatting_info=True)
    sheet = workbook.sheet_by_name(sheet1) 
    rowNum = sheet.nrows
    colNum = sheet.ncols
    newbook = copy(workbook)  
    newsheet = newbook.get_sheet(sheet1)   
    for i in range(len(L)):  # 在末尾增加新行
        newsheet.write(rowNum,i,L[i])  
    newbook.save(filename)# 覆盖保存

class Ri_zhi():#日志和记录
    def __init__(self):
        now = int(time.time())
        self.timeArray = time.localtime(now)
        self.otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S",self.timeArray)
        f=open(r"执行日志.txt",'a')
        traceback.print_exc(file=f)
        f.write('*******************************'+self.otherStyleTime+'************************************\n\n')
        f.flush()  
        f.close()
    def xujiludnr(self,neirong):
        rq01='%s%s%s'%(self.timeArray[0],self.timeArray[1],self.timeArray[2])
        f=open(rq01+"旺旺号.txt",'a')
        f.write(neirong+'\n')
        f.flush()
        f.close()
        
class yeji():
    def __init__(self):
        self.cishu001=1
        self.guanbi1=False
        sj1=int(time.time())
        if sj1>1552613128:
            #win32api.MessageBox(0,'应用版本已过期，请联系作者QQ:1043014552', u'过期提醒',win32con.MB_SYSTEMMODAL)
            return
            #print('应用版本已过期')
        try:
            #self.driver = webdriver.Chrome()
            option = webdriver.ChromeOptions()
            option.add_argument('disable-infobars')
            option.add_argument("user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data")#设置成用户自己的数据目录
            self.driver= webdriver.Chrome(chrome_options=option)
            self.driver.get('https://login.taobao.com')
            self.driver.maximize_window()	#最大化浏览器窗口
        except:
            win32api.MessageBox(0,u'''
                                1.请检查是否安装Google Chrome<62.0.3202.62（
                                正式版本）（64 位）>（谷歌浏览器）
                                2.浏览器驱动chromedriver.exe，是否存在当前目录
                                3.应用版本是否过期，请联系作者QQ:1043014552
                                4.处理完成，手动退出''', u'提示',win32con.MB_SYSTEMMODAL)
            Ri_zhi()
            return
        
    def Get_headers(self):#获取请求头         
        headers={'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.8',
        'cache-control':'max-age=0',
        'referer':'https://sell.tmall.com/auction/item/item_list.htm?tab=onsale&status=item_on_sale',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
        cookies=self.driver.get_cookies()
        cookieslist = []
        for i in cookies:
            name = i['name']
            value = i['value']
            if i['name'] == 'c_csrf':
                headers['hcsrf']=i['value']
            cookieslist.append(name + '=' + value + '; ')
            headers['Cookie']=''.join(cookieslist)
        return headers
    
    def jingdianfengxi(self):#竞店分析：调用dianji（点击）进入到竞店分析，选择按日查看
        self.driver.get('https://mai.taobao.com/seller_admin.htm?')
        self.dianji('ul>li>a>span','生意参谋')#点击生意参谋
        self.driver.get('https://sycm.taobao.com/portal/home.htm')
        self.dianji('ul>li>a>span','竞争')#点击竞争
        self.dianji('ul>li>a>span','竞店分析')#点击'竞店分析'
        time.sleep(3)
        self.dianji('div.oui-date-picker-particle-button > button','日')#点击'日'

    def dianji(self,path01,str01):#传入元素css和条件，执行点击
        ulliaspan=self.driver.find_elements_by_css_selector(path01)
        for i in ulliaspan:
            if i.text==str01:
                print(i.text)
                i.click()
                break
        
    def xiala(self,Keys01):#滚动Keys.DOWN、Keys.UP、Keys.HOME、Keys.END
        #for i in range(199):
            #self.driver.find_element_by_xpath("//body").send_keys(Keys01)
        self.driver.find_element_by_xpath("//body").send_keys(Keys01)
        time.sleep(5)

    def llly01(self):#流量来源,点击打开数据详细
        try:
            llly=self.driver.find_element_by_css_selector('div[id="sycm-mc-flow-analysis"]')#流量来源
            ulliaspan=llly.find_elements_by_css_selector('tr>td>span:nth-child(2)')
            for i in ulliaspan:
                i.click()
        except:
            print('llly01,点击展开数据完成')

    def shurudianpu(self):#输入竟店店铺
        time.sleep(3)
        ulliaspan=self.driver.find_elements_by_css_selector('div>span>div>span')#选择店铺
        ulliaspan[1].click()
        ulliaspan=self.driver.find_elements_by_css_selector('input[placeholder="请输入已监控店铺关键词或在下方列表选择"]')
        time.sleep(1)
        ulliaspan[0].send_keys(self.shope_name)#('瑜然美化妆品旗舰店')
        ulliaspan=self.driver.find_elements_by_css_selector('div>div>span>span[title="%s"]'% self.shope_name)
        ulliaspan[0].click()
        time.sleep(3)
        ulliaspan=self.driver.find_elements_by_css_selector('div[class="oui-index-cell"]')
        zhishu={}
        for i in ulliaspan:
            re01=re.findall('(.*?)本店(.*?)竞店1(.*)',i.text.replace('\n','').replace(',',''))
            zhishu.update({re01[0][0]:re01[0][1:]})
        shijian=self.driver.find_element_by_css_selector('div.oui-date-picker-current-date').text
        shijian=re.findall('统计时间 (.*)',shijian)[0]
        zhishu.update({'日期':shijian})
        return zhishu

    def data001(self):#获取data001
        llly=self.driver.find_element_by_css_selector('div[id="sycm-mc-flow-analysis"]')#流量来源
        ulliaspan=llly.find_elements_by_css_selector('tr')
        data001={}
        for i in ulliaspan:
            self.i=i.text
            if not i.get_attribute('data-row-key'):
                print('没数据')
            else:
                re01=re.findall('(.*?)\n(.*?)\n(.*?)\n(.*?)\n趋势',i.text.replace(',',''))#[(名称，本店流量指数，竟店流量指数，本店访客数)]
                if (re01[0][1]!='0') or (re01[0][2]!='0') or (re01[0][3]!='0'):
                    data001.update({re01[0][0]:re01[0][2]})
                    print({re01[0][0]:re01[0][2]})
        return data001

    def shujuchuli(self): #数据处理，对返回的数据  self.data003、self.zhishu进行处理     
        liz=[int(self.zhishu['交易指数'][1]),int(self.zhishu['流量指数'][1]),int(self.zhishu['搜索人气'][1]),int(self.zhishu['收藏人气'][1]),int(self.zhishu['加购人气'][1])]
        li01=['手淘搜索','淘内免费其他','手淘微淘','手淘首页','手淘问大家','手淘旺信','手淘我的评价','手淘消息中心','手淘其他店铺商品详情','猫客搜索',
              '手淘淘宝直播','手淘其他店铺','手淘找相似','猫客其他店铺','我的淘宝','购物车','直接访问']
        lia=[]
        for i in self.data003:
            if i in li01:
                li01[li01.index(i)]=int(self.data003[i])
            else:
                if self.data003[i] !='0':
                    lia=lia+[i+':'+self.data003[i]]
        liz=[self.zhishu['日期'],self.shope_name]+liz+li01+lia
        excelwrite('sheet1',liz)  


    def run001(self):#❶打开
        self.jingdianfengxi()#竞店分析：调用dianji（点击）进入到竞店分析
        self.xiala(Keys.END)#滚动Keys.DOWN、Keys.UP、Keys.HOME、Keys.END
        self.llly01()#点击打开数据详细
        self.run003()#❷获取数据、输出

    def run003(self):#❷获取数据、输出
        li=['瑜然美化妆品旗舰店','草木之心旗舰店','玉泽官方旗舰店']
        for i in li:
            self.shope_name=i
            self.xiala(Keys.HOME)#滚动Keys.DOWN、Keys.UP、Keys.HOME、Keys.END
            self.zhishu=self.shurudianpu()#输入竟店店铺,同时返回指数
            self.xiala(Keys.END)#滚动Keys.DOWN、Keys.UP、Keys.HOME、Keys.END
            self.data003=self.data001()#返回竟店流量数据
            self.shujuchuli()#数据处理，对返回的数据  self.data003、self.zhishu进行处理


    def dianjihuoqu(self):#点击获取，获取点击次数
        self.driver.get('https://mai.taobao.com/seller_admin.htm?')
        self.dianji('ul>li>a>span','生意参谋')#点击生意参谋
        self.driver.get('https://sycm.taobao.com/bda/flow/decorate/index.htm#/?device=wireless&module=customized')
        ulliaspan=self.driver.find_elements_by_css_selector('ul.list>li')
        for i in ulliaspan:
            if '手淘店铺首页' in i.text:
                print(i.text)
                break
        dianpushouyie=i.find_element_by_css_selector('span[class="action big-button"]')
        dianpushouyie.click()
        url01=self.driver.window_handles
        for i in url01:
            self.driver.switch_to_window(i)
            if '%E5%BA%97%E9%93%BA%E9%A6%96%E9%A1%B5' in self.driver.current_url:
                b01=self.driver.find_element_by_css_selector('iframe.weex-iframe')
                self.driver.switch_to_frame(b01)
                time.sleep(6)
                b012=self.driver.find_elements_by_css_selector('[title*="模块点击次数"]')
                print(len(b012),226)
                for i in range(len(b012)):
                    b0123=self.driver.find_elements_by_css_selector('[title*="模块点击次数"]')
                    try:
                        for i1 in b0123[i].find_elements_by_css_selector('div'):
                            i1.click()
                    except:
                        pass
                    time.sleep(2)
                    b0123=self.driver.find_elements_by_css_selector('[title*="模块点击次数"]')
                    b0123[i].click()
                    d0101=self.driver.find_elements_by_xpath("//div[contains(text(),'模块点击次数')]")
                    d0101[i].click()
                    time.sleep(2)
                    b0123=self.driver.find_elements_by_css_selector('[title*="模块点击次数"]')
                    c=re.findall('模块点击次数：(.*)',b0123[i].text)[0]
                    z.tk.driver.save_screenshot('tupian/%s模块点击%s次.png'%(i+1,c))
                    print('tupian/%s模块点击%s次.png'%(i+1,c))




class jie4mian4():
    def __init__(self):
        try:
            self.tk=yeji()#实例化退款类
            pass
        except:
            win32api.MessageBox(0,u'''
                                1.请检查是否安装Google Chrome<62.0.3202.62（
                                正式版本）（64 位）>（谷歌浏览器）
                                2.浏览器驱动chromedriver.exe，是否存在当前目录
                                3.应用版本是否过期，请联系作者QQ:1043014552''', u'错误提示',win32con.MB_OK)
            return
        root =Tk()
        root.title("出售中的商品")#标题
        root.geometry("60x30+600+250")#参数'600x600'是x 不是*,“无参数默认是撑开.横x纵+左边距+上边距”
        root.resizable(width=True, height=True) #False不可变, True可变,默认为True

        Button1=Button(root, text="开始",font = ('', '14', 'bold'),command=self.tk.run001)#command=self.tk.zhixing01
        Button1.place(x=1, y=1,width=115,height=28)

        root.mainloop() # 进入消息循环
        command=root.quit
        root.quit
        #self.tk.driver.quit()
        #root.destroy()#没有这句command=root.quit 无效
        #self.tk.driver.quit()

    def kaishi(self):
        t1 = threading.Thread(target=self.xunhuan)
        t1.start()

    def xunhuan(self):#执行
        pass
        #self.tk.zhixing01()
        

if __name__ == '__main__':
    z=jie4mian4()







