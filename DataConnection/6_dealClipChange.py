#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal,pathArgs

def searchALL(targetpath):
    """��ȡ����ͼ���е�exp_bsm,fzh��bhlx�����ͼ��ͼ�㲻����fzh��bhlx���򴴽��ֶ�"""

    sql_clause = (None,"ORDER BY exp_bsm")

    datas = []
    fzhlist = []
    targetValueDict = {}

    searchFields = ["TSTYBM","exp_bsm",'bhlx','fzh']
    tempFields = ["TSTYBM","exp_bsm",'bhlx','fzh']

    arcpyDeal.ensureFields(targetpath,searchFields)

    arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,datas,sql_clause=sql_clause)

    for data in datas:
            
        fzh = dealNone.dealNoneAndBlank(data['fzh'])
        bhlx = dealNone.dealNoneAndBlank(data['bhlx'])
        
        if fzh != "" :

            if int(fzh) not in fzhlist:

                fzhlist.append(int(fzh))

        targetValueDict[data['TSTYBM']] = {"bhlx":bhlx,"fzh":fzh}

    fzhlist.sort()

    return datas,fzhlist,targetValueDict

def BhlxRules(bhlx):
    """������ͼ�α仯ʱ���仯���͸��ݹ�������ֵ"""

    newBhlx = bhlx

    if bhlx == "1":

        newBhlx = "2"
        
    elif bhlx == "0":

        newBhlx = "0"

    elif bhlx == "":

        newBhlx = "0"

    elif bhlx == "2":

        newBhlx = "0"

    return newBhlx

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

def collecteFzh(targetpath,targetdatas,fzhlist,targetValueDict):
    """�ռ�����ͱ仯����"""

    mergeFzhList = {}

    lastdata = {}

    for i in range(len(targetdatas)):

        targetdata = targetdatas[i]

        targettstybm = dealNone.dealNoneAndBlank(targetdata['TSTYBM'])
        targetexp_bsm = dealNone.dealNoneAndBlank(targetdata['exp_bsm'])
        targetbhlx = dealNone.dealNoneAndBlank(targetdata['bhlx'])

        #��������LINKTBS��ͼ�ߵı仯����
        
        targetfzh = targetValueDict[targettstybm]['fzh']

        if lastdata == {}:

            lastdata = targetdata

            continue

        #������������ͼ���ж�exp_bsm�Ƿ�һ��
            
        lastexp_bsm = dealNone.dealNoneAndBlank(lastdata['exp_bsm'])
        lasttstybm = dealNone.dealNoneAndBlank(lastdata['TSTYBM'])
        lastbhlx = dealNone.dealNoneAndBlank(lastdata['bhlx'])
        lastfzh = targetValueDict[lasttstybm]['fzh']

        if targetexp_bsm == lastexp_bsm:

            if targetfzh == "" and lastfzh == "":

                newFzh = getNewFzh(fzhlist)
                targetfzh = newFzh
                lastfzh = newFzh

            elif targetfzh == "" and lastfzh != "":

                targetfzh = lastfzh

            elif targetfzh != "" and lastfzh == "":

                lastfzh = targetfzh

            elif targetfzh != "" and lastfzh != "" and targetfzh != lastfzh:

                mergeFzhByFzh(targetfzh,lastfzh,fzhlist,mergeFzhList)

            targetValueDict[targettstybm]['bhlx'] = "2"
            targetValueDict[lasttstybm]['bhlx'] = "2"
            targetValueDict[targettstybm]['fzh'] = targetfzh
            targetValueDict[lasttstybm]['fzh'] = lastfzh

        lastdata = targetdata

        arcpy.SetProgressorPosition()
        
    return mergeFzhList

def updateTarget(targetpath,fzhlist,mergeFzhList,targetValueDict):
    """��������"""

    #���ݲ�ѯ�����ݸ�������
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

    arcpy.AddMessage("6_���Բ�ѯ")
    targetdatas,fzhlist,targetValueDict = searchALL(targetpath)

    arcpy.AddMessage("6_�ռ������")
    count = len(targetdatas)
    arcpy.SetProgressor('step',"6_�ռ������",0,count,1)

    mergeFzhList = collecteFzh(targetpath,targetdatas,fzhlist,targetValueDict)
    
    arcpy.AddMessage("6_���ݸ���")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step',"6_���ݸ���",0,count,1)

    updateTarget(targetpath,fzhlist,mergeFzhList,targetValueDict)
    
if __name__ == "__main__":
    
    arcpy.AddMessage("6_��ʼ���и�ͼ�߷���")

    targetpath = arcpy.GetParameterAsText(0)

    start(targetpath)

    arcpy.SetParameterAsText(1,targetpath)

    arcpy.AddMessage("6_����")
    