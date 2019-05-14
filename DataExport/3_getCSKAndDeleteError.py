#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,arcpyDeal

def getCskArea(cskpath):
    """计算初始库面积"""

    arcpyDeal.ensureFields(cskpath,["cskmianji"],type = "DOUBLE")

    cskcur = arcpy.da.UpdateCursor(cskpath,['cskmianji','SHAPE@AREA'])

    for row in cskcur:

        row[0] = row[1]
        
        cskcur.updateRow(row)

def createWidth(tempname):
    """创建平均宽度,用于处理狭长图斑"""

    arcpyDeal.ensureFields(tempname,["width"],type="Double")
    
    expression = "getClass(float(!SHAPE.area!),float(!SHAPE.length!))"
    codeblock = """def getClass(area,length):
        return area/length
        """

    arcpy.CalculateField_management(tempname,"width", expression, "PYTHON_9.3",codeblock)

def collectError(indentitypath):

    where_clause = "SHAPE_Area >0.5 and width > 0.1 and TSTYBM is not null and TSTYBM <> ''"

    sql_clause = (None,"ORDER BY TSTYBM,BSM DESC")

    searchFields = ["BSM","TSTYBM"]

    cursor = arcpy.da.SearchCursor(indentitypath, searchFields,where_clause = where_clause,sql_clause = sql_clause)

    lasttstybm = {"tstybm":"","cskbsm":[]}

    targetValueList = []

    number = 0

    for row in cursor:

        arcpy.SetProgressorPosition()

        number += 1

        data = dict(zip(searchFields,row))
        
        if lasttstybm["tstybm"] == "":

            lasttstybm["tstybm"] =  data["TSTYBM"]
            lasttstybm["cskbsm"] = [data["BSM"]]

        elif lasttstybm["tstybm"] != data["TSTYBM"]:

            if len(lasttstybm["cskbsm"]) > 1:

                targetValueList.append(lasttstybm["tstybm"])
 
            lasttstybm["tstybm"] =  data["TSTYBM"]
            lasttstybm["cskbsm"] = [data["BSM"]]

        elif lasttstybm["tstybm"]  == data["TSTYBM"]:

            # arcpy.AddMessage("%s,%s,%s,%s"%(data["TSTYBM"],data["BSM"],lasttstybm["cskbsm"],str(data["BSM"] not in lasttstybm["cskbsm"])))

            if data["BSM"] not in lasttstybm["cskbsm"]:

                lasttstybm["cskbsm"].append(data["BSM"])

    if len(lasttstybm["cskbsm"]) > 1:

        targetValueList.append(lasttstybm["tstybm"])

    arcpy.AddMessage("共有%s个错误图斑"%(len(targetValueList)))

    return targetValueList

def markError(xzkpath,targetValueList):
    """标记错误图斑"""

    searchFields = ["TSTYBM","error"]

    arcpyDeal.deleteFields(xzkpath,["error"])
    arcpyDeal.ensureFields(xzkpath,searchFields)

    with arcpy.da.UpdateCursor(xzkpath,searchFields) as cur:

        for row in cur:
            
            arcpy.SetProgressorPosition()

            TSTYBM  = row[0]

            if TSTYBM in targetValueList:

                row[1] = '0'

            else:

                row[1] = "1"

            cur.updateRow(row)

def outputError(xzkpath,errorpath):
    """删除错误图斑并输出"""

    where_clause = "error = '0'"

    arcpy.MakeFeatureLayer_management(xzkpath,"xzkpath")

    arcpy.SelectLayerByAttribute_management("xzkpath",where_clause=where_clause)

    arcpy.CopyFeatures_management("xzkpath",errorpath)

    arcpy.DeleteFeatures_management("xzkpath")

def judgeError(xzkpath,indentitypath,errorpath):
    """判断是否有超出初始库范围的现状库图斑"""

    where_clause = "TSTYBM is not null and TSTYBM <> ''"

    arcpy.MakeFeatureLayer_management(indentitypath,"indentitypath")

    arcpy.SelectLayerByAttribute_management("indentitypath",where_clause=where_clause)

    tmpnum =  int(arcpy.GetCount_management("indentitypath").getOutput(0))
    xzknum = int(arcpy.GetCount_management(xzkpath).getOutput(0))

    if xzknum != tmpnum:

        arcpy.AddMessage("3_现状库与初始库未套合，或包含重叠图斑 现状库数量：%s,临时图层数量：%s"%(xzknum,tmpnum))

        arcpy.AddMessage("3_创建平均宽度")
        createWidth(indentitypath)

        arcpy.AddMessage("3_收集错误图斑")
        arcpy.SetProgressor('step','3_收集错误图斑',0,int(arcpy.GetCount_management(indentitypath).getOutput(0)),1)
        targetValueList = collectError(indentitypath)

        arcpy.AddMessage("3_标记错误图斑")
        arcpy.SetProgressor('step','3_标记错误图斑',0,int(arcpy.GetCount_management(xzkpath).getOutput(0)),1)
        markError(xzkpath,targetValueList)

        arcpy.AddMessage("3_输出并删除错误图斑")
        outputError(xzkpath,errorpath)

