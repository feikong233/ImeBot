import re
import sqlite3
from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from jiting_cx import renshu_chaxun

channel = Channel.current()

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


# 编写函数对人数增减消息进行检测和拆分，然后上传到数据库
def zengjian_upload(n: str):
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
                    # 操作数据库
                    cur.execute("UPDATE jiting SET people=" + str(rs_now) + " WHERE name='" + str(jtsx[0]) + "'")
                    jtconn.commit()
                    return True

                else:
                    rs_now = rs_past - int(jtrs[0])
                    if rs_now >= 0:
                        cur.execute("UPDATE jiting SET people=" + str(rs_now) + " WHERE name='" + str(jtsx[0]) + "'")
                        jtconn.commit()
                        return True
                    # 如果人数小于0则判断为不合法值
                    else:
                        return False


# 实现监听消息链并检测条件
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage]
    )
)
async def upl(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    msg = str(message)
    if zengjian_upload(msg):
        await app.send_message(sender, MessageChain("数据已更新！"))
        await app.send_message(sender, MessageChain(renshu_chaxun()))
