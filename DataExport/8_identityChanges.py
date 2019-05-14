#!python
import arcpy,arcpyDeal

def judge(outputxzkpath):
    """�жϱ仯����"""

    arcpy.SetProgressor('step',"8_�жϱ仯����",0,int(arcpy.GetCount_management(outputxzkpath).getOutput(0)),1)

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

        if data["dlbm"] == data["cskdlbm"] and data['WJZLX'] == '' and data['GDLX'] == '' and data['TBXHDM'] == '' and data['GDZZSXDM'] == '':
        
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

def domain(xzkpath):

    nochangepath = "nochangepath_9"

    arcpy.AddMessage("8_�жϱ仯����")
    judge(xzkpath)

    arcpy.AddMessage("8_ɾ���ޱ仯ͼ��")
    delNoChange(xzkpath,nochangepath)

if __name__ == "__main__":
    
    arcpy.AddMessage("8_��ʼ�жϱ仯����")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    nochangepath = "nochangepath_8"

    arcpy.AddMessage("8_�жϱ仯����")
    judge(xzkpath)

    arcpy.AddMessage("8_ɾ���ޱ仯ͼ��")
    delNoChange(xzkpath,nochangepath)

    arcpy.SetParameterAsText(2,xzkpath)
    arcpy.AddMessage("8_�����жϱ仯����")




