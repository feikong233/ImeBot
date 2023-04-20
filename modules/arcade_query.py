import sqlite3
from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from botiime.arcade_processing import people_query, arcade_query

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage]
    )
)
async def jtj(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    # 检测对应命令
    if str(message) in ["ime jtj", "机厅几", "机厅人数", "jtrs", "ime jtrs", "ijtj"]:
        # 发送消息
        await app.send_message(sender, MessageChain("机厅信息：\n" + people_query() + "更多功能请使用ime help查询"))
    else:
        # 检测是否符合机厅查询条件，如果符合就返回函数内生成的字符串
        temp = arcade_query(str(message))
        if isinstance(temp, str):
            await app.send_message(sender, MessageChain(temp))
