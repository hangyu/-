'''
  规则：
  一、 红球最小号码小于16； 16的概率是1/ 158.74,17的概率是1/396...
  二、 红球最大号码大于17； 16的概率是1/ 279,17的概率是1/213...
  三、 奇数(偶数)个数大于0且小于6： 奇数个数为0的概率是0.011， 奇数个数为6的概率是0.013
  四、 质数(合数)个数大于0且小于6： 质数个数为0的概率是0.005， 质数个数为6的概率是0.000
  五、 除以3余0的个数小于5: 除以3余0的个数等于5的概率是0.007
  六、 除以3余1的个数小于5: 除以3余1的个数等于5的概率是0.011
  七、 除以3余2的个数小于5: 除以3余1的个数等于5的概率是0.007
  八、 所有篮球与红球之和大于69且小于137且不等于133或131
  九、 所有篮球与红球尾数之和大于12且小于40
  十、 红球连号个数大于应小于4，连号个数等于4的概率是0.001，等于3的概率是0.010
  十一、红球的跨度应大于13
  十二、红球AC值  AC值大于3小于10
  十三、红球重号个数计算
  十四、红球连号组个数计算
  十五、冷热比个数计算[[ik]]
  十六、红球遗漏次数大于10的个数不超过一个
  十七、孤邻规则
  十八、分区规则
  十九、连号规则
  二十、最小号间距

  @2024.9.1修改(优化)了统比较遗漏次数的方法。
  @2024.9.2  增加了统计孤邻值的方法。
  @2024.9.4  新增了规则文件，部分规则移动到RedSSQRule.py中

'''
from pickle import TRUE
import pandas as pd
import csv
#from random import sample
import random
import numpy as np 
import time
import math
import RedSSQRule
import logging
import sys
 


now = time.strftime("%Y-%m-%d%H%M%S", time.localtime())
logFilename = 'd:/mylog.txt' + '-'+now
logger = logging.getLogger(__name__)
logging.basicConfig(filename=logFilename,filemode='w',format='%(name)s-%(levelname)s -%(message)s',
                    encoding='UTF-8',level=logging.INFO)

ListRedBll = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
ListBlueBll =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

#产生红球随机数
def  createRedBall(eliminateCode):
    randList = []
    ListRedBllCp = ListRedBll

    if(eliminateCode != ""   ):

        delimiter = ","
        eliminateCodeArr = [int(num) for num in eliminateCode.split(delimiter)]

        for eliminateCode in eliminateCodeArr:
          ListRedBllCp.remove(eliminateCode)
         
        
   
    for i in range(12000000):
        
        series = random.sample(ListRedBllCp, 6) 
       
        randList.append(sorted(series))
    return randList

#验证红球开奖号码
def  identifyRedBall():
    
    randList = []
     
        
    series = [12,21,23,27,32,33]
      
    randList.append(sorted(series))
   
    return randList


def  dealRedRandBll(randList :list):
    
    print(len(randList))
    
    randListSet = np.array(list(set([tuple(t) for t in randList])))
    
    print(len(randListSet))

   # randRedBallArr = analyRedBall(randListSet,hisLotNum, recentLotCode,  minSameCodeNum, maxSameCodeNum) 

    return randListSet 

