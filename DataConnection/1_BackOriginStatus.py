#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,arcpyDeal,pathArgs

def ensureSHFields(targetpath):

    fields = ["DLBM_1","GDZZSXMC_1","TBXHMC_1","GDLX_1"]

    arcpy.ensureFields(targetpath,fields)

def deleteFields(targetpath):
    """ɾ�������ֶ�"""

    delFieldsList = ["unionfzh","exp_bsm","exp_tbbh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm","exp_tblx","exp_tbwym","bhlx","exp_wjzlx","fzh"]

    arcpyDeal.deleteFields(targetpath,delFieldsList)

def collectIntersectFeauture(TempAnalysis):
    """������ͬͼ��ͳһ���������˭���������Ǿʹ���ԭ��ͼ�������ĸ���ʼ��ͼ��"""

    fields = ["TSTYBM","BSM","BSM_1","ZLDWDM","SJDLBM","ZLDWDM_1","DLBM_12","SHAPE@AREA"]
    showFields = ["tstybm","bsm","bsm_1","zldwdm","sjdlbm","zldwdm_1","sjdlbm_1","area"]

    cursor = arcpy.da.SearchCursor(TempAnalysis,fields,sql_clause=(None, 'ORDER BY TSTYBM'))

    matchedData = {}
    
    matchedDataDict = {}

    arcpyDeal.checkField(TempAnalysis,fields)

    for row in cursor:
        
        arcpy.SetProgressorPosition()

        newRowData = {}

        for i in range(len(showFields)):

            newRowData[showFields[i]] = row[i]

        if matchedData == {}:

            matchedData = newRowData

            continue

        if matchedData['tstybm'] != newRowData['tstybm']:

            matchedDataDict[matchedData['tstybm']] = matchedData

            matchedData = newRowData

            continue
                
        if matchedData['area'] < newRowData['area']:

            matchedData = newRowData

    matchedDataDict[matchedData['tstybm']] = matchedData

    arcpy.Delete_management(TempAnalysis)

    return matchedDataDict

def UpdateTarget(targetpath,matchedDataDict):
    """���»�ԭ��ʼ������"""

    bsmDifference = []
    zldwdmDifference = []
    sjdlbmDifference = []
    tstybmDifference = []

    fields = ["TSTYBM","exp_bsm","exp_sjdlbm","exp_zldwdm"]
    fields = ["tstybm","exp_bsm","exp_sjdlbm","exp_zldwdm"]

    arcpyDeal.ensureFields(targetpath,fields)

    cursor = arcpy.da.UpdateCursor(targetpath,fields,sql_clause=(None, 'ORDER BY TSTYBM'))

    for row in cursor:

        arcpy.SetProgressorPosition()

        tstybm = row[0]

        if tstybm not in matchedDataDict:

            tstybmDifference.append(tstybm)

            continue

        if matchedDataDict[tstybm]["bsm"] != matchedDataDict[tstybm]["bsm_1"]:

            bsmDifference.append(tstybm)

        if matchedDataDict[tstybm]["zldwdm"] != matchedDataDict[tstybm]["zldwdm_1"]:

            zldwdmDifference.append(tstybm)

        if matchedDataDict[tstybm]["sjdlbm"] != matchedDataDict[tstybm]["sjdlbm_1"]:

            sjdlbmDifference.append(tstybm)

        row[1] = matchedDataDict[tstybm]["bsm_1"]
        row[2] = matchedDataDict[tstybm]["sjdlbm_1"]
        row[3] = matchedDataDict[tstybm]["zldwdm_1"]

        cursor.updateRow(row)

    arcpy.AddMessage("1_����%s��ͼ��bsm��ͬ"%(len(bsmDifference)))
    arcpy.AddMessage("1_����%s��ͼ��zldwdm��ͬ"%(len(zldwdmDifference)))
    arcpy.AddMessage("1_����%s��ͼ��sjdlbm��ͬ"%(len(sjdlbmDifference)))
    arcpy.AddMessage("1_����%s��ͼ���޳�ʼ��ͼ��"%(len(tstybmDifference)))

    arcpy.AddMessage("1_"+json.dumps(bsmDifference))
    arcpy.AddMessage("1_"+json.dumps(zldwdmDifference))
    arcpy.AddMessage("1_"+json.dumps(sjdlbmDifference))
    arcpy.AddMessage("1_"+json.dumps(tstybmDifference))

def start(targetpath,cskpath,tempname):

    #ȷ������ֶ��Ƿ����
    arcpy.AddMessage("1_ȷ������ֶ�")
    deleteFields(targetpath)

    #ɾ�������ܹ��������ֶ�
    arcpy.AddMessage("1_ɾ���ֶ�")
    deleteFields(targetpath)

    #�ཻ����
    arcpy.AddMessage("1_�ཻ����")
    
    arcpy.Intersect_analysis ([targetpath, cskpath],tempname, "ALL", "", "")
    
    #�ռ�
    arcpy.AddMessage("1_�ռ�")
    result = arcpy.GetCount_management(tempname)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','1_�ռ�',0,count,1)

    matchedDataDict = collectIntersectFeauture(tempname)
    
    #��ԭ����
    arcpy.AddMessage("1_��ԭ����")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','1_��ԭ����',0,count,1)

    UpdateTarget(targetpath,matchedDataDict)
   
if __name__ == "__main__":
    
    arcpy.AddMessage("1_��ʼ��ԭ��ʼ������")
    
    arcpy.env.overwriteOutput = True

    targetpath = arcpy.GetParameterAsText(0)
    cskpath = arcpy.GetParameterAsText(1)

    enviroment = arcpy.GetParameterAsText(2)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = enviroment

    tempname = "output_01"

    start(targetpath,cskpath,tempname)

    arcpy.SetParameterAsText(3,targetpath)

    arcpy.AddMessage("1_������ԭ��ʼ������")