def collectCskData(indentitypath):
    """收集现状库图斑数据"""

    fields = ["TSTYBM","BSM","ZLDWDM","DLBM","CZCSXM","BSM_1","ZLDWDM_1","SJDLBM","CZCSXM_1","cskmianji","SHAPE_AREA"]
    showFields = ["tstybm","cskbsm","cskzldwdm","cskdlbm","cskczcsxm","xzkbsm","xzkzldwdm","xzksjdlbm","xzkczcsxm","cskmianji","SHAPE_AREA"]

    where_clause="TSTYBM is not null and TSTYBM <> ''"

    datas = {}

    with arcpy.da.SearchCursor(indentitypath,fields,where_clause=where_clause) as cursor:

        for row in cursor:

            data = dict(zip(showFields,row))

            if data["tstybm"] in datas:

                if data["SHAPE_AREA"] >datas[data["tstybm"]]["SHAPE_AREA"]:

                    datas[data["tstybm"]] = data
                
            else:

                datas[data["tstybm"]] = data

    return datas

def UpdateTarget(xzkpath,datas):
    """更新还原初始库属性"""

    bsmDifference = []
    zldwdmDifference = []
    sjdlbmDifference = []
    czcsxmDifference = []
    tstybmDifference = []

    arcpyDeal.ensureFields(xzkpath,["cskmianji"],type="DOUBLE")

    fields = ["TSTYBM","cskbsm","cskzldwdm","cskdlbm","cskczcsxm","cskmianji","BSM","ZLDWDM","SJDLBM","CZCSXM"]

    arcpyDeal.ensureFields(xzkpath,fields)

    fields.append("SHAPE@AREA")

    cursor = arcpy.da.UpdateCursor(xzkpath,fields,where_clause=" TSTYBM is not null",sql_clause=(None, 'ORDER BY TSTYBM'))

    for row in cursor:

        arcpy.SetProgressorPosition()

        tstybm = row[0]

        if tstybm not in datas:

            tstybmDifference.append(tstybm)

            row[1] = row[6]
            row[2] = row[7]
            row[3] = row[8]
            row[4] = row[9]
            row[5] = row[10]

            cursor.updateRow(row)

            continue

        if datas[tstybm]["cskbsm"] != datas[tstybm]["xzkbsm"]:

            bsmDifference.append(tstybm)

        if datas[tstybm]["cskzldwdm"] != datas[tstybm]["xzkzldwdm"]:

            zldwdmDifference.append(tstybm)

        if datas[tstybm]["cskdlbm"] != datas[tstybm]["xzksjdlbm"]:

            sjdlbmDifference.append(tstybm)
            zldwdmDifference.append(tstybm)

        if datas[tstybm]["cskczcsxm"] != datas[tstybm]["xzkczcsxm"]:

            czcsxmDifference.append(tstybm)

        row[1] = datas[tstybm]["cskbsm"]
        row[2] = datas[tstybm]["cskzldwdm"]
        row[3] = datas[tstybm]["cskdlbm"]
        row[4] = datas[tstybm]["cskczcsxm"]
        row[5] = datas[tstybm]["cskmianji"]

        cursor.updateRow(row)

    arcpy.AddMessage("3_共有%s个图斑无初始库图斑"%(len(tstybmDifference)))
    arcpy.AddMessage("3_共有%s个图斑bsm不同"%(len(bsmDifference)))
    arcpy.AddMessage("3_共有%s个图斑zldwdm不同"%(len(zldwdmDifference)))
    arcpy.AddMessage("3_共有%s个图斑sjdlbm不同"%(len(sjdlbmDifference)))
    arcpy.AddMessage("3_共有%s个图斑czcsxm不同"%(len(czcsxmDifference)))

    # arcpy.AddMessage("3_"+json.dumps(tstybmDifference))
    # arcpy.AddMessage("3_"+json.dumps(bsmDifference))
    # arcpy.AddMessage("3_"+json.dumps(zldwdmDifference))
    # arcpy.AddMessage("3_"+json.dumps(sjdlbmDifference))

if __name__ == "__main__":
    
    arcpy.AddMessage("3_开始还原初始库属性")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)
    cskpath = arcpy.GetParameterAsText(2)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    indentitypath = "indentitypath_3"
    errorpath = "error_3"

    arcpy.AddMessage("3_计算初始库面积")
    getCskArea(cskpath)

    #标识分析
    arcpy.AddMessage("3_标识分析")
    arcpy.Identity_analysis (cskpath,xzkpath,indentitypath,cluster_tolerance="0.01")
    
    #判断是否有产出初始库范围的错误图斑
    arcpy.AddMessage("3_判断初始库和现状库是否套合")
    judgeError(xzkpath,indentitypath,errorpath)

    #收集
    arcpy.AddMessage("3_收集现状库图斑数据")
    arcpy.SetProgressor('step','3_收集现状库图斑数据',0,int(arcpy.GetCount_management(indentitypath).getOutput(0)),1)
    matchedDataDict = collectCskData(indentitypath)
    
    #还原数据
    arcpy.AddMessage("3_还原数据")
    arcpy.SetProgressor('step','3_还原数据',0, int(arcpy.GetCount_management(xzkpath).getOutput(0)),1)
    UpdateTarget(xzkpath,matchedDataDict)

    arcpy.SetParameterAsText(3,xzkpath)
    arcpy.AddMessage("3_结束还原初始库属性")