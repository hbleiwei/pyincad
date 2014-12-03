# -*- coding: utf-8 -*-
# 版本0.0002
import win32com.client
def u(s):
    if isinstance(s, unicode):
        return s
    else:
        return s.decode('utf-8')
class vertical():
    def __init__(self, temp=True, parent=None):
        #ok
        self.istemp=False
        self.parent=parent
        self.object=None
        if temp:
            self.istemp=True
            self.object=win32com.client.Dispatch("incadopera.vertical")
    def id(self):
        #ok
        if self.istemp:
            return -1
        return self.object.id
    def load(self):
        #ok
        if self.istemp:
            return
        self.object.Load()
    def arclength(self, index):
        #ok
        return self.object.ArcLength(index) #注意修改原始的com，arclength有错误
    def betweenline(self, index):
        #ok
        return self.object.BetweenLine(index)
    def ch(self, index):
        #ok
        return self.object.ch(index)
    def setch(self, index, ch):
        #ok
        self.object.Setch(index, ch)
    def comment(self):
        #ok
        return self.object.comment
    def count(self):
        #ok
        return self.object.count
    def empty(self):
        #ok
        return self.object.Empty
    def high(self, ch):
        #ok
        return self.object.high(ch)
    def pthigh(self, index):
        #ok
        return self.object.PTHigh(index)
    def setpthigh(self, index, high):
        #ok
        return self.object.SetPTHigh(index, high)
    def radius(self, index):
        #ok
        return self.object.Radius(index)
    def setradius(self, index, r):
        #ok
        self.object.SetRadius(index, r)
    def tlength(self, index):
        #ok
        return self.object.TLength(index)
    def w(self, index):
        #ok
        return self.object.W(index)
    def remove(self, index):
        #ok
        self.object.Remove(index)
    def removeall(self):
        #ok
        self.object.RemoveAll()
    def save(self):
        #ok
        if self.istemp:
            return
        self.object.Save()
    def check(self):
        self.object.Check()
    def cal(self):
        #ok
        return self.object.Cal()
    def append(self, ch, high, r):
        #ok
        self.object.Append(ch, high, r)
    def insert(self, pos, ch, high, r):
        #在pos之前插入
        self.object.Insert(pos, ch, high, r)
    def linkedradius(self, index):
        return self.object.LinkedRadius(index)
    def index(self, ch):
        return self.object.Index(ch)
    def startch(self):
        #ok
        return self.object.startch
    def endch(self):
        #ok
        return self.object.EndCH
    def nearpoint(self, x, y, dist):
        self.object.NearPoint(x, y, dist)
    def testradius(self, pos, x, y):
        self.object.TestRadius(pos, x, y)
    def preslope(self, index):
        #ok
        return self.object.PreSlope(index)
    def nextslope(self, index):
        #ok
        return self.object.NextSlope(index)
    def calradiusfromtlength(self, index, tlen):
        return self.object.CalRadiusFromTLength(index, tlen)
    def last(self):
        return self.object.Last
    def project(self):
        return self.parent
    def rampid(self):
        #ok
        return self.object.rampid
    def modifycomment(self, comment):
        #ok
        self.object.ModifyComment(u(comment))
    def calradiusfromarclength(self, pos, arclen):
        return self.object.CalRadiusFromArcLength(index, tlen)
        ########################新增
    def insert1(self, ch, high, r):
        #ok
        #按照桩号顺序插入，如果遇到相同桩号，则在相同桩号之前
        pos=-1
        i=0
        for i in range(0, self.count()):
            chs=self.ch(i)
            if ch <= chs:
                pos=i
                break
        if pos==-1:
            self.append(ch, high, r)
        else:
            self.insert(pos, ch, high, r)
    def getitems(self):
        #ok
        pts=[]
        if self.count() != 0:
            for i in range(0, self.count()):
                pts.append((self.ch(i), self.pthigh(i), self.radius(i)))
        return pts
    def setitems(self, pts):
        #ok
        #检查
        if len(pts) == 0:
            self.removeall()
            return
        for pt in pts:
            if(len(pt) < 3):
                print u"错误，数据最小为3个,ch,high,r"
        self.removeall()
        for pt in pts:
            self.append(pt[0], pt[1], pt[2])
    def list(self):
        #ok
        print ""
        print "######################"
        print u"匝道id=<%d>,纵断面id=<%d>，备注:'%s'"%(self.rampid(), self.id(), self.comment())
        pts=self.getitems()
        print  u"id   ch   high    r"
        i=0
        for pt in pts:
            print i, pt[0], pt[1], pt[2]
            i=i+1
        print "######################"
    def tempvertical(self,index):
        vv=self.object.tempvertical(index)
        v1=vv[0]
        va=vertical()
        va.object=v1
        return (va,vv[1])
