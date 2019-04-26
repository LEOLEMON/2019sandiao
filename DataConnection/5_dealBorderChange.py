#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal

def searchLinkTBS(targetpath):
    """查找拥有LINKTBS的图斑，并返回数据列表"""

    where_clause = "LINKTBS <> '' and LINKTBS is not null  "

    tempTargerPah = "tempLinkTBS"
    datas = []
    searchFields = ["TSTYBM",'LINKTBS','bhlx','fzh']
    tempFields = ["TSTYBM",'linktbs','bhlx','fzh']

    arcpyDeal.ensureFields(targetpath,searchFields)

    arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,datas,where_clause = where_clause)

    arcpy.Delete_management(tempTargerPah)
    
    arcpy.AddMessage("5_共有%s个图斑存在LINKTBS"%(len(datas)))

    return datas

def searchFzh(targetpath):
    """获取所有图斑中的fzh和bhlx，如果图斑图层不存在fzh和bhlx，则创建字段"""

    fzhlist = []
    targetValueDict = {}

    datas = []
    searchFields = ["TSTYBM", "bhlx","fzh"]
    tempFields = ["TSTYBM","bhlx","fzh"]

    arcpyDeal.ensureFields(targetpath,searchFields)

    sql_clause = (None,"ORDER BY fzh")

    arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,datas,sql_clause = sql_clause)

    for data in datas:
        
        fzh = dealNone.dealNoneAndBlank(data['fzh'])
        bhlx = dealNone.dealNoneAndBlank(data['bhlx'])
        
        if fzh != "":
            fzhlist.append(int(fzh))

        targetValueDict[data['TSTYBM']] = {"bhlx":bhlx,"fzh":fzh}

    fzhlist.sort()

    return fzhlist,targetValueDict

def BhlxRules(bhlx):
    """当发生图形变化时，变化类型根据规则赋予新值"""

    newBhlx = bhlx

    if bhlx == "1":

        newBhlx = "2"
        
    elif bhlx == "0":

        newBhlx = "0"

    elif bhlx == "":

        newBhlx = "0"

    elif bhlx == "2":

        newBhlx = "2"

    return newBhlx

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

def collecteFzh(targetpath,targetdatas,fzhlist,targetValueDict):
    """收集分组和变化类型"""

    linktbsLack = []

    mergeFzhList = {}

    for i in range(len(targetdatas)):

        targetdata = targetdatas[i]

        targettstybm1 = dealNone.dealNoneAndBlank(targetdata['TSTYBM'])
        targetlinktbs1 = dealNone.dealNoneAndBlank(targetdata['linktbs'])
        targetbhlx1 = dealNone.dealNoneAndBlank(targetdata['bhlx'])

        #分析存在LINKTBS的图斑的变化类型
        targetNewBhlx1 = BhlxRules(targetbhlx1)
        
        targetfzh1 = ""
        if targettstybm1 in targetValueDict:

            targetfzh1 = targetValueDict[targettstybm1]['fzh']

        targetValueDict[targettstybm1]['bhlx'] = targetNewBhlx1

        #查找LINKTBS对应图斑数据

        where_clause = "bsm = '%s' and TSTYBM <> '%s'"%(targetlinktbs1,targettstybm1)
        
        targetdatas2 = []
        searchFields = ["TSTYBM",'bhlx']
        tempFields = ["TSTYBM",'bhlx']

        arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,targetdatas2,where_clause=where_clause)

        #遍历图斑，分析LinkTBS对应的图斑的变化类型；分析存在LINKTBS的图斑和对应图斑的分组号
        for targetdata2 in targetdatas2:

            targettstybm2 = dealNone.dealNoneAndBlank(targetdata2['TSTYBM'])
            targetbhlx2 = dealNone.dealNoneAndBlank(targetdata2['bhlx'])

            targetNewBhlx2 = BhlxRules(targetbhlx2)
            targetValueDict[targettstybm2]['bhlx'] = targetNewBhlx2

            targetfzh2 = ""
            if targettstybm2 in targetValueDict:

                targetfzh2 = targetValueDict[targettstybm1]['fzh']

            if targetfzh1 == "" and targetfzh2 == "":

                newFzh = getNewFzh(fzhlist)
                targetfzh1 = newFzh
                targetfzh2 = newFzh

            elif targetfzh1 == "" and targetfzh2 != "":

                targetfzh1 = targetfzh2

            elif targetfzh1 != "" and targetfzh2 == "":

                targetfzh2 = targetfzh1

            elif targetfzh1 != "" and targetfzh2 != "" and targetfzh1 != targetfzh2:

                mergeFzhByFzh(targetfzh1,targetfzh2,fzhlist,mergeFzhList)

            targetValueDict[targettstybm1]['fzh'] = targetfzh1
            targetValueDict[targettstybm2]['fzh'] = targetfzh2

            arcpy.SetProgressorPosition()
        
        if len(targetdatas2) == 0:

            linktbsLack.append(targettstybm1)

    arcpy.AddMessage("5_共有%s个图斑存在LINKTBS但无法找到对应BSM图斑"%(len(linktbsLack)))

    return mergeFzhList

def updateTarget(targetpath,fzhlist,mergeFzhList,targetValueDict):
    """更新数据"""

    #根据查询的数据更新数据
    searchFields = ['TSTYBM','bhlx','fzh']
    with arcpy.da.UpdateCursor(targetpath,searchFields) as UpdateCursor:

        for updaterow in UpdateCursor:
            
            tstybm = updaterow[0]

            bhlx = targetValueDict[tstybm]['bhlx']
            fzh = targetValueDict[tstybm]['fzh']

            if fzh in mergeFzhList:

                fzh = mergeFzhList[fzh]

            if fzh == "":
                
                fzh = getNewFzh(fzhlist)

            updaterow[1] = bhlx
            updaterow[2] = fzh
        
            UpdateCursor.updateRow(updaterow)

            arcpy.SetProgressorPosition()

def start(targetpath):

    arcpy.AddMessage("5_linkTBS查询")
    targetdatas = searchLinkTBS(targetpath)

    arcpy.AddMessage("5_分组查询")
    fzhlist,targetValueDict = searchFzh(targetpath)

    arcpy.AddMessage("5_收集分组号")
    count = len(targetdatas)
    arcpy.SetProgressor('step','5_收集分组号',0,count,1)

    mergeFzhList = collecteFzh(targetpath,targetdatas,fzhlist,targetValueDict)
    
    arcpy.AddMessage("5_数据更新")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','5_数据更新',0,count,1)

    updateTarget(targetpath,fzhlist,mergeFzhList,targetValueDict)
    
if __name__ == "__main__":
    
    arcpy.AddMessage("5_开始给linkTBS分组")

    targetpath = arcpy.GetParameterAsText(0)

    start(targetpath)

    arcpy.SetParameterAsText(1,targetpath)

    arcpy.AddMessage("5_结束")
    