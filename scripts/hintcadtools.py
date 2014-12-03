# -*- coding: utf-8 -*-
# 纬地软件工具输入地面线
from pyincad.core import *
from pyincad import core
import string
def inputdmx(databasename,dmxfilename,rampid,groundid):
    #输入纬地数据的纵断面地面线
    theproject=incadproject()
    theproject.openproject(databasename)
    if theproject.haveramp(rampid):
        print("\n错误，未找到指定的匝道")
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
def cgtoeicad(brch,hintcgfile,eicadcgfile):
    #纬地超高文件转为eicad超高文件，可以处理断链,brch为brokench对象
    import re
    fi=file(hintcgfile)
    start=True
    dic={'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}
    lobj=core.crossslope() #左侧超高
    robj=core.crossslope() #右侧超高
    lsup=0
    rsup=0
    cgch=[]
    for lines in fi:
        if start:
            start=False
        else:
            di=lines.split()
            if len(di) > 0:
                ch=di[3]
                ch.strip()
                t1=di[2] #左侧超高
                t2=di[4] #右侧超高
                if re.match('^[A-Za-z0-9_]',ch):
                    c1=ch[0]
                    c1=c1.upper()
                    c1=dic[c1]
                    c2=string.atof(ch[1:])
                else:
                    c1=1
                    c2=string.atof(ch)
                cgch.append((c1,c2))
                if t1.find('9999') <> 0:
                    lsup=string.atof(t1)
                    cch=cc.calch(c1,c2)
                    lobj.append(cch,-lsup) #eicad 左侧为纬地的负值
                if t2.find('9999') <> 0:
                    rsup=string.atof(t2)
                    cch=cc.calch(c1,c2)
                    robj.append(cch,rsup)
    fi.close()
    for i in range(0,len(cgch)):
        c1=cgch[i][0]
        ch1=cgch[i][1]
        ch=cc.calch(c1,ch1)
        print ch1,lobj.slope(ch),robj.slope(ch),c1+1
def inputsqx1(databasename,sqxfilename,rampid,verid):
    #读入竖曲线
    #输入纬地数据的纵断面地面线
    theproject=incadproject()
    theproject.openproject(databasename)
    if not theproject.haveramp(rampid):
        print("\n错误，未找到指定的匝道")
    if theproject.havevertical(rampid,verid):
        grd=theproject.vertical(rampid,verid)
        grd.removeall()
    else:
        grd=theproject.newvertical(rampid,verid,"旧路地面线作为交点")
    #读入竖曲线设计线文件
    fi=file(sqxfilename)
    index=0
    ff=fi.readlines()
    for lines in ff:
        if index <> 0:
            #忽略文件头
            di=lines.split()
            ch=string.atof(di[0])
            high=string.atof(di[1])
            grd.append(ch,high,0)
            print "读入桩号/高程:", ch,high
        index=index+1
    grd.cal()
    grd.save()
    fi.close()
    theproject.closeproject()
    print "共读入交点<",index,">"
    print "完成读入纬地设计线输入"
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
def incadwidtoeicad(brch,lroad,learth,rroad,rearth):
    #incad转换为eicad宽度
    t1=lroad.getchlist()
    t2=learth.getchlist()
    t3=rroad.getchlist()
    t4=rearth.getchlist()
    tt=t1+t2+t3+t4
    tt=list(set(tt))
    tt.sort() #桩号列表
    for i in range(0,len(tt)):
        ch=tt[i]
        nn=cc.calsegnum(ch)
        cch=cc.calsegch(nn,ch)
        lr=lroad.width(ch)
        le=learth.width(ch)
        rr=rroad.width(ch)
        re=rearth.width(ch)
        print cch,le,0.000,lr,0.000,0.000,rr,0.000,re,nn+1 #eicad的正常段号为1
def widtoincad(brch,hintcgfile,lroad,learth,rroad,rearth):
    #纬地宽度文件转为incad宽度文件，可以处理断链,brch为brokench对象
    import re
    fi=file(hintcgfile)
    start=0
    isleft=False
    isright=False
    lroad.removeall()
    learth.removeall()
    rroad.removeall()
    rearth.removeall()
    dic={'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}
    #dict 为断链对照表，A对应正常
    for lines in fi:
        if start == 0:
            start=1 #不要第一行
        else:
            lines.strip()
            lines.upper()
            di=lines.split()
            if len(di) > 0:
                if di[0] == '[LEFT]':
                    isleft=True
                    isright=False
                elif di[0] == '[RIGHT]':
                    isleft=False
                    isright=True
                else:
                    ch=di[0]
                    ch.strip()
                    rwid=string.atof(di[2]) #路面宽度
                    ewid=string.atof(di[5]) #土路肩宽度
                    if re.match('^[A-Za-z0-9_]',ch):
                        c1=ch[0]
                        c1=c1.upper()
                        c1=dic[c1]
                        c2=string.atof(ch[1:])
                    else:
                        c1=1
                        c2=string.atof(ch)
                    cch=cc.calch(c1,c2)
                    if isleft:
                        learth.append(cch,ewid)
                        lroad.append(cch,rwid)
                    if isright:
                        rearth.append(cch,ewid)
                        rroad.append(cch,rwid)
    fi.close()
if __name__ == "__main__":
    #inputdmx("c://incadtest//shian.fdb","f://dd1.dmx",1,1)
    #inputhdx("c://incadtest//shian.fdb","f://dd1.hdx",1,1,55)
    #inputhdx(,"f://dd1.hdx","f://dd1.dmx",1,55)
    #test1("c://incadtest//shian.fdb",1)
    #inputsqx1("e://incadtest//lingyun.fdb","e://temp//nhjl.DMX",1,1)
    cc=core.brokench()
    cc.append(3837.326000, 3820.000000)
    cc.append(6741.076000, 6700.000000)
    cc.append(11493.735000, 11500.000000)
    cc.append(12806.883000, 12800.000000)
    cc.append(15753.411000, 15800.000000)
    cc.append(20579.488000, 20570.000000)
    cc.append(24791.846000, 24900.000000)
    cc.append(28111.412000, 28100.000000)
    #cgtoeicad(cc,"c:\\LYsc.sup","c:\\lysc.hdm")
    lroad=core.crosswidth()
    learth=core.crosswidth()
    rroad=core.crosswidth()
    rearth=core.crosswidth()
    widtoincad(cc,"c:\\LYZL.wid",lroad,learth,rroad,rearth)
    incadwidtoeicad(cc,lroad,learth,rroad,rearth)
    #print cc.calsegch(2,11050.407)

