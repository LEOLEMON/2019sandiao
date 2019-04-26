#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal

def searchLinkTBS(targetpath):
    """����ӵ��LINKTBS��ͼ�ߣ������������б�"""

    where_clause = "LINKTBS <> '' and LINKTBS is not null  "

    tempTargerPah = "tempLinkTBS"
    datas = []
    searchFields = ["TSTYBM",'LINKTBS','bhlx','fzh']
    tempFields = ["TSTYBM",'linktbs','bhlx','fzh']

    arcpyDeal.ensureFields(targetpath,searchFields)

    arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,datas,where_clause = where_clause)

    arcpy.Delete_management(tempTargerPah)
    
    arcpy.AddMessage("5_����%s��ͼ�ߴ���LINKTBS"%(len(datas)))

    return datas

def searchFzh(targetpath):
    """��ȡ����ͼ���е�fzh��bhlx�����ͼ��ͼ�㲻����fzh��bhlx���򴴽��ֶ�"""

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
    """������ͼ�α仯ʱ���仯���͸��ݹ�������ֵ"""

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

    linktbsLack = []

    mergeFzhList = {}

    for i in range(len(targetdatas)):

        targetdata = targetdatas[i]

        targettstybm1 = dealNone.dealNoneAndBlank(targetdata['TSTYBM'])
        targetlinktbs1 = dealNone.dealNoneAndBlank(targetdata['linktbs'])
        targetbhlx1 = dealNone.dealNoneAndBlank(targetdata['bhlx'])

        #��������LINKTBS��ͼ�ߵı仯����
        targetNewBhlx1 = BhlxRules(targetbhlx1)
        
        targetfzh1 = ""
        if targettstybm1 in targetValueDict:

            targetfzh1 = targetValueDict[targettstybm1]['fzh']

        targetValueDict[targettstybm1]['bhlx'] = targetNewBhlx1

        #����LINKTBS��Ӧͼ������

        where_clause = "bsm = '%s' and TSTYBM <> '%s'"%(targetlinktbs1,targettstybm1)
        
        targetdatas2 = []
        searchFields = ["TSTYBM",'bhlx']
        tempFields = ["TSTYBM",'bhlx']

        arcpyDeal.createTempDatas(searchFields,tempFields,targetpath,targetdatas2,where_clause=where_clause)

        #����ͼ�ߣ�����LinkTBS��Ӧ��ͼ�ߵı仯���ͣ���������LINKTBS��ͼ�ߺͶ�Ӧͼ�ߵķ����
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

    arcpy.AddMessage("5_����%s��ͼ�ߴ���LINKTBS���޷��ҵ���ӦBSMͼ��"%(len(linktbsLack)))

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

    arcpy.AddMessage("5_linkTBS��ѯ")
    targetdatas = searchLinkTBS(targetpath)

    arcpy.AddMessage("5_�����ѯ")
    fzhlist,targetValueDict = searchFzh(targetpath)

    arcpy.AddMessage("5_�ռ������")
    count = len(targetdatas)
    arcpy.SetProgressor('step','5_�ռ������',0,count,1)

    mergeFzhList = collecteFzh(targetpath,targetdatas,fzhlist,targetValueDict)
    
    arcpy.AddMessage("5_���ݸ���")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','5_���ݸ���',0,count,1)

    updateTarget(targetpath,fzhlist,mergeFzhList,targetValueDict)
    
if __name__ == "__main__":
    
    arcpy.AddMessage("5_��ʼ��linkTBS����")

    targetpath = arcpy.GetParameterAsText(0)

    start(targetpath)

    arcpy.SetParameterAsText(1,targetpath)

    arcpy.AddMessage("5_����")
    