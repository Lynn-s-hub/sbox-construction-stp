import os
import re

#读取输出文件中的内容，并从中筛选S盒的
file=open('test.result','r')
file_contents=file.readlines()
file.close()

#将生成的S盒存放在文件中，并添加到约束条件中
print_file=open('lastresult.txt','w')
for content in file_contents:
    if 'S[' in content:
        #print(content)
        print_file.write(content)
print_file.close()

file=open('lastresult.txt','r')
tmp=file.read()
#tmp = os.popen('stp 1.cvc').read()
file.close()

#print(tmp) #运行文件
tmp = tmp.replace('ASSERT', '')
t=tmp.replace('0x','')
m=re.findall('[ABCDEF0-9]',str(t))


file=open('S_box.txt','a')
file.write(str(m))
file.write('\n')
file.close
S=[0]*16

for i in range(0,16):
   x=m[2*i]
   y=m[2*i+1]
   xx=int(x,16)
   yy=int(y,16)
   S[xx]=yy
print(S)    

file=open('solution.txt','a')
file.write(str(S))
file.write('\n')
file.close

text='ASSERT(S[0x%X'%0 + ']/=0x%X'%S[0] 
for i in range(1,len(S)):
    text=text+' OR S[0x%X'%i+']/=0x%X'%S[i]
text=text+');'

fp =open('test.cvc','r')         
lines = []
for line in fp:                  #内置的迭代器, 效率很高
    lines.append(line)
fp.close()

lines.insert(78, text) #在第 LINE+1 行插入
s = ''.join(lines)
fp = open('test.cvc', 'w')
fp.write(s)
fp.close()







