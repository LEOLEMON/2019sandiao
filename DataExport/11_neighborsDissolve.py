#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,json

def dissolve2(xzkpath,dissolvepath,outputxzkpath):
    """融合相同属性数据"""

    arcpy.Dissolve_management(xzkpath,dissolvepath,'dlbm;zldwdm;gdlx;tbxhdm;gdzzsxdm;xzkfzh','','SINGLE_PART','UNSPLIT_LINES')

    arcpyDeal.deleteFields(dissolvepath,['ZLDWDM','DLBM','GDLX','TBXHDM','GDZZSXDM'])

    # arcpy.SpatialJoin_analysis(target_features=dissolvepath, join_features=xzkpath, out_feature_class=outputxzkpath, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_COMMON", field_mapping="""bsm_list "bsm_list" true true false 1024 Text 0 0 ,Join,",",%s,cskbsm,-1,-1;cskbsm "cskbsm" true true false 1024 Text 0 0 ,First,#,%s,cskbsm,-1,-1"""%(xzkpath,xzkpath), match_option="CONTAINS", search_radius="", distance_field_name="")

    arcpy.SpatialJoin_analysis(target_features=dissolvepath, join_features=xzkpath, out_feature_class=outputxzkpath,join_operation="JOIN_ONE_TO_ONE",join_type="KEEP_ALL",field_mapping="""
    ZLDWDM "ZLDWDM" true true false 255 Text 0 0 ,First,#,%s,ZLDWDM,-1,-1;
    DLBM "DLBM" true true false 255 Text 0 0 ,First,#,%s,DLBM,-1,-1;
    GDLX "GDLX" true true false 255 Text 0 0 ,First,#,%s,GDLX,-1,-1;
    TBXHDM "TBXHDM" true true false 255 Text 0 0 ,First,#,%s,TBXHDM,-1,-1;
    GDZZSXDM "GDZZSXDM" true true false 255 Text 0 0 ,First,#,%s,GDZZSXDM,-1,-1;
    xzkfzh "xzkfzh" true true false 10 Text 0 0 ,First,#,%s,xzkfzh,-1,-1;
    TSTYBM "TSTYBM" true true false 255 Text 0 0 ,First,#,%s,TSTYBM,-1,-1;
    BSM "BSM" true true false 255 Text 0 0 ,First,#,%s,BSM,-1,-1;
    JZSJ "JZSJ" true true false 255 Text 0 0 ,First,#,%s,JZSJ,-1,-1;
    WJZLX "WJZLX" true true false 255 Text 0 0 ,First,#,%s,WJZLX,-1,-1;
    CZCSXM "CZCSXM" true true false 255 Text 0 0 ,First,#,%s,CZCSXM,-1,-1;
    TBXHMC "TBXHMC" true true false 255 Text 0 0 ,First,#,%s,TBXHMC,-1,-1;
    GDZZSXMC "GDZZSXMC" true true false 255 Text 0 0 ,First,#,%s,GDZZSXMC,-1,-1;
    SJDLBM "SJDLBM" true true false 255 Text 0 0 ,First,#,%s,SJDLBM,-1,-1;
    width "width" true true false 8 Double 0 0 ,First,#,%s,width,-1,-1;
    cskmianji "cskmianji" true true false 8 Double 0 0 ,First,#,%s,cskmianji,-1,-1;
    cskbsm "cskbsm" true true false 255 Text 0 0 ,First,#,%s,cskbsm,-1,-1;
    cskzldwdm "cskzldwdm" true true false 255 Text 0 0 ,First,#,%s,cskzldwdm,-1,-1;
    cskdlbm "cskdlbm" true true false 255 Text 0 0 ,First,#,%s,cskdlbm,-1,-1;
    cskczcsxm "cskczcsxm" true true false 255 Text 0 0 ,First,#,%s,cskczcsxm,-1,-1;
    OLDTAG "OLDTAG" true true false 20 Text 0 0 ,First,",",%s,OLDTAG,-1,-1;
    ZZJZTB "ZZJZTB" true true false 10 Text 0 0 ,First,",",%s,ZZJZTB,-1,-1;
    bsm_list "bsm_list" true true false 1024 Text 0 0 ,Join,",",%s,cskbsm,-1,-1;
    tstybmlist "tstybmlist" true true false 2000 Text 0 0 ,Join,",",%s,TSTYBM,-1,-1;
    """%(xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath), match_option="CONTAINS")

    arcpy.MakeFeatureLayer_management(outputxzkpath,"test")

def getRelation(outputxzkpath,enviroment,relationpath):
    """插入新旧图属统一编码关系"""
    
    relationList = []

    count = int(arcpy.GetCount_management(outputxzkpath).getOutput(0))

    arcpy.SetProgressor('step','11_获取照片点融合',0,count,1)

    with arcpy.da.SearchCursor(outputxzkpath,["TSTYBM","tstybmlist"]) as cur:

        for row in cur:

            if len(row[1]) > 36:

                tstybmlist = row[1].split(",")

                for oldtstybm in tstybmlist:

                    relationList.append([oldtstybm,row[0]])

            arcpy.SetProgressorPosition()

    arcpy.CreateTable_management(enviroment,relationpath)

    newFields = ["oldfield","newfields"]

    arcpyDeal.ensureFields(relationpath,newFields)

    insertcur = arcpy.da.InsertCursor(relationpath,newFields)

    for relation in relationList:

        insertcur.insertRow(relation)

        arcpy.SetProgressorPosition()

if __name__ == "__main__":
    """融合前后BSM总数一定要对的上"""
    
    arcpy.AddMessage("11_开始更新范围")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    relationpath = "relationpath_11"
    dissolvepath = 'dissolvepath_11'
    outputxzkpath = 'outputxzkpath_11'

    arcpy.AddMessage("11_修复数据")
    arcpy.RepairGeometry_management (xzkpath, "KEEP_NULL")

    arcpy.AddMessage("11_融合相同属性数据")
    dissolve2(xzkpath,dissolvepath,outputxzkpath)

    arcpy.AddMessage("11_获取融合照片点")
    getRelation(outputxzkpath,enviroment,relationpath)
        
    arcpy.SetParameterAsText(2,outputxzkpath)
    arcpy.SetParameterAsText(3,relationpath)
    arcpy.AddMessage("11_结束更新范围")