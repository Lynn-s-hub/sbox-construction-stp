import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('a', type=str, default = None)
args = parser.parse_args()

file = open('init.txt','r')
text=file.read()
file.close()
file=open('init.txt','w')
#file.truncate()

file.close()
#a=input('')
with open('{:s}'.format(args.a),'r+') as f:
    content=f.read()
    f.seek(0,0)
    f.write(text+'\n'+content)



