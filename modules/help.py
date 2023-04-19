from typing import Union
from PIL import Image, ImageDraw, ImageFont
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
async def help_msg(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    if str(message) in ["ime help", "!ime", "！ime"]:
        # help信息
        help_message_one = [
            "ImeBot DX v0.0.1 By Botiime\n"
            "你可以使用!ime help或者ime help来打开帮助菜单！\n"
        ]
        help_message_two = [
            "ime jtj - 查询机厅当前的人数\n"
            "ime <机厅名或缩写> [±] <数值> - 上报机厅人数\n"
            "ime b40/b50 - 简短的查看自己的b40/b50数值\n"
        ]
        help_message_three = [
            "ime bz/mryt/每日一图 - 获取今日的必应每日一图\n"
            "ime dragon/随机龙图 - 获取一张随机龙图\n"
        ]
        await app.send_message(sender, MessageChain(help_message_one))
        await app.send_message(sender, MessageChain(help_message_two))
        await app.send_message(sender, MessageChain(help_message_three))

