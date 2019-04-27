#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,sys
for p in sys.path:
    arcpy.AddMessage(p)
import json,arcpyDeal

def ensureSHFields(targetpath):

    fields = ["DLBM_1","GDZZSXMC_1","TBXHMC_1","GDLX_1"]

    arcpyDeal.ensureFields(targetpath,fields)

def deleteFields(targetpath):
    """ɾ�������ֶ�"""

    delFieldsList = ["unionfzh","exp_bsm","exp_tbbh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm","exp_tblx","exp_tbwym","bhlx","exp_wjzlx","fzh","intersecrteddeal"]

    arcpyDeal.deleteFields(targetpath,delFieldsList)

def createWidth(tempname):
    """����ƽ�����"""

    arcpy.AddField_management(tempname, "width", "Double")

    expression = "getClass(float(!SHAPE.area!),float(!SHAPE.length!))"
    codeblock = """def getClass(area,length):
        return area/length
        """

    arcpy.CalculateField_management(tempname,"width", expression, "PYTHON_9.3",codeblock)

def collectIntersectFeauture(TempAnalysis):
    """������ͬͼ��ͳһ���������˭���������Ǿʹ���ԭ��ͼ�������ĸ���ʼ��ͼ��"""

    fields = ["TSTYBM","BSM","ZLDWDM","DLBM","BSM_1","ZLDWDM_1","SJDLBM","SHAPE@AREA"]
    showFields = ["tstybm","bsm","zldwdm","sjdlbm","bsm_1","zldwdm_1","sjdlbm_1","area"]

    cursor = arcpy.da.SearchCursor(TempAnalysis,fields,where_clause=" TSTYBM is not null",sql_clause=(None, 'ORDER BY TSTYBM'))

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

    return matchedDataDict

def UpdateTarget(targetpath,matchedDataDict):
    """���»�ԭ��ʼ������"""

    bsmDifference = []
    zldwdmDifference = []
    sjdlbmDifference = []
    tstybmDifference = []

    fields = ["TSTYBM","exp_bsm","exp_sjdlbm","exp_zldwdm"]

    arcpyDeal.ensureFields(targetpath,fields)

    cursor = arcpy.da.UpdateCursor(targetpath,fields,where_clause=" TSTYBM is not null",sql_clause=(None, 'ORDER BY TSTYBM'))

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

        row[1] = matchedDataDict[tstybm]["bsm"]
        row[2] = matchedDataDict[tstybm]["sjdlbm"]
        row[3] = matchedDataDict[tstybm]["zldwdm"]

        cursor.updateRow(row)

    arcpy.AddMessage("2_����%s��ͼ��bsm��ͬ"%(len(bsmDifference)))
    arcpy.AddMessage("2_����%s��ͼ��zldwdm��ͬ"%(len(zldwdmDifference)))
    arcpy.AddMessage("2_����%s��ͼ��sjdlbm��ͬ"%(len(sjdlbmDifference)))
    arcpy.AddMessage("2_����%s��ͼ���޳�ʼ��ͼ��"%(len(tstybmDifference)))

    arcpy.AddMessage("2_"+json.dumps(bsmDifference))
    arcpy.AddMessage("2_"+json.dumps(zldwdmDifference))
    arcpy.AddMessage("2_"+json.dumps(sjdlbmDifference))
    arcpy.AddMessage("2_"+json.dumps(tstybmDifference))

def start(targetpath,cskpath,tempname):

    #ȷ������ֶ��Ƿ����
    arcpy.AddMessage("2_ȷ������ֶ�")
    ensureSHFields(targetpath)

    #ɾ�������ܹ��������ֶ�
    # arcpy.AddMessage("2_ɾ���ֶ�")
    # deleteFields(targetpath)

    #��ʶ����
    arcpy.AddMessage("2_�ཻ����")
    arcpy.Identity_analysis  (cskpath,targetpath,tempname, "ALL", "", "")

    arcpy.AddMessage("2_����ƽ�����")
    createWidth(tempname)
    
    #�ռ�
    arcpy.AddMessage("2_�ռ�")
    result = arcpy.GetCount_management(tempname)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','2_�ռ�',0,count,1)

    matchedDataDict = collectIntersectFeauture(tempname)
    
    #��ԭ����
    arcpy.AddMessage("2_��ԭ����")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','2_��ԭ����',0,count,1)

    UpdateTarget(targetpath,matchedDataDict)
   
if __name__ == "__main__":

    arcpy.AddMessage("2_��ʼ��ԭ��ʼ������")
    
    arcpy.env.overwriteOutput = True

    targetpath = arcpy.GetParameterAsText(0)
    cskpath = arcpy.GetParameterAsText(1)

    enviroment = arcpy.GetParameterAsText(2)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = enviroment

    tempname = "output_02"

    start(targetpath,cskpath,tempname)

    arcpy.SetParameterAsText(3,targetpath)
    arcpy.SetParameterAsText(4,tempname)

    arcpy.AddMessage("2_������ԭ��ʼ������")