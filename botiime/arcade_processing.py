import sqlite3
import re


def people_query():
    num = 1
    cx = ""
    # 加载数据库并初始化指针
    jtconn = sqlite3.connect("./db/jiting.db")
    cur = jtconn.cursor()

    # 从数据库检索id列的行数量，存为jts（机厅数）
    cur.execute("SELECT COUNT(id) FROM jiting")
    jts = cur.fetchall()
    # 这里是通过num自增遍历一遍数据库里对应的条目，数据库中id列的数值是从1开始的正序整数
    while num <= int(jts[0][0]):
        # 获取对应的机厅名称
        cur.execute("SELECT fullname FROM jiting WHERE id=" + str(num))
        jtmc = cur.fetchall()
        # 获取对应的机厅人数
        cur.execute("SELECT people FROM jiting WHERE id=" + str(num))
        jtrs = cur.fetchall()
        # 生成包含机厅的名称和信息的字符串，然后进入下一次循环
        cx = cx + str(jtmc[0][0]) + " 现在有 " + str(jtrs[0][0]) + " 人\n"
        num = num + 1
    # 关闭指针
    cur.close()
    return cx


def arcade_query(n: str):
    # 初始化变量
    num = 1
    sx = []
    # 初始化数据库的连接并创建指针
    jtconn = sqlite3.connect("./db/jiting.db")
    cur = jtconn.cursor()

    # 获取机厅数量jts
    cur.execute("SELECT COUNT(id) FROM jiting")
    jts = cur.fetchall()
    # 从数据库提取机厅缩写
    while num <= jts[0][0]:
        cur.execute("SELECT name FROM jiting WHERE id=" + str(num))
        sx.append(cur.fetchall())
        num = num + 1
    # 正则表达式，分别匹配 <任意字母>[+-]<任意数字>，如ch+1
    if re.match('[a-z]+[$j]', n):
        jtsx = re.findall('[a-z]+', n)  # 机厅缩写
        # 检测输入的机厅缩写是否与数据库中的机厅缩写匹配
        for i in sx:
            if str(jtsx[0]) == str(i[0][0]):
                # 操作数据库，提取机厅的全名和人数并且存储在对应的变量里
                cur.execute("SELECT fullname FROM jiting WHERE name='" + str(jtsx[0]) + "'")
                fullname = str(cur.fetchall()[0][0])
                cur.execute("SELECT people FROM jiting WHERE name='" + str(jtsx[0]) + "'")
                people = str(cur.fetchall()[0][0])
                # 用一个字符串返回查询结果
                query = fullname + "现在有" + people + "人"
                cur.close()
                return True
            else:
                # 如果不符合，那么关闭指针并返回False
                cur.close()
                return False


# 编写函数对人数增减消息进行检测和拆分，然后上传到数据库
def changes_upload(n: str):
    # 初始化变量
    num = 1
    sx = []
    # 初始化数据库的连接并创建指针
    jtconn = sqlite3.connect("./db/jiting.db")
    cur = jtconn.cursor()

    # 获取机厅数量jts
    cur.execute("SELECT COUNT(id) FROM jiting")
    jts = cur.fetchall()
    # 从数据库提取机厅缩写
    while num <= jts[0][0]:
        cur.execute("SELECT name FROM jiting WHERE id=" + str(num))
        sx.append(cur.fetchall())
        num = num + 1
    # 正则表达式，分别匹配 <任意字母>[+-]<任意数字>，如ch+1
    if re.match('[a-z]+[+-][0-9]+', n):
        jtsx = re.findall('[a-z]+', n)  # 机厅缩写
        zj = re.findall('[+-]', n)  # 增减变化
        jtrs = re.findall('[0-9]+', n)  # 机厅变化人数
        # 检测输入的机厅缩写是否与数据库中的机厅缩写匹配
        for i in sx:
            if str(jtsx[0]) == str(i[0][0]):
                # 获取对应机厅的人数并存储
                cur.execute("SELECT people FROM jiting WHERE name='" + str(jtsx[0]) + "'")
                rs_past = int(cur.fetchall()[0][0])
                # 判断正负
                if str(zj[0]) == '+':
                    rs_now = rs_past + int(jtrs[0])
                    # 数据为增，操作数据库并返回True
                    cur.execute("UPDATE jiting SET people=" + str(rs_now) + " WHERE name='" + str(jtsx[0]) + "'")
                    jtconn.commit()
                    cur.close()
                    return True

                else:
                    # 数据为减，验证数据合理性
                    rs_now = rs_past - int(jtrs[0])
                    if rs_now >= 0:
                        # 计算后数值合理，操纵数据库并返回True
                        cur.execute("UPDATE jiting SET people=" + str(rs_now) + " WHERE name='" + str(jtsx[0]) + "'")
                        jtconn.commit()
                        cur.close()
                        return True
                    # 人数小于0，不合理，关闭指针并返回False
                    else:
                        cur.close()
                        return False


def number_upload(n: str):
    # 初始化变量
    num = 1
    sx = []
    # 初始化数据库的连接并创建指针
    jtconn = sqlite3.connect("./db/jiting.db")
    cur = jtconn.cursor()

    # 获取机厅数量jts
    cur.execute("SELECT COUNT(id) FROM jiting")
    jts = cur.fetchall()
    # 从数据库提取机厅缩写
    while num <= jts[0][0]:
        cur.execute("SELECT name FROM jiting WHERE id=" + str(num))
        sx.append(cur.fetchall())
        num = num + 1
    # 正则表达式，分别匹配 <任意字母><任意数字>，如ch1
    if re.match('[a-z]+[0-9]+', n):
        jtsx = re.findall('[a-z]+', n)  # 机厅缩写
        jtrs = re.findall('[0-9]+', n)  # 机厅人数
        # 判断数据是否合理
        if int(jtrs[0]) >= 0:
            # 数据合理，执行数据库操作并返回True
            cur.execute("UPDATE jiting SET people=" + str(int(jtrs[0])) + " WHERE name='" + str(jtsx[0]) + "'")
            jtconn.commit()
            cur.close()
            return True
        else:
            # 数据不合理，返回False并关闭指针
            cur.close()
            return False
