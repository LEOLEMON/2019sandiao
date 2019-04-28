#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,arcpyDeal

if __name__ == "__main__":
    
    arcpy.AddMessage("2_������ʱ����")

    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)
    cskpath = arcpy.GetParameterAsText(2)
    photopath = arcpy.GetParameterAsText(3)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    tempxzkpath = "outputxzkpath_2"
    tempPhotoPath = "outputtppath_2"
    tempcskpath = "outputcskpath_2"

    keepTargetFields = ["TSTYBM","BSM","ZLDWDM","JZSJ",'DLBM',"WJZLX","CZCSXM",'GDLX','TBXHDM','TBXHMC','GDZZSXDM','GDZZSXMC','LINKTBS','SJDLBM']
    keepBDTBFields = ["ZLDWDM","BSM","DLBM","CZCSXM"]

    arcpy.AddMessage("2_��״��")
    arcpyDeal.copyToTempLayer(enviroment,xzkpath,tempxzkpath,keepFields=keepTargetFields)

    arcpy.AddMessage("2_��ʼ��")
    arcpyDeal.copyToTempLayer(enviroment,cskpath,tempcskpath,keepFields=keepBDTBFields)

    arcpy.AddMessage("2_��Ƭ��")
    # arcpyDeal.createExistsTempLayer(photopath,tempPhotoPath)

    arcpy.SetParameterAsText(4,tempxzkpath)
    arcpy.SetParameterAsText(5,tempcskpath)
    arcpy.SetParameterAsText(6,tempPhotoPath)
    arcpy.AddMessage("2_����")