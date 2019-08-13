import pymysql

class Ri_zhi():#日志和记录
    def __init__(self):
        now = int(time.time())
        self.timeArray = time.localtime(now)
        self.otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S",self.timeArray)
        if traceback.format_exc()!='NoneType: None\n':
            f=open(r"执行日志.txt",'a')
            traceback.print_exc(file=f)
            f.write('*******************************'+self.otherStyleTime+'************************************\n\n')
            f.flush()  
            f.close()
    def xujiludnr(self,neirong):
        rq01='%s%s%s'%(self.timeArray[0],self.timeArray[1],self.timeArray[2])
        f=open("错误订单.txt",'a')
        f.write(neirong+'\n')
        f.flush()
        f.close()

def create_baseTable():#增数据库和表
    con = pymysql.connect(host='localhost', user='root',
                          passwd='123456', charset='utf8')
    cur = con.cursor()
    #sql="create database awesome character set utf8;"
    sql="create database if not exists awesome12 character set utf8mb4;"
    cur.execute(sql)#建库
    
    cur.execute("use awesome12;")#使用库
    sql="create table if not exists blogs(id char(20),user_id char(20),name char(20))character set utf8mb4;"
    cur.execute(sql)#建表

def insert01():#增记录
    db = pymysql.connect("localhost","root","123456","awesome")
    cur_insert = db.cursor()
    # sql插入语句 表名blogs
    #sql_insert ="""insert into blogs(id,user_id,name) values ("test_id",'test_user_id','test_name')"""
    sql_insert ="insert into blogs values (%s,%s,%s)"#不支持问号占位
    try:
        cur_insert.execute(sql_insert,['003','c003','cccc'])
        db.commit()# 提交
        print('开始数据库插入操作')
    except Exception as e:
        db.rollback()
        print('数据库插入操作错误回滚')
        raise e
    finally:
        db.close()

def delete01():#删除记录
    db = pymysql.connect("localhost","root","123456","awesome")
    cur_delete = db.cursor()
    sql_delete = "delete from awesome.blogs where name = '%s'"
    try:
        cur_delete.execute(sql_delete,("update_test_name"))  # 像sql语句传递参数
        db.commit()# 提交
        print('开始数据库删除操作')
    except Exception as e:
        db.rollback()
        print('数据库删除操作错误回滚')
        raise e
    finally:
        db.close()

def update01():#修改记录
    db = pymysql.connect("localhost","root","123456","awesome")
    cur_update = db.cursor()
    sql_update = "update blogs set id = %s where name = %s"#更新操作
    try:
        cur_update.execute(sql_update,['999',"钱志伟"])
        db.commit()# 提交
        print('开始数据库更新操作')
    except Exception as e:
        db.rollback()
        print('数据库更新操作错误回滚')
        raise e
    finally:
        db.close()

def select01():#查询记录
    # 1.建立连接，用户root mysql密码123456 dbname：awesome
    db = pymysql.connect("localhost","root","123456","awesome")
    cur = db.cursor()#获取游标
    sql = "select * from blogs"# sql查询语句 表名blogs
    try:
        cur.execute(sql)    #执行sql语句
        results = cur.fetchall()  #获取查询的所有记录
        print("id", "user_id", "name")
        for row in results:# 遍历结果
            print('id1:',row[0])
            print('user_id:',row[1])
            print('name:',row[2])
    except Exception as e:
        raise e
    finally:
        db.close()  #关闭连接












