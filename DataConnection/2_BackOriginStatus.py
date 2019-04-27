#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,sys
for p in sys.path:
    arcpy.AddMessage(p)
import json,arcpyDeal

def ensureSHFields(targetpath):

    fields = ["DLBM_1","GDZZSXMC_1","TBXHMC_1","GDLX_1"]

    arcpyDeal.ensureFields(targetpath,fields)

def deleteFields(targetpath):
    """删除过程字段"""

    delFieldsList = ["unionfzh","exp_bsm","exp_tbbh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm","exp_tblx","exp_tbwym","bhlx","exp_wjzlx","fzh","intersecrteddeal"]

    arcpyDeal.deleteFields(targetpath,delFieldsList)

def createWidth(tempname):
    """创建平均宽度"""

    arcpy.AddField_management(tempname, "width", "Double")

    expression = "getClass(float(!SHAPE.area!),float(!SHAPE.length!))"
    codeblock = """def getClass(area,length):
        return area/length
        """

    arcpy.CalculateField_management(tempname,"width", expression, "PYTHON_9.3",codeblock)

def collectIntersectFeauture(TempAnalysis):
    """分析相同图属统一编码的数据谁的面积最大，那就代表原本图斑属于哪个初始库图斑"""

    fields = ["TSTYBM","BSM","ZLDWDM","DLBM","BSM_1","ZLDWDM_1","SJDLBM","SHAPE@AREA"]
    showFields = ["tstybm","bsm","zldwdm","sjdlbm","bsm_1","zldwdm_1","sjdlbm_1","area"]

    cursor = arcpy.da.SearchCursor(TempAnalysis,fields,where_clause=" TSTYBM is not null",sql_clause=(None, 'ORDER BY TSTYBM'))

    matchedData = {}
    
    matchedDataDict = {}

    arcpyDeal.checkField(TempAnalysis,fields)

    for row in cursor:
        
        arcpy.SetProgressorPosition()

        newRowData = {}

        for i in range(len(showFields)):

            newRowData[showFields[i]] = row[i]

        if matchedData == {}:

            matchedData = newRowData

            continue

        if matchedData['tstybm'] != newRowData['tstybm']:

            matchedDataDict[matchedData['tstybm']] = matchedData

            matchedData = newRowData

            continue
                
        if matchedData['area'] < newRowData['area']:

            matchedData = newRowData

    matchedDataDict[matchedData['tstybm']] = matchedData

    return matchedDataDict

def UpdateTarget(targetpath,matchedDataDict):
    """更新还原初始库属性"""

    bsmDifference = []
    zldwdmDifference = []
    sjdlbmDifference = []
    tstybmDifference = []

    fields = ["TSTYBM","exp_bsm","exp_sjdlbm","exp_zldwdm"]

    arcpyDeal.ensureFields(targetpath,fields)

    cursor = arcpy.da.UpdateCursor(targetpath,fields,where_clause=" TSTYBM is not null",sql_clause=(None, 'ORDER BY TSTYBM'))

    for row in cursor:

        arcpy.SetProgressorPosition()

        tstybm = row[0]

        if tstybm not in matchedDataDict:

            tstybmDifference.append(tstybm)

            continue

        if matchedDataDict[tstybm]["bsm"] != matchedDataDict[tstybm]["bsm_1"]:

            bsmDifference.append(tstybm)

        if matchedDataDict[tstybm]["zldwdm"] != matchedDataDict[tstybm]["zldwdm_1"]:

            zldwdmDifference.append(tstybm)

        if matchedDataDict[tstybm]["sjdlbm"] != matchedDataDict[tstybm]["sjdlbm_1"]:

            sjdlbmDifference.append(tstybm)

        row[1] = matchedDataDict[tstybm]["bsm"]
        row[2] = matchedDataDict[tstybm]["sjdlbm"]
        row[3] = matchedDataDict[tstybm]["zldwdm"]

        cursor.updateRow(row)

    arcpy.AddMessage("2_共有%s个图斑bsm不同"%(len(bsmDifference)))
    arcpy.AddMessage("2_共有%s个图斑zldwdm不同"%(len(zldwdmDifference)))
    arcpy.AddMessage("2_共有%s个图斑sjdlbm不同"%(len(sjdlbmDifference)))
    arcpy.AddMessage("2_共有%s个图斑无初始库图斑"%(len(tstybmDifference)))

    arcpy.AddMessage("2_"+json.dumps(bsmDifference))
    arcpy.AddMessage("2_"+json.dumps(zldwdmDifference))
    arcpy.AddMessage("2_"+json.dumps(sjdlbmDifference))
    arcpy.AddMessage("2_"+json.dumps(tstybmDifference))

def start(targetpath,cskpath,tempname):

    #确认审核字段是否存在
    arcpy.AddMessage("2_确认审核字段")
    ensureSHFields(targetpath)

    #删除规则能够产生的字段
    # arcpy.AddMessage("2_删除字段")
    # deleteFields(targetpath)

    #标识分析
    arcpy.AddMessage("2_相交分析")
    arcpy.Identity_analysis  (cskpath,targetpath,tempname, "ALL", "", "")

    arcpy.AddMessage("2_创建平均宽度")
    createWidth(tempname)
    
    #收集
    arcpy.AddMessage("2_收集")
    result = arcpy.GetCount_management(tempname)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','2_收集',0,count,1)

    matchedDataDict = collectIntersectFeauture(tempname)
    
    #还原数据
    arcpy.AddMessage("2_还原数据")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','2_还原数据',0,count,1)

    UpdateTarget(targetpath,matchedDataDict)
   
if __name__ == "__main__":

    arcpy.AddMessage("2_开始还原初始库属性")
    
    arcpy.env.overwriteOutput = True

    targetpath = arcpy.GetParameterAsText(0)
    cskpath = arcpy.GetParameterAsText(1)

    enviroment = arcpy.GetParameterAsText(2)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = enviroment

    tempname = "output_02"

    start(targetpath,cskpath,tempname)

    arcpy.SetParameterAsText(3,targetpath)
    arcpy.SetParameterAsText(4,tempname)

    arcpy.AddMessage("2_结束还原初始库属性")