# -*- coding: utf-8 -*-
import win32com.client
def u(s):
    if isinstance(s, unicode):
        return s
    else:
        return s.decode('utf-8')
class constructions():
    def __init__(self, temp=True, parent=None):
        self.istemp=False
        self.parent=parent
        self.object=None
        if temp:
            self.istemp=True
            self.object=win32com.client.Dispatch("incadopera.constructions")
    def append(self):
        return self.object.Append()
    def insert(self, pos):
        #TODO test
        self.object.Insert(pos)
    def load(self):
        self.object.Load()
    def comment(self,pos):
        return self.object.comment(pos)
    def setcomment(self,pos,newval):
        self.object.Setcomment(pos,newval)
    def count(self):
        return self.object.count
    def empty(self):
        sta=self.object.Empty
        if sta ==0:
            return False
        return True
    def startch(self,pos):
        return self.object.startch(pos)
    def setstartch(self,pos,ch):
        return self.object.Setstartch(pos,ch)
    def endch(self,pos):
        return self.object.EndCH(pos)
    def setendch(self,pos,ch):
        return self.object.SetEndCH(pos,ch)
    def ctype(self,pos):
        return self.object.Type(pos)
    def setctype(self,pos,typ):
        self.object.SetType(pos,typ)
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
    def angle(self, pos):
        return self.object.angle(pos)
    def setangle(self,pos,ang):
        self.object.Setangle(pos,ang)
    def basehigh(self,pos):
        return self.object.BaseHigh(pos)
    def setbasehigh(self,pos,high):
        self.object.SetBaseHigh(pos,high)
    def takeout(self,pos):
        return self.object.TakeOut(pos)
    def settakeout(self,pos,tk):
        self.object.SetTakeOut(pos,tk)
    def spanstr(self,pos):
        return self.object.SpanStr(pos)
    def setspanstr(self,pos,span):
        self.object.SetSpanStr(pos,span)
    def getspans(self,pos):
        return self.object.GetSpans(pos)
    def length(self,pos):
        return self.object.Length(pos)
    def last(self):
        return self.object.Last
    def rampid(self):
        return self.object.rampid
    def setrampid(self,id):
        self.object.rampid=id
    def project(self):
        return self.parent
    def getallitem(self):
        aa=self.object.GetAllItem()
        li=aa[1]
        i=0
        lt=[]
        if aa[0] == 0:
            return lt
        for i in range(0, len(li)/9):
            lt.append((li[9*i], li[9*i+1], li[9*i+2], li[9*i+3], li[9*i+4], li[9*i+5], li[9*i+6], li[9*i+7], li[9*i+8]))
        return lt
    """新增自定义"""
    def list(self):
        li=self.getallitem()
        print "*********************"
        print u"构造物总数%d"%(len(li))
        print u"桩号\t\t类型\t\t交角\t\t孔数孔径\t\t底高\t\t是否扣除土方\t\t起始桩号\t\t终止桩号\t\t备注"
        for pt in li:
            print u"%f\t%d\t%f\t%s\t%f\t%d\t%f\t%f\t%s"%(pt[1], pt[0],pt[2],pt[3],pt[4],pt[5],pt[6],pt[7],pt[8])
    def insert1(self,ch):
        #TODO test
        #根据桩号顺序直接插入，如果是相同桩号，插入在第一个发现的桩号的前面
        pts=self.getallitem()
        i=0
        for pt  in pts:
            if ch<= pt[1]:
                id=self.insert(i)
                self.setch(i,ch)
                return
            i=i+1
        id=self.append()
        self.setch(id,ch)

