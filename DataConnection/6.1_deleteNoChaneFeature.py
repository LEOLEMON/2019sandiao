#-*- coding:utf-8 -*-
#encoding:utf-8
#!python

import arcpy,json,dealNone,arcpyDeal,pathArgs

def start(targetpath,outname):

    arcpyDeal.createExistsTempLayer(targetpath,outname)

    cursor = arcpy.da.UpdateCursor(outname,["bhlx"])

    result = arcpy.GetCount_management(outname)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','遍历进度',0,count,1)

    for row in cursor:
        
        bhlx = dealNone.dealNoneAndBlank(row[0])

        if bhlx == "":

            cursor.deleteRow()

        arcpy.SetProgressorPosition()

if __name__ == "__main__":
    
    arcpy.AddMessage("6.1_开始删除无任何变化的图斑")

    targetpath = arcpy.GetParameterAsText(0)
    enviroment = arcpy.GetParameterAsText(1)
    outname = arcpy.GetParameterAsText(2)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = enviroment

    start(targetpath,outname)

    outpath = arcpy.Describe(outname).catalogPath

    arcpy.SetParameterAsText(3,outpath)

    arcpy.AddMessage("6.1_结束")
    
    