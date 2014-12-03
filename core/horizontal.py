# -*- coding: utf-8 -*-
import win32com.client
import math
from pyincad.mmath import geo
def u(s):
    if isinstance(s, unicode):
        return s
    else:
        return s.decode('utf-8')
class horizontal():
    def __init__(self, temp=True, parent=None):
        self.istemp=False
        self.parent=parent
        self.object=None
        if temp:
            self.istemp=True
            self.object=win32com.client.Dispatch("incadopera.horizontal")
    def load(self):
        self.object.Load()
    def append(self):
        #TODO test
        horele=horizontalelement(False,self)
        horele.object=self.object.Append()
        return horele
    def calch(self,startch=0):
        self.object.CalCH(startch)
    def calptch(self,x,y,chref=0):
        #计算指定点的桩号,如果没有计算到，则返回None，否则返回值第一位为桩号，第二位为距离
        #TODO 目前距离计算返回值错误
        re=self.object.CalPTCH(x,y,chref)
        if re[0] == 0:
            return None
        return (re[1],re[2])
    def reverse(self):
        #TODO 此处存在错误
        self.object.Reverse()
    def coxy(self,ch,offset):
        return self.object.COXY(ch,offset)
    def insert(self,pos):
        #TODO test
        horele=horizontalelement(False,self)
        horele.object=self.object.Insert(pos)
        return horele
    def translation(self,dx,dy):
        self.object.Translation(dx,dy)
    def remove(self,pos):
        #TODO test
        self.object.Remove(pos)
    def removeall(self):
        #TODO test
        self.object.RemoveAll()
    def rotate(self,x,y,ang):
        self.object.Rotate(x,y,ang)
    def save(self):
        self.object.Save()
    def  count(self):
        return self.object.count
    def empty(self):
        if self.object.Empty == 0:
            return False
        return True
    def endch(self):
        return self.object.EndCH
    def item(self,pos):
        #TODO test
        horele=horizontalelement(False,self)
        horele.object=self.object.Item(pos)
        return horele
    def startch(self):
        return self.object.startch
    def modified(self):
        if self.object.Modified == 0:
            return False
        return True
    def intersectwithline(self,lx,ly,laz):
        #TODO test
        return self.object.IntersectWithLine(lx,ly,laz)
    def azflag(self,ch):
        #TODO test
        return self.object.AzFlag(ch)
    def calks(self):
        #TODO test
        self.object.CalKS()
    def getmainpoints(self):
        #TODO test
        return self.object.GetMainPoints()
    def last(self):
        #TODO test
        return self.object.Last()
    def rampid(self):
        return self.object.rampid
    def setrampid(self,id):
        #TODO test
        self.object.rampid=id
    ################################
    #user define
    ################################
