from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import Bot,  GroupMessageEvent
from nonebot.adapters.onebot.v11.helpers import Cooldown
from nonebot.adapters.onebot.v11.message import MessageSegment
from .calc import *

on_command(
    "算分",
    aliases={},
    priority=20,
    block=True,
    handlers=[calc_rank]
)