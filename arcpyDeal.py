#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,sys,json,dealNone

def deleteFields(targetpath,delfieldslist):
    """确认字段是否存在，存在则删除"""

    fieldslist = [field.name for field in arcpy.ListFields(targetpath)]

    deleteList = []

    for field in delfieldslist:

        if field in fieldslist:

            deleteList.append(field)
    
    if len(deleteList) > 0:

        arcpy.DeleteField_management(targetpath,deleteList)

def ensureFields(targetpath,newfieldslist):
    """确认字段是否存在，不存在创建新字段"""

    fieldslist = [field.name for field in arcpy.ListFields(targetpath)]

    for field in newfieldslist:

        if field not in fieldslist:

            arcpy.AddMessage("创建  "+field)

            arcpy.AddField_management(targetpath, field, "TEXT")

def checkField(targetpath,fieldslist):

    list = [field.name for field in arcpy.ListFields(targetpath)]

    for f in fieldslist:

        if f not in list and "SHAPE@" not in f:

            arcpy.AddMessage("createTempDatas : 不存在 "+f)

def createTempDatas(searchFields,tempFields,targetpath,datas,where_clause = "",sql_clause = (None,None)):
    """根据输入字段和条件SQL筛选数据，并把每条记录构建成dict格式"""

    checkField(targetpath,searchFields)

    for row in arcpy.da.SearchCursor(targetpath, searchFields,where_clause = where_clause,sql_clause = sql_clause):

        data = {}
        for i in range(len(tempFields)):

            data[tempFields[i]]  = dealNone.dealNoneAndBlank(row[i]) 

        datas.append(data)

def createTempLayer(targetpath,tempTargetPath,indexFields = [],where_clause = ""):
    """根据筛选条件创建临时图层,并创建索引"""

    arcpy.MakeFeatureLayer_management(targetpath, tempTargetPath,where_clause)

    createIndex(tempTargetPath,indexFields)

def createIndex(targetpath,indexFields = []):
    """创建空间索引和属性索引,创建属性索引之前判断是否存在该索引"""

    arcpy.AddSpatialIndex_management(targetpath)

    indexlist = [str(index.name.lower()) for index in arcpy.ListIndexes(targetpath)]

    for field in indexFields:
        
        if field not in indexlist:

                try:
                        arcpy.AddIndex_management(targetpath,field,field)
                except arcpy.ExecuteError:
                        arcpy.GetMessages() 

def createExistsTempLayer(targetpath,outputPath,indexFields = [],where_clause = ""):
    """创建临时图层的文件，写入到磁盘中"""

    if arcpy.Exists(outputPath):
        
        arcpy.Delete_management(outputPath)

    createTempLayer(targetpath,"tempTargetPath",indexFields = indexFields,where_clause = where_clause)

    arcpy.CopyFeatures_management("tempTargetPath",outputPath)