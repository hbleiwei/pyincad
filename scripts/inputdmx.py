# -*- coding: utf-8 -*-
# 输入地面线
from pyincad.core import *
from pyincad import core
import string
def inputdmx(databasename,dmxfilename,rampid,groundid):
    #输入纵断面地面线
    theproject=incadproject()
    theproject.openproject(databasename)
    if theproject.haveground(rampid,groundid):
        grd=theproject.ground(rampid,groundid)
        grd.removeall()
    else:
        grd=theproject.newground(rampid,groundid)
    #读入地面线
    fi=file(dmxfilename)
    for lines in fi:
        di=lines.split()
        ch=string.atof(di[0])
        high=string.atof(di[1])
        grd.append(ch,high)
        print "读入桩号/高程:", ch,high
    grd.save()
    fi.close()
    theproject.closeproject()
    print "完成读入纵断面地面线"
def inputhdx(databasename,hdxfilename,rampid,groundid,hdxid):
    import string
    thepro=core.incadproject()
    thepro.openproject(databasename)
    cset=thepro.crossset(rampid)
    cset.removeall()
    grd=thepro.ground(rampid,groundid)
    grd.load()
    hdxfi=file(hdxfilename)
    iii=1
    for lines in hdxfi:
        #print i,":",lines
        if iii == 1:
            cursec=core.crosssection()
            curline=core.crossline()
            #输入桩号
            ch=string.atof(lines)
            dmxhigh=grd.high(ch)
            print "横断面地面线桩号",ch,"中心高程",dmxhigh
            cursec=cset.append(ch)
            curline=cursec.addline(hdxid)
            curline.append1(0,dmxhigh)
            cursec.save()
        if iii == 2:
            #左侧点
            lpts=lines.split()
            for (offset,pt) in enumerate(lpts):
                lpts[offset]=string.atof(pt)
            for i in range(0,len(lpts),2):
                curline.append1(-lpts[i],lpts[i+1],0,True)
        if iii == 3:
            #右侧点
            rpts=lines.split()
            for (offset,pt) in enumerate(rpts):
                rpts[offset]=string.atof(pt)
            for i in range(0,len(rpts),2):
                curline.append1(rpts[i],rpts[i+1])
        if iii==4 :
            curline.save()
            iii=0
        iii=iii+1
    #print fi
    hdxfi.close()
    thepro.closeproject()
    print "完成读入横断面地面线"
def test():
    inputhdx("c://incadtest//shian.fdb","f://dd1.hdx","f://dd1.dmx",1,55)
def drawhdm(secline):
    #绘制横断面
    from pyincad.cadtools import pyacad
    acad=pyacad()
    acad.linkautocad()
    pts=secline.getallpoint()
    acad.addpoly(pts)
def test1(databasename,rampid):
    #测试横断面取值
    thepro=core.incadproject()
    thepro.openproject(databasename)
    cset=thepro.crossset(rampid)
    cset.load()
    for i in range(0,cset.count()):
        sec=cset.item(i)
        sec.load()
        secline=sec.getat(55)
        h1=secline.high(1.50)
        h2=secline.high(2.0)
        dh=h2-h1
        if abs(dh) > 2.0/100.*0.5+0.05:
            #print "aleart:",sec.ch(),h2-h1
            drawhdm(secline)
            break
    print "finished"
    thepro.closeproject()
if __name__ == "__main__":
    #inputdmx("c://incadtest//shian.fdb","f://dd1.dmx",1,1)
    #inputhdx("c://incadtest//shian.fdb","f://dd1.hdx",1,1,55)
    #inputhdx(,"f://dd1.hdx","f://dd1.dmx",1,55)
    test1("c://incadtest//shian.fdb",1)


