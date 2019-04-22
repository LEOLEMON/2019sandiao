#-*- coding:utf-8 -*-
#coding:utf-8
import datetime

def dealNoneAndBlank(Value):

    if  type(Value) == str or Value == None:

        return '' if Value == None or str(Value) == 'None'  else Value.strip()

    else:
        
        return Value

