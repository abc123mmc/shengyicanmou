import currency,flow,competitive_goods,compete,AppMain,sys#导入通用包
from PySide2 import QtCore, QtGui, QtWidgets
import ctypes  #弹出框

driver=currency.starUpChrome()
def b(driver):
    b=flow.BS_Flow(driver.driver)
    b.mian()
    ctypes.windll.user32.MessageBoxW(0, '流量数据获取完成！！！','提示',1)
    
def c(driver):
    c=compete.BS_Compete(driver.driver)
    c.mian()
    ctypes.windll.user32.MessageBoxW(0, '竟店数据获取完成！！！','提示',1)

def d(driver):
    d=competitive_goods.BS_Compete(driver.driver)
    d.mian()
    ctypes.windll.user32.MessageBoxW(0, '竟品数据获取完成！！！','提示',1)


app=QtWidgets.QApplication(sys.argv)
widget=QtWidgets.QWidget()
ui=AppMain.Ui_Form()
#ui.pushButton.clicked.connect(self.kaishi)
ui.setupUi(widget)
ui.pushButton_2.clicked.connect(lambda:b(driver))
ui.pushButton_3.clicked.connect(lambda:c(driver))
ui.pushButton_4.clicked.connect(lambda:d(driver))
widget.show()
sys.exit(app.exec_())


s0=[['Shop_Flow','店铺流量'],['commodity_Flow','商品来源']]#flow.py#流量
s0=[['cruxIndex','关键指标'],['commoditylist','TOP商品'],['transactionComposition','交易构成'],
    ['price_band','价格带'],['sourceOfEntry','入店来源']]#compete.py#竟店
s0=[['goodsCruxIndex','竟品关键指标'],['drainageKeywords','引流关键词'],
    ['transactionKeywords','成交关键词'],['goodsSourceOfEntry','竟品入店来源']]#competitive_goods.py#竟品


if 1:
    s=s0[0][0]
    print(s)
    e=currency.sqlite_weiwei()
    e.cursor.execute('pragma table_info(%s)'%s)
    lie=[i[1] for i in e.cursor.fetchall()]#表头
    sql="select * from %s where %s like '%%2019-8-8%%'"%(s,lie[0])
    hang=e.sel(sql)
    print(len(hang))
    for i1 in hang:
        print(i1)
    lie