class RedBallAnalysis:

  def __init__(self, randRedBallList :list, hisBallDf, recentLotCode, paramAcValueMin:int,
               paramAcValueMax:int,ballLostSumMin:int,
               ballLostSumMax:int,redBallSumMin:int,redBallSumMax:int,
               minSameCodeNum :int, maxSameCodeNum :int,ballLostMT10CountLimitMin:int,
               ballLostMT10CountLimitMax,tailRedSum :int,continueNumCount:int,
                evenRedSum:int) -> None:
     
     self.randRedBallList = randRedBallList
     self.hisBallDf = hisBallDf
     self.recentLotCode = recentLotCode
     self.paramAcValueMin  = paramAcValueMin
     self.paramAcValueMax = paramAcValueMax
     self.ballLostSumMin = ballLostSumMin
     self.ballLostSumMax = ballLostSumMax
     self.redBallSumMin = redBallSumMin
     self.redBallSumMax = redBallSumMax
     self.minSameCodeNum = minSameCodeNum
     self.maxSameCodeNum   = maxSameCodeNum
     self.ballLostMT10CountLimitMin = ballLostMT10CountLimitMin
     self.ballLostMT10CountLimitMax = ballLostMT10CountLimitMax
     self.tailRedSum = tailRedSum
     self.continueNumCount = continueNumCount
     self.evenRedNumCount = evenRedSum
    
     logging.info(minSameCodeNum)
     logging.info(maxSameCodeNum)

  #Normal distributionx rule
  def analyRedBall(self):

    validBall = []
    
    preRedCodeList = self.hisBallDf.tail(9)

    recentRedCodeArray = self.hisBallDf.tail(1)

    

    print('RandBallList Size is ', len(self.randRedBallList))
    #先用最近9期进行比较，相同数不能大于3,不能小于1 @2024.9.8优化
    preRandBallList = cmpRandNumArrWithLosHis(self.randRedBallList, preRedCodeList, 1, 3)
    print('preRandBallList Size is ', len(preRandBallList))
    
    #历史50期比较，相同数不能大于4
    time_startcmphis = time.time() #开始时间 
    now1 = time.strftime("%Y-%m-%d%H%M%S", time.localtime())
    print(now1)

       
    if( self.minSameCodeNum != "" and self.maxSameCodeNum !="" ):
        cmpSameCodeMin = self.minSameCodeNum
        cmpSameCodeMax = self.maxSameCodeNum
    else:
        cmpSameCodeMin = 3
        cmpSameCodeMax = 4
    validFliterBall = cmpRandNumArrWithLosHis(preRandBallList,self.hisBallDf, cmpSameCodeMin, cmpSameCodeMax)
    
    print('validfliterBall Size is ', len(validFliterBall))
    time_endcmphis = time.time() #结束时间
    now2= time.strftime("%Y-%m-%d%H%M%S", time.localtime())
    print(now2)

    time_cost = time_endcmphis - time_startcmphis 

    print('cmphis time cost is:', time_cost,'s')

    time_start_otherrulue = time.time() #开始时间 
    print( time_start_otherrulue)


    if( self.tailRedSum != "" and self.tailRedSum !="" ):
          delimiter = ","
          tailRedSumArr = [int(num) for num in self.tailRedSum .split(delimiter)]

      
    for i in range(0, len(validFliterBall)):
        redBallSum = 0
        ballLostSum = 0
        ballLostMT10Count = 0
        acValue = 0
        #概率因子，为各个规则出现概率进行加权得到一个量化因子
        LotPossibility = 1
        
       
        redFailureStr= '日志开始： '  
       #print(type(validFliterBall[i]))
       # for column in range(0,len(RandBallList[i])):
       #     ballNumSum += RandBallList[i][column]
       #  优化，使用NumPy自带函数，提升计算速度
       # ；
        redBallSum = validFliterBall[i].sum()

       

        tailRedSumFlag = False
        if tailRedSumArr :
          tailRedBallSum = redBallSum % 10
          for tailRedSummury in tailRedSumArr:
              if( tailRedBallSum == tailRedSummury):
                  tailRedSumFlag = True
                  continue
        if tailRedSumFlag:
              continue
        
        oldRedFailureStr = ' '
        
        if( self.redBallSumMin != "" and self.redBallSumMax !="" ):
           if( redBallSum < self.redBallSumMin or redBallSum > self.redBallSumMax):
                #print('违反AC值规则')
                continue
                redFailureStr+= 'and 违反AC值规则' + str(acValue)
                pass
        else:
            #if(redBallSum < 65 or redBallSum > 138 ):
            if(redBallSum < 65 or redBallSum > 130 ):
                continue
                #logging.info('违反红球和规则')
                redFailureStr += '违反红球和规则 ' + str(redBallSum)
                
                pass 
        

        minMaxFlag = RedSSQRule.minMaxRedBall(validFliterBall[i])
        if not minMaxFlag:
           # print('违反红球最大，最小值规则')
            continue
            redFailureStr+= 'and 违反红球最大，最小值规则' + str(minMaxFlag)
            pass

        firstLength,secondLength,thridLength = RedSSQRule.threeDistrictRule(validFliterBall[i])
        if(firstLength>4 or secondLength>4 or thridLength > 4): 
            # print('违反分3区规则')
            continue
            redFailureStr += 'and 违反分3区规则' + str(firstLength)+ ' '+ str(secondLength)+ ' '+str(thridLength)
             
            pass

        lonelyCount,neiberCount,sameCodeCount  =  RedSSQRule.calcLonelyRedBallcount(validFliterBall[i], recentRedCodeArray.iloc[-1]) 

        #重码在与前9期开奖号码比对中比较了，所以这里就不判断了
        #孤码大于5的概率是1.9%， 等于0的概率是0.3% 
        #邻码等于5的概率是0.8%，等于6的概率是0
        if(neiberCount >4 or lonelyCount>5 or lonelyCount <1 ):
            
            continue
            #logging.info('违反孤邻规则')
            redFailureStr += 'and 违反孤邻规则' +'邻'+  str(neiberCount) +'孤'+ str(lonelyCount) 
            pass
        
        evenCount = RedSSQRule.judgementBytheOddOrEven(validFliterBall[i])
        #优化，允许奇数个数等于5
        #if(evenCount < 1 or evenCount > 5):
        
        if(self.evenRedNumCount != "" ):
            if evenCount < self.evenRedNumCount :
           # print('违反连号个数大于3规则')
              continue
              redFailureStr+='and 反连号个数大于3规则' +str( continueCodeCount)
              pass
        else: 
            if (evenCount < 2 or evenCount > 5):
            #print(judgementBytheOddOrEven(RandBallList[i]))
            #print(RandBallList[i])
                continue
                print('违反奇偶规则')
                redFailureStr += 'and 违反奇偶规则' + str(evenCount)
                pass
        if evenCount >1 and evenCount < 5:
            LotPossibility += 0.2
            pass

        continueCodeGroup, continueCodeCount = RedSSQRule.continueBall(validFliterBall[i])

        if(self.continueNumCount !="" ):
            if continueCodeCount > self.continueNumCount :
           # print('违反连号个数大于3规则')
              continue
              redFailureStr+='and 反连号个数大于3规则' +str( continueCodeCount)
              pass

        #连号等于4的概率是2.4%，等于5的概率是0.1%
        else:
            if continueCodeCount > 3 :
           # print('违反连号个数大于3规则')
              continue
              redFailureStr+='and 反连号个数大于3规则' +str( continueCodeCount)
              pass
        if continueCodeCount < 3:
            LotPossibility += 0.15
        if continueCodeCount == 3:
            LotPossibility += 0.05

        
        #当AC值大于10或者小于4时去掉
        acValue = RedSSQRule.calcACValue(validFliterBall[i]) 

        if( self.paramAcValueMax != "" and self.paramAcValueMin !="" ):
           if( acValue < self.paramAcValueMin or acValue > self.paramAcValueMax):
                #print('违反AC值规则')
                continue
                redFailureStr+= 'and 违反AC值规则' + str(acValue)
                pass
        else:
        # if( acValue < 4 or acValue > 10):
            if( acValue < 6 or acValue > 10):
                #print('违反AC值规则')
                continue
                redFailureStr+= 'and 违反AC值规则' + str(acValue)
                pass
        if ( acValue > 6 and acValue > 9):
            LotPossibility += 0.2
        elif (acValue ==6 or acValue == 10):
            LotPossibility += 0.15
        elif (acValue == 9 or acValue == 5):
            LotPossibility += 0.15
        else:
            LotPossibility += 0.05
 
 
        primeCount = RedSSQRule.judgementBythePrime(validFliterBall[i])

        divide3Remainder = RedSSQRule.dividedBy3remainder(validFliterBall[i])
        if not divide3Remainder:
           # print('违反除以3规则')
            continue
            redFailureStr+= 'and 违反除以3规则' + str(divide3Remainder)
            pass
             
        ballLostSum,ballLostMT10Count,rebBallHot = calcCurrentBllLostCount(validFliterBall[i], recentLotCode)
        
        if(self.ballLostMT10CountLimitMin != "" and self.ballLostMT10CountLimitMax != ""):
             if  ballLostMT10Count < self.ballLostMT10CountLimitMin or ballLostMT10Count > ballLostMT10CountLimitMax:
                #print('违反AC值规则')
                continue
                redFailureStr+= 'and 违反遗漏次数大于10不超过'+str(ballLostMT10CountLimit)+ '个规则' + str(ballLostMT10CountLimit)
                pass
        else:
            #遗漏次数大于10的个数不超过2
            if ballLostMT10Count > 2 :
                continue
                #print('违反遗漏次数大于10不超过2个规则')
                redFailureStr+= 'and 违反遗漏次数大于10不超过2个规则' + str(ballLostMT10Count)
                pass
        if ballLostMT10Count == 1:
            LotPossibility += 0.1
        else:
            LotPossibility += 0.05
        #当热号大于5个或者小于2个时去掉
        #热号大于5的概率是4.2%， 热号小于2的概率是1.8%
        if(rebBallHot>5 or rebBallHot <2):
            continue
            redFailureStr+= 'and 违反红球热码规则' + str(rebBallHot)
           # print('违反红球热码规则')
            pass

        #质数等于0的比例是4.2%，质数等于4的比例是7.8%，大于4的比例是0
        if(primeCount >4 or primeCount < 1):
            continue
           # print('违反红球素数个数规则')
            redFailureStr+= 'and 违反红球素数个数规则' + str(primeCount)
            pass
        elif primeCount == 2:
            LotPossibility += 0.2
        elif primeCount == 1 or primeCount == 3:
            LotPossibility += 0.12
        else:
            LotPossibility += 0.05

        if( self.ballLostSumMin != "" and self.ballLostSumMax !="" ):
           if( ballLostSum < self.ballLostSumMin or ballLostSum > self.ballLostSumMax):
                #print('违反AC值规则')
                continue
                redFailureStr+= 'and 违反AC值规则' + str(acValue)
                pass             
        else:       
            if( ballLostSum  < 10 or ballLostSum >54 ):          
                continue
                redFailureStr += 'and 违反总遗漏次数规则'+ str(ballLostSum)
                pass
        if ballLostSum >15 and ballLostSum <31:
                LotPossibility += 0.13
        elif ballLostSum >30 and ballLostSum <43:
                LotPossibility += 0.082
        else:
                LotPossibility += 0.039
         
        
        # validBall.append(RandBallList[i].append(ballLostSum))

        if(LotPossibility < 1.55 or LotPossibility >1.90):
           continue
         
        validBallList = validFliterBall[i].tolist()
        validBallList.append(redBallSum)
        validBallList.append(tailRedBallSum)
        validBallList.append(acValue)
        validBallList.append(ballLostSum)
        validBallList.append(ballLostMT10Count) 
        validBallList.append(rebBallHot)
        validBallList.append(primeCount)
        validBallList.append(round(LotPossibility,2))


            
        validBall.append(validBallList)
           
    
    validBalldf = pd.DataFrame(validBall)
    try:
        validBalldf.columns = ['red1','red2','red3','red4','red5','red6','红球之和','红球尾号','AC值',
                           '遗漏次数和','遗漏大于10个数','热球个数','质数个数','概率']
        newSave_contents(validBalldf, 'redBalllist')
    except :
        print('Dateframe 为空！')  

   # validFliterBall = cmpRandNumArrWithLosHis(validBall,hisLotNum,3)
    print('validBall Size is ', len(validBall))
    print(type(validBall))
   

    
    time_end_otherrulue = time.time() #结束时间 
    print(time_end_otherrulue)
    time_otherrule_cost = time_endcmphis- time_startcmphis  

    print('time_otherrule_cost :', time_otherrule_cost,'s')
      #从结果中选取
    randomizerFinal(validBall)


    #unieBallSet = np.array(list(set([tuple(t) for t in validFliterBall])))
    return validBall


