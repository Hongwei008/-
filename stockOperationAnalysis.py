#coding=gbk
#Copyright@Hongwei008
import requests
import time
import sys
import os

def getName(record,history_str1):
	name= (history_str1[record[1]])[0][21:]

	return name

		
def getPrice(record,history_str1):
	
	now= (history_str1[record[1]])[3]

	return now[:-1]
	
def getRate(record,history_str1):
	
	buy5=float(0.3*int((history_str1[record[1]])[10])+0.3*int((history_str1[record[1]])[12])+0.2*int((history_str1[record[1]])[14])+0.1*int((history_str1[record[1]])[16])+0.1*int((history_str1[record[1]])[18]))
	sell5=float(0.3*int((history_str1[record[1]])[20])+0.3*int((history_str1[record[1]])[22])+0.2*int((history_str1[record[1]])[24])+0.1*int((history_str1[record[1]])[26])+0.1*int((history_str1[record[1]])[28]))
	if buy5>sell5:
		rate= str(format(float((history_str1[record[1]])[3])/float((history_str1[record[1]])[2])-1,'.2%'))+'↑'*int(buy5/sell5)
	else:
		rate= str(format(float((history_str1[record[1]])[3])/float((history_str1[record[1]])[2])-1,'.2%'))+'↓'*int(sell5/buy5)
	
	return rate

		
def buyingAnalysis(record,history_str1):
	code=record[1]
	price=record[2]
	volume=record[3]
	str0=getName(record,history_str1)+" "+getPrice(record,history_str1)+" "+getRate(record,history_str1)+" 买入收益：{:.2f}".format(volume*(float(getPrice(record,history_str1))-price))+" | "
	profit=volume*(float(getPrice(record,history_str1))-price)
	return str0,profit

def selling_analysis(record,history_str1):
	code=record[1]
	price=record[2]
	volume=record[3]
	str0=getName(record,history_str1)+" "+getPrice(record,history_str1)+" "+getRate(record,history_str1)+" 卖出收益：{:.2f}".format(volume*(-float(getPrice(record,history_str1))+price))+" | "
	profit=volume*(-float(getPrice(record,history_str1))+price)
	return str0,profit

def historyAnalysis(records,history_str1):
	profit=0
	for record in records:
		
		if record[0]=='买入':
			text0,profit2=buyingAnalysis(record,history_str1)
		else:
			text0,profit2=selling_analysis(record,history_str1)
		profit=profit+profit2
	str0="，历史收益：{:.2f}".format(profit)

	return str0,profit

def recentAnalysis(records,history_str1):
	text=""
	profit=0
	profit0=0
	profit1=0
	for record in records:
		if record[0]=='买入':
			text0,profit2=buyingAnalysis(record,history_str1)
			profit1=profit1+profit2
		else:
			text0,profit2=selling_analysis(record,history_str1)
			profit0=profit0+profit2
		text=text0+text
		profit=profit1+profit0
	#str1=" 买入收益：{:.2f}，卖出收益：{:.2f}，本次操作收益：{:.2f}".format(profit1,profit0,profit)
	str1="本次操作收益：{:.2f}".format(profit)
	text=text+str1
	return text,profit

def getData(records):
	dic={}
	for record in records:
		dic[record[1]]=1#只取不重复值
		dic[record[1]]=requests.get("http://hq.sinajs.cn/list=%s" % (record[1])).text.split(",")
	return dic


history_records=[['买入','sz300498',15.16,10100],['卖出','sz300498',15.19,10100],['买入','sz300498',14.49,10100],['买入','sz300002',5.8,20600],['卖出','sz300498',14.71,16600],['卖出','sz300498',14.8,1500],['买入','sz300498',14.324,18100],['卖出','sz300766',13.01,20000],['卖出','sz300766',14.68,20000],['买入','sz300766',14.88,19700],['卖出','sz300766',14.51,19700],['买入','sz300766',14.36,19800],['卖出','sz300766',14.40,19800],['买入','sz300766',13.94,19800],['卖出','sz300987',34,8300],['买入','sz300766',13.02,20000],['买入','sz300987',31.688,8300],['卖出','sz300766',13.3,20000]]
recent_operation=[['买入','sz300498',14.88,8300],['卖出','sz300002',6,20600]]
input("任意键开始")
os.system("cls")

global history_str
global recent_str






msg0=""
while True:
	try:
		history_str=getData(history_records)
		recent_str=getData(recent_operation)
		history_text,history_profit=historyAnalysis(history_records,history_str)
		recent_text,recent_profit=recentAnalysis(recent_operation,recent_str)
		
		text=recent_text+history_text+"，操作总收益：{:.2f}".format(history_profit+recent_profit)
		
		msg="{} | {}".format(time.strftime("%H:%M:%S", time.localtime()),text)
		if len(msg)>=len(msg0):
			sys.stdout.write("\r{}".format(msg))
		else:
			blanks="  "*(len(msg0)-len(msg))
			sys.stdout.write("\r{}{}".format(msg,blanks))
		msg0=msg
		sys.stdout.flush()
		time.sleep(.1)
	except:
		pass
