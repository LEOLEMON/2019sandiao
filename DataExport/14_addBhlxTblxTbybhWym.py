#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,json

def judgeTBLX(oldTag,zzjztb):

    value = ""

    if oldTag == u'�ص�˲�':

        value = u'��һ��ͼ��'

    elif oldTag == u'һ��˲�' and zzjztb == '0':

        value = u'һ��˲�ͼ��'

    elif oldTag == u'һ��˲�' and zzjztb == '1':

        value = u'������֤ͼ��'

    return value

def judgeBHLX(shuvary,shpvary)

if __name__ == "__main__":
    
    arcpy.AddMessage("12_��ʼ����ֶ�")
    
    xzkpath = arcpy.GetParameterAsText(0)

    searchFields = ['OLDTAG','ZZJZTB','TBLX'��"TBYBH",'TBWYM',"TSTYBM",'shuvary','shpvary',"BHLX"]

    arcpyDeal.ensureFields(xzkpath,searchFields)

    count = int(arcpy.GetCount_management(targetpath).getOutput(0))
    arcpy.SetProgressor('step',"12_�ֶ�ֵ����",0,count,1)

    number = 0
    
    with arcpy.da.UpdateCursor(targetpath,searchFields) as UpdateCursor:

        for updaterow in UpdateCursor:

            number += 1 

            data = dict(zip(searchFields,updaterow))

            oldTag = data["OLDTAG"]
            zzjztb = data["ZZJZTB"]

            shuvary = data["shuvary"]
            shpvary = data["shpvary"]

            TBLX = judgeTBLX(oldTag,zzjztb)
            TBWYM = "00000000"[0:8-len(str(number))]+str(number)

            updaterow[2] = TBLX
            updaterow[3] = TBWYM
            updaterow[4] = updaterow[5]

            UpdateCursor.updateRow(updaterow)

            arcpy.SetProgressorPosition()

    arcpy.SetParameterAsText(1,xzkpath)
    arcpy.AddMessage("12_��������ֶ�")