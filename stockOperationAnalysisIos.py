
#Copyright@Hongwei008
import requests
import time
import sys
import appex, ui
import socket
def getName(record,history_str):
	name= (history_str[record[1]])[0][21:]

	return name

		
def getPrice(record,history_str):
	
	now= (history_str[record[1]])[3]

	return now[:-1]
	
def getRate(record,history_str):
	
	buy5=float(0.3*int((history_str[record[1]])[10])+0.3*int((history_str[record[1]])[12])+0.2*int((history_str[record[1]])[14])+0.1*int((history_str[record[1]])[16])+0.1*int((history_str[record[1]])[18]))
	sell5=float(0.3*int((history_str[record[1]])[20])+0.3*int((history_str[record[1]])[22])+0.2*int((history_str[record[1]])[24])+0.1*int((history_str[record[1]])[26])+0.1*int((history_str[record[1]])[28]))
	if buy5>sell5:
		rate= str(format(float((history_str[record[1]])[3])/float((history_str[record[1]])[2])-1,'.2%'))+'↑'*int(buy5/sell5)
	else:
		rate= str(format(float((history_str[record[1]])[3])/float((history_str[record[1]])[2])-1,'.2%'))+'↓'*int(sell5/buy5)
	
	return rate

		
def buyingAnalysis(record,history_str):
	code=record[1]
	price=record[2]
	volume=record[3]
	str0=getName(record,history_str)+" "+getPrice(record,history_str)+" "+getRate(record,history_str)+" 买入收益：{:.2f}".format(volume*(float(getPrice(record,history_str))-price))+"\n "
	profit=volume*(float(getPrice(record,history_str))-price)
	return str0,profit

def selling_analysis(record,history_str):
	code=record[1]
	price=record[2]
	volume=record[3]
	str0=getName(record,history_str)+" "+getPrice(record,history_str)+" "+getRate(record,history_str)+" 卖出收益：{:.2f}".format(volume*(-float(getPrice(record,history_str))+price))+"\n "
	profit=volume*(-float(getPrice(record,history_str))+price)
	return str0,profit

def historyAnalysis(records,history_str):
	profit=0
	for record in records:
		
		if record[0]=='买入':
			text0,profit2=buyingAnalysis(record,history_str)
		else:
			text0,profit2=selling_analysis(record,history_str)
		profit=profit+profit2
	str0="，历史收益：{:.2f}".format(profit)

	return str0,profit

def recentAnalysis(records,history_str):
	text=""
	profit=0
	profit0=0
	profit1=0
	for record in records:
		if record[0]=='买入':
			text0,profit2=buyingAnalysis(record,history_str)
			profit1=profit1+profit2
		else:
			text0,profit2=selling_analysis(record,history_str)
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


history_records=[['卖出','sz300498',14.71,16600],['卖出','sz300498',14.8,1500],['买入','sz300498',14.324,18100],['卖出','sz300766',13.01,20000],['卖出','sz300766',14.68,20000],['买入','sz300766',14.88,19700],['卖出','sz300766',14.51,19700],['买入','sz300766',14.36,19800],['卖出','sz300766',14.40,19800],['买入','sz300766',13.94,19800],['卖出','sz300987',34,8300],['买入','sz300766',13.02,20000],['买入','sz300987',31.688,8300],['卖出','sz300766',13.3,20000]]
recent_operation=[['买入','sz300498',14.49,10100],['买入','sz300002',5.8,20600]]

global history_str
global recent_str

history_str=getData(history_records)
recent_str=getData(recent_operation)

history_text,history_profit=historyAnalysis(history_records,history_str)

msg0=""

recent_text,recent_profit=recentAnalysis(recent_operation,recent_str)

text=recent_text+history_text+"，操作总收益：{:.2f}".format(history_profit+recent_profit)

msg="{} 更新：\n{}".format(time.strftime("%H:%M:%S", time.localtime()),text)
if len(msg)>=len(msg0):
	sys.stdout.write("\r{}".format(msg))
else:
	blanks="  "*(len(msg0)-len(msg))
	sys.stdout.write("\r{}{}".format(msg,blanks))
msg0=msg
sys.stdout.flush()
v = ui.View(frame=(0, 0, 320,300))
label = ui.Label(frame=(0, 0, 320, 280),alignment=ui.ALIGN_CENTER,flex='wh')
label.font = ('Menlo', 12)
label.number_of_lines=0
label.text = msg
v.add_subview(label)
	
appex.set_widget_view(v)
