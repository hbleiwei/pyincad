# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#2014.6.8
#标准的mgraph2d
__version__ = 0.002

"""
Module implementing mgraph2d.
"""
import PyQt4,  PyQt4.QtGui, sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4 import QtGui
from pyincad.mmath import geo
import math
#QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
class graphbase:
    def __init__(self):
        self.objname="graphbase"
        self.layername='0'
        self.objectbox=(0,0,0,0) #图形实体框
        self.boxcaled=False
        self.zoomenable=True #如果此值为False,该实体不参加zoom
        self.objpen=QPen(Qt.black)
        self.objbrush=QBrush(Qt.SolidPattern)
        self.Antialiasing=True
        self.mainpoint=[] #主点，主点的结构为pt=(x,y,type)其中type为类型标记,type也可以没有，但至少要有x，y
    def setcolor(self,color):
        self.objpen.setColor(color)
    def setwidth(self,wid):
        self.objpen.setWidthF(wid)
    def setstyle(self,style):
        self.objpen.setStyle(style)
    def calbox(self):
        pass
    def show(self, painter):
        raise NotImplementedError
    def pickmainpoint(self,x,y,dist):
        #选择与点x，y距离小于dist的点
        rpts=[]
        dist=abs(dist)
        for pt in self.mainpoint:
            dx=x-pt[0]
            dy=y-pt[1]
            di=math.sqrt(dx*dy+dy*dy)
            if (di <= dist ):
                rpts.append(pt)
        return rpts
    def showmainpoint(self,painter):
        #显示主点
        trans=painter.worldTransform()
        bsta=painter.worldMatrixEnabled()
        painter.setWorldMatrixEnabled(False)
        oldpen=painter.pen()
        painter.setPen(Qt.red)
        oldbrush=painter.brush()
        painter.setBrush(QBrush(Qt.magenta,Qt.SolidPattern))
        for pt in self.mainpoint:
            x=pt[0]
            y=pt[1]
            typ=pt[2]
            rpt=trans.map(float(x),float(y))#世界坐标转换为屏幕坐标
            #绘制点
            dx=4
            painter.drawEllipse(QPointF(rpt[0],rpt[1]),dx,dx)
        painter.setWorldMatrixEnabled(bsta)
        painter.setPen(oldpen)
        painter.setBrush(oldbrush)
class lineobject(graphbase):
    def __init__(self, sx, sy, ex, ey):
        graphbase.__init__(self)
        self.objname="lineobject"
        self.sx=sx
        self.sy=sy
        self.ex=ex
        self.ey=ey
        self.calbox()
    def calbox(self):
        minx=min(self.sx, self.ex)
        miny=min(self.sy, self.ey)
        maxx=max(self.sx, self.ex)
        maxy=max(self.sy, self.ey)
        self.objectbox=(minx,miny,maxx,maxy)
        self.boxcaled=True
    def show(self, painter):
        oldpen=painter.pen()
        painter.setPen(self.objpen)
        painter.setRenderHint(PyQt4.QtGui.QPainter.Antialiasing,self.Antialiasing)
        painter.drawLine(QtCore.QLineF(self.sx, self.sy, self.ex, self.ey))
        painter.setPen(oldpen)
class staticyline(graphbase):
    #绘制线的y坐标为屏幕坐标，x坐标为世界坐标
    def __init__(self, sx, sy, ex, ey):
        graphbase.__init__(self)
        self.objname="staticyline"
        self.sx=sx
        self.sy=sy
        self.ex=ex
        self.ey=ey
        self.calbox()
    def calbox(self):
        minx=min(self.sx, self.ex)
        miny=min(self.sy, self.ey)
        maxx=max(self.sx, self.ex)
        maxy=max(self.sy, self.ey)
        self.objectbox=(minx,miny,maxx,maxy)
        self.boxcaled=True
    def show(self, painter):
        oldpen=painter.pen()
        painter.setPen(self.objpen)
        painter.drawLine(QtCore.QLineF(self.sx, self.sy, self.ex, self.ey))
        painter.setPen(oldpen)
