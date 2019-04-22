#-*- coding:utf-8 -*-
#encoding:utf-8
#!python

import arcpy,json,dealNone,arcpyDeal,pathArgs

def judgeTBLX(oldTag,zzjztb):

    value = ""

    if oldTag == u'�ص�˲�':

        value = u'��һ��ͼ��'

    elif oldTag == u'һ��˲�' and zzjztb == '0':

        value = u'һ��˲�ͼ��'

    elif oldTag == u'һ��˲�' and zzjztb == '1':

        value = u'������֤ͼ��'

    return value

def updateDatas(targetpath):
    """����OLDTAG��ZZJZTB����ͼ�߱仯����,���ͼ��Ԥ��ţ�tbybh��"""

    #���ݲ�ѯ�����ݸ�������
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

    arcpy.AddMessage("6.1_���ݸ���")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step',"6.1_���ݸ���",0,count,1)

    updateDatas(targetpath)

if __name__ == "__main__":
    
    arcpy.AddMessage("6.2_��ʼɾ�����κα仯��ͼ��")

    targetpath = arcpy.GetParameterAsText(0)

    start(targetpath)

    arcpy.SetParameterAsText(1,targetpath)

    arcpy.AddMessage("6.2_����")