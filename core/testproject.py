# -*- coding: utf-8 -*-
# 测试incadproject
# __author__ = 'leiwei'
from pyincad import core
pro=core.incadproject()
sta=pro.openproject("c:\\incadtest\\test1.fdb")
#id=pro.nametoid('b')
#pro.modifycomment('test project12345 ')
id=pro.nametoid('a')
print id
print pro.projectpath()
print "OK"
