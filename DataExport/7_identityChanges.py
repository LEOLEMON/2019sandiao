#!python
import arcpy,arcpyDeal

def dissolve(xzkpath,dissolvepath,outputxzkpath):
    """融合相同属性，bsm一致的图斑,保证只有属性变化的图斑与周边图斑不在同一个分组号内"""

    arcpy.RepairGeometry_management (xzkpath, "KEEP_NULL")

    arcpy.CheckGeometry_management(xzkpath,"dissolvepath_7_CheckGeometry")

    searchFields = ['cskbsm','dlbm','zldwdm','gdlx','tbxhdm','gdzzsxdm']

    arcpy.AddMessage("融合字段："+';'.join(searchFields))

    arcpy.Dissolve_management(xzkpath,dissolvepath,"ZLDWDM;DLBM;GDLX;TBXHDM;GDZZSXDM;cskbsm","#","SINGLE_PART","UNSPLIT_LINES")

    arcpyDeal.deleteFields(dissolvepath,searchFields)

    arcpy.SpatialJoin_analysis(dissolvepath,xzkpath,outputxzkpath,join_operation= "JOIN_ONE_TO_ONE",join_type="KEEP_ALL",match_option="CONTAINS")

def judge(outputxzkpath):
    """判断变化类型"""

    xzknum = int(arcpy.GetCount_management(outputxzkpath).getOutput(0))

    arcpyDeal.ensureFields(outputxzkpath,['shuvary','shpvary'])

    xzkcur = arcpy.da.UpdateCursor(outputxzkpath,['cskmianji','SHAPE@AREA','shpvary'])

    for row in xzkcur:

        if abs(row[0]- row[1])<0.1:
        
            row[2] = 'N'
            
        else:
        
            row[2] = 'Y'
            
        xzkcur.updateRow(row)
    
    searchFields = ['shuvary','dlbm','cskdlbm',"WJZLX",'GDLX','TBXHDM','GDZZSXDM']

    xzkcur = arcpy.da.UpdateCursor(outputxzkpath,searchFields)

    for row in xzkcur:

        data = dict(zip(searchFields,row))

        if data["dlbm"] == data["cskdlbm"] and data['WJZLX'] != '' and data['GDLX'] != '' and data['TBXHDM'] != '' and data['GDZZSXDM'] != '':
        
            row[0] = 'N'
            
        else:
        
            row[0] = 'Y'   
            
        xzkcur.updateRow(row)   

def delNoChange(outputxzkpath,nochangepath):
    """删除无变化图斑"""

    where_clause = "shuvary = 'N' and shpvary = 'N'"

    arcpy.MakeFeatureLayer_management(outputxzkpath,"outputxzkpath")

    arcpy.SelectLayerByAttribute_management("outputxzkpath",where_clause=where_clause)

    arcpy.CopyFeatures_management("outputxzkpath",nochangepath)

    arcpy.DeleteFeatures_management("outputxzkpath")

if __name__ == "__main__":
    
    arcpy.AddMessage("7_开始判断变化类型")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    nochangepath = "nochangepath_7"
    dissolvepath = "dissolvepath_7"
    outputxzkpath = "outputxzkpath_7"

    arcpy.AddMessage("7_融合相同初始库BSM，属性一致的图斑")
    dissolve(xzkpath,dissolvepath,outputxzkpath)

    arcpy.AddMessage("7_判断变化类型")
    judge(outputxzkpath)

    arcpy.AddMessage("7_删除无变化图斑")
    delNoChange(outputxzkpath,nochangepath)

    arcpy.SetParameterAsText(2,outputxzkpath)
    arcpy.AddMessage("7_结束判断变化类型")




