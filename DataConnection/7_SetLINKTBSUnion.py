#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal,pathArgs

def searchLinkTBS(targetpath):
    """查找拥有LINKTBS的图斑，并返回数据列表"""

    where_clause = "LINKTBS <> '' and LINKTBS is not null  "

    tempTargerPah = "tempLinkTBS"
    datas = []
    searchFields = ["TSTYBM",'LINKTBS','unionfzh']
    tempFields = ["TSTYBM",'linktbs','unionfzh']

    arcpyDeal.ensureFields(targetpath,searchFields)

    arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,datas,where_clause = where_clause)

    arcpy.Delete_management(tempTargerPah)
    
    arcpy.AddMessage("7_共有%s个图斑存在LINKTBS"%(len(datas)))

    return datas

def searchFzh(targetpath):
    """获取所有图斑中的unionfzh，如果图斑图层不存在unionfzhfzh，则创建字段"""

    unionfzhlist = []
    targetValueDict = {}

    datas = []
    searchFields = ["TSTYBM", "unionfzh"]
    tempFields = ["TSTYBM","unionfzh"]

    arcpyDeal.ensureFields(targetpath,searchFields)

    sql_clause = (None,"ORDER BY unionfzh")

    arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,datas,sql_clause = sql_clause)

    for data in datas:
        
        unionfzh = dealNone.dealNoneAndBlank(data['unionfzh'])
        
        if unionfzh != "":
            unionfzhlist.append(int(unionfzh))

        targetValueDict[data['TSTYBM']] = {"unionfzh":unionfzh}

    unionfzhlist.sort()

    return unionfzhlist,targetValueDict

def getNewFzh(unionfzhlist):
    """获取新的fzh"""

    newFzh = None

    if len(unionfzhlist) == 0:

        newFzh = 1
        unionfzhlist.append(newFzh)

    else:

        newFzh = unionfzhlist[len(unionfzhlist) - 1] + 1
        unionfzhlist.append(newFzh)

    return newFzh

def mergeFzhByFzh(fzh1,fzh2,unionfzhlist,mergeunionfzhlist):
    """两个相互关联的已存在不同分组号的图斑的分组号合并处理"""
    """mergeunionfzhlist数据结构为DICT，键代表原分组号，值代表合并后分组号"""

    if fzh1 not in mergeunionfzhlist and fzh2 not in mergeunionfzhlist:

        newFzh = getNewFzh(unionfzhlist)
        mergeunionfzhlist[fzh1] = newFzh
        mergeunionfzhlist[fzh2] = newFzh
    
    elif fzh1 not in mergeunionfzhlist and fzh2 in mergeunionfzhlist:

        mergeunionfzhlist[fzh1] = mergeunionfzhlist[fzh2]
    
    elif fzh1 in mergeunionfzhlist and fzh2 not in mergeunionfzhlist:

        mergeunionfzhlist[fzh2] = mergeunionfzhlist[fzh1]

    elif fzh1 in mergeunionfzhlist and fzh2 in mergeunionfzhlist:
        """如果两个图斑都已经和其他图斑合并了分组号，则将所有相关联的图斑的分组号合并"""

        newFzh = getNewFzh(unionfzhlist)

        fzh1_merge = mergeunionfzhlist[fzh1]
        fzh2_merge = mergeunionfzhlist[fzh2]

        for key in mergeunionfzhlist:

            if mergeunionfzhlist[key] == fzh1_merge or mergeunionfzhlist[key] == fzh2_merge:

                mergeunionfzhlist[key] = newFzh