class staticxline(graphbase):
    #绘制线的x坐标为屏幕坐标，y坐标为世界坐标
    def __init__(self, sx, sy, ex, ey):
        graphbase.__init__(self)
        self.objname="staticxline"
        self.sx=sx
        self.sy=sy
        self.ex=ex
        self.ey=ey
        self.calbox()
        self.sign=1
    def calbox(self):
        minx=min(self.sx, self.ex)
        miny=min(self.sy, self.ey)
        maxx=max(self.sx, self.ex)
        maxy=max(self.sy, self.ey)
        self.objectbox=(minx,miny,maxx,maxy)
        self.boxcaled=True
    def show(self, painter):
        oldpen=painter.pen()
        painter.setPen(self.objpen)
        painter.setRenderHint(PyQt4.QtGui.QPainter.Antialiasing,self.Antialiasing)
        painter.drawLine(QtCore.QLineF(self.sx, self.sy, self.ex, self.ey))
        painter.setPen(oldpen)
class plineobject(graphbase):
    def __init__(self, pts):
        graphbase.__init__(self)
        self.objname="plineobject"
        self.setpoints(pts)
    def setpoints(self,pts):
        self.pointarray=[]
        for pt in pts:
            self.pointarray.append(QtCore.QPointF(pt[0], pt[1]))
        if len(pts) > 0:
            self.calbox()
    def calbox(self):
        if len(self.pointarray) == 0:
            self.zoomenable=False
        else:
            self.zoomenable=True
        minx=maxx=self.pointarray[0].x()
        miny=maxy=self.pointarray[0].y()
        self.mainpoint=[]
        for pt in self.pointarray:
            minx=min(minx, pt.x())
            miny=min(miny, pt.y())
            maxx=max(maxx, pt.x())
            maxy=max(maxy, pt.y())
        self.objectbox=(minx,miny,maxx,maxy)
        self.boxcaled=True
    def show(self, painter):
        if len(self.pointarray) == 0:
            return
        oldpen=painter.pen()
        painter.setPen(self.objpen)
        painter.setRenderHint(PyQt4.QtGui.QPainter.Antialiasing,self.Antialiasing)
        painter.drawPolyline(QtGui.QPolygonF(self.pointarray))
        painter.setPen(oldpen)
class textobject(graphbase):
    def __init__(self, x, y,textcon):
        graphbase.__init__(self)
        self.objname="textobject"
        self.x=x
        self.y=y
        self.text=textcon
        self.rectwidth=0
        self.recthigh=0
        self.angle=0
        self.flag=Qt.AlignLeft|Qt.AlignTop
        self.basepointoffsetx=0
        self.basepointoffsety=0
        self.calbox()
    def calbox(self):
        minx=self.x
        miny=self.y
        maxx=self.x
        maxy=self.y
        self.objectbox=(minx,miny,maxx,maxy)
        self.boxcaled=True
    def setrect(self, width, high):
        self.rectwidth=width
        self.recthigh=high
    def setAngle(self, ang):
        self.angle=ang
    def setflag(self, flag):
        self.flag=flag
    def show(self, painter):
        painter.save()
        oldpen=painter.pen()
        painter.setPen(self.objpen)
        t1=painter.combinedTransform()
        pt=t1.map(self.x, self.y) #屏幕坐标
        pt2=t1.map(self.x+10.0*math.cos(self.angle),self.y+10.0*math.sin(self.angle))
        az=geo.getaz(pt2[0]-pt[0],pt2[1]-pt[1])/math.pi*180.
        painter.resetTransform()
        #painter.setWorldMatrixEnabled(False)
        #painter.setViewTransformEnabled(False)
        painter.setRenderHint(PyQt4.QtGui.QPainter.Antialiasing,self.Antialiasing)
        #painter.translate(pt[0],pt[1]) #坐标原点平移
        painter.translate(pt[0], pt[1]) #坐标原点平移
        painter.rotate(az)
        painter.translate(self.basepointoffsetx,self.basepointoffsety)
        if self.rectwidth ==0 and self.recthigh==0:
            painter.drawText(0,0, self.text)
        else:
            painter.drawText(0,0,self.rectwidth,self.recthigh,self.flag, self.text)
        painter.setViewTransformEnabled(True)
        painter.setWorldMatrixEnabled(True)
        painter.setPen(oldpen)
        painter.restore()
