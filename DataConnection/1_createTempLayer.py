#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,arcpyDeal

def start(targetpath,BDTBpath,photopath,tempTargetPath,tempBDTBpath,tempPhotoPath):

    keepTargetFields = ["TSTYBM","BSM","ZLDWDM","JZSJ",'DLBM',"WJZLX","CZCSXM",'GDLX','TBXHDM','TBXHMC','GDZZSXDM','GDZZSXMC','LINKTBS','SJDLBM',"DLBM_1","GDZZSXMC_1","GDLX_1","TBXHMC_1"]
    keepBDTBFields = ["ZLDWDM","BSM","DLBM","CZCSXM"]

    arcpy.AddMessage("1_现状库")
    arcpyDeal.createExistsTempLayer(targetpath,tempTargetPath,keepFields=keepTargetFields)

    arcpy.AddMessage("1_初始库")
    arcpyDeal.createExistsTempLayer(BDTBpath,tempBDTBpath,keepFields=keepBDTBFields)

    arcpy.AddMessage("1_照片点")
    arcpyDeal.createExistsTempLayer(photopath,tempPhotoPath)

if __name__ == "__main__":
    
    arcpy.AddMessage("1_生成临时数据")
    
    arcpy.env.overwriteOutput = True

    enviroment = arcpy.GetParameterAsText(0)

    targetpath = arcpy.GetParameterAsText(1)
    BDTBpath = arcpy.GetParameterAsText(2)
    photopath = arcpy.GetParameterAsText(3)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = enviroment

    tempTargetPath = "BYZTB01"
    tempPhotoPath = "TP01"
    tempBDTBpath = "BDTP01"

    start(targetpath,BDTBpath,photopath,tempTargetPath,tempBDTBpath,tempPhotoPath)

    arcpy.SetParameterAsText(4,tempTargetPath)
    arcpy.SetParameterAsText(5,tempBDTBpath)
    arcpy.SetParameterAsText(6,tempPhotoPath)

    arcpy.AddMessage("1_结束")