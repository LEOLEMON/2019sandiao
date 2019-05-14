#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,arcpyDeal

def getCskArea(cskpath):
    """�����ʼ�����"""

    arcpyDeal.ensureFields(cskpath,["cskmianji"],type = "DOUBLE")

    cskcur = arcpy.da.UpdateCursor(cskpath,['cskmianji','SHAPE@AREA'])

    for row in cskcur:

        row[0] = row[1]
        
        cskcur.updateRow(row)

def createWidth(tempname):
    """����ƽ�����,���ڴ�������ͼ��"""

    arcpyDeal.ensureFields(tempname,["width"],type="Double")
    
    expression = "getClass(float(!SHAPE.area!),float(!SHAPE.length!))"
    codeblock = """def getClass(area,length):
        return area/length
        """

    arcpy.CalculateField_management(tempname,"width", expression, "PYTHON_9.3",codeblock)

def collectError(indentitypath):

    where_clause = "SHAPE_Area >0.5 and width > 0.1 and TSTYBM is not null and TSTYBM <> ''"

    sql_clause = (None,"ORDER BY TSTYBM,BSM DESC")

    searchFields = ["BSM","TSTYBM"]

    cursor = arcpy.da.SearchCursor(indentitypath, searchFields,where_clause = where_clause,sql_clause = sql_clause)

    lasttstybm = {"tstybm":"","cskbsm":[]}

    targetValueList = []

    number = 0

    for row in cursor:

        arcpy.SetProgressorPosition()

        number += 1

        data = dict(zip(searchFields,row))
        
        if lasttstybm["tstybm"] == "":

            lasttstybm["tstybm"] =  data["TSTYBM"]
            lasttstybm["cskbsm"] = [data["BSM"]]

        elif lasttstybm["tstybm"] != data["TSTYBM"]:

            if len(lasttstybm["cskbsm"]) > 1:

                targetValueList.append(lasttstybm["tstybm"])
 
            lasttstybm["tstybm"] =  data["TSTYBM"]
            lasttstybm["cskbsm"] = [data["BSM"]]

        elif lasttstybm["tstybm"]  == data["TSTYBM"]:

            # arcpy.AddMessage("%s,%s,%s,%s"%(data["TSTYBM"],data["BSM"],lasttstybm["cskbsm"],str(data["BSM"] not in lasttstybm["cskbsm"])))

            if data["BSM"] not in lasttstybm["cskbsm"]:

                lasttstybm["cskbsm"].append(data["BSM"])

    if len(lasttstybm["cskbsm"]) > 1:

        targetValueList.append(lasttstybm["tstybm"])

    arcpy.AddMessage("����%s������ͼ��"%(len(targetValueList)))

    return targetValueList

def markError(xzkpath,targetValueList):
    """��Ǵ���ͼ��"""

    searchFields = ["TSTYBM","error"]

    arcpyDeal.deleteFields(xzkpath,["error"])
    arcpyDeal.ensureFields(xzkpath,searchFields)

    with arcpy.da.UpdateCursor(xzkpath,searchFields) as cur:

        for row in cur:
            
            arcpy.SetProgressorPosition()

            TSTYBM  = row[0]

            if TSTYBM in targetValueList:

                row[1] = '0'

            else:

                row[1] = "1"

            cur.updateRow(row)

def outputError(xzkpath,errorpath):
    """ɾ������ͼ�߲����"""

    where_clause = "error = '0'"

    arcpy.MakeFeatureLayer_management(xzkpath,"xzkpath")

    arcpy.SelectLayerByAttribute_management("xzkpath",where_clause=where_clause)

    arcpy.CopyFeatures_management("xzkpath",errorpath)

    arcpy.DeleteFeatures_management("xzkpath")

def judgeError(xzkpath,indentitypath,errorpath):
    """�ж��Ƿ��г�����ʼ�ⷶΧ����״��ͼ��"""

    where_clause = "TSTYBM is not null and TSTYBM <> ''"

    arcpy.MakeFeatureLayer_management(indentitypath,"indentitypath")

    arcpy.SelectLayerByAttribute_management("indentitypath",where_clause=where_clause)

    tmpnum =  int(arcpy.GetCount_management("indentitypath").getOutput(0))
    xzknum = int(arcpy.GetCount_management(xzkpath).getOutput(0))

    if xzknum != tmpnum:

        arcpy.AddMessage("3_��״�����ʼ��δ�׺ϣ�������ص�ͼ�� ��״��������%s,��ʱͼ��������%s"%(xzknum,tmpnum))

        arcpy.AddMessage("3_����ƽ�����")
        createWidth(indentitypath)

        arcpy.AddMessage("3_�ռ�����ͼ��")
        arcpy.SetProgressor('step','3_�ռ�����ͼ��',0,int(arcpy.GetCount_management(indentitypath).getOutput(0)),1)
        targetValueList = collectError(indentitypath)

        arcpy.AddMessage("3_��Ǵ���ͼ��")
        arcpy.SetProgressor('step','3_��Ǵ���ͼ��',0,int(arcpy.GetCount_management(xzkpath).getOutput(0)),1)
        markError(xzkpath,targetValueList)

        arcpy.AddMessage("3_�����ɾ������ͼ��")
        outputError(xzkpath,errorpath)