class graphlayer:
    def __init__(self,lname='NULL'):
        self.layername=lname
        self.visible=True
class graphcommand(QObject):
    """图形操作命令"""
    def __init__(self, name, pos=(0, 0)):
        super(graphcommand,self).__init__()
        self.name=name
        self.pos=pos #保存一组坐标信息
        self.status=0 # 可以作为计数的状态量
    def _processcommand(self, parent,eventname, pos):
        #对命令进行相应
        pass
class command_panwindow(graphcommand):
    #命令：取得点
    def __init__(self,status=1,pos=(0, 0)):
        #如果status = 0，那么选择开始点，否则以pos作为开始点
        super(command_panwindow,self).__init__("panwindow",pos)
        if status == 0:
            self.status=0
            self.startpos=None
        else :
            self.status=1
            self.startpos=pos
    def _processcommand(self,parent, eventname, pos):
        if eventname == "rightmousepress":
            if self.status == 0:
                self.status=1
                self.startpos=pos
        elif eventname == "mousemove":
            pos1=self.startpos
            pos2=pos
            pt1=parent.screentoworld(pos1[0], pos1[1])
            pt2=parent.screentoworld(pos2[0], pos2[1])
            parent._clearmouseview()
            parent._drawrubberline(pt1,pt2)
        elif eventname == "mouserelease":
            pos1=self.startpos
            pos2=pos
            pt1=parent.screentoworld(pos1[0], pos1[1])
            pt2=parent.screentoworld(pos2[0], pos2[1])
            dx=pt2[0]-pt1[0]
            dy=pt2[1]-pt1[1]
            parent.c_panwindow(dx, dy)
            parent._clearmouseview()
            parent.update()
            return True
        return False
class command_zoomwindow(graphcommand):
    #命令：窗口放大
    def __init__(self, pos=(0, 0)):
        super(command_zoomwindow,self).__init__("zoomwindow",pos)
        self.pos=pos
        self.status=0
    def _processcommand(self,parent, eventname, pos):
        if eventname == "leftmousepress":
            if self.status == 0:
                self.status=1
                self.pos=pos
                parent.update()
            else:
                parent.mousestatus=0
                pt1=self.pos
                pt2=pos
                pt1=parent.screentoworld(pt1[0], pt1[1])
                pt2=parent.screentoworld(pt2[0], pt2[1])
                box=(pt1[0], pt1[1], pt2[0], pt2[1])
                parent.c_zoomwindow(box)
                parent._clearmouseview()
                parent.update()
                return True
        elif eventname == "mousemove":
            if self.status == 1:
                pt1=self.pos
                pt2=pos
                pt1=parent.screentoworld(pt1[0], pt1[1])
                pt2=parent.screentoworld(pt2[0], pt2[1])
                parent._clearmouseview()
                parent._drawrubberrect(pt1,pt2)
        return False
