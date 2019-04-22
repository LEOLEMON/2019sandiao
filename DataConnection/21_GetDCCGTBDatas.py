#-*- coding:utf-8 -*-
import arcpy,arcpyDeal

class RelationClass:

    oldFields = ""
    newFields = ""

    def __init__(self,oldFields,newFields):

        self.oldFields = oldFields
        self.newFields = newFields

class RelationsClass:

    value = []

    def __init__(self):

        self.value.append(RelationClass("exp_bsm","BSM"))
        self.value.append(RelationClass("exp_tbybh","TBYBH"))
        self.value.append(RelationClass("exp_tbbh","TBBH"))
        self.value.append(RelationClass("exp_zldwdm","ZLDWDM"))
        self.value.append(RelationClass("exp_dlbm","DLBM"))
        self.value.append(RelationClass("exp_dlmc","DLMC"))
        self.value.append(RelationClass("exp_gdlx","GDLXMC"))
        self.value.append(RelationClass("exp_tbxhdm","TBXHDM"))
        self.value.append(RelationClass("exp_tbxhmc","TBXHMC"))
        self.value.append(RelationClass("exp_gdzzsxdm","ZZSXDM"))
        self.value.append(RelationClass("exp_gdzzsxmc","ZZSXMC"))
        self.value.append(RelationClass("exp_czcsxm","CZCSXM"))
        self.value.append(RelationClass("exp_tblx","TBLX"))
        self.value.append(RelationClass("exp_tbwym","WYM"))
        self.value.append(RelationClass("bhlx","BHLX"))
        self.value.append(RelationClass("exp_wjzlx","WJZLX"))
        self.value.append(RelationClass("fzh","FZH"))
        self.value.append(RelationClass("SHAPE@","SHAPE@"))

def getFields():

    relationsClass = RelationsClass()

    oldFields,newFields = [],[]

    for relation in relationsClass.value:

        oldFields.append(relation.oldFields)
        newFields.append(relation.newFields)

    return oldFields,newFields

def updateDatas(dccgtb,sourcePath,oldFields,newFields):

    insertrows = arcpy.da.InsertCursor(dccgtb,newFields)

    arcpyDeal.checkField(sourcePath,oldFields)
    arcpyDeal.checkField(dccgtb,newFields)

    cursor = arcpy.da.SearchCursor(sourcePath,oldFields)

    for row in cursor:

        insertrows.insertRow(row)

        arcpy.SetProgressorPosition()

def start(dccgtb,sourcePath):

    arcpy.AddMessage("21_获取新旧字段")
    oldFields,newFields = getFields()

    arcpy.AddMessage("21_获取数据")
    result = arcpy.GetCount_management(sourcePath)
    count = int(result.getOutput(0))

    updateDatas(dccgtb,sourcePath,oldFields,newFields)

if __name__ == "__main__":
    
    arcpy.AddMessage("21_获取调查成果图斑")
    
    dccgtb = arcpy.GetParameterAsText(0)
    sourcePath = arcpy.GetParameterAsText(1)

    start(dccgtb,sourcePath)

    arcpy.SetParameterAsText(2,dccgtb)

    arcpy.AddMessage("21_结束")