def collectCskData(indentitypath):
    """�ռ���״��ͼ������"""

    fields = ["TSTYBM","BSM","ZLDWDM","DLBM","CZCSXM","BSM_1","ZLDWDM_1","SJDLBM","CZCSXM_1","cskmianji","SHAPE_AREA"]
    showFields = ["tstybm","cskbsm","cskzldwdm","cskdlbm","cskczcsxm","xzkbsm","xzkzldwdm","xzksjdlbm","xzkczcsxm","cskmianji","SHAPE_AREA"]

    where_clause="TSTYBM is not null and TSTYBM <> ''"

    datas = {}

    with arcpy.da.SearchCursor(indentitypath,fields,where_clause=where_clause) as cursor:

        for row in cursor:

            data = dict(zip(showFields,row))

            if data["tstybm"] in datas:

                if data["SHAPE_AREA"] >datas[data["tstybm"]]["SHAPE_AREA"]:

                    datas[data["tstybm"]] = data
                
            else:

                datas[data["tstybm"]] = data

    return datas

def UpdateTarget(xzkpath,datas):
    """���»�ԭ��ʼ������"""

    bsmDifference = []
    zldwdmDifference = []
    sjdlbmDifference = []
    czcsxmDifference = []
    tstybmDifference = []

    arcpyDeal.ensureFields(xzkpath,["cskmianji"],type="DOUBLE")

    fields = ["TSTYBM","cskbsm","cskzldwdm","cskdlbm","cskczcsxm","cskmianji","BSM","ZLDWDM","SJDLBM","CZCSXM"]

    arcpyDeal.ensureFields(xzkpath,fields)

    fields.append("SHAPE@AREA")

    cursor = arcpy.da.UpdateCursor(xzkpath,fields,where_clause=" TSTYBM is not null",sql_clause=(None, 'ORDER BY TSTYBM'))

    for row in cursor:

        arcpy.SetProgressorPosition()

        tstybm = row[0]

        if tstybm not in datas:

            tstybmDifference.append(tstybm)

            row[1] = row[6]
            row[2] = row[7]
            row[3] = row[8]
            row[4] = row[9]
            row[5] = row[10]

            cursor.updateRow(row)

            continue

        if datas[tstybm]["cskbsm"] != datas[tstybm]["xzkbsm"]:

            bsmDifference.append(tstybm)

        if datas[tstybm]["cskzldwdm"] != datas[tstybm]["xzkzldwdm"]:

            zldwdmDifference.append(tstybm)

        if datas[tstybm]["cskdlbm"] != datas[tstybm]["xzksjdlbm"]:

            sjdlbmDifference.append(tstybm)
            zldwdmDifference.append(tstybm)

        if datas[tstybm]["cskczcsxm"] != datas[tstybm]["xzkczcsxm"]:

            czcsxmDifference.append(tstybm)

        row[1] = datas[tstybm]["cskbsm"]
        row[2] = datas[tstybm]["cskzldwdm"]
        row[3] = datas[tstybm]["cskdlbm"]
        row[4] = datas[tstybm]["cskczcsxm"]
        row[5] = datas[tstybm]["cskmianji"]

        cursor.updateRow(row)

    arcpy.AddMessage("3_����%s��ͼ���޳�ʼ��ͼ��"%(len(tstybmDifference)))
    arcpy.AddMessage("3_����%s��ͼ��bsm��ͬ"%(len(bsmDifference)))
    arcpy.AddMessage("3_����%s��ͼ��zldwdm��ͬ"%(len(zldwdmDifference)))
    arcpy.AddMessage("3_����%s��ͼ��sjdlbm��ͬ"%(len(sjdlbmDifference)))
    arcpy.AddMessage("3_����%s��ͼ��czcsxm��ͬ"%(len(czcsxmDifference)))

    # arcpy.AddMessage("3_"+json.dumps(tstybmDifference))
    # arcpy.AddMessage("3_"+json.dumps(bsmDifference))
    # arcpy.AddMessage("3_"+json.dumps(zldwdmDifference))
    # arcpy.AddMessage("3_"+json.dumps(sjdlbmDifference))

if __name__ == "__main__":
    
    arcpy.AddMessage("3_��ʼ��ԭ��ʼ������")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)
    cskpath = arcpy.GetParameterAsText(2)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    indentitypath = "indentitypath_3"
    errorpath = "error_3"

    arcpy.AddMessage("3_�����ʼ�����")
    getCskArea(cskpath)

    #��ʶ����
    arcpy.AddMessage("3_��ʶ����")
    arcpy.Identity_analysis (cskpath,xzkpath,indentitypath,cluster_tolerance="0.01")
    
    #�ж��Ƿ��в�����ʼ�ⷶΧ�Ĵ���ͼ��
    arcpy.AddMessage("3_�жϳ�ʼ�����״���Ƿ��׺�")
    judgeError(xzkpath,indentitypath,errorpath)

    #�ռ�
    arcpy.AddMessage("3_�ռ���״��ͼ������")
    arcpy.SetProgressor('step','3_�ռ���״��ͼ������',0,int(arcpy.GetCount_management(indentitypath).getOutput(0)),1)
    matchedDataDict = collectCskData(indentitypath)
    
    #��ԭ����
    arcpy.AddMessage("3_��ԭ����")
    arcpy.SetProgressor('step','3_��ԭ����',0, int(arcpy.GetCount_management(xzkpath).getOutput(0)),1)
    UpdateTarget(xzkpath,matchedDataDict)

    arcpy.SetParameterAsText(3,xzkpath)
    arcpy.AddMessage("3_������ԭ��ʼ������")