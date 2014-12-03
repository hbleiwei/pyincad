# -*- coding: utf-8 -*-
from pyincad import cadtools
import pyincad.cadtools.horizontal
import math
from pyincad import core
if __name__ == "__main__":
    acadapp=cadtools.pyacad()
    acadapp.linkautocad()
    ele=core.horizontalelement()
    ele1=core.horizontalelement()
    ele2=core.horizontalelement()
    ele1.initline(10,10,100,100)
    ele2.initline(100,100,250,100)
    ele1.translation(10,0)
    ele2=ele1.birthpre(1.0/50,20,30,30)
    ele2.setequalto(ele1)
    #pyincad.cadtools.horizontal.drawhorizontalelement(acadapp,ele2)
    ele1.calch(0)
    re=ele1.coxy(10,0)
    #acadapp.addpoint(re[1],re[2])
    #acadapp.addtext(10,10,u"好的",6,math.pi/4.)
    pyincad.cadtools.horizontal.drawhorizontalelement(acadapp,ele2)
    ele.initarc(100,100,50,-1,0,math.pi/2.0)
    ele.setaas(40)
    ele.setaae(40)
    ele.cal()
    ele.threeelement(ele1,ele2)
    pyincad.cadtools.horizontal.drawhorizontalelement(acadapp,ele)
    from pyincad import cadtools
    #pa1=cadtools.pyacad()
    #pa1.linkautocad()
    #pa1.sendcommand("_plot ")