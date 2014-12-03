# -*- coding: utf-8 -*-
import win32com.client
def u(s):
    if isinstance(s, unicode):
        return s
    else:
        return s.decode('utf-8')
class crosssection():
    def __init__(self, temp=True, parent=None):
        self.istemp=False
        self.parent=parent
        self.object=None
        if temp:
            self.istemp=True
            self.object=win32com.client.Dispatch("incadopera.crosssection")
    def addline(self,linetype):
        con=crossline(False)
        con.object=self.object.AddLine(linetype)
        return con
    def remove(self,linetype):
        self.object.Remove(linetype)
    def removeall(self):
        self.object.RemoveAll()
    def count(self):
        return self.object.count
    def haveline(self,linetype):
        return self.object.HaveLine(linetype)
    def getat(self,linetype):
        if not self.haveline(linetype):
            return None
        con=crossline(False)
        con.object=self.object.GetAt(linetype)
        return con
    def ch(self):
        return self.object.ch
    def setch(self,ch):
        self.object.ch=ch
    def empty(self):
        return self.object.Empty
    def refid(self):
        return self.object.RefID
    def setrefid(self,id):
        self.object.RefID=id
    def save(self):
        if self.istemp:
            return
        self.object.Save()
    def sectionindex(self):
        return self.object.SectionIndex
    def rampid(self):
        return self.object.RampID
    def id(self):
        return self.object.ID
    def getlinelist(self):
        pass
    def load(self):
        self.object.Load()
    def item(self,index):
        con=crossline(False)
        con.object=self.object.Item(index)
        return con
