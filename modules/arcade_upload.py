from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from botiime.arcade_processing import changes_upload, people_query, number_upload

channel = Channel.current()


# 实现监听消息链并检测条件
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage]
    )
)
async def upl(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    msg = str(message)
    if changes_upload(msg):
        await app.send_message(sender, MessageChain("数据已更新！"))
        # 查询一次人数
        await app.send_message(sender, MessageChain(people_query()))
    elif number_upload(msg):
        await app.send_message(sender, MessageChain("数据已更新！"))
        # 查询一次人数
        await app.send_message(sender, MessageChain(people_query()))