# calc the bllLostCount(). 根据上一期的开奖结果计算遗漏次数。
# 参数1是产生的红球随机数，参数2是上一期的开奖号码遗漏次数，上一期开出的号码遗漏次数已经置为0
# 红球冷热比当遗漏次数大于4为冷号，否则为热号
def calcCurrentBllLostCount(RandBllArr, primalLotNum):
 
        totalbllLostCount = 0
        #print(type(primalLotNum))
        #红球大于10的个数
        ballLostMT10Count = 0
        rebBallHot = 0
        for i in range(0, len(RandBllArr)):
             randBllCode = RandBllArr[i]

             #print(primalLotNum.iloc[randBllCode+2])
             bllLostCount = primalLotNum.iloc[randBllCode+2]
             if(bllLostCount > 9 ):
                    ballLostMT10Count += 1
             elif(bllLostCount < 5):
                 rebBallHot += 1
                
             totalbllLostCount += bllLostCount
    
        return totalbllLostCount, ballLostMT10Count,rebBallHot
 
# get rid of continue 4 number  
# #当红球为4连号或者红球跨度小于13时返回false  
def  del4con(codeArr):
     
    for i in range (0, 2):
       
        if i==0  and (codeArr[i+4] - codeArr[i] < 13):
            #print(codeArr[i+4] - codeArr[i])
            return False
        else:
            continue
    return  True

