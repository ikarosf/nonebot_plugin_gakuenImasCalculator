from math import ceil
from decimal import Decimal

attrmaxMap = {
    "h":1500,
    "m":1800
}

def _calc_rank(vo,di,vi,attrmax):
    _attrmax = attrmax - 30
    shuxingyichuFLAG = False
    VO = Decimal(vo)
    DI = Decimal(di)
    VI = Decimal(vi)

    if VO > _attrmax:
        VO = Decimal(_attrmax)
        shuxingyichuFLAG = True
    if DI > _attrmax:
        DI = Decimal(_attrmax)
        shuxingyichuFLAG = True
    if VI > _attrmax:
        VI = Decimal(_attrmax)
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
    Sp_rank = 14500
    biaoxianfenlist = [1500,2250,3050,3450,3650,3750]

    juliA = A_rank - shuxingfen - mingcifen
    juliAp = Ap_rank - shuxingfen - mingcifen
    juliS = S_rank - shuxingfen - mingcifen
    juliSp = Sp_rank - shuxingfen - mingcifen

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

    if juliSp <= 0:
        Spscore = 0
    elif juliSp <= 1500:
        Spscore = ceil(juliSp / 0.3)
    elif juliSp <= 2250:
        Spscore = ceil((juliSp - 750 )/ 0.15)
    elif juliSp <= 3050:
        Spscore = ceil((juliSp - 1450 )/ 0.08)
    elif juliSp <= 3450:
        Spscore = ceil((juliSp - 2250 )/ 0.04)
    elif juliSp <= 3650:
        Spscore = ceil((juliSp - 2850 )/ 0.02)
    elif juliSp <= 3950:
        Spscore = ceil((juliSp - 3250 )/ 0.01)
    else:
        Spscore = -1

    retmessage = ""
    if shuxingyichuFLAG:
        retmessage += "属性溢出了，单属性最高只计算" + str(attrmax) + "\n"
    retmessage += "你的属性总合为： " + str(VO) + " + " + str(DI) + " + " + str(VI) + " + 90 = " + str((VO + DI + VI + Decimal(90))) + "\n"
    if Ascore == -1:
        retmessage += "杂鱼连A都不可能到的，杂鱼杂鱼"
        return retmessage
    elif Ascore == 0:
        retmessage += "已经稳A了\n"
    else:
        retmessage += "A评价需要获得" + str(Ascore) + "分\n"

    if Apscore == -1:
        retmessage += "想拿到A+就做梦吧"
        return retmessage
    elif Apscore == 0:
        retmessage += "一把抓住A+，顷刻炼化！\n"
    else:
        retmessage += "A+评价需要获得" + str(Apscore) + "分\n"

    if Sscore == -1:
        retmessage += "S是你得不到的"
        return retmessage
    elif Sscore == 0:
        retmessage += "已经稳S了???你开了吧\n"
    else:
        retmessage += "S评价需要获得" + str(Sscore) + "分\n"

    if Spscore == -1:
        retmessage += ""
    elif Spscore == 0:
        retmessage += "已经稳S+了???你这是在做梦吧\n"
    else:
        retmessage += "S+评价需要获得" + str(Spscore) + "分\n"
    return retmessage