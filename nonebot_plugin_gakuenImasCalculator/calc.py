from nonebot.adapters import Bot, Message, Event
from nonebot.plugin.on import on_command
from nonebot.params import Arg, CommandArg
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from math import ceil
from decimal import Decimal
from typing import List


calc_rank = on_command(
    "算分",
    aliases={},
    priority=20,
    block=True,
)

@calc_rank.handle()
async def _(bot: Bot, event: Event , matcher: Matcher, cmd_arg: Message = CommandArg()):
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
    elif juliA <= 3950:
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
    elif juliAp <= 3950:
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
    elif juliS <= 3950:
        Sscore = ceil((juliS - 3250 )/ 0.01)
    else:
        Sscore = -1

    retmessage = ""
    if shuxingyichuFLAG:
        retmessage += "属性溢出了，单属性最高只计算1500\n"
    retmessage += "你的属性总合为： " + str(VO) + " + " + str(DI) + " + " + str(VI) + " + 90 = " + str((VO + DI + VI + Decimal(90))) + "\n"
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





calc_highattr = on_command(
    "算属性",
    aliases={},
    priority=20,
    block=True,
)

indextrans = ["红","蓝","黄"]

def _caclattr2(attrlist , attrbonuslist , choose):
    #choose 165 all 145
    addattrlist = [145,145,145]
    addattrlist[choose] += 165
    addattrlist =  [x * (1+y) for x, y in zip(addattrlist, attrbonuslist)]
    resultlist =  [x + y for x, y in zip(attrlist, addattrlist)]
    return resultlist

def _caclattr1(attrlist , attrbonuslist , examsplist , choose):
    if examsplist is None:
        raise ValueError("examsplist长度错误")
    #150 sp 220
    addattr = 220 if examsplist[choose] == 1 else 150
    addattr += addattr * attrbonuslist[choose]
    resultlist = attrlist.copy()
    resultlist[choose] += addattr
    return resultlist

    

def _caclattr(stage , attrlist , attrbonuslist , examsplist):
    if len(attrlist) < 3 or len(attrbonuslist) < 3:
        raise ValueError("attrlist/attrbonuslist长度错误")
    
    attrbonuslist =  [number / 100 for number in attrbonuslist]
    
    templist = []
    resultlist = []
    if stage == 1:
        for i in range(3):
            templist.append(
                _caclattr1(attrlist , attrbonuslist , examsplist , i)
                )
    else:
        templist.append(attrlist)

    for i in range(3):
        for j in range(3):
            if(len(templist) <= i):
                break
            resultlist.append((i,j,
                              _caclattr2(templist[i],attrbonuslist,j)
            ))
            
    return resultlist
    
def printallitem(resultlist):
    messgae = ""
    for item in resultlist:
        sumattr = sum(min(thisattr, 1470) for thisattr in item[2]) + 90
        
        if len(resultlist) == 3:
            messgae += "选择 " + indextrans[item[1]] + "："
        else:
            messgae += "选择 " + indextrans[item[0]] + " " + indextrans[item[1]] + "："

        sumattr = sum(min(thisattr, 1470) for thisattr in item[2]) + 90
        messgae += "属性为" + str(min(1470,int(item[2][0]))) + "+" + str(min(1470,int(item[2][1]))) + "+" + str(min(1470,int(item[2][2]))) + "+90=" + str(int(sumattr)) + "\n"

    return messgae


def printmaxitem(resultlist):
    maxattr = 0
    maxitem = None
    for item in resultlist:
        sumattr = sum(min(thisattr, 1470) for thisattr in item[2])
        if sumattr > maxattr:
            maxattr = sumattr
            maxitem = item

    messgae = ""
    if len(resultlist) == 3:
        messgae += "选择 " + indextrans[maxitem[1]] + "："
    else:
        messgae += "选择 " + indextrans[maxitem[0]] + " " + indextrans[maxitem[1]] + "："

    sumattr = sum(min(thisattr, 1470) for thisattr in maxitem[2]) + 90
    messgae += "属性为" + str(min(1470,int(maxitem[2][0]))) + "+" + str(min(1470,int(maxitem[2][1]))) + "+" + str(min(1470,int(maxitem[2][2]))) + "+90=" + str(int(sumattr)) + "\n"
    return messgae



@calc_highattr.handle()
async def _(bot: Bot, event: Event , matcher: Matcher, cmd_arg: Message = CommandArg()):
    pass

@calc_highattr.got("examstage",prompt="请输入数字指定场景：1、最后一次普通训练或者sp训练2、期末前追训")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("examstage")):
    args: List[str] = cmd_arg.extract_plain_text().strip().split()

    if(len(args) == 3):
        if(state["examstage1"] != 1):
            await matcher.finish("参数错误，算属性结束！1")
        state["examstagesp"] = [int(x) for x in args]
        await matcher.send("请输入当前三维属性红蓝黄，以空格分割")
    elif(len(args) == 1):
        myarg = int(args[0])
        if myarg == 1 :
            state["examstage1"] = myarg
            await matcher.reject("请输入3训练是否有sp，1代表有0代表没有，以空格分割，如1 0 0")
        if myarg == 2 :
            state["examstage1"] = myarg
            state["examstagesp"] = None
            await matcher.send("请输入当前三维属性红蓝黄，以空格分割")
        else:
            await matcher.finish("参数错误，算属性结束！2")
    else:
        await matcher.finish("参数错误，算属性结束！3")

@calc_highattr.got("examattr")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("examattr")):
    args: List[str] = cmd_arg.extract_plain_text().strip().split()

    if(len(args) != 3):
        await matcher.finish("参数错误，算属性结束！4")

    try:
        state["attrlist"] = [int(args[0]),int(args[1]),int(args[2])]
    except:
        await matcher.finish("参数错误，算属性结束！5")
    await matcher.send("请输入三属性额外增加百分比（省略百分号），以空格分割")

@calc_highattr.got("examattrbonus")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("examattrbonus")):
    args: List[str] = cmd_arg.extract_plain_text().strip().split()

    if(len(args) != 3):
        await matcher.finish("参数错误，算属性结束！6")

    try:
        state["attrbonuslist"] = [float(args[0]),float(args[1]),float(args[2])]
    except:
        await matcher.finish("参数错误，算属性结束！7")

    resultlist = _caclattr(state["examstage1"],state["attrlist"],state["attrbonuslist"],state["examstagesp"])
    message = printmaxitem(resultlist)
    state["resultlist"] = resultlist
    await matcher.send(message + "输入1查看详细属性，其他输入会结束本次计算")

@calc_highattr.got("detail")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("detail")):
    args = cmd_arg.extract_plain_text().strip()
    if args != "1":
        await matcher.finish("已结束！")

    message = printallitem(state["resultlist"])

    await matcher.finish(message)