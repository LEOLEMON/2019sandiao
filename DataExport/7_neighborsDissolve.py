#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,json

def dissolve1(xzkpath,dissolvepath,outputxzkpath1):
    """融合相同属性，bsm一致的图斑,保证只有属性变化的图斑与周边图斑不在同一个分组号内"""

    arcpy.CheckGeometry_management(xzkpath,"dissolvepath_7_CheckGeometry")

    searchFields = ['cskbsm','dlbm','zldwdm','gdlx','tbxhdm','gdzzsxdm']

    arcpy.AddMessage("融合字段："+';'.join(searchFields))

    arcpy.Dissolve_management(xzkpath,dissolvepath1,"ZLDWDM;DLBM;GDLX;TBXHDM;GDZZSXDM;cskbsm","#","SINGLE_PART","UNSPLIT_LINES")

    arcpyDeal.deleteFields(dissolvepath1,searchFields)

    arcpy.SpatialJoin_analysis(dissolvepath1,xzkpath,outputxzkpath1,join_operation= "JOIN_ONE_TO_ONE",join_type="KEEP_ALL",match_option="CONTAINS",field_mapping="""
        DLBM "DLBM" true true false 5 Text 0 0 ,First,#,%s,DLBM,-1,-1;
        ZLDWDM "ZLDWDM" true true false 19 Text 0 0 ,First,#,%s,ZLDWDM,-1,-1;
        GDLX "GDLX" true true false 2 Text 0 0 ,First,#,%s,GDLX,-1,-1;
        TBXHDM "TBXHDM" true true false 4 Text 0 0 ,First,#,%s,TBXHDM,-1,-1;
        GDZZSXDM "GDZZSXDM" true true false 8 Text 0 0 ,First,#,%s,GDZZSXDM,-1,-1;
        LINKTBS "LINKTBS" true true false 254 Text 0 0 ,First,#,%s,LINKTBS,-1,-1;
        TBXHMC "TBXHMC" true true false 20 Text 0 0 ,First,#,%s,TBXHMC,-1,-1;
        GDZZSXMC "GDZZSXMC" true true false 20 Text 0 0 ,First,#,%s,GDZZSXMC,-1,-1;
        CZCSXM "CZCSXM" true true false 4 Text 0 0 ,First,#,%s,CZCSXM,-1,-1;
        TSTYBM "TSTYBM" true true false 100 Text 0 0 ,First,#,%s,TSTYBM,-1,-1;
        SJDLBM "SJDLBM" true true false 100 Text 0 0 ,First,#,%s,SJDLBM,-1,-1;
        OLDTAG "OLDTAG" true true false 20 Text 0 0 ,First,#,%s,OLDTAG,-1,-1;
        JZSJ "JZSJ" true true false 8 Date 0 0 ,First,#,%s,JZSJ,-1,-1;
        BSM "BSM" true true false 18 Text 0 0 ,First,#,%s,BSM,-1,-1;
        ZZJZTB "ZZJZTB" true true false 1 Text 0 0 ,First,#,%s,ZZJZTB,-1,-1;
        WJZLX "WJZLX" true true false 8 Text 0 0 ,First,#,%s,WJZLX,-1,-1;
        cskmianji "cskmianji" true true false 8 Double 0 0 ,First,#,%s,cskmianji,-1,-1;
        cskbsm "cskbsm" true true false 255 Text 0 0 ,First,#,%s,cskbsm,-1,-1;
        cskzldwdm "cskzldwdm" true true false 255 Text 0 0 ,First,#,%s,cskzldwdm,-1,-1;
        cskdlbm "cskdlbm" true true false 255 Text 0 0 ,First,#,%s,cskdlbm,-1,-1;
        cskczcsxm "cskczcsxm" true true false 255 Text 0 0 ,First,#,%s,cskczcsxm,-1,-1;
        tstybmlist "tstybmlist" true true false 2000 Text 0 0 ,Join,",",%s,TSTYBM,-1,-1;"""%(xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath))

