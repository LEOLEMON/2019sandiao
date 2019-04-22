#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal

def getFinal2(datas,linktbs):

    for i in range(len(datas)):

        if datas[i]["bsm"] == linktbs:

            if datas[i]["linktbs"] == "":

                return datas[i]

    return getFinal2(datas,datas[i]["linktbs"])

def getFinal(lastdata):

    if len(lastdata["datas"]) == 1:

        return lastdata["datas"][0]

    else:

        return getFinal2(lastdata["datas"],lastdata["datas"][0]["linktbs"])

def collectUnionAttributes(targetpath):

    targetValueDict = {}

    tbwymRelation = {}

    datas = []
    searchFields = ["unionfzh","LINKTBS","BSM","exp_tbybh","exp_bsm","exp_tbbh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm","exp_tblx","exp_tbwym","bhlx","exp_wjzlx","fzh"]
    tempFields = ["unionfzh","linktbs","bsm","exp_tbybh","exp_bsm","exp_tbbh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm","exp_tblx","exp_tbwym","bhlx","exp_wjzlx","fzh"]

    arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,datas,sql_clause=(None,"ORDER BY unionfzh,LINKTBS DESC"))

    lastdata = {"lastunionfzh":"","datas":[]}

    for data in datas:

        #分析存在LINKTBS的图斑的变化类型

        if lastdata["lastunionfzh"] == "":

            lastdata["lastunionfzh"] = data["unionfzh"]
            lastdata["datas"].append(data)

            continue

        #查找两个相邻图斑判断exp_bsm是否一致
         
        if data["unionfzh"] == lastdata["lastunionfzh"]:

            lastdata["datas"].append(data)

            continue

        else:

            targetValueDict[lastdata["lastunionfzh"]] = getFinal(lastdata)

            for ld in lastdata["datas"]:

                tbwymRelation[ld["exp_tbwym"]] = targetValueDict[lastdata["lastunionfzh"]]["exp_tbwym"]

            lastdata = {"lastunionfzh":data["unionfzh"],"datas":[data]}

        arcpy.SetProgressorPosition()

    targetValueDict[lastdata["lastunionfzh"]] = getFinal(lastdata)

    return targetValueDict,tbwymRelation

def updateTarget(targetpath,targetValueDict):
    """更新数据"""

    #根据查询的数据更新数据
    searchFields = ["unionfzh","exp_bsm","exp_tbybh","exp_tbbh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm","exp_tblx","exp_tbwym","bhlx","exp_wjzlx","fzh"]

    arcpyDeal.ensureFields(targetpath,searchFields)

    with arcpy.da.UpdateCursor(targetpath,searchFields) as UpdateCursor:

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
    """合并照片"""

    searchFields = ["TSTYBM","exp_tstybm"]

    arcpyDeal.ensureFields(photopath,searchFields)

    with arcpy.da.UpdateCursor(photopath,searchFields) as UpdateCursor:

        for updaterow in UpdateCursor:

            updaterow[1] = updaterow[0]

            UpdateCursor.updateRow(updaterow)

            arcpy.SetProgressorPosition()

    #根据查询的数据更新数据
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
    arcpy.SetProgressor('step','7.1_查找unionfzh对应属性',0,count,1)

    targetValueDict,tbwymRelation = collectUnionAttributes(targetpath)

    arcpy.AddMessage("7.1_数据融合")
    arcpy.Dissolve_management(targetpath,outpath,"unionfzh","","MULTI_PART")
    
    arcpy.AddMessage("7.1_更新所有图斑属性")
    result = arcpy.GetCount_management(outpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','7.1_更新所有属性',0,count,1)

    updateTarget(outpath,targetValueDict)

    arcpy.AddMessage("7.1_合并照片点")
    result = arcpy.GetCount_management(photopath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','8.1_更新所有属性',0,count,1)

    mergePhoto(photopath,tbwymRelation)

if __name__ == "__main__":
    
    arcpy.AddMessage("7.1_开始给linkTBS分组")

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

    arcpy.AddMessage("7.1_结束")