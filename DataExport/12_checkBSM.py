#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,json

def calculteBSM(xzkpath,xzkdissolvepath):
    """����BSM�����Ƿ�ȱʧ"""

    count = int(arcpy.GetCount_management(xzkpath).getOutput(0)) + int(arcpy.GetCount_management(xzkdissolvepath).getOutput(0))

    arcpy.SetProgressor('step','12_��ʧBSM',0,count,1)

    searchFields = ["cskbsm"]

    originLackBSMList = []
    outputBSMList = []

    with arcpy.da.SearchCursor(xzkdissolvepath,searchFields) as cursor:

        for row in cursor:

            if row[0] not in outputBSMList:

                outputBSMList.append(row[0])

            arcpy.SetProgressorPosition()

    arcpy.AddMessage("�����ں�ͼ����%s��BSM"%(len(outputBSMList)))

    with arcpy.da.SearchCursor(xzkpath,searchFields) as cursor:

        for row in cursor:

            if row[0] not in outputBSMList and row[0] not in originLackBSMList:

                originLackBSMList.append(row[0])
                
            arcpy.SetProgressorPosition()

    arcpy.AddMessage("��%s��BSMȱʧ"%(len(originLackBSMList)))
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

    arcpy.AddMessage("ȱʧ��BSM��%s,���滻��BSM��%s,���滻��BSMʣ��������%s,bsmlist���ȣ�%s,bsmlist��������:%s"%(lackbsm.encode(),oldbsm.encode(),count,len(bsmlist),json.dumps(bsmlist)))

    if count == 0:

        if oldbsm not in bsmlist:

            traverseLayer(oldbsm,xzkdissolvepath,table,bsmlist)

        else:

            arcpy.AddMessage("��ʼ��BSMΪ��%s ��ͼ���ظ���ֵ"%oldbsm)

def takeBsmBack(xzkdissolvepath,originLackBSMList):
    """��ȱʧ��BSM�һ���"""

    arcpy.SetProgressor('step','12_��ȱʧ��BSM�һ���',0,len(originLackBSMList),1)

    table = "xzkdissolvepath_12"

    arcpy.MakeFeatureLayer_management ( xzkdissolvepath, table)

    for i in range(len(originLackBSMList)):

        bsm = originLackBSMList[i]

        arcpy.AddMessage("�����%s��ȱʧ��BSM"%(i+1))

        traverseLayer(bsm,xzkdissolvepath,table,[])

        arcpy.SetProgressorPosition()

if __name__ == "__main__":
    """�ںϷ���ǰ��BSM����һ��Ҫ�Ե���"""
    
    arcpy.AddMessage("12_��ʼ���BSM")
    
    xzkpath = arcpy.GetParameterAsText(0)
    xzkdissolvepath = arcpy.GetParameterAsText(1)

    arcpy.AddMessage("12_����BSM")
    originLackBSMList = calculteBSM(xzkpath,xzkdissolvepath)

    arcpy.AddMessage("12_��ԭBSM")
    takeBsmBack(xzkdissolvepath,originLackBSMList)
        
    arcpy.SetParameterAsText(2,xzkdissolvepath)
    arcpy.AddMessage("12_�������BSM")