def dissolve2(xzkpath,dissolvepath,outputxzkpath2):
    """融合相同属性数据"""

    arcpy.Dissolve_management(xzkpath,dissolvepath2,'dlbm;zldwdm;gdlx;tbxhdm;gdzzsxdm','','SINGLE_PART','UNSPLIT_LINES')

    arcpyDeal.deleteFields(dissolvepath2,['ZLDWDM','DLBM','GDLX','TBXHDM','GDZZSXDM'])

    # arcpy.SpatialJoin_analysis(target_features=dissolvepath, join_features=xzkpath, out_feature_class=outputxzkpath, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_COMMON", field_mapping="""bsm_list "bsm_list" true true false 1024 Text 0 0 ,Join,",",%s,cskbsm,-1,-1;cskbsm "cskbsm" true true false 1024 Text 0 0 ,First,#,%s,cskbsm,-1,-1"""%(xzkpath,xzkpath), match_option="CONTAINS", search_radius="", distance_field_name="")

    arcpy.SpatialJoin_analysis(target_features=dissolvepath2, join_features=xzkpath, out_feature_class=outputxzkpath2,join_operation="JOIN_ONE_TO_ONE",join_type="KEEP_ALL",field_mapping="""
    ZLDWDM "ZLDWDM" true true false 255 Text 0 0 ,First,#,%s,ZLDWDM,-1,-1;
    DLBM "DLBM" true true false 255 Text 0 0 ,First,#,%s,DLBM,-1,-1;
    GDLX "GDLX" true true false 255 Text 0 0 ,First,#,%s,GDLX,-1,-1;
    TBXHDM "TBXHDM" true true false 255 Text 0 0 ,First,#,%s,TBXHDM,-1,-1;
    GDZZSXDM "GDZZSXDM" true true false 255 Text 0 0 ,First,#,%s,GDZZSXDM,-1,-1;
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
    tstybmlist "tstybmlist" true true false 2000 Text 0 0 ,Join,",",%s,TSTYBM,-1,-1；
    """%(xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath), match_option="CONTAINS")

    arcpy.MakeFeatureLayer_management(outputxzkpath2,"test")

def getRelation(outputxzkpath1,outputxzkpath2,enviroment,relationpath):
    """插入新旧图属统一编码关系"""
    
    relationList = []

    count = int(arcpy.GetCount_management(outputxzkpath1).getOutput(0)) + int(arcpy.GetCount_management(outputxzkpath2).getOutput(0))

    arcpy.SetProgressor('step','7_获取照片点融合',0,count,1)

    with arcpy.da.SearchCursor(outputxzkpath1,["TSTYBM","tstybmlist"]) as cur:

        for row in cur:

            if len(row[1]) > 36:

                tstybmlist = row[1].split(",")

                for oldtstybm in tstybmlist:

                    relationList.append([oldtstybm,row[0]])

            arcpy.SetProgressorPosition()

    with arcpy.da.SearchCursor(outputxzkpath2,["TSTYBM","tstybmlist"]) as cur:

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
    
    arcpy.AddMessage("7_开始更新范围")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    relationpath = "relationpath_7"
    dissolvepath1 = "dissolvepath_7_1"
    outputxzkpath1 = "outputxzkpath_7_1"
    dissolvepath2 = 'dissolvepath_7_2'
    outputxzkpath2 = 'outputxzkpath_7_2'

    arcpy.AddMessage("7_修复数据")
    arcpy.RepairGeometry_management (xzkpath, "KEEP_NULL")

    arcpy.AddMessage("7_融合相同初始库BSM，属性一致的图斑")
    dissolve1(xzkpath,dissolvepath1,outputxzkpath1)

    arcpy.AddMessage("7_融合相同属性数据")
    dissolve2(outputxzkpath1,dissolvepath2,outputxzkpath2)

    arcpy.AddMessage("7_获取融合照片点")
    getRelation(outputxzkpath1,outputxzkpath2,enviroment,relationpath)
        
    arcpy.SetParameterAsText(2,outputxzkpath2)
    arcpy.AddMessage("7_结束更新范围")