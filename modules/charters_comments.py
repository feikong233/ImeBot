from graia.ariadne.message.element import Image
from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Friend, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

from botiime.get_comments import check_if_ruiping, is_ruiping, if_requesting_ruiping

channel = Channel.current()


# 实现监听消息链并检测条件
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage]
    )
)
async def charters_commenting(app: Ariadne, sender: Union[Group, Friend], message: MessageChain, member: Member):
    if check_if_ruiping(str(message)):
        qq_id = str(member.id)
        member_name = str(member.name)
        res = is_ruiping(str(message), qq_id, member_name)
        await app.send_message(sender, MessageChain(res))
    elif str(message) in ["ime 谱师别名列表", "ime rplb", "ime 别名列表"]:
        await app.send_message(sender, MessageChain(Image(path="./imgs/charters.png")))
    else:
        res = if_requesting_ruiping(str(message))
        if res:
            await app.send_message(sender, MessageChain(res))
