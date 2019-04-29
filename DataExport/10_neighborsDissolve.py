#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,json

def dissolve(xzkpath,dissolvepath,outputxzkpath):
    """融合相同属性数据"""

    arcpyDeal.ensureFields(xzkpath,['tmpshpvary'],"LONG")

    xzkcur = arcpy.da.UpdateCursor(xzkpath,['shpvary','tmpshpvary'])

    for row in xzkcur:
        
        if row[0] == 'Y':
            
            row[1] = 2
        
        elif row[0] == 'N':
        
            row[1] = 1
            
        xzkcur.updateRow(row)

    arcpy.Dissolve_management(xzkpath,dissolvepath,'dlbm;zldwdm;gdlx;tbxhdm;gdzzsxdm;xzkfzh','','SINGLE_PART','UNSPLIT_LINES')

    arcpy.SpatialJoin_analysis(target_features=dissolvepath, join_features=xzkpath, out_feature_class=outputxzkpath, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_COMMON", field_mapping="""TSTYBM "TSTYBM" true true false 1024 Text 0 0 ,Join,",",%s,TSTYBM,-1,-1;bsm_list "bsm_list" true true false 1024 Text 0 0 ,Join,",",%s,cskbsm,-1,-1;cskbsm "cskbsm" true true false 1024 Text 0 0 ,First,#,%s,cskbsm,-1,-1;shpvary "shpvary" true true false 100 Text 0 0 ,Join,#,%s,shpvary,-1,-1"""%(xzkpath,xzkpath,xzkpath,xzkpath), match_option="CONTAINS", search_radius="", distance_field_name="")

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