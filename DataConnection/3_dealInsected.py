#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal,shapely
from shapely.wkt import loads

def compary(list):
    """把数据内所有数据进行对比，得到哪些数据需要删除，哪些数据需要保留,1保留，0删除"""

    if len(list) == 1:

        list[0]["intersecrteddeal"] = "1"

        return

    else:

        #arcpy.AddMessage("%s,%s"%(list[0]["exp_bsm"],len(list)))

        for i in range(len(list)):
            
            shpi = loads(list[i]["SHAPE@WKT"])

            if list[i]["intersecrteddeal"] == "":

                list[i]["intersecrteddeal"] = "1"

            for k in range(i+1,len(list)):

                if list[k]["intersecrteddeal"] == "0":

                    continue

                shpk = loads(list[k]["SHAPE@WKT"])

                intersection =  shpi.intersection(shpk)

                ratio1 = intersection.area/shpi.area
                ratio2 = intersection.area/shpk.area
                
                #arcpy.AddMessage("%s,%s,%s,%s,%s"%(i,k,str(ratio1 > 0.1),str(ratio2 > 0.1),intersection.area > 10))
                
                #由于数据事先已按照时间倒序，所以排在最前面的数据如果与后面的数据重叠，则把前面的数据保留，后面的删除
                if ratio1 > 0.1 or ratio2 > 0.1 or intersection.area > 10:
                    
                    list[k]["intersecrteddeal"] = "0"

                else:

                    list[k]["intersecrteddeal"] = "1"

    return list
                    
def collect(targetpath):
    """收集保留和需要删除的图斑"""

    searchFields = ["TSTYBM","exp_bsm","intersecrteddeal","JZSJ"]

    sql_clause = (None," ORDER BY exp_bsm,JZSJ DESC")

    arcpyDeal.ensureFields(targetpath,searchFields)

    searchFields.append("SHAPE@WKT")

    targetValueDict = {}

    datas = {}

    lastbsm = ""

    for row in arcpy.da.SearchCursor(targetpath,searchFields,sql_clause= sql_clause):
        
        data = dict(zip(searchFields,row))

        data["intersecrteddeal"] = dealNone.dealNoneAndBlank(data["intersecrteddeal"])

        if lastbsm == "":

            lastbsm = data["exp_bsm"]

        elif lastbsm != data["exp_bsm"]:

            compary(datas[lastbsm])

            lastbsm = data["exp_bsm"]

        if data["exp_bsm"] not in datas:

            datas[data["exp_bsm"]] = [data]

        else:

            datas[data["exp_bsm"]].append(data)

        arcpy.SetProgressorPosition()

    compary(datas[lastbsm])

    for key in datas:

        for data in datas[key]:

            targetValueDict[data["TSTYBM"]] = data["intersecrteddeal"]

    return targetValueDict

def collect2(indentitypath):
    "从临时标识图层中，如果同一个图属统一编码包含多个初始库BSM，说明这个图斑超出了初始库范围，应该删除"

    where_clause = "(width > 0.1 or SHAPE_Area >1) and TSTYBM is not null and TSTYBM <> ''"

    sql_clause = (None,"ORDER BY TSTYBM,BSM DESC")

    searchFields = ["BSM","TSTYBM"]

    cursor = arcpy.da.SearchCursor(indentitypath, searchFields,where_clause = where_clause,sql_clause = sql_clause)

    lasttstybm = {"tstybm":"","bsm":[]}
    datas = []
    targetValueList = []

    number = 0

    for row in cursor:
        
        number += 1

        data = dict(zip(searchFields,row))

        arcpy.AddMessage("%s,%s,%s,%s,%s,%s"%(number,lasttstybm["tstybm"],str(lasttstybm["tstybm"] == ""),str(lasttstybm["tstybm"] != data["TSTYBM"]),str(len(lasttstybm["bsm"]) > 1),str(lasttstybm["tstybm"]  == data["TSTYBM"])))

        if lasttstybm["tstybm"] == "":

            lasttstybm["tstybm"] =  data["TSTYBM"]
            lasttstybm["bsm"].append(data["BSM"])

        elif lasttstybm["tstybm"] != data["TSTYBM"]:

            if len(lasttstybm["bsm"]) > 1:

                targetValueList.append(lasttstybm["tstybm"])

            lasttstybm["tstybm"] =  data["TSTYBM"]
            lasttstybm["bsm"].append(data["BSM"])

        elif lasttstybm["tstybm"]  == data["TSTYBM"]:

            targetValueList.append(lasttstybm["tstybm"])

    if len(lasttstybm["bsm"]) > 1:

        targetValueList.append(lasttstybm["tstybm"])

    return targetValueList

def mark(targetpath,targetValueDict,targetValueList):
    """标记保留和需要删除的图斑"""

    searchFields = ["TSTYBM","intersecrteddeal"]

    cur = arcpy.da.UpdateCursor(targetpath,searchFields)

    for row in cur:

        TSTYBM = row[0]

        if TSTYBM in targetValueList:

            row[1] = "1"

        else:

            row[1] = targetValueDict[TSTYBM]

        cur.updateRow(row)

        arcpy.SetProgressorPosition() 

def createLayer(targetpath,outname,tempoutname):
    """根据标记生成临时图层和输出图层"""

    where_clause1 =  " intersecrteddeal = '1'"
    where_clause2 =  " intersecrteddeal = '0'"

    arcpyDeal.createExistsTempLayer(targetpath,outname,where_clause = where_clause1)
    arcpyDeal.createExistsTempLayer(targetpath,tempoutname,where_clause = where_clause2)

def start(targetpath,indentitypath,outname,tempoutname):

    # arcpy.AddMessage("3_收集保留和需要删除的图斑")
    # result = arcpy.GetCount_management(targetpath)
    # count = int(result.getOutput(0))
    # arcpy.SetProgressor('step',"3_收集保留和需要删除的图斑",0,count,1)

    # targetValueDict = collect(targetpath)

    arcpy.AddMessage("3_收集超出初始库范围的图斑")
    targetValueList = collect2(indentitypath)

    # arcpy.AddMessage("3_标记保留和需要删除的图斑")
    # result = arcpy.GetCount_management(targetpath)
    # count = int(result.getOutput(0))
    # arcpy.SetProgressor('step',"3_标记保留和需要删除的图斑",0,count,1)

    # mark(targetpath,targetValueDict,targetValueList)

    # arcpy.AddMessage("3_生成输出图层")
    # createLayer(targetpath,outname,tempoutname)

if __name__ == "__main__":
    
    arcpy.AddMessage("3_开始删除重叠图斑")

    targetpath = arcpy.GetParameterAsText(0)
    indentitypath = arcpy.GetParameterAsText(1)
    enviroment = arcpy.GetParameterAsText(2)

    outname = "output_3"
    tempoutname = "output_3_temp"

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = enviroment

    start(targetpath,indentitypath,outname,tempoutname)

    arcpy.SetParameterAsText(3,outname)

    arcpy.AddMessage("3_结束")