class command_getpoint(graphcommand):
    #命令：取得点
    def __init__(self, pos=None):
        #如果status=0,鼠标左键单点后级返回，如果status=1,则以pos为起始点，取得相对点的位置
        super(command_getpoint,self).__init__("getpoint",pos)
        if (pos):
            self.status=1
        else:
            self.status=0
        self.pos=pos
        self.resultpos=None
    def _processcommand(self,parent, eventname, pos):
        if eventname == "leftmousepress":
                self.resultpos=pos
                parent.mousestatus=0
                pt=parent.screentoworld(pos[0],pos[1])
                parent._pointstatus.status=1
                parent._pointstatus.x=pt[0]
                parent._pointstatus.y=pt[1]
                if self.status == 1:
                    parent._clearmouseview()
                    parent.update()
                return True
        elif eventname == "mousemove":
            if self.status == 1:
                pt2=parent.screentoworld(pos[0],pos[1])
                parent._clearmouseview()
                parent._drawrubberline(self.pos,pt2)
        elif eventname == "keyrelease":
            if pos == 73: #"i"
                #如果是鼠标按键，且按键等于"i",则弹出对话框进行选择坐标点
                #TODO  这个方法还没写完
                from getpointdia import getpointdia
                dia=getpointdia()
                dia.setModal(True)
                dia.exec_()
        return False #未经过处理
class graphcolor():
    """
    本类保存graph图像的颜色属性
    """
    def __init__(self):
        self.settoblack()
    def settoblack(self):
        #设置为'black'
        self.configname='black' #颜色组合名称
        self.background=QColor(51,51,51) #背景
        self.crossline=QColor(212,197,93) #十字线颜色
    def settocyan(self):
        self.configname='cyan' #颜色组合名称
        self.background=QColor(PyQt4.QtCore.Qt.cyan) #背景
        self.crossline=QColor(PyQt4.QtCore.Qt.white) #十字线颜色
class graphobjectsopera:
    """
    图形数据的操作
    """
    def __init__(self):
        #初始化图形数据
        self.layers={}        #图层数据
        self.graphobject=[]   #绘图数据
        self.modified=False   #是否经过了修改，如果是，则需要进行绘图
        #默认数据
        self.layers['0']=graphlayer()  #新建图层0
        self._currentlayer='0'         #当前层设为0
        self.activepen=Qt.black        #当前绘图笔
    def _getextendbox(self):
        """取得显示的最大外框"""
        first=True
        minx=miny=maxx=maxy=0
        for ob in self.graphobject:
            ln=ob.layername
            if self.layers[ln].visible :
                if ob.zoomenable:
                    if not ob.boxcaled:
                        ob.calbox()
                    if ob.boxcaled:
                        #print ob.objname
                        #print ob.objectbox
                        if first:
                            minx=ob.objectbox[0]
                            miny=ob.objectbox[1]
                            maxx=ob.objectbox[2]
                            maxy=ob.objectbox[3]
                            first=False
                        else:
                            minx=min(ob.objectbox[0], minx)
                            miny=min(ob.objectbox[1], miny)
                            maxx=max(ob.objectbox[2], maxx)
                            maxy=max(ob.objectbox[3], maxy)
        return (minx, miny, maxx, maxy)
    def newobject(self, obj):
        """新建对象，使得对象数据符合当前激活数据"""
        #按照当前绘图层绘制对象
        obj.objpen=self.activepen
        obj.layername=self._currentlayer
        self.modified=True
        return obj
    def appendobject(self, ob):
        #添加实体对象
        self.graphobject.append(ob)
        self.modified=True
    def clearall(self):
        #删除所有数据,修改20130616
        self.layers={}
        self.layers['0']=graphlayer()
        self._currentlayer='0'
        self.graphobject=[]
        self.modified=True
    def clearlayer(self,layername):
        #清除图层的数据
        if not (self.havelayer(layername)):
            return
        cc=len(self.graphobject)
        if cc ==0 :
            return
        for i in range(cc-1, -1, -1):
            #逆序删除
            if self.graphobject[i].layername == layername:
                del  self.graphobject[i]
        self.modified=True
    def havelayer(self, layername):
        #是否存在指定图层
        havel=False
        return self.layers.has_key(layername)
    def newlayer(self, layername):
        #新建图层
        """新建图层"""
        if self.havelayer(layername):
            return
        self.layers[layername]=graphlayer(layername)
        self.modified=True
    def islayervisible(self,layername):
        if not self.havelayer(layername):
            return False
        if self.layers[layername].visible:
            return True
        return False
    def setlayervisible(self,layername,val):
        if not self.havelayer(layername):
            return
        if self.layers[layername].visible == val:
            return
        else:
            self.layers[layername].visible=val
            self.modified=True
    def currentlayer(self):
        #取得当前层
        return self._currentlayer
    def setcurrentlayer(self, lnname):
        #设置当前绘图层
        if self.layers.has_key(lnname):
            self._currentlayer=lnname
            return True
        else:
            return False
    def clearobjectlayers(self):
        """清除所有可见实体图层的图像数据，即将图像清空"""
        for k in self.layers.keys():
            if self.layers[k].visible :
                self.layers[k].fresh()
        self.modified=True
    def freshbyobjects(self,pixpainter,showmainpoint=False):
        """ 按照图形数据重新绘制"""
        for ob in self.graphobject:
            if self.islayervisible(ob.layername):
                ob.show(pixpainter)
                if showmainpoint:
                    ob.showmainpoint(pixpainter)
    def freshbylayers(self,pixpainter,showmainpoint=False):
        """ 按照图层顺序重新绘制"""
        #TODO 今后要建立按照图层关系的对象索引
        for k in self.layers.keys():
            if self.layers[k].visible :
                for ob in self.graphobject:
                    if ob.layername == k:
                        ob.show(pixpainter)
                        if showmainpoint:
                            ob.showmainpoint(pixpainter)
