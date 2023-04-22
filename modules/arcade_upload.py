from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

from botiime.arcade_processing import changes_upload, number_upload

channel = Channel.current()


# 实现监听消息链并检测条件
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage]
    )
)
async def upl(app: Ariadne, sender: Union[Group, Friend], message: MessageChain, group: Group):
    # if str(group.id) in ["823160932"]:
        # msg = str(message)
        # case_changes = changes_upload(msg, "zhoukou")
        # case_number = number_upload(msg, "zhoukou")
        # if isinstance(case_changes, str):
            # 查询一次人数
            # await app.send_message(sender, MessageChain(case_changes))
        # elif isinstance(case_number, str):
            # 查询一次人数
            # await app.send_message(sender, MessageChain(case_number))
    if str(group.id) in ["738392519"]:
        msg = str(message)
        case_changes = changes_upload(msg, "arcade")
        case_number = number_upload(msg, "arcade")
        if isinstance(case_changes, str):
            # 查询一次人数
            await app.send_message(sender, MessageChain(case_changes))
        elif isinstance(case_number, str):
            # 查询一次人数
            await app.send_message(sender, MessageChain(case_number))
    elif str(group.id) in ["1003802944"]:
        msg = str(message)
        case_changes = changes_upload(msg, "galiwo")
        case_number = number_upload(msg, "galiwo")
        if isinstance(case_changes, str):
            # 查询一次人数
            await app.send_message(sender, MessageChain(case_changes))
        elif isinstance(case_number, str):
            # 查询一次人数
            await app.send_message(sender, MessageChain(case_number))