class horizontalelement():
    def __init__(self, temp=True, parent=None):
        #TODO test
        self.istemp=False
        self.parent=parent
        self.object=None
        if temp:
            self.istemp=True
            self.object=win32com.client.Dispatch("incadopera.horizontalelement")
    def parent(self):
        #TODO test
        return self.object.Parent
    def modified(self):
        #TODO test
        return self.object.Modified
    def birthnext(self,ks=0,arclength=0,aas=0,aae=0,kss=0,kse=0):
        obj=self.object.BirthNext(ks,arclength,aas,aae,kss,kse)
        tobj=horizontalelement(True,None)
        tobj.object=obj
        return tobj
    def birthpre(self,ks=0,arclength=0,aas=0,aae=0,kss=0,kse=0):
        obj=self.object.BirthPre(ks,arclength,aas,aae,kss,kse)
        tobj=horizontalelement(True,None)
        tobj.object.SetEqualTo(obj)
        return tobj
    def cal(self,caltrans=False):
        self.object.Cal(caltrans)
    def calch(self,startch=0):
        #TODO test
        self.object.CalCH(startch)
    def calptch(self,x,y,chref):
        #TODO test
        return self.object.CalPTCH(x,y,chref)
    def reverse(self):
        #TODO test
        self.object.Reverse()
    def coxy(self,ch,offset):
        #计算指定点的坐标，返回值（计算是否成功，x，y,az,ks)
        return self.object.COXY(ch,offset)
    def setequalto(self,ele):
        self.object.SetEqualTo(ele.object)
    def getendtransitionline(self):
        return self.object. GetEndTransitionLine()
    def getstarttransitionline(self):
        return self.object.GetStartTransitionLine()
    def initarc(self,cx,cy,r,azflag,sang,eang):
        return self.object.InitArc(cx,cy,r,azflag,sang,eang)
    def initarc1(self,sx,sy,ex,ey,r):
        #TODO test
        return self.object.InitArc1(sx,sy,ex,ey,r)
    def initbylines(self,x1,y1,az1,x2,y2,az2):
        #根据直线初始化曲线，自动计算左右偏
        self.object.InitByLines(x1,y1,az1,x2,y2,az2)
    def initline(self,sx,sy,ex,ey):
        return self.object.InitLine(sx,sy,ex,ey)
    def initline1(self,sx,sy,saz,length):
        return self.object.InitLine1(sx,sy,saz,length)
    def rotate(self,x,y,ang):
        self.object.Rotate(x,y,ang)
    def rotateto(self,x,y,angle,typ,ch):
        #TODO test
        self.object.RotateTo(x,y,angle,typ,ch)
    def threeelement(self,preele,nextele,offset=0,typ=0):
        return self.object.ThreeElement(preele.object,nextele.object,offset,typ)
    def translation(self,dx,dy):
        self.object.Translation(dx,dy)
    def aae(self):
        #TODO test
        return self.object.Ae
    def setaae(self,newval):
        self.object.Ae=newval
    def arcendaz(self):
        #TODO test
        return self.object.ArcEndAZ
    def arcendx(self):
        #TODO test
        return self.object.ArcEndX
    def arcendy(self):
        #TODO test
        return self.object.ArcEndY
    def arclength(self):
        #TODO test
        return self.object.ArcLength
    def setarclength(self,newval):
        #TODO test
        self.object.ArcLength=newval
    def arcstartaz(self):
        #TODO test
        return self.object.ArcStartAZ
    def setarcstartaz(self,newval):
        #TODO test
        self.object.ArcStartAZ=newval
    def arcstartx(self):
        #TODO test
        return self.object.ArcStartX
    def setarcstartx(self,newval):
        #TODO test
        self.object.ArcStartX=newval
    def arcstarty(self):
        #TODO test
        return self.object.ArcStartY
    def setarcstarty(self,newval):
        #TODO test
        self.object.ArcStartY=newval
    def aas(self):
        #TODO test
        return self.object.As
    def setaas(self,newval):
        self.object.As=newval
    def azflag(self):
        #TODO test
        return self.object.AzFlag
    def setazflag(self,newval):
        #TODO test
        self.object.AzFlag=newval
    def cadcenter(self):
        return self.object.CadCenter
    def  cadeang(self):
        return self.object.CadEAng
    def cadendpoint(self):
        #TODO test
        return self.object.CadEndPoint
    def cadsang(self):
        return self.object.CadSAng
    def cadstartpoint(self):
        #TODO test
        return self.object.CadStartPoint
    def centerx(self):
        #TODO test
        return self.object.CenterX
    def centery(self):
        #TODO test
        return self.object.CenterY
    def endaz(self):
        #TODO test
        return self.object.EndAZ
    def endch(self):
        #TODO test
        return self.object.EndCH
    def endks(self):
        #TODO test
        return self.object.EndKS
    def setendks(self,newval):
        #TODO test
        self.object.EndKS=newval
    def endx(self):
        return self.object.EndX
    def endy(self):
        return self.object.EndY
    def hych(self):
        #TODO test
        return self.object.HYCH
    def id(self):
        #TODO test
        return self.object.id
    def index(self):
        #TODO test
        return self.object.Index
    def jdx(self):
        #TODO test
        return self.object.JDX
    def jdy(self):
        #TODO test
        return self.object.JDY
    def ks(self):
        #TODO test
        return self.object.KS
    def setks(self,newval):
        #TODO test
        self.object.KS=newval
    def le(self):
        #TODO test
        return self.object.LE
    def ls(self):
        #TODO test
        return self.object.LS
    def radius(self):
        #TODO test
        return self.object.Radius
    def setradius(self,newval):
        #TODO test
        self.object.Radius=newval
    def startaz(self):
        #TODO test
        return self.object.StartAz
    def startch(self):
        #TODO test
        return self.object.startch
    def startks(self):
        #TODO test
        return self.object.StartKS
    def setstartks(self,ks):
        #TODO test
        self.object.StartKS=ks
    def startx(self):
        return self.object.StartX
    def starty(self):
        return self.object.StartY
    def yhch(self):
        #TODO test
        return self.object.YHCH
    def linkto(self,preobject,modifystart=True):
        #TODO test
        return self.object.LinkTo(preobject.object,modifystart)
    def cala1(self,preobject):
        #TODO test
        #两单元计算缓和曲线参数
        return self.object.CalA1(preobject.object)
    def offset(self,offsetdist,offsettrans=False):
        #TODO test
        self.object.Offset(offsetdist,offsettrans)
    def startradius(self):
        #TODO test
        return self.object.StartRadius
    def setstartradius(self,newval):
        #TODO test
        self.object.StartRadius=newval
    def endradius(self):
        #TODO test
        return self.object.EndRadius
    def setendradius(self,newval):
        #TODO test
        self.object.EndRadius=newval
    def setls(self,ls,kss):
        #TODO test
        self.object.SetLS(ls,kss)
    def setle(self,le,kse):
        #TODO test
        self.object.SetLE(le,kse)