#distance rule
def delwrongDistance(codeArr):
    for i in range(0,3):
        if((codeArr[i+1] - codeArr[i])>23 or((codeArr[i+2] - codeArr[i+1]) >12 and (codeArr[i+1] - codeArr[i]) >12)):
            return False
        #get rid of extremity condition
        elif (i == 0 and (codeArr[i] > 25 or codeArr[i+4] < 15)):
            return False
        else:
            continue
    return True       

#get a qunentity lot Number
def getspecifyLotNum(balldf, startPos, endPos):
   
  if not balldf is None:
    
    #print(len(lotNumArr))
     return balldf.iloc[startPos:endPos+1]
  else: 
      print("period is null")

#get any One lot Number       
def getSingleLotNum(balldf,index):
    if not balldf is None:
       return  balldf.loc[index]
    else:
       print("balldf is null")       

#discard
def cmpRandNumWithPre(RandBallList, preRedCodeList,sameCodeNum):

    choiceBList = RandBallList

    for i in range(0, len(preRedCodeList)):
        backBallList =  identifyBall(choiceBList, preRedCodeList.iloc[i],sameCodeNum);
       #每次都用筛选过后的列表
        choiceBList = backBallList 
    
    return  choiceBList
    
    pass


 #判断与历史开奖红球数字相同的个数，
 #  参数1：产生的随机数列表（经过前序规则过滤后）
 #  参数2：历史开奖的红球号列表（包括期号与星期几）
 #  参数3：相同的数字个数
