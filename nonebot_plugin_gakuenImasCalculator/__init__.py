from nonebot.plugin.on import on_command
from .calc import *

from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="学园偶像大师算分插件",
    description="学院偶像大师算分",
    usage="在群聊中输入“算分”与三维属性",

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="https://github.com/ikarosf/nonebot_plugin_gakuenImasCalculator",
    # 发布必填。

    #config=Config,
    # 插件配置项类，如无需配置可不填写。

    #supported_adapters={},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

on_command(
    "算分",
    aliases={},
    priority=20,
    block=True,
    handlers=[calc_rank]
)