from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.saya import Channel
from graia.scheduler import timers, GraiaScheduler
from graia.scheduler.saya import SchedulerSchema

from botiime.arcade_processing import db_reload

channel = Channel.current()
sche = create(GraiaScheduler)


@channel.use(
    SchedulerSchema(
        timers.crontabify(
            "30 23 * * * *"
        )
    )
)
async def db_reloader(app: Ariadne):
    db_reload()
    await app.send_group_message(738392519, MessageChain("现在是晚上11：30，机厅人数已经自动重置！"))
