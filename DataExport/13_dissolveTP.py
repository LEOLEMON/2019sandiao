#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy

def getTstybmRelation(tablelist):
    """��ȡ�¾�ͼ��ͳһ������չ�ϵ"""

    relationDict = {}

    for i in range(len(tablelist)):

        table = tablelist[i]

        with arcpy.da.SearchCursor(table,["oldfield","newfields"]) as cur:

            for row in cur:

                if row[0] == row[1]:

                    continue

                #����ɵ�TSTYBM���ϴ��ںϱ仯����µ�TSTYBM���Ǿ�ɾ����ǰ��ļ�¼
                if row[0] in relationDict:

                    old = relationDict[row[0]]

                    relationDict.pop(row[0])

                    if row[1] in relationDict:

                        relationDict[row[1]] =  relationDict[row[1]] + old

                    else:

                        relationDict[row[1]] = old

                if row[1] in relationDict:

                    relationDict[row[1]].append(row[0])

                else:
                    
                    relationDict[row[1]] = [row[0]]

    reverseRelationDict = {}

    for key in relationDict:

        for i in range(len(relationDict[key])):

            reverseRelationDict[relationDict[key][i]] = key

    arcpy.AddMessage(reverseRelationDict)

    return reverseRelationDict

def updateTSTYBM(tp,reverseRelationDict):

    arcpy.SetProgressor('step','13_����TPֵ',0,int(arcpy.GetCount_management(tp).getOutput(0)),1)

    with arcpy.da.UpdateCursor(tp,"TSTYBM") as cur:

        for row in cur:

            if row[0] in reverseRelationDict:

                row[0] = reverseRelationDict[row[0]]

                cur.updateRow(row)
                
            arcpy.SetProgressorPosition()

if __name__ == "__main__":
    
    arcpy.AddMessage("13_��ʼת����Ƭ��tstybm")
    
    tp = arcpy.GetParameterAsText(0)
    relationpath_6 = arcpy.GetParameterAsText(1)
    relationpath_7 = arcpy.GetParameterAsText(2)
    relationpath_11 = arcpy.GetParameterAsText(3)

    tablelist = [relationpath_6,relationpath_7,relationpath_11]

    arcpy.AddMessage("����¾�TSTYBM���չ�ϵ")
    reverseRelationDict = getTstybmRelation(tablelist)

    arcpy.AddMessage("������Ƭ��TSTYBM")
    updateTSTYBM(tp,reverseRelationDict)

    arcpy.SetParameterAsText(4,tp)
    arcpy.AddMessage("13_��ʼת����Ƭ��tstybm")

    