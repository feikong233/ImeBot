import re
import sqlite3
import datetime
import random

# 初始化变量
num = 1
nc = []
# 初始化数据库连接并创建指针
dbconn = sqlite3.connect('../db/pushi_bieming.db', check_same_thread=False)
ps_cur = dbconn.cursor()

# 获取谱师数量cts
ps_cur.execute("SELECT COUNT(id) FROM charters")
cts = ps_cur.fetchall()

# 拉取谱师昵称列表
while num <= cts[0][0]:
    ps_cur.execute("SELECT bieming FROM charters WHERE id=" + str(num))
    res = str(ps_cur.fetchall()[0][0])
    # 分割生成列表便于匹配
    reslst = res.split(",")
    # 拼接列表
    nc.extend(reslst)
    num = num + 1
ps_cur.close()


# 检测匹配到的谱师名称是否存在在数据库缓存中
def check_if_legal(in_str):
    if in_str in nc:
        print("成功匹配到 " + in_str)
        return True
    else:
        print(in_str + "不在数据库缓存的谱师别名中")
        return False


# 实现随机抽取一个瑞萍，原函数random_charter_ruiping()
def api_random_ruiping():
    # 初始化新的指针
    rpconn = sqlite3.connect("../db/pushi_ruiping.db",check_same_thread=False)
    rp_cur = rpconn.cursor()

    # 随机抽取一个谱师的标准名
    ram = random.randint(1, cts[0][0])
    bm_cur = dbconn.cursor()
    bm_cur.execute(
        "SELECT charter_name FROM charters WHERE id= " + str(ram)
    )
    standard_charter = bm_cur.fetchall()[0][0]
    bm_cur.close()
    # 获取对应表里评论的数量
    rp_cur.execute(
        "SELECT COUNT(id) FROM " + standard_charter
    )
    comm_num = rp_cur.fetchall()[0][0]

    # 抽取到了一名没有被瑞萍过的谱师
    if int(comm_num) == 0:
        back_msg = {
            "is_match": True,
            "is_commented": False,
            "charter": standard_charter,
            "input_charter": None
        }
        return back_msg

    # 随机选择一条评论
    random_id = random.randint(1, comm_num)
    # 获取这条评论的内容和信息
    rp_cur.execute(
        "SELECT comments, date, member_name, qq_id FROM " + standard_charter + " WHERE id=" + str(random_id)
    )
    result = rp_cur.fetchall()[0]
    print(result)
    rp_cur.close()

    # 返回生成的list
    lst_ram_comment = {
        "charter": standard_charter,
        "member_name": result[2],
        "qq_id": result[3],
        "date": result[1],
        "comments": result[0]
    }
    return lst_ram_comment


# 实现抽取指定谱师的一条瑞萍，原函数if_requesting_ruiping()
def api_random_charter_ruiping(input_str):
    # 调用检测函数检测是否符合缓存的缩写
    if check_if_legal(input_str):
        charter = input_str

        # 初始化指针
        bm_cur = dbconn.cursor()
        rpconn = sqlite3.connect("../db/pushi_ruiping.db",check_same_thread=False)
        rp_cur = rpconn.cursor()

        # 获取别名对应的谱师标准名称
        bm_cur.execute("SELECT charter_name FROM charters WHERE bieming LIKE '%" + charter + "%'")
        standard_charter = str(bm_cur.fetchall()[0][0])
        bm_cur.close()

        # 获取对应表里评论的数量
        rp_cur.execute(
            "SELECT COUNT(id) FROM " + standard_charter
        )
        comm_num = rp_cur.fetchall()[0][0]
        if int(comm_num) == 0:
            back_msg = {
                "is_match": True,
                "is_commented": False,
                "charter": standard_charter,
                "input_charter": input_str
                }
            return back_msg
        # 随机选择一条评论
        random_id = random.randint(1, comm_num)
        # 获取这条评论的内容和信息
        rp_cur.execute(
            "SELECT comments, date, member_name, qq_id FROM " + standard_charter + " WHERE id=" + str(random_id)
        )
        result = rp_cur.fetchall()[0]
        rp_cur.close()

        # 返回生成的list
        lst_ram_comment = {
            "sd_charter": standard_charter,
            "input_charter": input_str,
            "member_name": result[2],
            "qq_id": result[3],
            "comments": result[0]
        }
        return lst_ram_comment
    else:
        lst_back = {
            "is_match": False,
            "is_commented": False,
            "charter": None,
            "input_charter": input_str
        }
        return lst_back
