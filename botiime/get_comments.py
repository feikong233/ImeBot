import re
import sqlite3
import datetime
import random

# 初始化变量
num = 1
nc = []
# 初始化数据库连接并创建指针
dbconn = sqlite3.connect('./db/pushi_bieming.db')
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


# 检测接收到的消息链是否符合格式，符合则传回True
def check_if_ruiping(in_str):
    if re.findall(r'(ime\s(rp|ruiping|锐评|瑞平|瑞萍)|(rp|ruiping|锐评|瑞平|瑞萍)\s)\s*(\S+)\s(.+)', in_str):
        return True
    else:
        return False


# 检测匹配到的谱师名称是否存在在数据库缓存中
def check_if_legal(in_str):
    if in_str in nc:
        print("成功匹配到 " + in_str)
        return True
    else:
        print(in_str + "不在数据库缓存的谱师别名中")
        return False


# 入口函数，框架传入qq号和成员群昵称以及消息链内容，自动匹配截取对应的内容，格式化后传入瑞平函数进行上传
def is_ruiping(in_str, qq_id="114514", member_name="undefined"):
    lst = re.match(r'(ime\s(rp|ruiping|锐评|瑞平|瑞萍)|(rp|ruiping|锐评|瑞平|瑞萍)\s)\s*(\S+)\s(.+)', in_str, re.I)
    charter = str(lst.group(4))
    comments = str(lst.group(5))
    if check_if_legal(charter):
        back = ruiping(qq_id, member_name, charter, comments)
        return back
    else:
        back = "你输入的谱师别名不存在哦！"
        return back


# 瑞平功能函数，传入的参数为已经两次匹配正确符合格式并且存在对应条目的信息，这里实现对信息的上报
def ruiping(qq_id="undefined", member_name="undefined", charter="翠楼屋", comments="never mind the scandal and libel."):
    # 初始化新的指针
    rpconn = sqlite3.connect("./db/pushi_ruiping.db")
    rp_cur = rpconn.cursor()
    bm_cur = dbconn.cursor()

    # 获取别名对应的谱师标准名称
    bm_cur.execute("SELECT charter_name FROM charters WHERE bieming LIKE '%" + charter + "%'")
    standard_charter = str(bm_cur.fetchall()[0][0])

    # 获取当天日期
    date = str(datetime.datetime.now().strftime('%Y-%m-%d'))

    # 存入数据库
    rp_cur.execute(
        "INSERT INTO " + standard_charter + " (comments,date,member_name,qq_id) VALUES ('" + comments + "', '" + date + "', '" + member_name + "', '" + qq_id + "' )"
    )
    rpconn.commit()
    # 返回信息
    back_msg = "已经上传了对 " + standard_charter + " 的瑞平！"
    bm_cur.close()
    rp_cur.close()
    return back_msg


# 实现随机抽取一个瑞萍
def random_charter_ruiping():
    # 初始化新的指针
    rpconn = sqlite3.connect("./db/pushi_ruiping.db")
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
    if int(comm_num) == 0:
        back_msg = "抽到了一位没有被瑞平过的谱师哦：" + standard_charter + " 使用 ime 瑞平/rp " + standard_charter + " 瑞平内容 来瑞平他！"
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
    # 返回生成的字符串
    ram_comment = '"' + standard_charter + " " + result[0] + '"' + "\n——\n来自 " + result[2] + " @" + result[3] + " \n" + result[1]
    return ram_comment


# 检测输入的字符串是否满足标准并且在满足不同要求时分别调用两种函数
def if_requesting_ruiping(in_str):
    # 检测是否为 ime 随机瑞平 格式
    if re.findall(r'^(ime\s(随机瑞萍|随机瑞平|随机锐评|sjrp)|(随机锐评|随机瑞平|随机瑞萍)\s*)$', in_str, re.I):
        return random_charter_ruiping()
    # 检测是否为 ime 随机锐评 谱师 格式
    elif re.findall(r'ime\s(随机瑞萍|随机瑞平|随机锐评|sjrp)|(随机锐评|随机瑞平|随机瑞萍)\s', in_str, re.I):
        match_result = re.match(r'(ime\s(随机瑞萍|随机瑞平|随机锐评|sjrp)|(随机锐评|随机瑞平|随机瑞萍)\s)\s*(\S+)', in_str)
        print("已匹配 ime <瑞平> <谱师>！")
        # 检测输入的谱师是否合理，复用之前的函数
        if check_if_legal(match_result.group(4)):
            print(match_result.group(4))
            charter = match_result.group(4)

            # 初始化指针
            bm_cur = dbconn.cursor()
            rpconn = sqlite3.connect("./db/pushi_ruiping.db")
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
                back_msg = "这位谱师还没有被瑞平过：" + standard_charter + " 使用 ime 瑞平/rp " + standard_charter + " 瑞平内容 来瑞平他！"
                return back_msg
            # 随机选择一条评论
            random_id = random.randint(1, comm_num)
            # 获取这条评论的内容和信息
            rp_cur.execute(
                "SELECT comments, date, member_name, qq_id FROM " + standard_charter + " WHERE id=" + str(random_id)
            )
            result = rp_cur.fetchall()[0]
            rp_cur.close()

            # 返回生成的字符串
            ram_comment = '"' + standard_charter + " " + result[0] + '"' + "\n——\n来自 " + result[2] + " @" + result[3] + " \n" + result[1]
            return ram_comment
        else:
            return "你输入的谱师名不在已缓存的别名数据中！"


# 这个函数用来生成一个谱师被瑞平次数排行榜
def commented_rank():
    # 初始化变量
    num = 1
    sd_name = []
    lst = []
    # 初始化数据库指针
    bmconn = sqlite3.connect("./db/pushi_bieming.db")
    rpconn = sqlite3.connect("./db/pushi_ruiping.db")
    bm_cur = bmconn.cursor()
    rp_cur = rpconn.cursor()
    # 遍历所有谱师的表，计算条目数量
    # 拉取谱师标准名称列表
    while num <= cts[0][0]:
        bm_cur.execute("SELECT charter_name FROM charters WHERE id=" + str(num))
        fullname = str(ps_cur.fetchall()[0][0])
        # 拼接列表
        sd_name.append(fullname)
        num = num + 1
    bm_cur.close()
    # 遍历，输出一个字典列表，列表中包含标准谱师名称和次数
    for i in sd_name:
        rp_cur.execute(
            "SELECT COUNT(id) FROM " + i
        )
        result = dict(sd_name=rp_cur.fetchall())
        lst.append(result)