class mgraph2dbase(QWidget):
    """
    图形绘制的基本操作
    """
    def __init__(self, parent = None, scalexy=1.0):
        """scalexy,y/x的比例"""
        super(mgraph2dbase,self).__init__(parent)
        self.scalexy=scalexy
        self.graphdata=graphobjectsopera()
        self.tempdata=graphobjectsopera() #临时对象
        self.setAttribute(Qt.WA_PaintOnScreen,True) #关闭双缓冲绘图
        self.setAttribute(Qt.WA_OpaquePaintEvent,True) #NoBackground
        self.setAutoFillBackground(False)
        self.setMouseTracking(True)
        self.setCursor(PyQt4.QtGui.QCursor(PyQt4.QtCore.Qt.BlankCursor)) #隐藏鼠标
        self.viewpix=PyQt4.QtGui.QPixmap(self.width(), self.height()) #自行定义双缓冲使用的绘图图像
        self.tempviewpix=PyQt4.QtGui.QPixmap(self.width(), self.height()) #自行定义双缓冲使用的临时绘图图像
        self.mouseviewpix=PyQt4.QtGui.QPixmap(self.width(), self.height()) #鼠标绘图
        self.prewindowsize=[self.width(),self.height()] #前一个窗口，用来判断是否需要重新绘制图形
        self.pretransform=PyQt4.QtGui.QTransform() #前一个显示矩阵，用来判断是否需要重新绘制图形
        self.showmainpoint=False #是否显示主点
        self.firstshow=True
        self.mousepos=[0,0,0,0] #记录鼠标位置，0为现在x，1为现在y,2为原有x,3为原有y
        self._initviewmatrix(scalexy)
        #背景等颜色设置
        self._graphcfg=graphcolor()
        self._graphcfg.settocyan()
    def _initviewmatrix(self,scalexy):
        #初始化显示矩阵self.transform1为世界坐标向屏幕坐标的转化矩阵
        self.transform1=PyQt4.QtGui.QTransform()
        self._scalewindow1(1.0,-1.0)
        pt=self.screentoworld(0,self.height())
        self._panwindow(0,pt[1])
        self._scalewindow1(1,self.scalexy)
    def _scalewindow(self, bx, by, sc):
        """比例放大缩小窗口，bx，by为鼠标位置的屏幕坐标"""
        if sc == 0:
            return
        sc=abs(sc)
        #首先取得bx，by的世界坐标
        pt=self.screentoworld(bx,by)
        #坐标系平移至0
        self._panwindow(pt[0],pt[1])
        self._scalewindow1(sc,sc)
        self._panwindow(-pt[0],-pt[1])
    def _scalewindow1(self,sx,sy):
        if sx == 0:
            return
        if sy == 0:
            return
        self.transform1.scale(sx,sy)
    def _panwindow(self,dx,dy):
        st=QTransform()
        st.translate(dx,dy)
        self.transform1=st*self.transform1
    def screentoworld(self,bx, by):
        """屏幕坐标向世界坐标转换"""
        t1=self.transform1
        t2=t1.inverted()[0]
        pt=t2.map(float(bx),float(by))
        return pt
    def worldtoscreen(self, x, y):
        t1=self.transform1
        pt=t1.map(float(x),float(y))
        return pt
    def c_zoomextend(self):
        """窗口放至最大"""
        box=self.graphdata._getextendbox()
        self.c_zoomwindow(box)
    def c_panwindow(self, dx, dy):
        """平移坐标系"""
        self._panwindow(dx,dy)
    def c_zoomcenter(self, x, y):
        """移动显示至指定中心"""
        rx=self.width()
        ry=self.height()
        mx=rx/2.0
        my=ry/2.0
        cc=self.screentoworld(mx,my)
        dx=cc[0]-x
        dy=cc[1]-y
        self._panwindow(dx,dy)
        return True
    def c_zoomwindow(self, box):
        """放大窗口，其中box的组成为minx,miny,maxx,maxy为世界坐标系的对角坐标"""
        lx=box[0]
        ly=box[1]
        rx=box[2]
        ry=box[3]
        c1=self.worldtoscreen(lx,ly)
        c2=self.worldtoscreen(rx,ry)
        dw=abs(float(c2[0]-c1[0]))
        dh=abs(float(c2[1]-c1[1]))
        scx=0
        if dw !=0:
            scx=float(self.width())/float((dw))
        scy=0
        if dh !=0:
            scy=float(self.height())/float((dh))
        thesc=1
        if scx == scy == 0:
            thesc=1
        elif scx == 0:
            thesc=scy
        elif scy == 0:
            thesc=scx
        else:
            thesc=min(scx, scy)
        if thesc != 1:
            self._scalewindow(0,0,thesc)
        mcx=(box[0]+box[2])/2.0
        mcy=(box[1]+box[3])/2.0
        self.c_zoomcenter(mcx, mcy)
    def freshobjects(self):
        """ 重新绘制各个图层"""
        self.viewpix.fill(self._graphcfg.background)
        pixpainter=PyQt4.QtGui.QPainter(self.viewpix)
        pixpainter.setWindow(0, 0, self.width(), self.height())
        pixpainter.setWorldMatrixEnabled(True)
        pixpainter.setWorldTransform(self.transform1)
        self.graphdata.freshbyobjects(pixpainter) #按照对象绘制
        self.graphdata.modified=False
        pixpainter.end()
    def freshtempobjects(self):
        #重新绘制临时实体
        self.tempviewpix.fill(PyQt4.QtCore.Qt.transparent)
        pixpainter=PyQt4.QtGui.QPainter(self.tempviewpix)
        pixpainter.setWindow(0, 0, self.width(), self.height())
        pixpainter.setWorldMatrixEnabled(True)
        pixpainter.setWorldTransform(self.transform1)
        self.tempdata.freshbyobjects(pixpainter) #按照对象绘制
        self.tempdata.modified=False
        pixpainter.end()
    def _cleartempview(self):
        self.tempviewpix.fill(PyQt4.QtCore.Qt.transparent)
    def _clearmouseview(self):
        self.mouseviewpix.fill(PyQt4.QtCore.Qt.transparent)
    def resizeEvent(self, event):
        self.resizepix()
        self.update()
    def paintEvent(self, event):
        if self.firstshow :
            self.firstshow=False
            self.firstshowme()
        painter=PyQt4.QtGui.QPainter(self)
        #判断是否需要调用freshobject绘制
        #条件2：矩阵有变化
        #条件3：窗口尺寸有变化
        s1=self.graphdata.modified         #条件1：图像或图层有变化
        if self.pretransform == self.transform1 :
            s2=False
        else:
            s2=True
        if (self.prewindowsize[0] == self.width()) and (self.prewindowsize[1] == self.height()):
            s3=False
        else:
            s3=True
        if s1 or s2 or s3:
            self.objectready=False
            self.pretransform=self.transform1
            self.prewindowsize[0] =self.width()
            self.prewindowsize[1] =self.height()
            self.freshobjects()
        s1=self.tempdata.modified
        if s1 or s2 or s3:
            self.freshtempobjects()
        #判断结束
        painter.drawPixmap(0, 0, self.viewpix)
        #painter.drawPixmap(0,0,self.tempviewpix)
        painter.drawPixmap(0,0,self.mouseviewpix)
    def resizepix(self):
        self.viewpix=PyQt4.QtGui.QPixmap(self.width(),self.height())
        self.tempviewpix=PyQt4.QtGui.QPixmap(self.width(),self.height())
        self.mouseviewpix=PyQt4.QtGui.QPixmap(self.width(),self.height())
        self.mouseviewpix.fill(PyQt4.QtCore.Qt.transparent)
    def firstshowme(self):
        self.resizepix()
        self.freshobjects()
        self.freshtempobjects()
    def mouseMoveEvent(self, event):
        x=event.pos().x()
        y=event.pos().y()
        self.mousepos[2]=self.mousepos[0]
        self.mousepos[3]=self.mousepos[1]
        self.mousepos[0]=x
        self.mousepos[1]=y
        pt=self.screentoworld(x,y)
    #临时数据操作
    def _drawrubberline(self,spt,ept):
        #在鼠标绘图上绘制橡皮线,橡皮线使用的世界坐标
        pixpainter=PyQt4.QtGui.QPainter(self.mouseviewpix)
        pixpainter.setWindow(0, 0, self.width(), self.height())
        pixpainter.setWorldMatrixEnabled(True)
        pixpainter.setWorldTransform(self.transform1)
        oldpen = pixpainter.pen()
        pixpainter.setPen(self._graphcfg.crossline)
        pixpainter.drawLine(QtCore.QLineF(spt[0],spt[1],ept[0],ept[1]))
        pixpainter.setPen(oldpen)
        pixpainter.end()
    def _drawrubberrect(self,spt,ept):
        #在鼠标绘图上绘制橡皮线,橡皮线使用的世界坐标
        pixpainter=PyQt4.QtGui.QPainter(self.mouseviewpix)
        pixpainter.setWindow(0, 0, self.width(), self.height())
        pixpainter.setWorldMatrixEnabled(True)
        pixpainter.setWorldTransform(self.transform1)
        oldpen = pixpainter.pen()
        pixpainter.setPen(self._graphcfg.crossline)
        pixpainter.drawLine(QtCore.QLineF(spt[0],spt[1],ept[0],spt[1]))
        pixpainter.drawLine(QtCore.QLineF(ept[0],spt[1],ept[0],ept[1]))
        pixpainter.drawLine(QtCore.QLineF(ept[0],ept[1],spt[0],ept[1]))
        pixpainter.drawLine(QtCore.QLineF(spt[0],ept[1],spt[0],spt[1]))
        pixpainter.setPen(oldpen)
        pixpainter.end()
