#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,json

def calculteBSM(xzkpath,xzkdissolvepath):
    """计算BSM数量是否缺失"""

    searchFields = ["cskbsm"]

    originLackBSMList = []
    outputBSMList = []

    with arcpy.da.SearchCursor(xzkdissolvepath,searchFields) as cursor:

        for row in cursor:

            if row[0] not in outputBSMList:

                outputBSMList.append(row[0])

    arcpy.AddMessage("现在融合图层有%s个BSM"%(len(outputBSMList)))

    with arcpy.da.SearchCursor(xzkpath,searchFields) as cursor:

        for row in cursor:

            if row[0] not in outputBSMList and row[0] not in originLackBSMList:

                originLackBSMList.append(row[0])

    arcpy.AddMessage("有%s个BSM缺失"%(len(originLackBSMList)))
    arcpy.AddMessage(originLackBSMList)

    return originLackBSMList

def traverseLayer(bsm,xzkdissolvepath,table,bsmlist=[]):

    where_clause = " bsm_list like '%"+bsm+"%' "

    oldbsm = ""

    with arcpy.da.UpdateCursor(xzkdissolvepath,["bsm_list","cskbsm"],where_clause) as cur:

        for row in cur:

            oldbsm = row[1]

            row[1] = bsm

            cur.updateRow(row)

    where_clause = " cskbsm = '"+oldbsm+"' "

    arcpy.SelectLayerByAttribute_management(table,selection_type="CLEAR_SELECTION")

    arcpy.SelectLayerByAttribute_management(table,where_clause=where_clause)

    count = int(arcpy.GetCount_management(table).getOutput(0))

    arcpy.AddMessage("%s,%s"%(where_clause,count))

    if count == 0:

        arcpy.AddMessage("%s,%s,%s"%(oldbsm,len(bsmlist),json.dumps(bsmlist)))

        if oldbsm not in bsmlist:
            
            bsmlist.append(oldbsm)

            traverseLayer(bsm,xzkdissolvepath,table,bsmlist)

        else:

            arcpy.AddMessage("初始库BSM为：%s 的图斑重复赋值"%oldbsm)

def takeBsmBack(xzkdissolvepath,originLackBSMList):
    """把缺失的BSM找回来"""

    table = "xzkdissolvepath"

    arcpy.MakeFeatureLayer_management ( xzkdissolvepath, table)

    for i in range(len(originLackBSMList)):

        bsm = originLackBSMList[i]

        arcpy.AddMessage("处理第%s个缺失得BSM"%i)

        traverseLayer(bsm,xzkdissolvepath,table)

if __name__ == "__main__":
    """融合前后BSM总数一定要对的上"""
    
    arcpy.AddMessage("11_开始更新范围")
    
    xzkpath = arcpy.GetParameterAsText(0)
    xzkdissolvepath = arcpy.GetParameterAsText(1)

    arcpy.AddMessage("11_计算BSM")
    originLackBSMList = calculteBSM(xzkpath,xzkdissolvepath)

    arcpy.AddMessage("11_还原BSM")
    takeBsmBack(xzkdissolvepath,originLackBSMList)
        
    arcpy.SetParameterAsText(2,xzkdissolvepath)
    arcpy.AddMessage("11_结束更新范围")