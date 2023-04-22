from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.saya import Channel
from graia.scheduler import timers, GraiaScheduler
from graia.scheduler.saya import SchedulerSchema

from botiime.arcade_processing import db_reload
from botiime.bing import bing_image_get

channel = Channel.current()
sche = create(GraiaScheduler)


@channel.use(
    SchedulerSchema(
        timers.crontabify(
            "30 1 * * * 1"
        )
    )
)
async def db_reloader(app: Ariadne):
    await bing_image_get()
    db_reload("zhoukou")
    db_reload("galiwo")
    db_reload("arcade")
    await app.send_group_message(738392519, MessageChain("现在是凌晨1：30，机厅人数已经自动重置！"))
    await app.send_group_message(823160932, MessageChain("现在是凌晨1：30，机厅人数已经自动重置！"))
    await app.send_group_message(1003802944, MessageChain("现在是凌晨1：30，机厅人数已经自动重置！"))
