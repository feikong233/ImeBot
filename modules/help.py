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
async def help_msg(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    if str(message) in ["ime help", "!ime", "！ime"]:
        # help信息
        help_message_one = [
            "ImeBot DX Beta0.1.3 By Botiime\n"
            "这个Bot开源于https://github.com/feikong233/ImeBot\n"
            "你可以使用!ime或者ime help来打开帮助菜单！\n"
        ]
        help_message_two = [
            "ime jtj - 查询所有机厅当前的人数\n"
            "<机厅名或缩写>[±]<数值> - 上报机厅人数\n"
            "<机厅名或缩写>j - 查询机厅人数\n"
            "ime b40/b50 - 简短的查看自己的b40/b50数值(未实现)\n"
        ]
        help_message_three = [
            "ime bz/mryt/每日一图 - 获取今日的必应每日一图\n"
            "ime dragon/随机龙图 - 获取一张随机龙图(未实现)\n"
        ]
        await app.send_message(sender, MessageChain(help_message_one))
        await app.send_message(sender, MessageChain(help_message_two))
        await app.send_message(sender, MessageChain(help_message_three))