def cmpRandNumArrWithLosHis(RBallList,hisLotNumList, minSameCodeNum, maxSameCodeNum):

    choiceBList = []

    for randBall in RBallList:
           
           isValid = identifyRandRedBall(randBall,hisLotNumList, minSameCodeNum, maxSameCodeNum)

           if(isValid):
               choiceBList.append(randBall)
           else:
               continue
    return choiceBList

def identifyRandRedBall(randBall,hisLotNumList,minSameCodeNum,maxSameCodeNum):

    recodeSame = []
    choiceRandNum2Arr = []
    
    maxSameNum= 0
    for i in range(0,len(hisLotNumList)):
       length = len(set(randBall) & set(hisLotNumList.iloc[i].iloc[-6:]))
       if(length > maxSameNum):
           maxSameNum = length
       
    if(maxSameNum > maxSameCodeNum or maxSameNum < minSameCodeNum): 
           return False
    else:
    
        return True
    pass

def newSave_contents(saveList, fileName):
   
    now = time.strftime("%Y-%m-%d%H%M%S", time.localtime())
    print(now)
 
    localFilename = fileName+'-'+now
 
  
    writer = csv.writer(open('{}.csv'.format(localFilename),'w'))  
            #print(urlist)
           # name = []
    lotlist = pd.DataFrame( data=saveList)
    lotlist.to_csv('E:/python/ssqRst/{}.csv'.format(localFilename),encoding='gbk')

    pass