class verticalcontrolpoints():
    def __init__(self, temp=True, parent=None):
        self.istemp=False
        self.parent=parent
        self.object=None
        if temp:
            self.istemp=True
            self.object=win32com.client.Dispatch("incadopera.VerticalControlPoints")
    def append(self):
        return self.object.Append()
    def insert(self,pos):
        self.object.Insert(pos)
    def load(self):
        self.object.Load()
    def comment(self,pos):
        return self.object.comment(pos)
    def setcomment(self,pos,newval):
        self.object.Setcomment(pos,newval)
    def maxhigh(self,pos):
        return self.object.MaxHigh(pos)
    def setmaxhigh(self,pos,high):
        self.object.SetMaxHigh(pos,high)
    def minhigh(self,pos):
        return self.object.MinHigh(pos)
    def setminhigh(self,pos,high):
        self.object.SetMinHigh(pos,high)
    def permit(self,pos):
        return self.object.Permit(pos)
    def setpermit(self,pos,r):
        self.object.SetPermit(pos,r)
    def pointtype(self,pos):
        return self.object.pointType(pos)
    def setpointtype(self,pos,typ):
        self.object.SetpointType(pos,typ)
    def checkpt(self,pos,high):
        #TODO test
        return self.object.CheckPT(pos,high)
    def count(self):
        return self.object.count
    def empty(self):
        sta=self.object.Empty
        if sta ==0:
            return False
        return True
    def remove(self,pos):
        self.object.Remove(pos)
    def removeall(self):
        self.object.RemoveAll()
    def save(self):
        self.object.Save()
    def setch(self, pos, ch):
        self.object.Setch(pos, ch)
    def ch(self, pos):
        return self.object.ch(pos)
    def getallitem(self):
        aa=self.object.GetAllItem()
        li=aa[1]
        i=0
        lt=[]
        if aa[0] == 0:
            return lt
        for i in range(0, len(li)/6):
            lt.append((li[6*i], li[6*i+1], li[6*i+2], li[6*i+3], li[6*i+4], li[6*i+5]))
        return lt
    def last(self):
        return self.object.Last
    def project(self):
        return self.parent
    def rampid(self):
        return self.object.rampid
    def setrampid(self,id):
        self.object.rampid=id
    """新增自定义"""
    def list(self):
        #TODO 修改
        li=self.getallitem()
        print "*********************"
        print u"纵断面控制点总数%d"%(len(li))
        print u"桩号\t\t类型\t\t最大标高\t\t最小标高\t\t精度\t\t备注"
        for pt in li:
            print u"%f\t%d\t%f\t%f\t%f\t%s"%(pt[1], pt[0],pt[2],pt[3],pt[4],pt[5])
    def insert1(self,ch):
        #根据桩号顺序直接插入，如果是相同桩号，插入在第一个发现的桩号的前面
        pts=self.getallitem()
        i=0
        for pt  in pts:
            if ch<= pt[1]:
                self.insert(i)
                self.setch(i,ch)
                return
            i=i+1
        pos=self.append()
        self.setch(pos,ch)
