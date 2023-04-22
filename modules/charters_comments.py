import re
from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

from botiime.get_comments import check_if_ruiping

channel = Channel.current()


# 实现监听消息链并检测条件
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage]
    )
)
async def charters_commenting(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    check_if_ruiping(str(message))
