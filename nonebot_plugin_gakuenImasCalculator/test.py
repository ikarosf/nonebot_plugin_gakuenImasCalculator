from math import ceil
from decimal import Decimal
from typing import List

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

    print(messgae)


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
    print(messgae)

if __name__ == "__main__":
    stage = 1
    attrlist = [800,900,1000]
    attrbonuslist = [10,25,35]
    examsplist = [1 , 1 , 1]
    resultlist = _caclattr(stage , attrlist , attrbonuslist , examsplist)
    printmaxitem(resultlist)



    printallitem(resultlist)