class ground():
    def __init__(self, temp=True, parent=None):
        #ok
        self.istemp=False
        self.parent=parent
        self.object=None
        if temp:
            self.istemp=True
            self.object=win32com.client.Dispatch("incadopera.verticalground")
    def append(self, ch, high):
        #ok
        return self.object.Append(ch, high)
    def insert(self, pos, ch, high):
        #ok
        self.object.Insert(pos, ch, high)
    def load(self):
        #ok
        self.object.Load()
    def id(self):
        #ok
        return self.object.id
    def setid(self, id):
        #ok
        self.object.id=id
    def comment(self):
        #ok
        return self.object.comment
    def count(self):
        #ok
        return self.object.count
    def empty(self):
        #ok
        return self.object.Empty
    def startch(self):
        #ok
        return self.object.startch
    def endch(self):
        #ok
        return self.object.EndCH
    def modifycomment(self,newval):
        #ok
        self.object.ModifyComment(newval)
    def pthigh(self, pos):
        #Ok
        return self.object.PTHigh(pos)
    def setpthigh(self, pos, high):
        #ok
        self.object.SetPTHigh(pos, high)
    def remove(self,pos):
        #ok
        self.object.Remove(pos)
    def removeall(self):
        #ok
        self.object.RemoveAll()
    def save(self):
        #ok
        self.object.Save()
    def item(self,pos):
        #ok
        return self.object.Item(pos)
    def setitem(self, pos, ch, high):
        #ok
        self.object.SetItem(pos, (ch, high))
    def setch(self, pos, ch):
        #ok
        self.object.Setch(pos, ch)
    def ch(self, pos):
        #ok
        return self.object.ch(pos)
    def high(self, ch):
        #ok
        return self.object.high(ch)
    def getallitem(self):
        #ok
        aa=self.object.GetAllItem()
        li=aa[1]
        i=0
        lt=[]
        for i in range(0, len(li)/2):
            lt.append((li[2*i], li[2*i+1]))
        return lt
    def last(self):
        return self.object.Last
    """新增自定义"""
    def list(self):
        #ok
        li=self.getallitem()
        print "*********************"
        print u"交点总数%d"%(len(li))
        print u"桩号\t\t高程"
        for pt in li:
            print u"%f\t%f"%(pt[0], pt[1])
    def insert1(self,ch, high):
        #ok
        #根据桩号顺序直接插入，如果是相同桩号，插入在第一个发现的桩号的前面
        pts=self.getallitem()
        i=0
        for pt  in pts:
            if ch<= pt[0]:
                self.insert(i, ch, high)
                return
            i=i+1
        self.append(ch, high)
    def project(self):
        #ok
        return self.parent
    def rampid(self):
        #ok
        return self.object.rampid
    def setrampid(self,id):
        #ok
        self.object.rampid=id
def calptfromslp(prech,prehigh,preslp,nextch,nexthigh,nextslp):
    #固定前坡和后坡计算桩号和高程
    #prech，prehigh,前一交点的桩号和高程
    #nextch,nexthigh,后一交点的桩号和高程
    #preslp，本交点（待计算交点）的前坡
    #nextslp,本交点（待计算交点）的后坡
    from pyincad.mmath import geo
    if preslp == nextslp:
        #坡度平行，没有交点
        return None
    dx=100.
    dy1=preslp*dx
    dy2=nextslp*dx
    rpt=geo.lineinters(prech,prehigh,dx,dy1,nextch,nexthigh,dx,dy2)
    return rpt
if __name__ == "__main__":
    #print calptfromslp(-165.9202,2088.9133,-0.01,138.7101,2099.2136,0.05)
    pa=vertical()
    pa.append(100,10,0)
    pa.append(200,15,100)
    pa.append(300,10,0)
    print pa.tempvertical(1)