def newSave_contents4cmp(saveList, fileName, cmpNum):
  
    if(cmpNum == 5) :
       
        localFilename = fileName
        writer = csv.writer(open('{}norule.csv'.format(localFilename),'w'))  
            #print(urlist)
           # name = []
        lotlist = pd.DataFrame( data=saveList)
        #lotlist.to_csv('d:/pythons/spider/{}norule.csv'.format(localFilename),encoding='gbk')
        lotlist.to_csv('/home/google/python/{}norule.csv'.format(localFilename),encoding='gbk')
    else:
        
        localFilename = fileName
        writer = csv.writer(open('{}.csv'.format(localFilename),'w'))  
            #print(urlist)
           # name = []
        lotlist = pd.DataFrame( data=saveList)
       
        #lotlist.to_csv('d:/pythons/spider/{}.csv'.format(localFilename),encoding='gbk')
        lotlist.to_csv('/home/google/python/{}.csv'.format(localFilename),encoding='gbk')

    pass

#this function could be reuse
def  identifyBall(randNumArr, lotNumArr, sameCodeNum):

    recodeSame = []
    choiceRandNum2Arr = []
    
     
    for i in range(0,len(randNumArr)):
       subRcordSame = []
       #print(randNumArr[i]) #debug
       #print(lotNumArr.iloc[-6:])  #debug
       length = len(set(randNumArr[i]) & set(lotNumArr.iloc[-6:]))
       if(length > sameCodeNum): 
           continue
       else:
            choiceRandNum2Arr.append(randNumArr[i])
       recodeSame.append(subRcordSame)   
   # print(recodeSame)
   # print(len(randNumArr)-len(choiceRandNum2Arr))
    
    return choiceRandNum2Arr
    save_contents(recodeSame)
    
    pass   

def save_contents(urlist):
           # print(len(urlist))
    #try:  
          #with  as f:        
            writer = csv.writer(open("lostSameNum.csv",'w'))  
            #print(urlist)
           # name = []
            lotlist = pd.DataFrame( data=urlist)
            lotlist.to_csv('/home/google/python/lostSameNum.csv',encoding='gbk')
            #writer.writerow(['hexdata'])  
            newSave_contents

def randomizerFinal(rstRedballList):
    upRange = len(rstRedballList)
    #print(upRange)
    resultList = random.sample(range(1, upRange), 50) 
    mergerRandRedBallRet =[]
    effectiveCodeRet=[]
  
    codeList = []
    effectiveCodeList =[]
    for i in  range(0, 50):
        reslutIndex = resultList[i]
        codeList.extend(rstRedballList[reslutIndex])
        effectiveCodeList.extend(rstRedballList[reslutIndex][0:6])
        if i % 2 and i > 0 == 0:
            mergerRandRedBallRet.append(codeList)
            effectiveCodeRet.append(set(sorted(effectiveCodeList)))
            codeList = []
            effectiveCodeList = []
        
   

    #print(mergerRandRedBallRet)
 
    
    validRandBalldf = pd.DataFrame(sorted(mergerRandRedBallRet))
    effectiveCodedf = pd.DataFrame(sorted(effectiveCodeRet))


    try:
       validRandBalldf.columns = ['red1','red2','red3','red4','red5','red6','红球之和','红球尾号','AC值',
                           '遗漏次数和','遗漏大于10个数','热球个数','质数个数',
                           '概率','red11','red21','red31','red41','red51','red61','红球之和1','红球尾号1','AC值1',
                           '遗漏次数和1','遗漏大于10个数1','热球个数1','质数个数1', '概率1']
       newSave_contents(validRandBalldf, 'rstRedBalllist')

       newSave_contents(effectiveCodedf, 'effectiveCodeList')
    except :
       print('Dateframe 为空！')

    
    pass

def getParamsFromFile():
    # 打开文件
    with open('params.txt', 'r') as file:
        # 读取所有行
        lines = file.readlines()
    
    # 处理每一行
    params = {}
    for line in lines:
        # 去除行尾的空白字符
        line = line.strip()
        # 分割键和值
        key, value = line.split(':', maxsplit=1)
        # 存储键值对
        params[key] = value
        

    return params
    
    pass


def is_string_empty(s):
    return False if s == "" else True

