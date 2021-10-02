# stock-operation-analysis
作为资深韭菜，我经常做出追涨杀跌的谜之操作。为了纠正这种错误习惯，我打算分析自己每次操作的收益，用血淋淋的数字提醒自己，千万不要追涨杀跌！！！  

一、基本功能  
（一）最近一次操作分析  
股票操作最基本的分为买入、卖出，因此对应的收益分析为买入后的实际收益、卖出后的机会成本。

（二）历史操作分析  
做完第一个功能后，又想看看自己所有的操作究竟收益几何。因此又加入了历史操作的分析，不过此处只计算总收益，就没有再挨个展示每次操作的收益了。

（三）买卖比  
做收益分析肯定关心股价走势。我平时做交易决策是看挂单买卖数量的多寡。因此加了一个买五、卖五的买卖比指标。买五大于卖五则给出“↑”，否则给出“↓”。箭头数量体现多空双方力量对比，由买五、卖五两数的倍数的向下取整决定。

二、使用说明  
（一）买入  
基本形式为：['买入','股票代码',交易价格,交易数量]，如['买入','sz300498',14.33,100]。

（二）卖出  
基本形式为：['卖出','股票代码',交易价格,交易数量]，如['卖出','sz300498',14.33,100]。

（三）最近一次及历史操作  
找到stockOperationAnalysis.py里的recent_operation和history_records列表，将买入、卖出操作加到列表中即可。

目前只实现桌面文本提示，效果图如下。后面有需要再慢慢添加其他功能，比如将操作记录放入数据库、通过input方式加入操作记录、用tkinter做展示、加入图表分析等。


![image](https://github.com/Hongwei008/stock-operation-analysis/blob/main/%E6%95%88%E6%9E%9C%E5%9B%BE.png)


2021年10月3日 00:31:46更新：  

一、ios设备  

为了在手机上也能实时看到收益情况，利用Pythonista做了一个小组件。代码见stockOperationAnalysisIos.py，效果图见下：  

![image](https://github.com/Hongwei008/stock-operation-analysis/blob/main/ios%E6%95%88%E6%9E%9C%E5%9B%BE.jpg)

二、windows设备  

在实现ios设备上查看实时收益功能的时候，发现手机上从新浪api获取数据的速度较慢，严重影响程序速度，甚至大部分时候都是跑不出来结果的。  

因此我将原代码（stockOperationAnalysis.py）做了优化。主要是将历史操作、最近操作的股票的实时数据从最底层的函数中剥离出来，放到最上一层，一次性从历史操作数据、最近操作数据中读取涉及的股票代码，并从新浪api获取数据以备分析。  

优化后，windows上运行速度提升了近7倍。

