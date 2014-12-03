# -*- coding: utf-8 -*-
# 文件操作
#from pyincad.core import *
#from pyincad import core
import string
def fileopera1(inname,outname):
    #给纬地的横断面地面线桩号前加上字母
    fi=file(inname)
    of=file(outname,'w')
    fdata=fi.readlines()
    fi.close()
    i=0
    first=True
    for ff in fdata:
        if first:
            of.write(ff)
            first=False
        else:
            if i==0:
                of.write('D'+string.strip(ff)+"\n")
                i=i+1
            elif i == 1:
                of.write(ff)
                i=i+1
            elif i == 2:
                of.write(ff)
                i=i+1
            elif i ==3:
                of.write(ff)
                i=0
    of.close()
def fileopera2(inname,outname):
    #给纬地的纵断面地面线桩号前加上字母
    fi=file(inname)
    of=file(outname,'w')
    fdata=fi.readlines()
    fi.close()
    i=0
    first=True
    for ff in fdata:
        if first:
            of.write(ff)
            first=False
        else:
            of.write('D'+string.strip(ff)+"\n")
    of.close()
if __name__ == "__main__":
    fileopera2("d:\\D.DMX","d:\\D.DMX1")
