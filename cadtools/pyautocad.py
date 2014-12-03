# -*- coding: utf-8 -*-
#versopm 0.001
import array
import comtypes.client
class pyacad:
    acadapp=None
    def startautocad(self):
        self.linkstatus=False
        try:
            self.acadapp=comtypes.client.CreateObject("autocad.application")
            self.acadapp.Visible=True
            self.linkstatus=True
            return True
        except:
            self.linkstatus=False
            return False
    def linkautocad(self):
        try:
            self.acadapp=comtypes.client.GetActiveObject("autocad.application")
            self.linkstatus=True
            return True
        except:
            self.linkstatus=False
            return False
    def islinked(self):
        if self.acadapp == None:
            return False
        return self.linkstatus;
    def autoStart(self):
        try:
            self.StartAutocad()
            return True
        except:
            try:
                self.GetAutocad()
                return True
            except:
                return False
    def sendcommand(self,commandstr):
        acadDoc=self.acadapp.ActiveDocument
        acadDoc.SendCommand(commandstr)
    def regen(self):
        acadDoc=self.acadapp.ActiveDocument
        acadDoc.Regen(1)
    def test(self):
        import win32api,win32con,win32gui
        cap=self.acadapp.Caption
        print cap
        #cap=u"%s"%cap
        hw=win32gui.FindWindow(None,cap)
        print hw
        print self.acadapp.HWND
        print self.acadapp.ActiveDocument.HWND
        hw=0X00010C84
        win32api.SendMessage(hw,win32con.WM_COPYDATA,0,"good")
    def commandesc(self):
        import win32api,win32con
        #cad执行命令前的预处理，等于按esc键，防止正有命令运行
        #acadDoc=self.acadapp.ActiveDocument
        #acadDoc.SendCommand(chr(27))
        #tmp = win32api.MAKELONG(200,200)
        #acadDoc.SendCommand("good")
        #win32api.PostMessage(acadDoc.HWND,win32con.WM_SETTEXT,0,"good")
        #win32api.SendMessage(acadDoc.HWND,win32con.WM_SETTEXT,0,"good")
        ##win32api.SendMessage(self.acadapp.HWND,win32con.WM_KEYDOWN,win32con.VK_ESCAPE)
        #win32api.SendMessage(self.acadapp.HWND,win32con.WM_KEYUP,win32con.VK_ESCAPE)
        #win32api.SendMessage(self.acadapp.HWND,win32con.WM_COPYDATA,0,"X1BX1B")
        pass
    def setvisible(self,val):
        self.acadapp.Visible=val
    def setvariable(self,valname,newval):
        if newval == None:
            return
        acadDoc=self.acadapp.ActiveDocument
        oldval=acadDoc.GetVariable(valname)
        acadDoc.SetVariable(valname,newval)
    def addline3d(self,sx,sy,sz,ex,ey,ez):
        acadDoc=self.acadapp.ActiveDocument
        ms=acadDoc.ModelSpace
        pt1=array.array('d',[sx,sy,sz])
        pt2=array.array('d',[ex,ey,ez])
        ms.AddLine(pt1,pt2)
    def addline2d(self,sx,sy,ex,ey):
        acadDoc=self.acadapp.ActiveDocument
        ms=acadDoc.ModelSpace
        pt1=array.array('d',[sx,sy,0])
        pt2=array.array('d',[ex,ey,0])
        ms.AddLine(pt1,pt2)
    def addtext(self,x,y,con,high=4,ang=0):
        acadDoc=self.acadapp.ActiveDocument
        ms=acadDoc.ModelSpace
        pt1=array.array('d',[x,y,0])
        textobj=ms.AddText(con,pt1,high)
        textobj.Rotate(pt1,ang)
    def addpoint(self,x,y,z=0):
        acadDoc=self.acadapp.ActiveDocument
        ms=acadDoc.ModelSpace
        pt1=array.array('d',[x,y,z])
        ms.AddPoint(pt1)
    def addpoly(self,pointarray):
        #pointarray =([x,y,z],[x,y,z])z可以不输入
        pts=[]
        for pt in pointarray:
            cc=len(pt)
            x=pt[0]
            y=pt[1]
            z=0
            if cc == 3:
                z=pt[2]
            pts.append(x)
            pts.append(y)
            pts.append(z)
        acadDoc=self.acadapp.ActiveDocument
        ms=acadDoc.ModelSpace
        pt1=array.array('d',pts)
        ms.AddPolyline(pt1)
    def addarc(self,cx,cy,r,sang,eang):
        acadDoc=self.acadapp.ActiveDocument
        ms=acadDoc.ModelSpace
        cpt=array.array('d',[cx,cy,0])
        ms.AddArc(cpt,r,sang,eang)

if __name__ == "__main__":
    import sys
    acad=pyacad()
    acad.linkautocad()
    #acad.sendcommand("_line 10,10,0 100,100,0  ") #这是一个直接发送命令的做法
    #acad.test()
    #acad.addpoly(([10,10],[100,200,5]))
    print "good"