class horjd():
    #交点设计平面的交点,一个平面交点由一个曲线单元组成，曲线单元的起始参数为0
    def __init__(self,x=0,y=0,r=0,ls=0,le=0):
        self.x=x
        self.y=y
        self.eleobj=horizontalelement()
        self.eleobj.setazflag(1)
        self.eleobj.setradius(r)
        self.eleobj.setls(ls,0)
        self.eleobj.setle(le,0)
        self.eleobj.setarclength(1)
        self.eleobj.cal()
        self.t1=0
        self.t2=0
        self.ang=0
        self.flag=1
        self.status=0#正常交点，=1为虚交点（一般为两个），=2与前交点形成卵形曲线，=3与后交点形成卵形曲线。
        self.xjpts=[] #虚交点数组
    def initbyang(self,ang,r,ls,le):
        #根据转角，起始缓和曲线，终止缓和曲线进行计算,需要注意的是如果转角左偏，为正值
        self.__init__(0,0,r,ls,le)
        self.eleobj.setazflag(1)
        if ang < 0:
            self.eleobj.setazflag(-1)
        az1=0
        az2=az1+ang
        self.eleobj.initbylines(0,0,az1,0,0,az2)
    def cal(self,prejd,nextjd):
        #根据前一交点和后一交点计算本交点
        #判断左偏和右偏
        self.flag=1 #左偏曲线
        if self.status == 0:
            az1=geo.getaz(self.x-prejd.x,self.y-prejd.y)
            az2=geo.getaz(nextjd.x-self.x,nextjd.y-self.y)
            f=geo.left2line(prejd.x,prejd.y,self.x,self.y,az2)
            if f == 0:
                return False
            self.ang=geo.neatangle(az2-az1)
            if  (f < 0):#右偏
                self.ang=math.pi*2.0-self.ang
            self.flag=f
        elif self.status == 1:
            az1=geo.getaz(self.xjpts[0].x-prejd.x,self.xjpts[0].y-prejd.y)
            az2=geo.getaz(nextjd.x-self.xjpts[1].x,nextjd.y-self.xjpts[1].y)
        #self.eleobj.setazflag(self.flag)
        self.eleobj.initbylines(prejd.x,prejd.y,az1,nextjd.x,nextjd.y,az2)
        #self.eleobj.cal(True)
        self.t1=geo.dist(self.eleobj.startx()-self.x,self.eleobj.starty()-self.y)
        self.t2=geo.dist(self.eleobj.endx()-self.x,self.eleobj.endy()-self.y)
    def radius(self):
        return self.eleobj.radius()
    def setradius(self,r):
        self.eleobj.setradius(abs(r))
    def azflag(self):
        return self.eleobj.azflag()
    def setazflag(self,newval):
        self.eleobj.setazflag(newval)
    def ls(self):
        return self.eleobj.ls()
    def le(self):
        return self.eleobj.le()
    def setls(self,ls):
        self.eleobj.setls(ls,self.eleobj.startks())
    def setle(self,le):
        self.eleobj.setle(le,self.eleobj.endks())
    def arclength(self):
        return self.eleobj.arclength()
    def tlen1(self):
        return self.t1
    def tlen2(self):
        return self.t2
    def angle(self):
        return self.ang
    def distto(self,jd):
        #计算交点间距
        return geo.dist(self.x-jd.x,self.y-jd.y)
    def betweenline(self,nextjd):
        #计算夹直线长度
        di=self.distto(nextjd)
        return di-self.tlen2()-nextjd.tlen1()
class jddesign():
    #交点法设计曲线
    def __init__(self):
        self.pts=[]
    def append(self,x,y,r=0,ls=0,le=0):
        pt=horjd(x,y,r,ls,le)
        self.pts.append(pt)
    def remove(self,index):
        pass
    def getat(self,index):
        return self.pts[index]
    def count(self):
        return len(self.pts)
    def cal(self,startch):
        pass
    def coxy(self,ch,offset):
        pass
    def calch(self,x,y):
        pass
    def convert2hor(self):
        #转换为平面单元
        pass
if __name__ == "__main__":
    #ele=horizontalelement()
    #print geo.left2line(2025.5791,855.2230,1362.6623,484.2829,50.61611176)
    jd=horjd(100,200,500,100,100)
