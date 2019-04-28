#!python
import arcpy,arcpyDeal

def judge(xzkPath):
    """�жϱ仯����"""

    xzknum = int(arcpy.GetCount_management(xzkPath).getOutput(0))

    arcpyDeal.ensureFields(xzkPath,['shuvary','shpvary'])

    xzkcur = arcpy.da.UpdateCursor(xzkPath,['cskmianji','SHAPE@AREA','shpvary'])

    for row in xzkcur:

        if abs(float(row[0].decode("utf-8"))- row[1])<0.1:
        
            row[2] = 'N'
            
        else:
        
            row[2] = 'Y'
            
        xzkcur.updateRow(row)
    
    searchFields = ['shuvary','dlbm','cskdlbm',"WJZLX",'GDLX','TBXHDM','GDZZSXDM']

    xzkcur = arcpy.da.UpdateCursor(xzkPath,searchFields)

    for row in xzkcur:

        data = dict(zip(searchFields,row))

        if data["dlbm"] == data["cskdlbm"] and data['WJZLX'] != '' and data['GDLX'] != '' and data['TBXHDM'] != '' and data['GDZZSXDM'] != '':
        
            row[0] = 'N'
            
        else:
        
            row[0] = 'Y'   
            
        xzkcur.updateRow(row)   

def delNoChange(xzkPath,nochangepath):
    """ɾ���ޱ仯ͼ��"""

    where_clause = "shuvary = 'N' and shpvary = 'N'"

    arcpy.MakeFeatureLayer_management(xzkPath,"xzkPath")

    arcpy.SelectLayerByAttribute_management("xzkPath",where_clause=where_clause)

    arcpy.CopyFeatures_management("xzkPath",nochangepath)

    arcpy.DeleteFeatures_management("xzkPath")

if __name__ == "__main__":
    
    arcpy.AddMessage("6_��ʼ�жϱ仯����")
    
    xzkPath = arcpy.GetParameterAsText(0)
    nochangepath = "nochangepath_5"

    arcpy.AddMessage("6_�жϱ仯����")
    judge(xzkPath)

    arcpy.AddMessage("6_ɾ���ޱ仯ͼ��")
    delNoChange(xzkPath,nochangepath)

    arcpy.SetParameterAsText(1,xzkPath)
    arcpy.AddMessage("6_�����жϱ仯����")




