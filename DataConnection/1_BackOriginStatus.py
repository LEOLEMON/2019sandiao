#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,arcpyDeal,pathArgs

def ensureSHFields(targetpath):

    fields = ["DLBM_1","GDZZSXMC_1","TBXHMC_1","GDLX_1"]

    arcpy.ensureFields(targetpath,fields)

def deleteFields(targetpath):
    """删除过程字段"""

    delFieldsList = ["unionfzh","exp_bsm","exp_tbbh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm","exp_tblx","exp_tbwym","bhlx","exp_wjzlx","fzh"]

    arcpyDeal.deleteFields(targetpath,delFieldsList)

def collectIntersectFeauture(TempAnalysis):
    """分析相同图属统一编码的数据谁的面积最大，那就代表原本图斑属于哪个初始库图斑"""

    fields = ["TSTYBM","BSM","BSM_1","ZLDWDM","SJDLBM","ZLDWDM_1","DLBM_12","SHAPE@AREA"]
    showFields = ["tstybm","bsm","bsm_1","zldwdm","sjdlbm","zldwdm_1","sjdlbm_1","area"]

    cursor = arcpy.da.SearchCursor(TempAnalysis,fields,sql_clause=(None, 'ORDER BY TSTYBM'))

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

    arcpy.Delete_management(TempAnalysis)

    return matchedDataDict

def UpdateTarget(targetpath,matchedDataDict):
    """更新还原初始库属性"""

    bsmDifference = []
    zldwdmDifference = []
    sjdlbmDifference = []
    tstybmDifference = []

    fields = ["TSTYBM","exp_bsm","exp_sjdlbm","exp_zldwdm"]
    fields = ["tstybm","exp_bsm","exp_sjdlbm","exp_zldwdm"]

    arcpyDeal.ensureFields(targetpath,fields)

    cursor = arcpy.da.UpdateCursor(targetpath,fields,sql_clause=(None, 'ORDER BY TSTYBM'))

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

        row[1] = matchedDataDict[tstybm]["bsm_1"]
        row[2] = matchedDataDict[tstybm]["sjdlbm_1"]
        row[3] = matchedDataDict[tstybm]["zldwdm_1"]

        cursor.updateRow(row)

    arcpy.AddMessage("1_共有%s个图斑bsm不同"%(len(bsmDifference)))
    arcpy.AddMessage("1_共有%s个图斑zldwdm不同"%(len(zldwdmDifference)))
    arcpy.AddMessage("1_共有%s个图斑sjdlbm不同"%(len(sjdlbmDifference)))
    arcpy.AddMessage("1_共有%s个图斑无初始库图斑"%(len(tstybmDifference)))

    arcpy.AddMessage("1_"+json.dumps(bsmDifference))
    arcpy.AddMessage("1_"+json.dumps(zldwdmDifference))
    arcpy.AddMessage("1_"+json.dumps(sjdlbmDifference))
    arcpy.AddMessage("1_"+json.dumps(tstybmDifference))

def start(targetpath,cskpath,tempname):

    #确认审核字段是否存在
    arcpy.AddMessage("1_确认审核字段")
    deleteFields(targetpath)

    #删除规则能够产生的字段
    arcpy.AddMessage("1_删除字段")
    deleteFields(targetpath)

    #相交分析
    arcpy.AddMessage("1_相交分析")
    
    arcpy.Intersect_analysis ([targetpath, cskpath],tempname, "ALL", "", "")
    
    #收集
    arcpy.AddMessage("1_收集")
    result = arcpy.GetCount_management(tempname)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','1_收集',0,count,1)

    matchedDataDict = collectIntersectFeauture(tempname)
    
    #还原数据
    arcpy.AddMessage("1_还原数据")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','1_还原数据',0,count,1)

    UpdateTarget(targetpath,matchedDataDict)
   
if __name__ == "__main__":
    
    arcpy.AddMessage("1_开始还原初始库属性")
    
    arcpy.env.overwriteOutput = True

    targetpath = arcpy.GetParameterAsText(0)
    cskpath = arcpy.GetParameterAsText(1)

    enviroment = arcpy.GetParameterAsText(2)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = enviroment

    tempname = "output_01"

    start(targetpath,cskpath,tempname)

    arcpy.SetParameterAsText(3,targetpath)

    arcpy.AddMessage("1_结束还原初始库属性")