if __name__ == '__main__':

    
   #历史50期比较，相同数不能大于4
    time_startrand = time.time() #开始时间 
   #d:/pythons/spider
    balldf = pd.read_csv('E:/python/ssqRst/ssqredcode.csv',encoding='gbk')
    ballLostdf = pd.read_csv('E:/python/ssqRst/ssqdxb.csv',encoding='gbk') 
    
    acValueMin=''
    acValueMax=''
    minSameCodeNum=''
    maxSameCodeNum=''
    ballLostSumMin=''
    ballLostSumMax=''
    redBallSumMin=''
    redBallSumMax=''
    tailRedSum=''
    continueNumCount=''
    evenRedSum =''
    eliminateCode=''

    params = getParamsFromFile()
    print(params.get('acValueMin'))

    if is_string_empty(params.get('acValueMin')):
       acValueMin = int(params.get('acValueMin'))
    if is_string_empty(params.get('acValueMax')):
       acValueMax = int(params.get('acValueMax'))
    if is_string_empty(params.get('minSameCodeNum')):
       minSameCodeNum = int(params.get('minSameCodeNum'))
    if is_string_empty(params.get('maxSameCodeNum')):
       maxSameCodeNum = int(params.get('maxSameCodeNum'))
    if is_string_empty(params.get('ballLostSumMin')):
       ballLostSumMin = int(params.get('ballLostSumMin'))
    if is_string_empty(params.get('ballLostSumMax')):
       ballLostSumMax = int(params.get('ballLostSumMax'))
    if is_string_empty(params.get('redBallSumMin')):
       redBallSumMin = int(params.get('redBallSumMin'))
    if is_string_empty(params.get('redBallSumMax')):
       redBallSumMax = int(params.get('redBallSumMax'))
    if is_string_empty(params.get('ballLostMT10CountLimitMin')):
       ballLostMT10CountLimitMin = int(params.get('ballLostMT10CountLimitMin'))
    if is_string_empty(params.get('ballLostMT10CountLimitMax')):
       ballLostMT10CountLimitMax = int(params.get('ballLostMT10CountLimitMax'))
    if is_string_empty(params.get('tailRedSum')):
       tailRedSum = str(params.get('tailRedSum'))
    if is_string_empty(params.get('continueNumCount')):
       continueNumCount = str(params.get('continueNumCount'))
    if is_string_empty(params.get('evenRedSum')):
       evenRedSum = int(params.get('evenRedSum'))
    if is_string_empty(params.get('eliminateCode')):
       eliminateCode = str(params.get('eliminateCode'))


    print(eliminateCode)

    randRedBll = createRedBall(eliminateCode)
    print(type(randRedBll))

    #验证
    #randRedBll =  identifyRedBall()
    
    rowCount = len(balldf)
    hislotNum = getspecifyLotNum(balldf,450, rowCount-1)
    print(type(hislotNum))
    
   # contrastRedLotNum = getSingleLotNum(balldf,499)
   

    recentLotCode = ballLostdf.loc[rowCount-1]
     
    print(recentLotCode)
    minSameCodeNumParams = 3  
    maxSameCodeNumParams = 4
    randRedBNorule = dealRedRandBll(randRedBll)

   
    
    if (minSameCodeNum == " " or  maxSameCodeNum == " "):
        minSameCodeNumParams = 3
        maxSameCodeNumParams = 4
    else:
        minSameCodeNumParams = minSameCodeNum
        maxSameCodeNumParams = maxSameCodeNum
        

    rba = RedBallAnalysis(randRedBNorule,hislotNum, recentLotCode,acValueMin,acValueMax,ballLostSumMin,
                          ballLostSumMax,redBallSumMin,redBallSumMax,minSameCodeNumParams,
                          maxSameCodeNumParams,ballLostMT10CountLimitMin,ballLostMT10CountLimitMax,
                          tailRedSum,continueNumCount,evenRedSum)
    rba.analyRedBall()

   

  
    time_endrand = time.time() #结束时间
    now2= time.strftime('总用时结束'+"%Y-%m-%d%H%M%S", time.localtime())
    print(now2)

    time_cost = time_endrand - time_startrand 

    timeStr =  'total time cost is:' + str(time_cost) +'s'
    logging.info(timeStr)
 
 
     
    
    