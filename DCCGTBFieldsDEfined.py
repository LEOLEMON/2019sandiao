#-*- coding:utf-8 -*-
import arcpy

#原数据和规划院对接数据值域对应关系
class ValueRelationClass:

    oldValue = ""
    newValue = ""

    def __init__(self,oldValue,newValue):

        self.oldValue = oldValue
        self.newValue = newValue

#字段数据值域定义以及原数据和规划院对接数据值域对应关系集合
class ValuesDefined:

    fieldname = ""

    values = []

    relations = []

    def __init__(self,fieldname,values,relations):

        self.fieldname = fieldname
        self.values = values
        self.relations = relations

#所有字段集合
FieldsGroup = []

#不同字段值之间的对应关系
class FieldsValuesRelation:

    field1 = ""
    field2 = ""
    field1Value = ""
    field2Value = ""

    def __init__(self,field1,field1Value,field2,field2Value):

        self.field1 = field1
        self.field1Value = field1Value
        self.field2 = field2
        self.field2Value = field2Value

#不同字段值之间的对应关系集合
FieldsValuesRelationGroup = []

#各个字段的值域及新旧值对照关系

def TBBHvalue():

    fieldname = "TBBH"

    values = []

    relations = [ValueRelationClass(None,""),ValueRelationClass("","")]

    valuesdefined = ValuesDefined(fieldname,values,relations)

    FieldsGroup.append(valuesdefined)

def DLBMvalues():

    fieldname = "DLBM"

    values = ['0303','0304','0306','0402','0603','1105','1106','1108','0101','0102','0103','0201','0202','0203','0204','0201K','0202K','0203K','0204K','0301','0302','0305','0307','0301K','0302K','0307K','0401','0403','0404','0403K','1001','1002','1003','1004','1005','1006','1007','1008','1009','1101','1102','1103','1104','1107','1109','1110','1104A','1104K','1107A','1201','1202','1203','1204','1205','1206','1207','201','202','203','204','205','0810','1301','1302','1303','1304']

    relations = []

    valuesdefined = ValuesDefined(fieldname,values,relations)

    FieldsGroup.append(valuesdefined)

def DLMCvalues():

    fieldname = "DLMC"

    values = [u'红树林地',u'森林沼泽',u'灌丛沼泽',u'沼泽草地',u'盐田',u'沿海滩涂',u'内陆滩涂',u'沼泽地',u'水田',u'水浇地',u'旱地',u'果园',u'茶园',u'橡胶园',u'其他园地',u'可调整果园',u'可调整茶园',u'可调整橡胶园',u'可调整其他园地',u'乔木林地',u'竹林地',u'灌木林地',u'其他林地',u'可调整乔木林地',u'可调整竹林地',u'可调整其他林地',u'天然牧草地',u'人工牧草地',u'其他草地',u'可调整人工牧草地',u'铁路用地',u'轨道交通用地',u'公路用地',u'城镇村道路用地',u'交通服务场站用地',u'农村道路',u'机场用地',u'港口码头用地',u'管道运输用地',u'河流水面',u'湖泊水面',u'水库水面',u'坑塘水面',u'沟渠',u'水工建筑用地',u'冰川及永久积雪',u'养殖坑塘',u'可调整养殖坑塘',u'干渠',u'空闲地',u'设施农用地',u'田坎',u'盐碱地',u'沙地',u'裸土地',u'裸岩石砾地',u'城市',u'建制镇',u'村庄',u'盐田及采矿用地',u'特殊用地',u'公园与绿地',u'临时用地',u'光伏板区',u'推土区',u'拆除未尽区']

    relations = []

    valuesdefined = ValuesDefined(fieldname,values,relations)

    FieldsGroup.append(valuesdefined)

def GDLXMCvalues():

    fieldname = "GDLXMC"

    values = [u'平地',u'坡地',u'梯田','']

    relations = [ValueRelationClass("FD",u"平地"),ValueRelationClass("PD",u"坡地"),ValueRelationClass("TT",u"梯田"),ValueRelationClass(None,""),ValueRelationClass("","")]

    valuesdefined = ValuesDefined(fieldname,values,relations)

    FieldsGroup.append(valuesdefined)