def collecteUnionFzh(targetpath,targetdatas,unionfzhlist,targetValueDict):
    """收集分组和变化类型"""

    linktbsLack = []

    mergeunionfzhlist = {}

    for i in range(len(targetdatas)):

        targetdata = targetdatas[i]

        targettstybm1 = dealNone.dealNoneAndBlank(targetdata['TSTYBM'])
        targetlinktbs1 = dealNone.dealNoneAndBlank(targetdata['linktbs'])

        #分析存在LINKTBS的图斑的变化类型
        
        targetunionfzh1 = ""
        if targettstybm1 in targetValueDict:

            targetunionfzh1 = targetValueDict[targettstybm1]['unionfzh']


        #查找LINKTBS对应图斑数据

        where_clause = "bsm = '%s' and TSTYBM <> '%s'"%(targetlinktbs1,targettstybm1)
        
        targetdatas2 = []
        searchFields = ["TSTYBM"]
        tempFields = ["TSTYBM"]

        arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,targetdatas2,where_clause=where_clause)

        #遍历图斑，分析LinkTBS对应的图斑的变化类型；分析存在LINKTBS的图斑和对应图斑的分组号
        for targetdata2 in targetdatas2:

            targettstybm2 = dealNone.dealNoneAndBlank(targetdata2['TSTYBM'])

            targetunionfzh2 = ""
            if targettstybm2 in targetValueDict:

                targetunionfzh2 = targetValueDict[targettstybm1]['unionfzh']

            if targetunionfzh1 == "" and targetunionfzh2 == "":

                newFzh = getNewFzh(unionfzhlist)
                targetunionfzh1 = newFzh
                targetunionfzh2 = newFzh

            elif targetunionfzh1 == "" and targetunionfzh2 != "":

                targetunionfzh1 = targetunionfzh2

            elif targetunionfzh1 != "" and targetunionfzh2 == "":

                targetunionfzh2 = targetunionfzh1

            elif targetunionfzh1 != "" and targetunionfzh2 != "" and targetunionfzh1 != targetunionfzh2:

                mergeFzhByFzh(targetunionfzh1,targetunionfzh2,unionfzhlist,mergeunionfzhlist)

            targetValueDict[targettstybm1]['unionfzh'] = targetunionfzh1
            targetValueDict[targettstybm2]['unionfzh'] = targetunionfzh2

            arcpy.SetProgressorPosition()
        
        if len(targetdatas2) == 0:

            linktbsLack.append(targettstybm1)

    arcpy.AddMessage("7_共有%s个图斑存在LINKTBS但无法找到对应BSM图斑"%(len(linktbsLack)))

    return mergeunionfzhlist

def updateTarget(targetpath,unionfzhlist,mergeunionfzhlist,targetValueDict):
    """更新数据"""

    #根据查询的数据更新数据
    searchFields = ['TSTYBM','unionfzh']
    with arcpy.da.UpdateCursor(targetpath,searchFields) as UpdateCursor:

        for updaterow in UpdateCursor:
            
            tstybm = updaterow[0]

            unionfzh = targetValueDict[tstybm]['unionfzh']

            if unionfzh in mergeunionfzhlist:

                unionfzh = mergeunionfzhlist[unionfzh]

            if unionfzh == "":
                
                unionfzh = getNewFzh(unionfzhlist)

            updaterow[1] = unionfzh
        
            UpdateCursor.updateRow(updaterow)

            arcpy.SetProgressorPosition()

def start(targetpath):

    arcpy.AddMessage("7_linkTBS查询")
    targetdatas = searchLinkTBS(targetpath)

    arcpy.AddMessage("7_分组查询")
    unionfzhlist,targetValueDict = searchFzh(targetpath)

    arcpy.AddMessage("7_收集融合分组号")
    count = len(targetdatas)
    arcpy.SetProgressor('step','7_收集分组号',0,count,1)

    mergeunionfzhlist = collecteUnionFzh(targetpath,targetdatas,unionfzhlist,targetValueDict)
    
    arcpy.AddMessage("7_数据更新")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','7_数据更新',0,count,1)

    updateTarget(targetpath,unionfzhlist,mergeunionfzhlist,targetValueDict)
    
if __name__ == "__main__":
    
    arcpy.AddMessage("7_开始给linkTBS分组")

    targetpath = arcpy.GetParameterAsText(0)

    start(targetpath)

    arcpy.SetParameterAsText(1,targetpath)

    arcpy.AddMessage("7_结束")
    