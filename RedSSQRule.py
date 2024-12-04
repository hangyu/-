from pickle import TRUE
import pandas as pd
import numpy as np 
import math
#一、 红球最小号码小于16； 16的概率是1/ 158.74,17的概率是1/396...
#二、 红球最大号码大于17； 16的概率是1/ 279,17的概率是1/213...       
def minMaxRedBall(codeArra):
    minNum = 16
    maxNum = 17
    if(codeArra[0]> 15 or codeArra[5] < 18):
        return False
    return True
    pass

#五、 除以3余0的个数小于5: 除以3余0的个数等于5的概率是0.007
#六、 除以3余1的个数小于5: 除以3余1的个数等于5的概率是0.011
#七、 除以3余2的个数小于5: 除以3余1的个数等于5的概率是0.007

def dividedBy3remainder(codeArr):

    remainder0Count = 0
    remainder1Count = 0
    remainder2Count = 0
    for i in range (0, len(codeArr)):
        remainderCode =  codeArr[i]
        if remainderCode % 3 == 0:
                remainder0Count += 1
        elif remainderCode % 3 == 1:
                remainder1Count += 1
        elif  remainderCode % 3 == 2:
                remainder2Count += 1
    
    if remainder0Count > 4 or remainder1Count >4 or remainder2Count >4 :
        return False
    
    return True
 
#统计
def judgementBythePrime(codeArr0):

    primeCount = 0
    for i in range(len(codeArr0)):
        if(is_prime(codeArr0[i])):
            primeCount += 1   
    return primeCount
    pass

def is_prime(num):
    if num <= 1:
        return True #这里与数据逻辑定义有区别，数学定义中1既不是质数也不是合数，但双色球统计中1算作质数
    for i in range(2, int(math.sqrt(num)) + 1):
        if (num % i) == 0:
            return False
    return True

    pass

 
#奇数或偶数大于4个或小于1个返回false
def judgementBytheOddOrEven(codeArr):
     
    evenCount = 0
    for i in range (0, len(codeArr)):
       if calcOddorEvenCount(codeArr[i] ) :
         evenCount += 1
    return evenCount     
    pass
 
def calcOddorEvenCount(singleCode):    
    if singleCode % 2 == 0:
        return  True
    else:
        return False

#连号规则
#用于判断连号，以连号中断为分割，将数据存放在列表中    
def  continueBall(codeArr):
    continueList = []
    codeList = []
    continueCodeCount = 0
    continueCodeGroup = 0
    for code in codeArr:
        codeList.append(code)
        if code+1 not in codeArr:
            if len(codeList) != 0:
               # print(codeList)
                continueList.append(codeList)
            #如果此处不连续new一个新的list
            codeList = []
    
    for codeList in continueList:
        if len(codeList) > 1 :
            continueCodeGroup += 1
            continueCodeCount +=  len(codeList)
            if(continueCodeGroup > 1 ):
                continueCodeCount -= 1
    
   # print('continueCodeGroup is ',  continueCodeGroup)
   # print('continueCodeCount is', continueCodeCount)

    return  continueCodeGroup, continueCodeCount

#计算AC值 ：AC值=D(t)-(r-1)  r表示数字个数
def calcACValue(codeArr):
   
    calcACValue = 0
    diffArr = []
  
    for i in range(0,len(codeArr)-1):
        for  j in range(i+1,len(codeArr)):
          diffArr.append(codeArr[j] - codeArr[i]) 

    calcACValue = len(list(set(diffArr))) - 5
    
    return calcACValue

#分区规则，一区个数为5,6的概率分别是0.3%，0.4%
#         二区个数为5,6的概率分别是1.3%，0%
#          三区个数为5,6的概率分别是0.9%，0%
def threeDistrictRule(codeArra):
    firstDist = [1,2,3,4,5,6,7,8,9,10,11]
    secondDist = [12,13,14,15,16,17,18,19,20,21,22]
    thirdDist = [23,24,25,26,27,28,29,30,31,32,33]
    firstLength = len(set(codeArra) & set(firstDist))
    secondLength = len(set(codeArra) & set(secondDist))
    thridLength = len(set(codeArra) & set(thirdDist))

    return firstLength,secondLength,thridLength

#判断是否孤码数根据近665期统计， 孤码为0的情况占比0.4%，孤码为6的情况占比1.6%
#孤码为1的情况占比4.8%.孤码的定义,重邻孤:某两期号码的对比的一种形态：重指有两同的号码，
# 邻指有相邻的号码，否则为孤。

def  calcLonelyRedBallcount(redCodeArray, recentHisLotArray):
     
      lonelyCount = 0
      neiberCount = 0 
      sameCodeCount =0 
      for redCode in redCodeArray:
          lonelyRedCount = 0
          for j in range(3, len(recentHisLotArray)):
              recentRedCode = recentHisLotArray.iloc[j]
              
              if abs(redCode - recentRedCode) > 1:
                  lonelyRedCount += 1
              elif abs(redCode - recentRedCode) == 0:
                  sameCodeCount += 1
              else:
                  continue
           
          if lonelyRedCount == 6:
              lonelyCount += 1
        
      neiberCount =  6 - sameCodeCount - lonelyCount
      
    
      return lonelyCount,neiberCount,sameCodeCount 

#判断红球中奖号码末尾数相同的个数之和是多少

def calcTheSameCodeOflastRedBall():

    pass