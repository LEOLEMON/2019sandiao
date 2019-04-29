#-*- coding:utf-8 -*-
#coding:utf-8
import datetime

def dealNoneAndBlank(Value):

    if  type(Value) == str or Value == None:

        if Value == None:

            return ''

        elif Value.strip() == "":

            return ''

        else:
           
            return Value

    else:
        
        return Value


def dealSpacialAndBlank(Value):

    if  type(Value) == str or Value == None:

        if Value == None:

            return ''

        elif Value.strip() == u"0" or Value.strip() == u'无' or Value.strip() == "":

            return ''

        else:
           
            return Value

    else:
        
        return Value

