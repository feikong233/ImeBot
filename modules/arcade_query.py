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
async def jtj(app: Ariadne, sender: Union[Group, Friend], message: MessageChain, group: Group):
    if str(group.id) in ["823160932"]:
        # 检测对应命令
        if str(message) in ["ime jtj", "机厅几", "机厅人数", "jtrs", "ime jtrs", "ijtj"]:
            # 发送消息
            await app.send_message(sender, MessageChain("ImeBotDX β0.1.5\n当前地区：周口\n\n" + people_query("zhoukou")))
        else:
            # 检测是否符合机厅查询条件，如果符合就返回函数内生成的字符串
            temp = arcade_query(str(message), "zhoukou")
            if isinstance(temp, str):
                await app.send_message(sender, MessageChain(temp))
    elif str(group.id) in ["738392519"]:
        # 检测对应命令
        if str(message) in ["ime jtj", "机厅几", "机厅人数", "jtrs", "ime jtrs", "ijtj"]:
            # 发送消息
            await app.send_message(sender, MessageChain("ImeBotDX β0.1.5\n当前地区：梦里\n\n" + people_query("arcade")))
        else:
            # 检测是否符合机厅查询条件，如果符合就返回函数内生成的字符串
            temp = arcade_query(str(message), "arcade")
            if isinstance(temp, str):
                await app.send_message(sender, MessageChain(temp))
    elif str(group.id) in ["1003802944"]:
        # 检测对应命令
        if str(message) in ["ime jtj", "机厅几", "机厅人数", "jtrs", "ime jtrs", "ijtj"]:
            # 发送消息
            await app.send_message(sender, MessageChain("ImeBotDX β0.1.5\n当前地区：咖喱窝\n\n" + people_query("galiwo")))
        else:
            # 检测是否符合机厅查询条件，如果符合就返回函数内生成的字符串
            temp = arcade_query(str(message), "arcade")
            if isinstance(temp, str):
                await app.send_message(sender, MessageChain(temp))
