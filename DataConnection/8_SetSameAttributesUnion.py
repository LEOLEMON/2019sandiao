#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal,shapely,pathArgs
from shapely.wkt import loads

def searchALL(targetpath):
    """获取所有图斑中的exp_bsm,fzh和bhlx，如果图斑图层不存在fzh和bhlx，则创建字段"""

    datas = []
    fzhlist = []
    targetValueDict = {}

    searchFields = ["exp_tbwym",'fzh']
    tempFields = ["exp_tbwym",'fzh']

    arcpyDeal.ensureFields(targetpath,searchFields)

    arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,datas)

    for data in datas:
            
        fzh = dealNone.dealNoneAndBlank(data['fzh'])
        
        if fzh != "" :

            if int(fzh) not in fzhlist:

                fzhlist.append(int(fzh))

        targetValueDict[data['exp_tbwym']] = {"fzh":fzh}

    fzhlist.sort()

    return fzhlist,targetValueDict

def getNewFzh(fzhlist):
    """获取新的fzh"""

    newFzh = None

    if len(fzhlist) == 0:

        newFzh = 1
        fzhlist.append(newFzh)

    else:

        newFzh = fzhlist[len(fzhlist) - 1] + 1
        fzhlist.append(newFzh)

    return newFzh

def mergeFzhByFzh(fzh1,fzh2,fzhlist,mergeFzhList):
    """两个相互关联的已存在不同分组号的图斑的分组号合并处理"""
    """mergeFzhList数据结构为DICT，键代表原分组号，值代表合并后分组号"""

    if fzh1 not in mergeFzhList and fzh2 not in mergeFzhList:

        newFzh = getNewFzh(fzhlist)
        mergeFzhList[fzh1] = newFzh
        mergeFzhList[fzh2] = newFzh
    
    elif fzh1 not in mergeFzhList and fzh2 in mergeFzhList:

        mergeFzhList[fzh1] = mergeFzhList[fzh2]
    
    elif fzh1 in mergeFzhList and fzh2 not in mergeFzhList:

        mergeFzhList[fzh2] = mergeFzhList[fzh1]

    elif fzh1 in mergeFzhList and fzh2 in mergeFzhList:
        """如果两个图斑都已经和其他图斑合并了分组号，则将所有相关联的图斑的分组号合并"""

        newFzh = getNewFzh(fzhlist)

        fzh1_merge = mergeFzhList[fzh1]
        fzh2_merge = mergeFzhList[fzh2]

        for key in mergeFzhList:

            if mergeFzhList[key] == fzh1_merge or mergeFzhList[key] == fzh2_merge:

                mergeFzhList[key] = newFzh

def getNewUnionFzh(unionfzhlist):
    """获取新的fzh"""

    newUnionFzh = None

    if len(unionfzhlist) == 0:

        newUnionFzh = 1
        unionfzhlist.append(newUnionFzh)

    else:

        newUnionFzh = unionfzhlist[len(unionfzhlist) - 1] + 1
        unionfzhlist.append(newUnionFzh)

    return newUnionFzh

def collecteUnionFzh(targetpath,fzhlist,unionfzhlist,targetValueDict):
    """收集分组和变化类型"""

    mergeFzhList = {}

    datas = []
    sql_clause =(None,"ORDER BY exp_zldwdm,exp_dlbm,exp_dlmc,exp_gdlx,exp_tbxhdm,exp_tbxhmc,exp_gdzzsxdm,exp_gdzzsxmc,exp_czcsxm") 
    searchFields = ["bhlx","exp_tbwym","SHAPE@WKT","fzh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm"]
    tempFields = ["bhlx","exp_tbwym","shpwkt","fzh","exp_zldwdm","exp_dlbm","exp_dlmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_czcsxm"]
    
    arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,datas,sql_clause=sql_clause)

    lastdata = {}

    for data in datas:

        data["shpwkt"] = loads(data['shpwkt'])

        if lastdata == {}:

            lastdata = data

            targetValueDict[data["exp_tbwym"]]["unionfzhlist"] = getNewUnionFzh(unionfzhlist)
            targetValueDict[data["exp_tbwym"]]["fzh"]  = data["fzh"]

            continue

        equals = True
        for field in tempFields:

            if field in ["shpwkt", "exp_tbwym","fzh"]:

                continue

            if data[field] != lastdata[field]:

                equals = False

                break

        if data["bhlx"] == "1" or lastdata["bhlx"] == "1":

            targetValueDict[data["exp_tbwym"]]["unionfzhlist"]  = getNewUnionFzh(unionfzhlist)
            
            targetValueDict[data["exp_tbwym"]]["fzh"]  = data["fzh"]

            continue

        if equals == True and data['shpwkt'].intersects(lastdata['shpwkt']):
            
            targetValueDict[data["exp_tbwym"]]["unionfzhlist"]  = targetValueDict[lastdata["exp_tbwym"]]["unionfzhlist"] 

            targetfzh = data["fzh"]
            lastfzh = lastdata["fzh"]
            
            mergeFzhByFzh(targetfzh,lastfzh,fzhlist,mergeFzhList)

        else:
            
            targetValueDict[data["exp_tbwym"]]["unionfzhlist"]  = getNewUnionFzh(unionfzhlist)

        targetValueDict[data["exp_tbwym"]]["fzh"]  = data["fzh"]

        lastdata = data

        arcpy.SetProgressorPosition()

    return mergeFzhList

def updateTarget(targetpath,unionfzhlist,targetValueDict,mergeFzhList):
    """更新数据"""

    #根据查询的数据更新数据
    searchFields = ['exp_tbwym','unionfzh','fzh']
    with arcpy.da.UpdateCursor(targetpath,searchFields) as UpdateCursor:

        for updaterow in UpdateCursor:
            
            exp_tbwym = updaterow[0]

            unionfzh = targetValueDict[exp_tbwym]["unionfzhlist"]

            fzh = targetValueDict[exp_tbwym]["fzh"]

            if fzh in mergeFzhList:

                fzh = mergeFzhList[fzh]

            updaterow[1] = unionfzh
            updaterow[2] = fzh
        
            UpdateCursor.updateRow(updaterow)

            arcpy.SetProgressorPosition()

def start(targetpath):

    arcpy.AddMessage("8_重新生成union字段")
    arcpyDeal.deleteFields(targetpath,["unionfzh"])
    arcpyDeal.ensureFields(targetpath,["unionfzh"])

    arcpy.AddMessage("8_收集原有分组号")
    fzhlist,targetValueDict = searchALL(targetpath)

    arcpy.AddMessage("8_收集融合分组号")
    unionfzhlist = []
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','8_收集分组号',0,count,1)

    mergeFzhList = collecteUnionFzh(targetpath,fzhlist,unionfzhlist,targetValueDict)
    
    arcpy.AddMessage("8_数据更新")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','8_数据更新',0,count,1)

    updateTarget(targetpath,unionfzhlist,targetValueDict,mergeFzhList)

if __name__ == "__main__":
    
    arcpy.AddMessage("8_开始给linkTBS分组")
    
    targetpath = arcpy.GetParameterAsText(0)

    arcpy.AddMessage(targetpath+"   "+arcpy.GetParameterAsText(0))

    start(targetpath)
    
    arcpy.SetParameterAsText(1,targetpath)

    arcpy.AddMessage("8_结束")
    