def TBXHDMvalues():

    fieldname = "TBXHDM"

    values = ['HDGD','HQGD','LQGD','MQGD','HHGD','SMGD','LQYD','GCCD','']

    relations = [ValueRelationClass("0",""),ValueRelationClass(None,""),ValueRelationClass("","")]

    valuesdefined = ValuesDefined(fieldname,values,relations)

    FieldsGroup.append(valuesdefined)

def TBXHMCvalues():

    fieldname = "TBXHMC"

    values = [u'河道耕地',u'湖区耕地',u'林区耕地',u'牧区耕地',u'沙荒耕地',u'石漠化耕地',u'林区园地',u'灌丛草地','']

    relations = [ValueRelationClass(u"无",""),ValueRelationClass(None,""),ValueRelationClass("","")]

    valuesdefined = ValuesDefined(fieldname,values,relations)

    FieldsGroup.append(valuesdefined)

def ZZSXDMvalues():

    fieldname = "ZZSXDM"

    values = ['GZ','WG','YM','LM','LH','MC','GSYY','SSLM','']

    relations = [ValueRelationClass("0",""),ValueRelationClass(None,""),ValueRelationClass("",""),ValueRelationClass("SS","SSLM"),ValueRelationClass("GS","GSYY")]

    valuesdefined = ValuesDefined(fieldname,values,relations)

    FieldsGroup.append(valuesdefined)

def ZZSXMCvalues():

    fieldname = "ZZSXMC"

    values = [u'耕种',u'未耕种',u'临时种植园木',u'临时种植林木',u'绿化草地',u'临时种植牧草',u'观赏园艺',u'速生林木','']

    relations = [ValueRelationClass(u"无",""),ValueRelationClass(None,""),ValueRelationClass("","")]

    valuesdefined = ValuesDefined(fieldname,values,relations)

    FieldsGroup.append(valuesdefined)

def CZCSXMvalues():

    fieldname = "CZCSXM"

    values = ['201','202','203','204','205','201A','202A','203A','']

    relations = [ValueRelationClass(None,""),ValueRelationClass("","")]

    valuesdefined = ValuesDefined(fieldname,values,relations)

    FieldsGroup.append(valuesdefined)

def WJZLXvalues():

    fieldname = "WJZLX"

    values = [u'无法到达',u'城镇村建设用地',u'军事用地',u'小图斑','']

    relations = [ValueRelationClass("WFDD",u"无法到达"),ValueRelationClass("CZCJSYD",u"城镇村建设用地"),ValueRelationClass("JSYD",u"军事用地"),ValueRelationClass("XTB",u"小图斑"),ValueRelationClass(None,""),ValueRelationClass("","")]

    valuesdefined = ValuesDefined(fieldname,values,relations)

    FieldsGroup.append(valuesdefined)

def FZHvalue():

    fieldname = "FZH"

    values = []

    relations = [ValueRelationClass(None,""),ValueRelationClass("","")]

    valuesdefined = ValuesDefined(fieldname,values,relations)

    FieldsGroup.append(valuesdefined)

#各个字段之间的对照关系

