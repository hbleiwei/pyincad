# -*- coding: utf-8 -*-
import win32com.client
def u(s):
    if isinstance(s, unicode):
        return s
    else:
        return s.decode('utf-8')
class crosswidth():
    def __init__(self, temp=True, parent=None):
        self.istemp=False
        self.parent=parent
        self.object=None
        if temp:
            self.istemp=True
            self.object=win32com.client.Dispatch("incadopera.crosswidth")
    def append(self, ch, slp,typ=0):
        return self.object.Append(ch, slp,typ)
    def insert(self, pos, ch, slp,typ=0):
        self.object.Insert(pos, ch, slp,typ)
    def load(self):
        #TODO test
        self.object.Load()
    def id(self):
        return self.object.id
    def setid(self, id):
        self.object.id=id
    def comment(self):
        return self.object.comment
    def count(self):
        return self.object.count
    def empty(self):
        sta=self.object.Empty
        if sta ==0:
            return False
        return True
    def startch(self):
        return self.object.startch
    def endch(self):
        return self.object.EndCH
    def modifycomment(self,newval):
        self.object.ModifyComment(newval)
    def ptwidth(self, pos):
        return self.object.PTWidth(pos)
    def setptwidth(self, pos, wid):
        self.object.SetPTWidth(pos,wid)
    def pttype(self,pos):
        #取得横坡变化类型
        return self.object.Type(pos)
    def setpttype(self,pos,typ):
        self.object.SetType(pos,typ)
    def remove(self,pos):
        self.object.Remove(pos)
    def removeall(self):
        self.object.RemoveAll()
    def save(self):
        self.object.Save()
    def item(self,pos):
        #TODO 测试结果错误，可能需要修改C源代码
        return self.object.Item(pos)
    def setitem(self, pos, ch, wid,typ=0):
        #TODO 测试结果错误，可能需要修改C源代码
        self.object.SetItem(pos, (ch,wid,typ))
    def setch(self, pos, ch):
        self.object.Setch(pos, ch)
    def ch(self, pos):
        return self.object.ch(pos)
    def width(self, ch):
        return self.object.Width(ch)
    def getchlist(self):
        pt=[]
        for i in range(0,self.count()):
            pt.append(self.ch(i))
        return pt
    def getallitem(self):
        aa=self.object.GetAllItem()
        li=aa[1]
        i=0
        lt=[]
        if aa[0] == 0:
            return lt
        for i in range(0, len(li)/3):
            lt.append((li[3*i], li[3*i+1], li[3*i+2]))
        return lt
    def last(self):
        return self.object.Last
    """新增自定义"""
    def list(self):
        li=self.getallitem()
        print "*********************"
        print u"宽度变化点总数%d"%(len(li))
        print u"桩号\t\t宽度\t\t渐变类型"
        for pt in li:
            print u"%f\t%f\t%f"%(pt[0], pt[1],pt[2])
    def insert1(self,ch, slp,typ=0):
        #根据桩号顺序直接插入，如果是相同桩号，插入在第一个发现的桩号的前面
        pts=self.getallitem()
        i=0
        for pt  in pts:
            if ch<= pt[0]:
                self.insert(i, ch, slp,typ)
                return
            i=i+1
        self.append(ch, slp,typ )
    def project(self):
        return self.parent
    def rampid(self):
        return self.object.rampid
    def setrampid(self,id):
        self.object.rampid=id
