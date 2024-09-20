from nonebot.adapters import Bot, Message, Event
from nonebot.plugin.on import on_command
from nonebot.params import Arg, CommandArg
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from math import ceil
from decimal import Decimal
from typing import List
from .OCRattrs import getattrs
from .calcfun import _calc_rank , attrmaxMap

attrMAX = 1500
_attrMAX = attrMAX - 30

calc_rank = on_command(
    "算分",
    aliases={},
    priority=20,
    block=True,
)

@calc_rank.handle()
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State, cmd_arg: Message = CommandArg()):
    if cmd_arg:
        state["calcrankattr"] = cmd_arg


@calc_rank.got("calcrankattr",prompt="请输入三维数字或图片")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("calcrankattr")):
    for segment in cmd_arg:
        if segment.type == "image":
            args = getattrs(segment.data["url"])
            if(len(args) != 3):
                await matcher.finish("无法识别的图片")
            break
    else:
        args: List[str] = cmd_arg.extract_plain_text().strip().split()
        if(len(args) != 3):
            await matcher.finish("参数错误，请输入角色三维")

    VO = Decimal(args[0])
    DI = Decimal(args[1])
    VI = Decimal(args[2])

    onlyh = False
    onlym = False
    retmessage = ""

    if VO <= attrmaxMap["h"] - 30 and DI <= attrmaxMap["h"] - 30 and VI <= attrmaxMap["h"] - 30:
        onlyh = True

    if VO > attrmaxMap["h"] or DI > attrmaxMap["h"] or VI > attrmaxMap["h"]:
        onlym = True

    if not onlym:
        if not onlyh:
            retmessage += "在hard难度下：\n"
        retmessage += _calc_rank(VO,DI,VI,attrmaxMap["h"])

    if not onlyh:
        if not onlym:
            retmessage += "在master难度下：\n"
        retmessage += _calc_rank(VO,DI,VI,attrmaxMap["m"])

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
        sumattr = sum(min(thisattr, _attrMAX) for thisattr in item[2]) + 90
        
        if len(resultlist) == 3:
            messgae += "选择 " + indextrans[item[1]] + "："
        else:
            messgae += "选择 " + indextrans[item[0]] + " " + indextrans[item[1]] + "："

        sumattr = sum(min(thisattr, _attrMAX) for thisattr in item[2]) + 90
        messgae += "属性为" + str(min(_attrMAX,int(item[2][0]))) + "+" + str(min(_attrMAX,int(item[2][1]))) + "+" + str(min(_attrMAX,int(item[2][2]))) + "+90=" + str(int(sumattr)) + "\n"

    return messgae


def printmaxitem(resultlist):
    maxattr = 0
    maxitem = None
    for item in resultlist:
        sumattr = sum(min(thisattr, _attrMAX) for thisattr in item[2])
        if sumattr > maxattr:
            maxattr = sumattr
            maxitem = item

    messgae = ""
    if len(resultlist) == 3:
        messgae += "选择 " + indextrans[maxitem[1]] + "："
    else:
        messgae += "选择 " + indextrans[maxitem[0]] + " " + indextrans[maxitem[1]] + "："

    sumattr = sum(min(thisattr, _attrMAX) for thisattr in maxitem[2]) + 90
    messgae += "属性为" + str(min(_attrMAX,int(maxitem[2][0]))) + "+" + str(min(_attrMAX,int(maxitem[2][1]))) + "+" + str(min(_attrMAX,int(maxitem[2][2]))) + "+90=" + str(int(sumattr)) + "\n"
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
        try:
            state["examstagesp"] = [int(x) for x in args]
        except:
            await matcher.finish("参数错误，算属性结束！2")
        await matcher.send("请输入当前三维属性红蓝黄，以空格分割")
    elif(len(args) == 1):
        try:
            myarg = int(args[0])
        except:
            await matcher.finish("参数错误，算属性结束！3")
        if myarg == 1 :
            state["examstage1"] = myarg
            await matcher.reject("请输入3训练是否有sp，1代表有0代表没有，以空格分割，如1 0 0")
        if myarg == 2 :
            state["examstage1"] = myarg
            state["examstagesp"] = None
            await matcher.send("请输入当前三维属性红蓝黄，以空格分割")
        else:
            await matcher.finish("参数错误，算属性结束！4")
    else:
        await matcher.finish("参数错误，算属性结束！5")

@calc_highattr.got("examattr")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("examattr")):
    args: List[str] = cmd_arg.extract_plain_text().strip().split()

    if(len(args) != 3):
        await matcher.finish("参数错误，算属性结束！6")

    try:
        state["attrlist"] = [int(args[0]),int(args[1]),int(args[2])]
    except:
        await matcher.finish("参数错误，算属性结束！7")
    await matcher.send("请输入三属性额外增加百分比（省略百分号），以空格分割")

@calc_highattr.got("examattrbonus")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("examattrbonus")):
    args: List[str] = cmd_arg.extract_plain_text().strip().split()

    if(len(args) != 3):
        await matcher.finish("参数错误，算属性结束！8")

    try:
        state["attrbonuslist"] = [float(args[0]),float(args[1]),float(args[2])]
    except:
        await matcher.finish("参数错误，算属性结束！9")

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