class mgraph2d(mgraph2dbase):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None, scalexy=1.0):
        """scalexy,y/x的比例"""
        super(mgraph2d,self).__init__(parent,scalexy)
        self._commandstack=[] #命令堆栈
    def showmouse(self,painter):
        #绘制鼠标移动时的多义线
        w=self.width()
        h=self.height()
        x=self.mousepos[0]
        y=self.mousepos[1]
        oldpen=painter.pen()
        painter.setPen(self._graphcfg.crossline)
        #if self.mousestatus == 0:
        painter.drawLine(0, y, w, y)
        painter.drawLine(x, 0, x, h)
        painter.setPen(oldpen)
    def paintEvent(self, event):
        super(mgraph2d,self).paintEvent(event)
        painter=PyQt4.QtGui.QPainter(self)
        self.showmouse(painter)
    def mouseMoveEvent(self, event):
        #重载
        mgraph2dbase.mouseMoveEvent(self,event)
        self._processcommand("mousemove",(event.pos().x(), event.pos().y()))
        self.update()
    def _processcommand(self, eventname, pos):
        #处理命令消息
        #如果没有命令堆栈
        if eventname == "rightmousepress": #鼠标右键始终针对的是pan
            self._commandstack.append(command_panwindow(1,pos))
        if (len(self._commandstack) == 0):
            return
        #如果存在命令堆栈
        if self._commandstack[-1]._processcommand(self,eventname,pos) == True:
            self._commandstack.pop()
    def onkeyrelease(self,event):
        #处理快捷键盘消息,可重载
        if event.key() == 16777216: #esc
            self.eventstack=[]
            self._commandstack=[]
            self.tempdata.clearall()
            self._cleartempview()
            self._clearmouseview()
            self.repaint()
        if event.key() == 16777268: #F5
            #强制刷新
            self.repaint()
        if event.key() == 69: #"e"
            self.eventstack=[]
            self.c_zoomextend()
            self.repaint()
        if event.key() == 87: #"w"
            self.eventstack=[]
            self.zoomwindow()
        else:
            return False
        return True
    def keyReleaseEvent(self, event):
        if not self.onkeyrelease(event):
            self._processcommand("keyrelease",event.key())
    def mousePressEvent(self, event):
        if event.buttons() == PyQt4.QtCore.Qt.RightButton:
            self._processcommand("rightmousepress",(event.pos().x(), event.pos().y()))
        if event.buttons() == PyQt4.QtCore.Qt.LeftButton:
            self._processcommand("leftmousepress",(event.pos().x(), event.pos().y()))
    def mouseReleaseEvent(self, event):
        self._processcommand("mouserelease",(event.pos().x(), event.pos().y()))
    def wheelEvent(self, event):
        #鼠标滚轮目前定义为比例操作
        x=event.x()
        y=event.y()
        stepsc=abs(event.delta()/120.)
        stepsc=1.0
        if event.delta() > 0:
            self._scalewindow(x, y, stepsc*1.1)
        elif  event.delta() <0:
            self._scalewindow(x, y, 0.9/stepsc)
        self.update()
    def zoomwindow(self):
        #"""窗口放大命令"""
        self._commandstack.append(command_zoomwindow())
        self.repaint()
    def getmainpoint(self,x,y,distradius=1.0):
        ##捕捉主点,distradius为捕捉半径
        resultpt=[]
        for ob in self.graphobject:
            ln=ob.layername
            if self.layers[ln].visible:
                for pt in ob.mainpoint:
                    dx=pt[0]-x
                    dy=pt[1]-y
                    di=math.sqrt(dx*dx+dy*dy)
                    if (di <= distradius):
                        resultpt.append(pt)
        return resultpt
def testform():
    app=PyQt4.QtGui.QApplication([])
    form=mgraph2d(None,1)
    form.show()
    for i in range(0,100):
        form.graphdata.appendobject(lineobject(0,0,100,100))
    form.update()
    form.c_zoomextend()
    app.exec_()
if __name__ == '__main__':
     testform()
