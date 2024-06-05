from typing import List
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.matcher import Matcher
from math import ceil
from decimal import Decimal

async def calc_rank(bot: Bot, event: GroupMessageEvent , matcher: Matcher, cmd_arg: Message = CommandArg()):
    args: List[str] = cmd_arg.extract_plain_text().strip().split()

    if(len(args) != 3):
        await matcher.finish("参数错误，请输入角色三维")

    shuxingyichuFLAG = False
    VO = Decimal(args[0])
    DI = Decimal(args[1])
    VI = Decimal(args[2])

    if VO > 1470:
        VO = Decimal(1470)
        shuxingyichuFLAG = True
    if DI > 1470:
        DI = Decimal(1470)
        shuxingyichuFLAG = True
    if VI > 1470:
        VI = Decimal(1470)
        shuxingyichuFLAG = True
    
    shuxingfen = int((VO + DI + VI + Decimal(90))* Decimal(str(2.3)))
    mingcifen = 1700

    '''
    <5000 max:1500
    <10000 2250
    <20000 3050
    <30000 3450
    <40000 3650
    <50000 3750
    
    '''
    A_rank = 10000
    Ap_rank = 11500
    S_rank = 13000
    biaoxianfenlist = [1500,2250,3050,3450,3650,3750]

    juliA = A_rank - shuxingfen - mingcifen
    juliAp = Ap_rank - shuxingfen - mingcifen
    juliS = S_rank - shuxingfen - mingcifen

    if juliA <= 0:
        Ascore = 0
    elif juliA <= 1500:
        Ascore = ceil(juliA / 0.3)
    elif juliA <= 2250:
        Ascore = ceil((juliA - 750 )/ 0.15)
    elif juliA <= 3050:
        Ascore = ceil((juliA - 1450 )/ 0.08)
    elif juliA <= 3450:
        Ascore = ceil((juliA - 2250 )/ 0.04)
    elif juliA <= 3650:
        Ascore = ceil((juliA - 2850 )/ 0.02)
    elif juliA <= 3650:
        Ascore = ceil((juliA - 3250 )/ 0.01)
    else:
        Ascore = -1

    if juliAp <= 0:
        Apscore = 0
    elif juliAp <= 1500:
        Apscore = ceil(juliAp / 0.3)
    elif juliAp <= 2250:
        Apscore = ceil((juliAp - 750 )/ 0.15)
    elif juliAp <= 3050:
        Apscore = ceil((juliAp - 1450 )/ 0.08)
    elif juliAp <= 3450:
        Apscore = ceil((juliAp - 2250 )/ 0.04)
    elif juliAp <= 3650:
        Apscore = ceil((juliAp - 2850 )/ 0.02)
    elif juliAp <= 3650:
        Apscore = ceil((juliAp - 3250 )/ 0.01)
    else:
        Apscore = -1

    if juliS <= 0:
        Sscore = 0
    elif juliS <= 1500:
        Sscore = ceil(juliS / 0.3)
    elif juliS <= 2250:
        Sscore = ceil((juliS - 750 )/ 0.15)
    elif juliS <= 3050:
        Sscore = ceil((juliS - 1450 )/ 0.08)
    elif juliS <= 3450:
        Sscore = ceil((juliS - 2250 )/ 0.04)
    elif juliS <= 3650:
        Sscore = ceil((juliS - 2850 )/ 0.02)
    elif juliS <= 3650:
        Sscore = ceil((juliS - 3250 )/ 0.01)
    else:
        Sscore = -1

    retmessage = ""
    if shuxingyichuFLAG:
        retmessage += "属性溢出了，单属性最高只计算1500\n"
    if Ascore == -1:
        retmessage += "杂鱼连A都不可能到的，杂鱼杂鱼"
        await matcher.finish(retmessage)
    elif Ascore == 0:
        retmessage += "已经稳A了\n"
    else:
        retmessage += "A评价需要获得" + str(Ascore) + "分\n"

    if Apscore == -1:
        retmessage += "想拿到A+就做梦吧"
        await matcher.finish(retmessage)
    elif Apscore == 0:
        retmessage += "已经稳A+了\n"
    else:
        retmessage += "A+评价需要获得" + str(Apscore) + "分\n"

    if Sscore == -1:
        retmessage += "S是你得不到的"
    elif Sscore == 0:
        retmessage += "已经稳S了???你开了吧"
    else:
        retmessage += "S评价需要获得" + str(Sscore) + "分"
    await matcher.finish(retmessage)
