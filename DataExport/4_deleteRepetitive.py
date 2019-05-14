#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal,shapely
from shapely.wkt import loads

def compary(lastbsm,list):
    """把数据内所有数据进行对比，得到哪些数据需要删除，哪些数据需要保留,1保留，0删除"""

    if len(list) == 1:

        list[0]["repetitive"] = "1"

        return

    else:

        for i in range(len(list)):
            
            shpi = loads(list[i]["SHAPE@WKT"])

            if list[i]["repetitive"] == "":

                list[i]["repetitive"] = "1"

            for k in range(i+1,len(list)):

                if list[k]["repetitive"] == "0":

                    continue

                shpk = loads(list[k]["SHAPE@WKT"])

                intersection =  shpi.intersection(shpk)

                ratio1 = intersection.area/shpi.area
                ratio2 = intersection.area/shpk.area
                
                # arcpy.AddMessage("%s,%s,%s,%s,%s,%s,%s,%s"%(list[i]['TSTYBM'],i,k,str(ratio1 > 0.1),str(ratio2 > 0.1),intersection.area > 10,list[i]["SHAPE_AREA"],list[k]["SHAPE_AREA"]))
                
                #由于数据事先已按照时间倒序，所以排在最前面的数据如果与后面的数据重叠，则把前面的数据保留，后面的删除
                if ratio1 > 0.1 or ratio2 > 0.1 or intersection.area > 10:
                    
                    list[k]["repetitive"] = "0"

                else:

                    list[k]["repetitive"] = "1"

    return list
                    
def collectRepetitive(xzkpath):
    """收集需要删除的图斑"""

    searchFields = ["TSTYBM","cskbsm","repetitive"]

    sql_clause = (None," ORDER BY cskbsm,SHAPE_AREA DESC")

    arcpyDeal.deleteFields(xzkpath,["repetitive"])
    arcpyDeal.ensureFields(xzkpath,searchFields)

    searchFields.append("SHAPE@WKT")
    searchFields.append("SHAPE_AREA")

    targetValueDict = {}

    datas = {}

    lastbsm = ""

    for row in arcpy.da.SearchCursor(xzkpath,searchFields,sql_clause= sql_clause):
        
        arcpy.SetProgressorPosition()

        data = dict(zip(searchFields,row))

        data["repetitive"] = dealNone.dealNoneAndBlank(data["repetitive"])

        if lastbsm == "":

            lastbsm = data["cskbsm"]

        elif lastbsm != data["cskbsm"]:

            compary(lastbsm,datas[lastbsm])

            lastbsm = data["cskbsm"]

        if data["cskbsm"] not in datas:

            datas[data["cskbsm"]] = [data]

        else:

            datas[data["cskbsm"]].append(data)

    compary(lastbsm,datas[lastbsm])

    for key in datas:

        for data in datas[key]:

            targetValueDict[data["TSTYBM"]] = data["repetitive"]

    return targetValueDict

def markRepetitive(xzkpath,targetValueDict):
    """标记需要删除的图斑"""

    searchFields = ["TSTYBM","repetitive"]
    
    arcpyDeal.ensureFields(xzkpath,searchFields)

    with arcpy.da.UpdateCursor(xzkpath,searchFields) as cur:

        for row in cur:

            TSTYBM = row[0]

            row[1] = targetValueDict[TSTYBM]

            cur.updateRow(row)

            arcpy.SetProgressorPosition() 

def outputRepetitive(xzkpath,repetitivepath):
    """输出图层"""

    where_clause = "repetitive = '0'"

    arcpy.MakeFeatureLayer_management(xzkpath,"xzkpath")

    arcpy.SelectLayerByAttribute_management("xzkpath",where_clause=where_clause)

    arcpy.CopyFeatures_management("xzkpath",repetitivepath)

    arcpy.DeleteFeatures_management("xzkpath")

if __name__ == "__main__":
    
    arcpy.AddMessage("4_开始删除重叠图斑")

    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = enviroment

    repetitivepath = "repetitive_4"

    count = int(arcpy.GetCount_management(xzkpath).getOutput(0))
    arcpy.AddMessage("4_收集需要删除的图斑")
    arcpy.SetProgressor('step',"4_收集保留和需要删除的图斑",0,count,1)
    targetValueDict = collectRepetitive(xzkpath)

    arcpy.AddMessage("4_标记需要删除的图斑")
    arcpy.SetProgressor('step',"4_标记保留和需要删除的图斑",0,count,1)
    markRepetitive(xzkpath,targetValueDict)

    arcpy.AddMessage("4_输出需要删除的图斑")
    outputRepetitive(xzkpath,repetitivepath)

    arcpy.SetParameterAsText(2,xzkpath)

    arcpy.AddMessage("4_结束删除重叠图斑")