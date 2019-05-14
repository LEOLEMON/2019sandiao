#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal,shapely
from shapely.wkt import loads

def compary(lastbsm,list):
    """���������������ݽ��жԱȣ��õ���Щ������Ҫɾ������Щ������Ҫ����,1������0ɾ��"""

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
                
                #�������������Ѱ���ʱ�䵹������������ǰ���������������������ص������ǰ������ݱ����������ɾ��
                if ratio1 > 0.1 or ratio2 > 0.1 or intersection.area > 10:
                    
                    list[k]["repetitive"] = "0"

                else:

                    list[k]["repetitive"] = "1"

    return list
                    
def collectRepetitive(xzkpath):
    """�ռ���Ҫɾ����ͼ��"""

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
    """�����Ҫɾ����ͼ��"""

    searchFields = ["TSTYBM","repetitive"]
    
    arcpyDeal.ensureFields(xzkpath,searchFields)

    with arcpy.da.UpdateCursor(xzkpath,searchFields) as cur:

        for row in cur:

            TSTYBM = row[0]

            row[1] = targetValueDict[TSTYBM]

            cur.updateRow(row)

            arcpy.SetProgressorPosition() 

def outputRepetitive(xzkpath,repetitivepath):
    """���ͼ��"""

    where_clause = "repetitive = '0'"

    arcpy.MakeFeatureLayer_management(xzkpath,"xzkpath")

    arcpy.SelectLayerByAttribute_management("xzkpath",where_clause=where_clause)

    arcpy.CopyFeatures_management("xzkpath",repetitivepath)

    arcpy.DeleteFeatures_management("xzkpath")

if __name__ == "__main__":
    
    arcpy.AddMessage("4_��ʼɾ���ص�ͼ��")

    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = enviroment

    repetitivepath = "repetitive_4"

    count = int(arcpy.GetCount_management(xzkpath).getOutput(0))
    arcpy.AddMessage("4_�ռ���Ҫɾ����ͼ��")
    arcpy.SetProgressor('step',"4_�ռ���������Ҫɾ����ͼ��",0,count,1)
    targetValueDict = collectRepetitive(xzkpath)

    arcpy.AddMessage("4_�����Ҫɾ����ͼ��")
    arcpy.SetProgressor('step',"4_��Ǳ�������Ҫɾ����ͼ��",0,count,1)
    markRepetitive(xzkpath,targetValueDict)

    arcpy.AddMessage("4_�����Ҫɾ����ͼ��")
    outputRepetitive(xzkpath,repetitivepath)

    arcpy.SetParameterAsText(2,xzkpath)

    arcpy.AddMessage("4_����ɾ���ص�ͼ��")