from gettext import find
import requests
import time
import os
import re
import csv
from bs4 import BeautifulSoup
import urllib3
import pandas as pd


headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

 
# 获取ssq号
def getChapterInfo(urlist,novel_url):
    #正则表达式获取<tr></tr>之间内容
    #print(novel_url)
    urlist =[]
    redCodeList = []
    redCodeRt = []
    chapter_html = requests.get(novel_url, headers=headers).text
  
    soup = BeautifulSoup(chapter_html,'lxml') 
  
    tables = soup.findAll('tbody',id='cpdata')
   
 
    tab = tables[0]
    trs = tab.findAll('tr')
    for tr in trs: 
       
        ui = [] 
        absentCode = []
        redCode = []
        str1 = 'chartball01'
        str2 = 'chartball02'
        str3 = 'yl02'
        str4 = 'yl01'
        str5 = 'bg_p'
        str6 = 'chartball20'
        str7 = 'bg_bl'

 
        for td in  tr.findAll('td'):

            # 检查类名是否不为空
           if td.get('class'):
             # print("td 的 getclass 返回值不为空:", td['class'][0])
              if (str1 == td['class'][0] or str2 == td['class'][0] or str6 == td['class'][0] ):
                  absentCode.append(0) 
                  redCode.append(td.text)
              elif (str3 == td['class'][0] or str4 == td['class'][0] or str5 == td['class'][0] or str7 ==td['class'][0]):
                   absentCode.append(td.text)      
           
           else:
                 #获取期号，星期数据
                 absentCode.append(td.text)
                 redCode.append(td.text)
                # print("td 的 getclass 返回值为空")
         
       

        if len(absentCode) > 2:  
           #存储遗漏期数    
           urlist.append(absentCode) 
           #存储红球
           redCodeList.append(redCode[0:8])
        else:
             print('数组为空')
       #k redCodeRt = redCodeList[0:8]
         
    return urlist,redCodeList


def redball_Analy(urlist):

    arr=urlist 
    twoMarr = []
 
    lostDf =  pd.DataFrame()


    for i in range(0, len(arr)) :  
        RedlostNum = 0 
        RedBallSum =0 
        BuleLostNum = 0
        BuleBallSum = 0
        arrLostNum = []
          
        arrLostNum.append(arr[i][0])
        
        for column in  range(0,50):
         
          if(arr[i][column] == 0):
            if(column <= 34):
                RedlostNum += int(arr[i-1][column])
                RedBallSum += (column-1 )
            else:
                BuleLostNum += int(arr[i-1][column]) 
                BuleBallSum += (column -34 )

        arrLostNum.append(RedlostNum)
        arrLostNum.append(RedBallSum)
        arrLostNum.append(BuleLostNum)
        arrLostNum.append(BuleBallSum)
        #arrLostNum.append(arr[i][35])
        twoMarr.append(arrLostNum)
     
    #print(twoMarr)
    save2_contents(twoMarr)               
    
    #print (trs.len) 

def save2_contents(urlist):
           # print(len(urlist))
    #try:  
          #with  as f:        
            writer = csv.writer(open("lostNum.csv",'w'))  
            #print(urlist)
           # name = []
            lotlist = pd.DataFrame( data=urlist)
            lotlist.columns = ['开奖期号', '红球遗漏次数','红球和值','篮球遗漏次数','篮球号']
            lotlist.to_csv('E:/python/ssqRst/lostNum.csv',encoding='gbk')



    
def save_contents(urlist,redlist):
           # print(len(urlist))
    #try:  
          #with  as f:        
            writer = csv.writer(open("ssqdxb.csv",'w'))  
            #print(urlist)
           # name = []
            lotlist = pd.DataFrame( data=urlist)
            lotlist.to_csv('E:/python/ssqRst/ssqdxb.csv',encoding='gbk')

            writer = csv.writer(open("ssqredcode.csv",'w'))  
            #print(urlist)
           # name = []
            lotlist = pd.DataFrame( data=redlist)
            lotlist.columns = ['期号','星期','red1', 'red2','red3','red4','red5','red6']
            lotlist.to_csv('E:/python/ssqRst/ssqredcode.csv',encoding='gbk')
      


if __name__ == '__main__':
 
    urlist = []   
    novel_url = 'https://www.00038.cn/zs_ssq/chzs-2020046-2024138.htm' 
    novel_info,redCodeList = getChapterInfo(urlist,novel_url)  
    print(novel_info)
    redball_Analy(novel_info)
    save_contents(novel_info,redCodeList)
   
  