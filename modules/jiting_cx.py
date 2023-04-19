import sqlite3
from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()

# 加载数据库并初始化指针
jtconn = sqlite3.connect("./db/jiting.db")
cur = jtconn.cursor()

# 从数据库检索id列的行数量，存为jts（机厅数）
cur.execute("SELECT COUNT(id) FROM jiting")
jts = cur.fetchall()


def renshu_chaxun():
    num = 1
    cx = ""
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
    return cx


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage]
    )
)
async def jtj(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    # 检测对应命令
    if str(message) in ["ime jtj", "机厅几", "机厅人数", "jtrs", "ime jtrs", "ijtj"]:
        # 发送消息
        await app.send_message(sender, MessageChain("机厅信息：\n" + renshu_chaxun() + "更多功能请使用ime help查询"))
        # 关闭指针
        cur.close()
