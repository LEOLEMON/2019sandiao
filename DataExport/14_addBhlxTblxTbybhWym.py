#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,json

def judgeTBLX(oldTag,zzjztb):

    value = ""

    if oldTag == u'重点核查':

        value = u'不一致图斑'

    elif oldTag == u'一般核查' and zzjztb == '0':

        value = u'一般核查图斑'

    elif oldTag == u'一般核查' and zzjztb == '1':

        value = u'自主举证图斑'

    return value

def judgeBHLX(shuvary,shpvary)

if __name__ == "__main__":
    
    arcpy.AddMessage("12_开始添加字段")
    
    xzkpath = arcpy.GetParameterAsText(0)

    searchFields = ['OLDTAG','ZZJZTB','TBLX'，"TBYBH",'TBWYM',"TSTYBM",'shuvary','shpvary',"BHLX"]

    arcpyDeal.ensureFields(xzkpath,searchFields)

    count = int(arcpy.GetCount_management(targetpath).getOutput(0))
    arcpy.SetProgressor('step',"12_字段值更新",0,count,1)

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
    arcpy.AddMessage("12_结束添加字段")