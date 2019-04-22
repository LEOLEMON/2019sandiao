#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal

def collectUnionAttributes(targetpath):

    targetValueDict = {}

    tbwymRelation = {}

    datas = []
    searchFields = ["unionfzh","exp_bsm","exp_tbybh","exp_tbbh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm","exp_tblx","exp_tbwym","bhlx","exp_wjzlx","fzh"]
    tempFields = ["unionfzh","exp_bsm","exp_tbybh","exp_tbbh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm","exp_tblx","exp_tbwym","bhlx","exp_wjzlx","fzh"]

    arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,datas,sql_clause=(None,"ORDER BY unionfzh DESC"))

    lastdata = {}

    for data in datas:

        data["mergeTBWYM"] = []

        if lastdata == {}:

            targetValueDict[data["unionfzh"]] = data

            targetValueDict[data["unionfzh"]]["mergeTBWYM"].append(data["exp_tbwym"])

            lastdata = data

            continue
         
        if data["unionfzh"] != lastdata["unionfzh"]:

            targetValueDict[data["unionfzh"]] = data

        else:

            targetValueDict[data["unionfzh"]]["bhlx"] = "2" 
            targetValueDict[data["unionfzh"]]["exp_tblx"] = "��һ��ͼ��" 

        targetValueDict[data["unionfzh"]]["mergeTBWYM"].append(data["exp_tbwym"])

        lastdata = data

        arcpy.SetProgressorPosition()

    for t in targetValueDict:

        mergeTBWYM = targetValueDict[t]

        for m in mergeTBWYM:

            tbwymRelation[m] = targetValueDict[t]["exp_tbwym"]

    return targetValueDict,tbwymRelation

def updateTarget(targetpath,targetValueDict):
    """��������"""

    #���ݲ�ѯ�����ݸ�������
    searchFields = ["unionfzh","exp_bsm","exp_tbybh","exp_tbbh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm","exp_tblx","exp_tbwym","bhlx","exp_wjzlx","fzh"]

    arcpyDeal.ensureFields(targetpath,searchFields)

    UpdateCursor =  arcpy.da.UpdateCursor(targetpath,searchFields)

    for updaterow in UpdateCursor:
        
        unionfzh = updaterow[0]

        updaterow[1] = targetValueDict[unionfzh]['exp_bsm']
        updaterow[2] = targetValueDict[unionfzh]['exp_tbybh']
        updaterow[3] = targetValueDict[unionfzh]['exp_tbbh']
        updaterow[4] = targetValueDict[unionfzh]['exp_zldwdm']
        updaterow[5] = targetValueDict[unionfzh]['exp_dlbm']
        updaterow[6] = targetValueDict[unionfzh]['exp_dlmc']
        updaterow[7] = targetValueDict[unionfzh]['exp_gdlx']
        updaterow[8] = targetValueDict[unionfzh]['exp_tbxhdm']
        updaterow[9] = targetValueDict[unionfzh]['exp_tbxhmc']
        updaterow[10] = targetValueDict[unionfzh]['exp_gdzzsxdm']
        updaterow[11] = targetValueDict[unionfzh]['exp_gdzzsxmc']
        updaterow[12] = targetValueDict[unionfzh]['exp_czcsxm']
        updaterow[13] = targetValueDict[unionfzh]['exp_tblx']
        updaterow[14] = targetValueDict[unionfzh]['exp_tbwym']
        updaterow[15] = targetValueDict[unionfzh]['bhlx']
        updaterow[16] = targetValueDict[unionfzh]['exp_wjzlx']
        updaterow[17] = targetValueDict[unionfzh]['fzh']
    
        UpdateCursor.updateRow(updaterow)

        arcpy.SetProgressorPosition()

def mergePhoto(photopath,tbwymRelation):
    """�ϲ���Ƭ"""

    #���ݲ�ѯ�����ݸ�������
    searchFields = ["exp_tstybm"]

    with arcpy.da.UpdateCursor(photopath,searchFields) as UpdateCursor:

        for updaterow in UpdateCursor:

            exp_tstybm = updaterow[0]
            
            if exp_tstybm in tbwymRelation:

                updaterow[0] = tbwymRelation[exp_tstybm]

                UpdateCursor.updateRow(updaterow)

            else:

                continue

            arcpy.SetProgressorPosition()

def start(targetpath,outpath,photopath):

    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','8.1_����unionfzh��Ӧ����',0,count,1)

    targetValueDict,tbwymRelation = collectUnionAttributes(targetpath)

    arcpy.AddMessage("8.1_�����ں�")
    arcpy.Dissolve_management(targetpath,outpath,"unionfzh","","MULTI_PART")
    
    arcpy.AddMessage("8.1_��������ͼ������")
    result = arcpy.GetCount_management(outpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','8.1_������������',0,count,1)

    updateTarget(outpath,targetValueDict)
    
    arcpy.AddMessage("8.1_�ϲ���Ƭ��")
    result = arcpy.GetCount_management(photopath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','8.1_������������',0,count,1)

    mergePhoto(photopath,tbwymRelation)

if __name__ == "__main__":
    
    arcpy.AddMessage("8.1_�ں�����һ�²��ӱ�ͼ��")

    targetpath = arcpy.GetParameterAsText(0)
    outpath = arcpy.GetParameterAsText(1)

    targetpath = arcpy.GetParameterAsText(0)
    enviroment = arcpy.GetParameterAsText(1)
    outname = arcpy.GetParameterAsText(2)
    photopath = arcpy.GetParameterAsText(4)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = enviroment

    start(targetpath,outname,photopath)

    outpath = arcpy.Describe(outname).catalogPath

    arcpy.SetParameterAsText(3,outpath)
    arcpy.SetParameterAsText(5,photopath)

    arcpy.AddMessage("8.1_����")