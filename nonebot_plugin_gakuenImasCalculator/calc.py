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

def _caclattr1(attrlist , attrbonuslist , examsplist , choose , examLv):
    if examsplist is None:
        raise ValueError("examsplist长度错误")
    #h:150 sp 220
    #m:210 sp 280
    if examLv == "h":
        addattr = 220 if examsplist[choose] == 1 else 150
    else:
        addattr = 280 if examsplist[choose] == 1 else 210
    addattr += addattr * attrbonuslist[choose]
    resultlist = attrlist.copy()
    resultlist[choose] += addattr
    return resultlist

    

def _caclattr(stage , attrlist , attrbonuslist , examsplist, examLv):
    if len(attrlist) < 3 or len(attrbonuslist) < 3:
        raise ValueError("attrlist/attrbonuslist长度错误")
    
    attrbonuslist =  [number / 100 for number in attrbonuslist]
    
    templist = []
    resultlist = []
    if stage == 1:
        for i in range(3):
            templist.append(
                _caclattr1(attrlist , attrbonuslist , examsplist , i , examLv)
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
    
def printallitem(resultlist,_attrMAX):
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


def printmaxitem(resultlist,_attrMAX):
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

@calc_highattr.got("examstage",prompt="请输入数字指定场景：1、最后一次普通训练或者sp训练 2、期末前追训")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("examstage")):
    args: List[str] = cmd_arg.extract_plain_text().strip().split()

    if len(args) == 1:
        try:
            myarg = int(args[0])
        except:
            await matcher.finish("参数错误，算属性结束！examstage1")
        if myarg == 1 :
            state["examstage1"] = 1
        elif myarg == 2 :
            state["examstage1"] = 2
            state["examstagesp"] = -1
        else:
            await matcher.finish("参数错误，算属性结束！examstage2")
    else:
        await matcher.finish("参数错误，算属性结束！examstage3")


@calc_highattr.got("examstLv",prompt="请输入数字指定难度：1、hard难度 2、master难度")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("examstLv")):
    args: List[str] = cmd_arg.extract_plain_text().strip().split()

    if len(args) == 1:
        try:
            myarg = int(args[0])
        except:
            await matcher.finish("参数错误，算属性结束！examstLv1")
        if myarg == 1 :
            state["examstLv"] = "h"
        elif myarg == 2 :
            state["examstLv"] = "m"
        else:
            await matcher.finish("参数错误，算属性结束！examstLv2")
    else:
        await matcher.finish("参数错误，算属性结束！examstLv3")

@calc_highattr.got("examstagesp",prompt="请输入3训练是否有sp，1代表有0代表没有，以空格分割，如1 0 0")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("examstagesp")):
    args: List[str] = cmd_arg.extract_plain_text().strip().split()

    if state["examstage1"] == 2:
        return

    if(len(args) != 3):
        await matcher.finish("参数错误，算属性结束！examstagesp1")

    try:
        state["examstagesp"] = [int(x) for x in args]
    except:
        await matcher.finish("参数错误，算属性结束！examstagesp2")

@calc_highattr.got("examattr",prompt="请输入当前三维属性红蓝黄，以空格分割")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("examattr")):
    args: List[str] = cmd_arg.extract_plain_text().strip().split()

    if(len(args) != 3):
        await matcher.finish("参数错误，算属性结束！examattr1")

    try:
        state["attrlist"] = [int(args[0]),int(args[1]),int(args[2])]
    except:
        await matcher.finish("参数错误，算属性结束！examattr2")

@calc_highattr.got("examattrbonus" ,prompt="请输入三属性额外增加百分比（省略百分号），以空格分割")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("examattrbonus")):
    args: List[str] = cmd_arg.extract_plain_text().strip().split()

    if(len(args) != 3):
        await matcher.finish("参数错误，算属性结束！examattrbonus1")

    try:
        state["attrbonuslist"] = [float(args[0]),float(args[1]),float(args[2])]
    except:
        await matcher.finish("参数错误，算属性结束！examattrbonus2")

    resultlist = _caclattr(state["examstage1"],state["attrlist"],state["attrbonuslist"],state["examstagesp"],state["examstLv"])
    message = printmaxitem(resultlist,attrmaxMap[state["examstLv"]]-30)
    state["resultlist"] = resultlist
    await matcher.send(message + "输入1查看详细属性，其他输入会结束本次计算")

@calc_highattr.got("detail")
async def _(bot: Bot, event: Event , matcher: Matcher, state: T_State , cmd_arg: Message = Arg("detail")):
    args = cmd_arg.extract_plain_text().strip()
    if args != "1":
        await matcher.finish("已结束！")

    message = printallitem(state["resultlist"],attrmaxMap[state["examstLv"]]-30)

    await matcher.finish(message)