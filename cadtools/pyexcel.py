# -*- coding: utf-8 -*-
#versopm 0.001
import array
import win32com.client
class pyexcel:
    theapp=None
    def startexcel(self):
        self.linkstatus=False
        try:
            self.theapp=win32com.client.Dispatch("excel.application")
            self.theapp.Visible=True
            self.linkstatus=True
            return True
        except:
            self.linkstatus=False
            return False
    def linkexcel(self):
        try:
            self.theapp=win32com.client.GetActiveObject("excel.application")
            self.linkstatus=True
            return True
        except:
            self.linkstatus=False
            return False
    def islinked(self):
        if self.theapp == None:
            return False
        return self.linkstatus;
    def activesheet(self):
        return self.theapp.ActiveSheet
    def setformula(self,rang,value):
        sheet=self.theapp.ActiveSheet
        sheet.Range(rang).FormulaR1C1=value
    def setvalue(self,rang,value):
        sheet=self.theapp.ActiveSheet
        sheet.Range(rang).value=value
    def getformula(self,rang):
        sheet=self.theapp.ActiveSheet
        return sheet.Range(rang).FormulaR1C1
    def getvalue(self,rang):
        sheet=self.theapp.ActiveSheet
        return sheet.Range(rang).value
    def getrange(self,rang):
        #example:ex.getrange("A1:B10"),返回列表
        #((u'13/12/2', 1.0), (u'a2', 2.0), (u'a3', 3.0), (u'a4', 4.0), (u'a4', 5.0), (None, None), (None, None), (None, None), (None, None), (None, None))
        sheet=self.theapp.ActiveSheet
        return sheet.Range(rang)
def testexcel():
    ex=pyexcel()
    ex.linkexcel()
    from pyincad.cadtools.pyautocad import pyacad
    acad=pyacad()
    acad.linkautocad()
    xra=ex.getrange("A4:A769")
    yra=ex.getrange("B4:B769")
    pts=[]
    for i in range(0,len(xra)):
        x=xra[i].value
        if x == None:
            x=0
        y=yra[i].value
        if y == None:
            y=0
        pts.append([x,y*100.0,0])
    acad.addpoly(pts)
    print "OK"
if __name__ == "__main__":
    import sys
    ex=pyexcel()
    ex.startexcel()


