#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,dealNone,arcpyDeal
        
def collectWJZTB(targetpath,photopath):
    """关联图斑和照片点图层,得到关联数据"""

    baseName1 = arcpy.Describe(targetpath).baseName
    baseName2 = arcpy.Describe(photopath).baseName

    arcpy.AddMessage("6_7_创建临时图层")

    arcpy.MakeFeatureLayer_management ( targetpath, baseName1)
    arcpy.MakeFeatureLayer_management ( photopath, baseName2)

    arcpy.AddMessage("6_7_图层关联")

    arcpy.AddJoin_management(baseName1,"TSTYBM",baseName2,"TSTYBM")

    where_clause = u" exp_tblx = '一般核查图斑' and ZZJZTB = '0' and exp_tbxhdm = '' and exp_wjzlx = '' and %s.TSTYBM is null"%(baseName2)

    datas = []
    tempFields = ["TSTYBM","exp_sjdlbm","exp_czcsxm","exp_dlbm","exp_gdzzsxdm","exp_gdlx","CZCSXM"]
    searchFields =[baseName1+"."+f for f in tempFields]

    arcpyDeal.createTempDatas(searchFields,tempFields,baseName1,datas,where_clause=where_clause)

    return datas

def check01(data):
    "非耕地类型，内部流转"

    if data["exp_dlbm"][0:2] != "01" and data["exp_dlbm"][0:2] == data["exp_sjdlbm"][0:2]:

        if data["exp_gdlx"] != "" or data["exp_gdzzsxdm"] != "" :

            return True

    return False

def check02(data):
    """耕地类型，更改属性"""

    if data["exp_dlbm"][0:2] == "01" and data["exp_dlbm"] == data["exp_sjdlbm"]:

        if data["exp_gdlx"] != u"坡地":

            return True

    return False

def check03(data):

    if data["exp_dlbm"][0:2] in ["02","03"] and data["exp_sjdlbm"][0:2] in ["02","03"]:

        return True

    return False

def check04(data):

    if data["exp_sjdlbm"] in ["0702","GY","JY"] and data["exp_dlbm"][0:2] == "20" and data["CZCSXM"][0:2] == "20":

        return True

    return False

def check(datas):
    """遍历图斑进行检查"""

    targetValueList = []

    delTargetValueList = []

    for data in datas:

        bool01 = check01(data)

        bool02 = check02(data)

        bool03 = check03(data)

        bool04 = check04(data)

        if bool01 or bool02 or bool03 or bool04:

            targetValueList.append(data["TSTYBM"])
        
        else:

            delTargetValueList.append(data["TSTYBM"])

        arcpy.SetProgressorPosition()

    return targetValueList,delTargetValueList

def createLayer(targetpath,outname,tempoutname,delTargetValueList):
    """生成临时图层和要删除的要素的图层"""

    delstr = "'" + "','".join(delTargetValueList) + "'"

    where_clause = "TSTYBM in (%s)"%(delstr)

    arcpyDeal.createExistsTempLayer(targetpath,outname)

    arcpyDeal.createExistsTempLayer(targetpath,tempoutname,where_clause=where_clause)

def UpdateDatas(targetpath,targetValueList,delTargetValueList):
    """更新数据"""

    searchFields = ["TSTYBM","bhlx"]

    cursor = arcpy.da.UpdateCursor(targetpath,searchFields)

    for updateRow in cursor:

        TSTYBM = updateRow[0]

        if TSTYBM in targetValueList:

            updateRow[1] = "3"

            cursor.updateRow(updateRow)

        if TSTYBM in delTargetValueList:

            cursor.deleteRow()

        arcpy.SetProgressorPosition()

def start(targetpath,photopath,outname,tempoutname):
    
    arcpy.AddMessage("6_7_数据关联")
    datas = collectWJZTB(targetpath,photopath)

    arcpy.AddMessage("6_7_数据检查")
    count = len(datas)
    arcpy.SetProgressor('step',"6_7_数据检查",0,count,1)
    targetValueList,delTargetValueList =  check(datas)

    arcpy.AddMessage("6_7_生成输出图层")
    createLayer(targetpath,outname,tempoutname,delTargetValueList)

    arcpy.AddMessage("6_7_更新")
    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step',"6_7_更新",0,count,1)
    UpdateDatas(outname,targetValueList,delTargetValueList)

if __name__ == "__main__":
    
    arcpy.AddMessage("6_7_开始获取变化类型为3的图斑")

    targetpath = arcpy.GetParameterAsText(0)
    photopath = arcpy.GetParameterAsText(1)
    enviroment = arcpy.GetParameterAsText(2)

    outname = "output_6_7"
    tempoutname = "output_6_7_temp"

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = enviroment

    start(targetpath,photopath,outname,tempoutname)

    arcpy.SetParameterAsText(3,outname)

    arcpy.AddMessage("6_7_结束")