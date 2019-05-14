#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,json

def calculteBSM(xzkpath,xzkdissolvepath):
    """计算BSM数量是否缺失"""

    count = int(arcpy.GetCount_management(xzkpath).getOutput(0)) + int(arcpy.GetCount_management(xzkdissolvepath).getOutput(0))

    arcpy.SetProgressor('step','12_丢失BSM',0,count,1)

    searchFields = ["cskbsm"]

    originLackBSMList = []
    outputBSMList = []

    with arcpy.da.SearchCursor(xzkdissolvepath,searchFields) as cursor:

        for row in cursor:

            if row[0] not in outputBSMList:

                outputBSMList.append(row[0])

            arcpy.SetProgressorPosition()

    arcpy.AddMessage("现在融合图层有%s个BSM"%(len(outputBSMList)))

    with arcpy.da.SearchCursor(xzkpath,searchFields) as cursor:

        for row in cursor:

            if row[0] not in outputBSMList and row[0] not in originLackBSMList:

                originLackBSMList.append(row[0])
                
            arcpy.SetProgressorPosition()

    arcpy.AddMessage("有%s个BSM缺失"%(len(originLackBSMList)))
    arcpy.AddMessage(originLackBSMList)

    return originLackBSMList

def traverseLayer(lackbsm,xzkdissolvepath,table,bsmlist=[]):

    where_clause = " bsm_list like '%"+lackbsm+"%' "

    oldbsm = ""

    bsmlist.append(lackbsm)

    with arcpy.da.UpdateCursor(xzkdissolvepath,["bsm_list","cskbsm"],where_clause) as cur:

        for row in cur:

            if row[1] in bsmlist:

                continue

            else:

                oldbsm = row[1]

                row[1] = lackbsm

                cur.updateRow(row)

                break

    where_clause = " cskbsm = '"+oldbsm+"' "

    arcpy.SelectLayerByAttribute_management(table,selection_type="CLEAR_SELECTION")

    arcpy.SelectLayerByAttribute_management(table,where_clause=where_clause)

    count = int(arcpy.GetCount_management(table).getOutput(0))

    arcpy.AddMessage("缺失的BSM：%s,被替换的BSM：%s,被替换的BSM剩余总数：%s,bsmlist长度：%s,bsmlist包含内容:%s"%(lackbsm.encode(),oldbsm.encode(),count,len(bsmlist),json.dumps(bsmlist)))

    if count == 0:

        if oldbsm not in bsmlist:

            traverseLayer(oldbsm,xzkdissolvepath,table,bsmlist)

        else:

            arcpy.AddMessage("初始库BSM为：%s 的图斑重复赋值"%oldbsm)

def takeBsmBack(xzkdissolvepath,originLackBSMList):
    """把缺失的BSM找回来"""

    arcpy.SetProgressor('step','12_把缺失的BSM找回来',0,len(originLackBSMList),1)

    table = "xzkdissolvepath_12"

    arcpy.MakeFeatureLayer_management ( xzkdissolvepath, table)

    for i in range(len(originLackBSMList)):

        bsm = originLackBSMList[i]

        arcpy.AddMessage("处理第%s个缺失得BSM"%(i+1))

        traverseLayer(bsm,xzkdissolvepath,table,[])

        arcpy.SetProgressorPosition()

if __name__ == "__main__":
    """融合分组前后BSM总数一定要对的上"""
    
    arcpy.AddMessage("12_开始检查BSM")
    
    xzkpath = arcpy.GetParameterAsText(0)
    xzkdissolvepath = arcpy.GetParameterAsText(1)

    arcpy.AddMessage("12_计算BSM")
    originLackBSMList = calculteBSM(xzkpath,xzkdissolvepath)

    arcpy.AddMessage("12_还原BSM")
    takeBsmBack(xzkdissolvepath,originLackBSMList)
        
    arcpy.SetParameterAsText(2,xzkdissolvepath)
    arcpy.AddMessage("12_结束检查BSM")