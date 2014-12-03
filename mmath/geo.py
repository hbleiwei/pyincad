__author__ = 'leiwei'
# -*- coding: utf-8 -*-
# 版本0.0001
import math
def getaz(dx,dy):
    #计算方位角
    if dx == 0:
        if (dy > 0):
            return math.pi/2.0
        if (dy < 0):
            return math.pi*3.0/2.0
        if (dy == 0):
            return 0
    dx=float(dx)
    dy=float(dy)
    ang=abs(dy/dx)
    ang=math.atan(ang)
    if (dx >0) and (dy >= 0):
        ang=ang
    elif (dx > 0) and (dy <= 0):
        ang=math.pi*2.0-ang
    elif (dx < 0) and (dy >=0):
        ang=math.pi-ang
    elif (dx < 0) and (dy <=0):
        ang=math.pi+ang
    return ang
def neatangle(ang):
    if ang < 0:
        while(ang < 0):
            ang=ang+math.pi*2
        return ang
    elif ang > 2.0*math.pi:
        while(ang > math.pi*2.0):
            ang=ang-2*math.pi
        return ang
    return ang
def dist(dx,dy):
    return math.sqrt(dx*dx+dy*dy)
def dfm2d(ang):
    #度分秒向度转换
    flag=1
    if ang < 0:
        flag=-1
    ang=abs(ang)
    d=int(ang)
    f=ang-d
    f=int(f*100.)
    m=(ang-d-f/100.)*10000.
    print d,f,m
    return flag*(d+f/60.+m/3600.)
def d2r(ang):
    return ang/180.*math.pi
def r2d(ang):
    return ang/math.pi*180.
def left2line(ptx,pty,x,y,az):
    #计算点ptx,pty是否位于向量的左侧(1),右侧(-1)，或者线上
    az=az+math.pi/2.0
    dx=math.cos(az)
    dy=math.sin(az)
    dx1=ptx-x
    dy1=pty-y
    d=dx*dx1+dy*dy1
    if d < 0:
        return -1
    elif d > 0:
        return 1
    return 0
def lineinters(x1,y1,dx1,dy1,x2,y2,dx2,dy2):
    #计算直线x1,y1,dx1,dy1为增量和x2,y2,dx2,dy2的交点
    if (dx1 * dx2 == 0):
        if (dx1 == 0) & (dx2 == 0):
            return None
        if (dx1 == 0):
            x=x1
            y=(dy2/dx2)*x+(y2-(dy2/dx2)*x2)
        if (dx2 == 0):
            x=x2
            y=(dy1/dx1)*x+(y1-(dy1/dx1)*x1)
        return (x,y)
    else:
        k1=dy1/dx1
        k2=dy2/dx2
        b1=y1-k1*x1
        b2=y2-k2*x2
        if k1 == k2:
            #平行线，没有交点
            return None
        x=(b2-b1)/(k1-k2)
        y=k1*x+b1
        return (x,y)
if __name__ == "__main__":
    #print lineinters(100,100,0,30,640.339,960.7565,2852.1419,-755.4622)
    #print dist(10,20)
    print d2r(dfm2d(30.243724))


