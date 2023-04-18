import sqlite3
from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage]
    )
)
async def jtj(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    jtconn = sqlite3.connect("./db/jiting.db")
    cur = jtconn.cursor()
    if str(message) in ["jtj", "机厅几", "机厅人数", "jtrs"]:
        num = 1
        cx = ""
        cur.execute("SELECT COUNT(id) FROM jiting")
        jts = cur.fetchall()

        while num <= int(jts[0][0]):
            cur.execute("SELECT fullname FROM jiting WHERE id=" + str(num))
            jtmc = cur.fetchall()
            cur.execute("SELECT people FROM jiting WHERE id=" + str(num))
            jtrs = cur.fetchall()
            cx = cx + str(jtmc[0][0]) + " 现在有 " + str(jtrs[0][0]) + " 人\n"
            num = num + 1
        await app.send_message(sender, MessageChain("机厅信息：\n" + cx + "\n更多功能请使用ime help查询"))
