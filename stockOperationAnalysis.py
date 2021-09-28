#coding=gbk
import requests
import time
import sys
import os

def get_name(code):
	r = requests.get("http://hq.sinajs.cn/list=%s" % (code))
	res = r.text.split(',')
	if len(res) > 1:
		name= r.text.split(',')[0][21:]
		
		return name
	else:
		return "��������"
		
def get_price(code):
	r = requests.get("http://hq.sinajs.cn/list=%s" % (code))
	res = r.text.split(',')
	if len(res) > 1:
		now= r.text.split(',')[3]
		
		return now[:-1]
	else:
		return "��������"
		
def get_rate(code):
	r = requests.get("http://hq.sinajs.cn/list=%s" % (code))
	res = r.text.split(',')
	if len(res) > 1:
		buy5=int(r.text.split(',')[12])+int(r.text.split(',')[14])+int(r.text.split(',')[16])+int(r.text.split(',')[18])+int(r.text.split(',')[10])
		sell5=int(r.text.split(',')[22])+int(r.text.split(',')[24])+int(r.text.split(',')[26])+int(r.text.split(',')[28])+int(r.text.split(',')[20])
		if buy5>sell5:
			rate= str(format(float(r.text.split(',')[3])/float(r.text.split(',')[2])-1,'.2%'))+'��'*int(buy5/sell5)
		else:
			rate= str(format(float(r.text.split(',')[3])/float(r.text.split(',')[2])-1,'.2%'))+'��'*int(sell5/buy5)
		return rate
	else:
		return "��������"
		
def buying_analysis(record):
	code=record[1]
	price=record[2]
	volume=record[3]
	str0=get_name(code)+" "+get_price(code)+" "+get_rate(code)+" �������棺{:.2f}".format(volume*(float(get_price(code))-price))+" | "
	profit=volume*(float(get_price(code))-price)
	return str0,profit

def selling_analysis(record):
	code=record[1]
	price=record[2]
	volume=record[3]
	str0=get_name(code)+" "+get_price(code)+" "+get_rate(code)+" �������棺{:.2f}".format(volume*(-float(get_price(code))+price))+" | "
	profit=volume*(-float(get_price(code))+price)
	return str0,profit

def historyAnalysis(records):
	profit=0
	for record in records:
		if record[0]=='����':
			text0,profit2=buying_analysis(record)
		else:
			text0,profit2=selling_analysis(record)
		profit=profit+profit2
	str0="����ʷ���棺{:.2f}".format(profit)
	
	return str0,profit

def recentAnalysis(records):
	text=""
	profit=0
	profit0=0
	profit1=0
	for record in records:
		if record[0]=='����':
			text0,profit2=buying_analysis(record)
			profit1=profit1+profit2
		else:
			text0,profit2=selling_analysis(record)
			profit0=profit0+profit2
		text=text0+text
		profit=profit1+profit0
	#str1=" �������棺{:.2f}���������棺{:.2f}�����ղ������棺{:.2f}".format(profit1,profit0,profit)
	str1=" ���ղ������棺{:.2f}".format(profit)
	text=text+str1
	return text,profit

history_records=[['����','sz300766',14.68,20000],['����','sz300766',14.88,19700],['����','sz300766',14.51,19700],['����','sz300766',14.36,19800],['����','sz300766',14.40,19800],['����','sz300766',13.94,19800],['����','sz300987',34,8300],['����','sz300766',13.02,20000],['����','sz300987',31.688,8300],['����','sz300766',13.3,20000]]
recent_operation=[['����','sz300498',14.33,15300],['����','sz300766',13.01,20000]]
input("�������ʼ")
os.system("cls")


history_text,history_profit=historyAnalysis(history_records)
msg0=""
while True:
	try:
		
		recent_text,recent_profit=recentAnalysis(recent_operation)
		
		text=recent_text+history_text+"�����������棺{:.2f}".format(history_profit+recent_profit)
		
		msg="{} | {}".format(time.strftime("%H:%M:%S", time.localtime()),text)
		if len(msg)>=len(msg0):
			sys.stdout.write("\r{}".format(msg))
		else:
			blanks=" "*(len(msg0)-len(msg))
			sys.stdout.write("\r{}{}".format(msg,blanks))
		msg0=msg
		sys.stdout.flush()
		time.sleep(.1)
	except:
		pass