def DLRelation():

    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0303','DLMC',u'红树林地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0304','DLMC',u'森林沼泽'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0306','DLMC',u'灌丛沼泽'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0402','DLMC',u'沼泽草地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0603','DLMC',u'盐田'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1105','DLMC',u'沿海滩涂'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1106','DLMC',u'内陆滩涂'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1108','DLMC',u'沼泽地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0101','DLMC',u'水田'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0102','DLMC',u'水浇地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0103','DLMC',u'旱地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0201','DLMC',u'果园'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0202','DLMC',u'茶园'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0203','DLMC',u'橡胶园'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0204','DLMC',u'其他园地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0201K','DLMC',u'可调整果园'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0202K','DLMC',u'可调整茶园'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0203K','DLMC',u'可调整橡胶园'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0204K','DLMC',u'可调整其他园地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0301','DLMC',u'乔木林地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0302','DLMC',u'竹林地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0305','DLMC',u'灌木林地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0307','DLMC',u'其他林地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0301K','DLMC',u'可调整乔木林地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0302K','DLMC',u'可调整竹林地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0307K','DLMC',u'可调整其他林地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0401','DLMC',u'天然牧草地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0403','DLMC',u'人工牧草地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0404','DLMC',u'其他草地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0403K','DLMC',u'可调整人工牧草地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1001','DLMC',u'铁路用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1002','DLMC',u'轨道交通用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1003','DLMC',u'公路用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1004','DLMC',u'城镇村道路用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1005','DLMC',u'交通服务场站用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1006','DLMC',u'农村道路'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1007','DLMC',u'机场用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1008','DLMC',u'港口码头用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1009','DLMC',u'管道运输用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1101','DLMC',u'河流水面'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1102','DLMC',u'湖泊水面'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1103','DLMC',u'水库水面'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1104','DLMC',u'坑塘水面'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1107','DLMC',u'沟渠'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1109','DLMC',u'水工建筑用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1110','DLMC',u'冰川及永久积雪'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1104A','DLMC',u'养殖坑塘'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1104K','DLMC',u'可调整养殖坑塘'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1107A','DLMC',u'干渠'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1201','DLMC',u'空闲地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1202','DLMC',u'设施农用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1203','DLMC',u'田坎'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1204','DLMC',u'盐碱地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1205','DLMC',u'沙地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1206','DLMC',u'裸土地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1207','DLMC',u'裸岩石砾地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','201','DLMC',u'城市'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','202','DLMC',u'建制镇'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','203','DLMC',u'村庄'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','204','DLMC',u'盐田及采矿用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','205','DLMC',u'特殊用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','201A','DLMC',u'城市独立工业用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','202A','DLMC',u'建制镇独立工业用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','203A','DLMC',u'村庄独立工业用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0810','DLMC',u'公园与绿地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','0810A','DLMC',u'广场用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1301','DLMC',u'临时用地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1302','DLMC',u'光伏板区'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1303','DLMC',u'推土区'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('DLBM','1304','DLMC',u'拆除未尽区'))

def XHRelation():

    FieldsValuesRelationGroup.append(FieldsValuesRelation('TBXHDM','HDGD','TBXHMC',u'河道耕地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('TBXHDM','HQGD','TBXHMC',u'湖区耕地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('TBXHDM','LQGD','TBXHMC',u'林区耕地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('TBXHDM','MQGD','TBXHMC',u'牧区耕地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('TBXHDM','HHGD','TBXHMC',u'沙荒耕地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('TBXHDM','SMGD','TBXHMC',u'石漠化耕地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('TBXHDM','LQYD','TBXHMC',u'林区园地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('TBXHDM','GCCD','TBXHMC',u'灌丛草地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('TBXHDM','','TBXHMC',''))

def ZZRelation():

    FieldsValuesRelationGroup.append(FieldsValuesRelation('ZZSXDM','GZ','ZZSXMC',u'耕种'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('ZZSXDM','WG','ZZSXMC',u'未耕种'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('ZZSXDM','YM','ZZSXMC',u'临时种植园木'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('ZZSXDM','LM','ZZSXMC',u'临时种植林木'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('ZZSXDM','LH','ZZSXMC',u'绿化草地'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('ZZSXDM','MC','ZZSXMC',u'临时种植牧草'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('ZZSXDM','GSYY','ZZSXMC',u'观赏园艺'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('ZZSXDM','SSLM','ZZSXMC',u'速生林木'))
    FieldsValuesRelationGroup.append(FieldsValuesRelation('ZZSXDM','','ZZSXMC',''))

def initlitaize():

    TBBHvalue()
    DLBMvalues()
    DLMCvalues()
    GDLXMCvalues()
    TBXHDMvalues()
    TBXHMCvalues()
    ZZSXDMvalues()
    ZZSXMCvalues()
    CZCSXMvalues()
    WJZLXvalues()
    FZHvalue()

    DLRelation()
    XHRelation()
    ZZRelation()

initlitaize()