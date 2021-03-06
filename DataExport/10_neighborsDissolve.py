#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,json

def dissolve(xzkpath,dissolvepath,outputxzkpath):
    """融合相同属性数据"""

    arcpy.Dissolve_management(xzkpath,dissolvepath,'dlbm;zldwdm;gdlx;tbxhdm;gdzzsxdm;xzkfzh','','SINGLE_PART','UNSPLIT_LINES')

    arcpyDeal.deleteFields(dissolvepath,['ZLDWDM','DLBM','GDLX','TBXHDM','GDZZSXDM','xzkfzh'])

    # arcpy.SpatialJoin_analysis(target_features=dissolvepath, join_features=xzkpath, out_feature_class=outputxzkpath, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_COMMON", field_mapping="""bsm_list "bsm_list" true true false 1024 Text 0 0 ,Join,",",%s,cskbsm,-1,-1;cskbsm "cskbsm" true true false 1024 Text 0 0 ,First,#,%s,cskbsm,-1,-1"""%(xzkpath,xzkpath), match_option="CONTAINS", search_radius="", distance_field_name="")

    arcpy.SpatialJoin_analysis(target_features=dissolvepath, join_features=xzkpath, out_feature_class=outputxzkpath,join_operation="JOIN_ONE_TO_ONE",join_type="KEEP_ALL",field_mapping="""
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
    xzkfzh "xzkfzh" true true false 4 Long 0 0 ,First,#,%s,xzkfzh,-1,-1;
    OLDTAG "OLDTAG" true true false 10 Text 0 0 ,Join,",",%s,OLDTAG,-1,-1;
    ZZJZTB "ZZJZTB" true true false 10 Text 0 0 ,Join,",",%s,ZZJZTB,-1,-1;
    bsm_list "bsm_list" true true false 1024 Text 0 0 ,Join,",",%s,cskbsm,-1,-1;
    """%(xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath), match_option="CONTAINS")

    arcpy.MakeFeatureLayer_management(outputxzkpath,"test")

if __name__ == "__main__":
    """融合前后BSM总数一定要对的上"""
    
    arcpy.AddMessage("10_开始更新范围")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    dissolvepath = 'dissolvepath_10'
    outputxzkpath = 'outputxzkpath_10'

    arcpy.AddMessage("10_融合相同属性数据")
    dissolve(xzkpath,dissolvepath,outputxzkpath)
        
    arcpy.SetParameterAsText(2,outputxzkpath)
    arcpy.AddMessage("10_结束更新范围")