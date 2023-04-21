import datetime
from time import sleep
from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

from botiime.bing import try_todays_bing, bing_image_get, bing_info_get

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage]
    )
)
async def everyday_bing_image(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    if str(message) in ["ime 每日一图", "每日一图", "！每日一图", "!每日一图", "ime bz", "ime mryt"]:
        # 如果每日一图已经存在，那么直接从文件夹获取今天的每日一图
        if try_todays_bing():
            date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            bing_image = "./imgs/bing/" + date + "-bing.jpg"
            info = await bing_info_get()
            await app.send_message(sender, MessageChain(Image(path=bing_image)))
            sleep(0.7)
            await app.send_message(sender, MessageChain(
                '"' + info[0] + '"\n来源：Microsoft Bing & ' + info[1] + '\n地址' + info[2]))
        else:
            # 如果每日一图不存在，就生成后再获取
            await bing_image_get()

            date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            bing_image = "./imgs/bing/" + date + "-bing.jpg"
            info = await bing_info_get()
            await app.send_message(sender, MessageChain(Image(path=bing_image)))
            sleep(1)
            await app.send_message(sender, MessageChain(
                '"' + info[0] + '"\n来源：Microsoft Bing & ' + info[1] + '\n地址: ' + info[2]))
