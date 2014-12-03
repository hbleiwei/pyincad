# -*- coding: utf-8 -*-
__author__ = 'leiwei'
import string
from pyautocad import Autocad,APoint
filename="d:\\tangcao-54.txt"
fi=open(filename)
fiall=fi.readlines()
fi.close()
acad=Autocad()
for ele in fiall:
    la=ele.split(",")
    na=la[0]
    y=string.atof(la[1])
    x=string.atof(la[2])
    z=string.atof(la[3])
    acad.model.AddPoint(APoint(x,y))
    acad.model.AddText(na,APoint(x,y),40)
    print na,x,y