class crossline():
    def __init__(self, temp=True, parent=None):
        self.istemp=False
        self.parent=parent
        self.object=None
        if temp:
            self.istemp=True
            self.object=win32com.client.Dispatch("incadopera.crossline")
    def linetype(self):
        return self.object.linetype
    def setlinetype(self,newval):
        self.object.linetype=newval
    def append(self,x,y,pointtype=0,head=False):
        addright=1
        if head:
            addright=-1
        return self.object.Append(x,y,pointtype,addright)
    def append1(self,dx,dy,pointtype=0,head=False):
        if self.count() == 0:
            return self.append(dx,dy,pointtype,head)
        if head:
            dx=self.x(0)+dx
            dy=self.y(0)+dy
        else:
            dx=self.x(self.last())+dx
            dy=self.y(self.last())+dy
        return self.append(dx,dy,pointtype,head)
    def insert(self,pos,x,y,pointtype=0):
        return self.object.Insert(pos,x,y,pointtype)
    def remove(self,pos):
        self.object.Remove(pos)
    def removeall(self,pos):
        self.object.RemoveAll()
    def x(self,pos):
        return self.object.x(pos)
    def setx(self,pos,newval):
        self.object.Setx(pos,newval)
    def y(self,pos):
        return self.object.y(pos)
    def sety(self,pos,newval):
        return self.object.Sety(pos,newval)
    def point(self,pos):
        x=self.x(pos)
        y=self.y(pos)
        tp=self.pointtype(pos)
        return (x,y,tp)
    def setpoint(self,pos):
        pass
    def pointtype(self,pos):
        return self.object.pointType(pos)
    def setpointtype(self,pos,typ):
        self.object.SetpointType(pos,typ)
    def count(self):
        return self.object.count
    def last(self):
        if self.count() == 0:
            return -1
        return self.count()-1
    def pointcomment(self,pos):
        return self.object.PointComment(pos)
    def setpointcomment(self,pos,comm):
        self.object.SetPointComment(pos,comm)
    def high(self,x):
        h=self.object.High1(x)
        if h == -99999:
            return None
        return h
    def getpoint(self,pttype):
        pts=[]
        for i in range(0,self.count()):
            if self.pointtype(pos) == pttype:
                pts.append(self.point(i))
        return pts
    def remove(self,pos):
        self.object.Remove(pos)
    def removeall(self):
        self.object.RemoveAll()
    def translate(self,dx,dy):
        self.object.Translation(dx,dy)
    def areato(self,ncrossline,step1=1):
        return self.object.AreaTo(ncrossline.object,step1)
    def interray(self,x,y,dx,dy):
        return self.object.RayInters(x,y,dx,dy)
    def interline(self,sx,sy,ex,ey):
        return self.object.LineInters(sx,sy,ex,ey)
    def interslope(self,direct,upordown,sx,sy,slope):
        #求横断面线和边坡线的交点,direct=-1左侧添加边坡，direct=1右侧添加边坡
        #upordown=1填方边坡，=-1挖方边坡，sx,sy,起点坐标,slope边坡(1:x),为正值=0时为平坡，=99999为垂直边坡
        #interpt结果数组,pVal,返回值，=TRUE存在交点，否则不存在交点
        re=self.object.InterSlope(direct,upordown,sx,sy,slope)
        if (re[0] == 0):
            return None
        else:
            return re[1]
    def interlimitedslope(self,direct,upordown,sx,sy,slope,limitedhigh):
	    #和高度受限的边坡的交点,pVal=0,不存在交点。=1,高度受限，=2,计算成功,高度不受限
        #direct=-1左侧添加边坡，direct=1右侧添加边坡
        #upordown=1填方边坡，=-1挖方边坡，sx,sy,起点坐标,slope边坡(1:x),为正值=0时为平坡，=99999为垂直边坡
        #interpt结果数组,pVal,返回值，=TRUE存在交点，否则不存在交点
        re=self.object.InterLimitedSlope(direct,upordown,sx,sy,slope,limitedhigh)
        return re
    def save(self):
        if (self.istemp):
            return
        self.object.Save()
    def getallpoint(self):
        pts=[]
        if self.count() == 0:
            return pts
        for i in range(self.count()):
            pts.append(self.point(i))
        return pts
    #############################################################
    #以下为新增的python函数
    def setequal(self,line1):
        #将本线的数据和line1的数据设置相同
        self.removeall()
        if line1.count() == 0:
            return
        self.setlinetype(line1.linetype())
        for i in range(line1.count()):
            self.append(line1.x(i),line1.y(i),line1.pointtype(i),False)
    def appendline(self,line1,head=False):
        #line1放在本线的最后，line1的第一点将直接焊接在本线的最后一个点上。
        if (line1.count() == 0):
            return
        if (self.count() == 0):
            self.setequal(line1)
            return
        if head:
            x1=line1.x(line1.last())
            y1=line1.y(line1.last())
            x2=self.x(0)
            y2=self.y(0)
            dx=x2-x1
            dy=y2-y1
            for i in range(line1.count()-2,-1,-1):
                self.append(line1.x(i)+dx,line1.y(i)+dy,line1.pointtype(i),True)
        else:
            x1=line1.x(0)
            y1=line1.y(0)
            x2=self.x(self.last())
            y2=self.y(self.last())
            dx=x2-x1
            dy=y2-y1
            for i in range(1,line1.count()):
                self.append(line1.x(i)+dx,line1.y(i)+dy,line1.pointtype(i),False)
    def mirrorx(self,y):
        #绕x轴镜像
        for i in range(0,self.count()):
            dy=y-self.y(i)
            dy=2*dy;
            self.sety(i,self.y(i)+dy)
    def mirrory(self,x):
        #绕y轴镜像
        for i in range(0,self.count()):
            dx=x-self.x(i)
            dx=2*dx;
            self.setx(i,self.x(i)+dx)
    def reverse(self):
        #反转
        line1=crossline()
        l1=self.linetype()
        line1.setlinetype(l1)
        for i in range(0,self.count()):
            line1.append(self.x(i),self.y(i),self.pointtype(i),True)
        self.setequal(line1)
    def lx(self):
        if self.count() == 0:
            return None
        return self.x(0)
    def ly(self):
        if self.count() == 0:
            return None
        return self.y(0)
    def rx(self):
        if self.count() == 0:
            return None
        return self.x(self.last())
    def ry(self):
        if self.count() == 0:
            return None
        return self.y(self.last())
    def list(self):
        print "\n横断线,线上点总数%d"%(self.count())
        for i in range(0,self.count()):
            print"%d  %f  %f  %d"%(i,self.x(i),self.y(i),self.pointtype(i))
class crossset():
    def __init__(self, temp=True, parent=None):
        self.istemp=False
        self.parent=parent
        self.object=None
        if temp:
            self.istemp=True
            self.object=win32com.client.Dispatch("incadopera.crossset")
    def load(self):
        #载入横断面数据
        self.object.Load()
    def append(self, ch):
        #附加横断面数据
        con=crosssection(False)
        con.object=self.object.Append(ch)
        return con
    def remove(self,sectionindex):
        #注意该移除的是sectionindex
        self.object.Remove(sectionid)
    def removeall(self):
        self.object.RemoveAll()
    def count(self):
        return self.object.count
    def empty(self):
        if  self.object.Empty == 1:
            return True
        return False
    def item(self,index):
        con=crosssection(False)
        con.object=self.object.Item(index)
        return con
    def rampid(self):
        return self.object.rampid
    def test(self):
        from pyincad import core
        pro=core.incadproject()
        sta=pro.openproject("c:\\incadtest\\test1.fdb")
        id=pro.nametoid('a')
        cset=pro.crossset(id)
        cset.load()
        csec=cset.item(0)
        clin=csec.addline(55)
        csec.save()
        print csec.refid()
        pro.closeproject()
if __name__ == "__main__":
    line1=crossline()
    line1.append(-100,50,1)
    line1.append(109,50,2)
    #print line1.interlimitedslope(1,-1,10,41,1.5,8)
    #print line1.interray(0,0,1,-1)
    print line1.interline(0,0,200,200)

