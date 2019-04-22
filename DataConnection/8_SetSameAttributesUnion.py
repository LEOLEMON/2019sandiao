#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal,shapely,pathArgs
from shapely.wkt import loads

def searchALL(targetpath):
    """��ȡ����ͼ���е�exp_bsm,fzh��bhlx�����ͼ��ͼ�㲻����fzh��bhlx���򴴽��ֶ�"""

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
    """��ȡ�µ�fzh"""

    newFzh = None

    if len(fzhlist) == 0:

        newFzh = 1
        fzhlist.append(newFzh)

    else:

        newFzh = fzhlist[len(fzhlist) - 1] + 1
        fzhlist.append(newFzh)

    return newFzh

def mergeFzhByFzh(fzh1,fzh2,fzhlist,mergeFzhList):
    """�����໥�������Ѵ��ڲ�ͬ����ŵ�ͼ�ߵķ���źϲ�����"""
    """mergeFzhList���ݽṹΪDICT��������ԭ����ţ�ֵ����ϲ�������"""

    if fzh1 not in mergeFzhList and fzh2 not in mergeFzhList:

        newFzh = getNewFzh(fzhlist)
        mergeFzhList[fzh1] = newFzh
        mergeFzhList[fzh2] = newFzh
    
    elif fzh1 not in mergeFzhList and fzh2 in mergeFzhList:

        mergeFzhList[fzh1] = mergeFzhList[fzh2]
    
    elif fzh1 in mergeFzhList and fzh2 not in mergeFzhList:

        mergeFzhList[fzh2] = mergeFzhList[fzh1]

    elif fzh1 in mergeFzhList and fzh2 in mergeFzhList:
        """�������ͼ�߶��Ѿ�������ͼ�ߺϲ��˷���ţ��������������ͼ�ߵķ���źϲ�"""

        newFzh = getNewFzh(fzhlist)

        fzh1_merge = mergeFzhList[fzh1]
        fzh2_merge = mergeFzhList[fzh2]

        for key in mergeFzhList:

            if mergeFzhList[key] == fzh1_merge or mergeFzhList[key] == fzh2_merge:

                mergeFzhList[key] = newFzh

def getNewUnionFzh(unionfzhlist):
    """��ȡ�µ�fzh"""

    newUnionFzh = None

    if len(unionfzhlist) == 0:

        newUnionFzh = 1
        unionfzhlist.append(newUnionFzh)

    else:

        newUnionFzh = unionfzhlist[len(unionfzhlist) - 1] + 1
        unionfzhlist.append(newUnionFzh)

    return newUnionFzh

def collecteUnionFzh(targetpath,fzhlist,unionfzhlist,targetValueDict):
    """�ռ�����ͱ仯����"""

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
    """��������"""

    #���ݲ�ѯ�����ݸ�������
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

    arcpy.AddMessage("8_��������union�ֶ�")
    arcpyDeal.deleteFields(targetpath,["unionfzh"])
    arcpyDeal.ensureFields(targetpath,["unionfzh"])

    arcpy.AddMessage("8_�ռ�ԭ�з����")
    fzhlist,targetValueDict = searchALL(targetpath)

    arcpy.AddMessage("8_�ռ��ںϷ����")
    unionfzhlist = []
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','8_�ռ������',0,count,1)

    mergeFzhList = collecteUnionFzh(targetpath,fzhlist,unionfzhlist,targetValueDict)
    
    arcpy.AddMessage("8_���ݸ���")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','8_���ݸ���',0,count,1)

    updateTarget(targetpath,unionfzhlist,targetValueDict,mergeFzhList)

if __name__ == "__main__":
    
    arcpy.AddMessage("8_��ʼ��linkTBS����")
    
    targetpath = arcpy.GetParameterAsText(0)

    arcpy.AddMessage(targetpath+"   "+arcpy.GetParameterAsText(0))

    start(targetpath)
    
    arcpy.SetParameterAsText(1,targetpath)

    arcpy.AddMessage("8_����")
    