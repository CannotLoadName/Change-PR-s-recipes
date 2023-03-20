#-*-coding:utf-8;-*-
from os import listdir
from os.path import dirname,isdir,splitext,join
from sys import argv
from json import dumps,loads
path=dirname(__file__)
def addpth(a,b):
    return join(a,b)
def todic(j):
    for i in range(0,len(j)):
        j[i]=loads(j[i])
    return j
fla=open(addpth(path,'original.csv'),'r')
flb=open(addpth(path,'replacement.csv'),'r')
flc=open(addpth(path,'blacklist.csv'),'r')
fld=open(addpth(path,'declinematerials.csv'),'r')
ori=todic(fla.read().strip('\n').split('\n'))
repl=todic(flb.read().strip('\n').split('\n'))
blist=flc.read().strip('\n').split('\n')
decm=fld.read().strip('\n').split('\n')
fla.close()
flb.close()
flc.close()
fld.close()
def decline(dc):
    m=' '+dc[1][0]+' '
    dc[0]=m
    dc[2]=m
    return dc
def gettzm(nm):
    ret=splitext(nm)[1]
    if ret[0]=='.':
        ret=ret[1:]
    return ret
def repldic(dic):
    global ori,repl
    for i in range(0,len(ori)):
        if dic==ori[i]:
            dic=repl[i]
            break
    return dic
def repldics(dics):
    for i in dics:
        dics[i]=repldic(dics[i])
    return dics
def dealfile(fn,sgn):
    f=open(fn,'r')
    finc=loads(f.read())
    f.close()
    if finc.__contains__('key'):
        finc['key']=repldics(finc['key'])
    if sgn and finc.__contains__('pattern'):
        finc['pattern']=decline(finc['pattern'])
    f=open(fn,'w')
    f.write(dumps(finc,indent=2))
    f.close()
def dealdir(fp,sign):
    global blist,decm
    for f in listdir(fp):
        fn=addpth(fp,f)
        if isdir(fn):
            dealdir(fn,sign or f=='recipes')
        else:
            if sign and gettzm(f)=='json' and not(f in blist):
                dealfile(fn,f in decm)
if len(argv)>=2:
    dealdir(argv[1],False)
else:
    dealdir(input('输入模组文件解压到的目录：'),False)