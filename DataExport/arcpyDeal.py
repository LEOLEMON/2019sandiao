#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,sys,json,dealNone

def deleteNotInFields(targetpath,keepFields):
    """ɾ�������б��ڵ��ֶ�"""

    if len(keepFields) == 0:

        return

    list = [field.name for field in arcpy.ListFields(targetpath)]

    deleteList = []

    for f in list:

        if f not in keepFields and f not in ["OBJECTID","SHAPE_Length","SHAPE_Area","SHAPE"]:

            deleteList.append(f)

    if len(deleteList) > 0:

        arcpy.DeleteField_management(targetpath,deleteList)
    
def deleteFields(targetpath,delfieldslist):
    """ȷ���ֶ��Ƿ���ڣ�������ɾ��"""

    fieldslist = [field.name for field in arcpy.ListFields(targetpath)]

    deleteList = []

    for field in delfieldslist:

        if field in fieldslist:

            deleteList.append(field)
    
    if len(deleteList) > 0:

        arcpy.DeleteField_management(targetpath,deleteList)

def ensureFields(targetpath,newfieldslist,type = "Text"):
    """ȷ���ֶ��Ƿ���ڣ������ڴ������ֶ�"""

    fieldslist = [field.name for field in arcpy.ListFields(targetpath)]

    for field in newfieldslist:

        if field not in fieldslist:

            arcpy.AddMessage("����  "+field)

            arcpy.AddField_management(targetpath, field, type)

def checkField(targetpath,fieldslist):

    list = [field.name for field in arcpy.ListFields(targetpath)]

    for f in fieldslist:

        if f not in list and "SHAPE@" not in f:

            arcpy.AddMessage("createTempDatas : not exists "+f)

def createTempDatas(searchFields,tempFields,targetpath,datas,where_clause = "",sql_clause = (None,None)):
    """���������ֶκ�����SQLɸѡ���ݣ�����ÿ����¼������dict��ʽ"""

    checkField(targetpath,searchFields)

    for row in arcpy.da.SearchCursor(targetpath, searchFields,where_clause = where_clause,sql_clause = sql_clause):

        data = {}
        for i in range(len(tempFields)):

            data[tempFields[i]]  = dealNone.dealNoneAndBlank(row[i]) 

        datas.append(data)

def createTempDatasLimit(searchFields,tempFields,targetpath,datas,where_clause = "",sql_clause = (None,None),offset=0,limit=100000):

    checkField(targetpath,searchFields)

    number = -1

    for row in arcpy.da.SearchCursor(targetpath, searchFields,where_clause = where_clause,sql_clause = sql_clause):

        number += 1

        if number < offset:

            continue 

        data = {}

        for i in range(len(tempFields)):

            data[tempFields[i]]  = dealNone.dealNoneAndBlank(row[i]) 
        
        datas.append(data)

        if len(datas) >= limit:

            break

def createTempLayer(targetpath,tempTargetPath,indexFields = [],where_clause = ""):
    """����ɸѡ����������ʱͼ��,����������"""

    arcpy.MakeFeatureLayer_management(targetpath, tempTargetPath,where_clause)

    createIndex(tempTargetPath,indexFields)

def createIndex(targetpath,indexFields = []):
    """�����ռ���������������,������������֮ǰ�ж��Ƿ���ڸ�����"""

    arcpy.AddSpatialIndex_management(targetpath)

    indexlist = [str(index.name.lower()) for index in arcpy.ListIndexes(targetpath)]

    for field in indexFields:
        
        if field not in indexlist:

                try:
                        arcpy.AddIndex_management(targetpath,field,field)
                except arcpy.ExecuteError:
                        arcpy.GetMessages() 

def createExistsTempLayer(targetpath,outputPath,indexFields = [],where_clause = "",keepFields=[]):
    """������ʱͼ����ļ���д�뵽������"""

    if arcpy.Exists(outputPath):
        
        arcpy.Delete_management(outputPath)

    createTempLayer(targetpath,"tempTargetPath",indexFields = indexFields,where_clause = where_clause)

    arcpy.CopyFeatures_management("tempTargetPath",outputPath)

    deleteNotInFields(outputPath,keepFields)

def copyToTempLayer(env,targetpath,outputPath,keepFields):
    """�Ѿ�ͼ���ĳЩ�ֶ����Ϊ��ͼ��"""

    dtargetpath = arcpy.Describe(targetpath)

    SpatialReference = dtargetpath.spatialReference

    shapeType = dtargetpath.shapeType

    arcpy.CreateFeatureclass_management(env,outputPath, shapeType,"","","",SpatialReference)

    ensureFields(outputPath,keepFields)

    keepFields.append("SHAPE@")

    insertcursor = arcpy.da.InsertCursor(outputPath,keepFields)

    count = int(arcpy.GetCount_management(targetpath).getOutput(0))
    arcpy.SetProgressor('step','copyToTempLayer',0,count,1)

    with arcpy.da.SearchCursor(targetpath,keepFields) as cur:

        for row in cur:

            arcpy.SetProgressorPosition()

            insertcursor.insertRow(row)