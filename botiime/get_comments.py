import re
import sqlite3

# 初始化变量
num = 1
nc = []
# 初始化数据库连接并创建指针
dbconn = sqlite3.connect('../db/pushi_bieming.db')
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


# 检测接收到的消息链是否符合格式，符合则传回True
def check_if_ruiping(in_str):
    if re.findall('ime (rp|ruiping|锐评|瑞平|瑞萍)|(rp|ruiping|锐评|瑞平|瑞萍) ', in_str):
        lst = re.match(r'(ime\s(rp|ruiping|锐评|瑞平|瑞萍)|(rp|ruiping|锐评|瑞平|瑞萍)\s)\s*(\S+)\s(.+)', in_str, re.I)
        print(lst.group(4))
        print(lst.group(5))
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
    bm_cur = dbconn.cursor()

    # 获取别名对应的谱师标准名称
    bm_cur.execute("SELECT charter_name FROM charters WHERE bieming LIKE '%" + charter + "%'")
    standard_charter = str(bm_cur.fetchall()[0][0])
    return standard_charter


resdef = is_ruiping("ime rp 翠 你妈死了。")
print(resdef)