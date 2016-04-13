#!/usr/bin/python
#-*-coding:utf8-*-

# 
#                                 _oo8oo_
#                                o8888888o
#                                88" . "88
#                                (| -_- |)
#                                0\  =  /0
#                              ___/'==='\___
#                            .' \\|     |// '.
#                           / \\|||  :  |||// \
#                          / _||||| -:- |||||_ \
#                         |   | \\\  -  /// |   |
#                          | \_|  ''\---/''  |_/ |
#                         \  .-\__  '-'  __/-.  /
#                       ___'. .'  /--.--\  '. .'___
#                    ."" '<  '.___\_<|>_/___.'  >' "".
#                    | | :  `- \`.:`\ _ /`:.`/ -`  : | |
#                   \  \ `-.   \_ __\ /__ _/   .-` /  /
#               =====`-.____`.___ \_____/ ___.`____.-`=====
#                                  `=---=`
#  
# 
#               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                         佛祖保佑           永无bug
#


import math

fname = raw_input('enter the file name: ')
if len(fname) == 0:
	fname = 'text.txt'

	
fhand = open(fname, 'r')

text = ''
for i in fhand:
	text = text + i

dictionary = {}
for i in text:
	if i not in dictionary.keys():
		dictionary[i] = text.count(i)		#	dictionary formed

length = len(text)

lower = 0

dic = {}									#	需要被传导的字典
for i in dictionary:
	dic[i] = [lower, lower + dictionary[i]]
	lower = lower + dictionary[i]

m = 3 + int(math.log(length, 2))			# 	m = 编码位数

l = 0
u = 2 ** m - 1
b = 0
scale3 = 0
res = ''

for i in text:
	l, u = l + (u - l + 1) * dic[i][0] / length, l + (u - l + 1) * dic[i][1] / length - 1	#计算上下限
	l = '0' * (m + 2 - len(bin(l))) + bin(l)[2: ]
	u = '0' * (m + 2 - len(bin(u))) + bin(u)[2: ]	#	将 l、 u 二进制化
	#print l, u, int(l, 2), int(u, 2)
	while (l[0] == u[0] or (l[:2] == '01' and u[: 2] == '10')):
		if l[0] == u[0]:
			b = int(l[0])
			res = res + l[0]				#	发送 MSB
			l = l[1: ] + '0'				# 	l 向左移 末位补0
			u = u[1: ] + '1'				#	u 向左移 末位补1
			#print l, u, int(l, 2), int(u, 2)
			if (scale3 > 0):
				res = res + str(b ^ 1) * scale3		#	发送 b 的补码
 				scale3 = 0			#	递减scale3
 		else:								#	满足E3条件
 			l = '0' + l[2: ]  + '0'
 			u = '1' + u[2: ] + '1'			#	左移并高位取反
 			scale3 = scale3 + 1
 			#print l, u, int(l, 2), int(u, 2)
 	l = int(l, 2)
 	u = int(u, 2)
 	#print res
 	#print '\n'

#print len(res), length
#print m
#print dic
#print dictionary
#print res
l = '0' * (m + 2 - len(bin(l))) + bin(l)[2: ]
b = int(l[0])
b = str(b ^ 1)
#print l
#print 'scale3: ', scale3

x = '['
for i in dic:
	if i == ' ':
		x = x + '\' \'' + ' ' + str(dic[i][0]) + ' ' + str(dic[i][1]) + '  '
	else:
		x = x + i + ' ' + str(dic[i][0]) + ' ' + str(dic[i][1]) + '  '
x = x[: -2] + ']'

ffhand_name = fname[: -4] + '_code.txt'

ffhand = open(ffhand_name, 'w')
ffhand.write(str(m))
ffhand.write('.')
ffhand.write(res)
ffhand.write(l[0] + scale3 * b + l[1: ])
ffhand.write(x)
ffhand.close()
print 'Done!'





