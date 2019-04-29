#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,json

def calculteBSM(xzkpath,xzkdissolvepath):
    """����BSM�����Ƿ�ȱʧ"""

    searchFields = ["cskbsm"]

    originLackBSMList = []
    outputBSMList = []

    with arcpy.da.SearchCursor(xzkdissolvepath,searchFields) as cursor:

        for row in cursor:

            if row[0] not in outputBSMList:

                outputBSMList.append(row[0])

    arcpy.AddMessage("�����ں�ͼ����%s��BSM"%(len(outputBSMList)))

    with arcpy.da.SearchCursor(xzkpath,searchFields) as cursor:

        for row in cursor:

            if row[0] not in outputBSMList and row[0] not in originLackBSMList:

                originLackBSMList.append(row[0])

    arcpy.AddMessage("��%s��BSMȱʧ"%(len(originLackBSMList)))
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

            arcpy.AddMessage("��ʼ��BSMΪ��%s ��ͼ���ظ���ֵ"%oldbsm)

def takeBsmBack(xzkdissolvepath,originLackBSMList):
    """��ȱʧ��BSM�һ���"""

    table = "xzkdissolvepath"

    arcpy.MakeFeatureLayer_management ( xzkdissolvepath, table)

    for i in range(len(originLackBSMList)):

        bsm = originLackBSMList[i]

        arcpy.AddMessage("�����%s��ȱʧ��BSM"%i)

        traverseLayer(bsm,xzkdissolvepath,table)

if __name__ == "__main__":
    """�ں�ǰ��BSM����һ��Ҫ�Ե���"""
    
    arcpy.AddMessage("11_��ʼ���·�Χ")
    
    xzkpath = arcpy.GetParameterAsText(0)
    xzkdissolvepath = arcpy.GetParameterAsText(1)

    arcpy.AddMessage("11_����BSM")
    originLackBSMList = calculteBSM(xzkpath,xzkdissolvepath)

    arcpy.AddMessage("11_��ԭBSM")
    takeBsmBack(xzkdissolvepath,originLackBSMList)
        
    arcpy.SetParameterAsText(2,xzkdissolvepath)
    arcpy.AddMessage("11_�������·�Χ")