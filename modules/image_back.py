import os

from graia.ariadne.message.element import Image
from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

from botiime.get_image import get_dargon

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage]
    )
)
async def image_back(app: Ariadne, sender: Union[Group, Friend], msg: MessageChain):
    if str(msg) in ["随机龙图", "ime 随机龙图", "ime dragon", "ime sjlt"]:
        if get_dargon():
            await app.send_message(sender, MessageChain(Image(path="./imgs/dragon.jpg")))
            os.remove("./imgs/dragon.jpg")
        else:
            await app.send_message((sender, MessageChain("随机龙图 功能似乎发生了故障！")))
