#!python
import arcpy,arcpyDeal

def dissolve(xzkpath,dissolvepath,outputxzkpath):
    """�ں���ͬ���ԣ�bsmһ�µ�ͼ��,��ֻ֤�����Ա仯��ͼ�����ܱ�ͼ�߲���ͬһ���������"""

    arcpy.RepairGeometry_management (xzkpath, "KEEP_NULL")

    arcpy.CheckGeometry_management(xzkpath,"dissolvepath_7_CheckGeometry")

    searchFields = ['cskbsm','dlbm','zldwdm','gdlx','tbxhdm','gdzzsxdm']

    arcpy.AddMessage("�ں��ֶΣ�"+';'.join(searchFields))

    arcpy.Dissolve_management(xzkpath,dissolvepath,"ZLDWDM;DLBM;GDLX;TBXHDM;GDZZSXDM;cskbsm","#","SINGLE_PART","UNSPLIT_LINES")

    arcpyDeal.deleteFields(dissolvepath,searchFields)

    arcpy.SpatialJoin_analysis(dissolvepath,xzkpath,outputxzkpath,join_operation= "JOIN_ONE_TO_ONE",join_type="KEEP_ALL",match_option="CONTAINS")

def judge(outputxzkpath):
    """�жϱ仯����"""

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
    """ɾ���ޱ仯ͼ��"""

    where_clause = "shuvary = 'N' and shpvary = 'N'"

    arcpy.MakeFeatureLayer_management(outputxzkpath,"outputxzkpath")

    arcpy.SelectLayerByAttribute_management("outputxzkpath",where_clause=where_clause)

    arcpy.CopyFeatures_management("outputxzkpath",nochangepath)

    arcpy.DeleteFeatures_management("outputxzkpath")

if __name__ == "__main__":
    
    arcpy.AddMessage("7_��ʼ�жϱ仯����")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    nochangepath = "nochangepath_7"
    dissolvepath = "dissolvepath_7"
    outputxzkpath = "outputxzkpath_7"

    arcpy.AddMessage("7_�ں���ͬ��ʼ��BSM������һ�µ�ͼ��")
    dissolve(xzkpath,dissolvepath,outputxzkpath)

    arcpy.AddMessage("7_�жϱ仯����")
    judge(outputxzkpath)

    arcpy.AddMessage("7_ɾ���ޱ仯ͼ��")
    delNoChange(outputxzkpath,nochangepath)

    arcpy.SetParameterAsText(2,outputxzkpath)
    arcpy.AddMessage("7_�����жϱ仯����")




