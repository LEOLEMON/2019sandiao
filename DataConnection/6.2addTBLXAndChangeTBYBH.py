#-*- coding:utf-8 -*-
#encoding:utf-8
#!python

import arcpy,json,dealNone,arcpyDeal,pathArgs

def judgeTBLX(oldTag,zzjztb):

    value = ""

    if oldTag == u'重点核查':

        value = u'不一致图斑'

    elif oldTag == u'一般核查' and zzjztb == '0':

        value = u'一般核查图斑'

    elif oldTag == u'一般核查' and zzjztb == '1':

        value = u'自主举证图斑'

    return value

def updateDatas(targetpath):
    """根据OLDTAG和ZZJZTB更新图斑变化类型,添加图斑预编号（tbybh）"""

    #根据查询的数据更新数据
    searchFields = ['OLDTAG','ZZJZTB',"exp_tblx","exp_tbybh","exp_tbwym","TSTYBM"]

    arcpyDeal.ensureFields(targetpath,searchFields)

    number = 0

    with arcpy.da.UpdateCursor(targetpath,searchFields) as UpdateCursor:

        for updaterow in UpdateCursor:

            number += 1 

            oldTag = updaterow[0]
            zzjztb = updaterow[1]

            exp_tblx = judgeTBLX(oldTag,zzjztb)
            exp_tbybh = "00000000"[0:8-len(str(number))]+str(number)

            updaterow[2] = exp_tblx
            updaterow[3] = exp_tbybh
            updaterow[4] = updaterow[5]
        
            UpdateCursor.updateRow(updaterow)

            arcpy.SetProgressorPosition()

def start(targetpath):

    arcpy.AddMessage("6.1_数据更新")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step',"6.1_数据更新",0,count,1)

    updateDatas(targetpath)

if __name__ == "__main__":
    
    arcpy.AddMessage("6.2_开始删除无任何变化的图斑")

    targetpath = arcpy.GetParameterAsText(0)

    start(targetpath)

    arcpy.SetParameterAsText(1,targetpath)

    arcpy.AddMessage("6.2_结束")