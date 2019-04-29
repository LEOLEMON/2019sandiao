#!python
import arcpy,arcpyDeal

def judge(xzkpath,dissolvepath):

    arcpy.Dissolve_management(xzkpath,dissolvepath,'cskbsm','','SINGLE_PART','UNSPLIT_LINES')

    bsmareaList = {}

    with arcpy.da.SearchCursor(dissolvepath,["cskbsm","SHAPE@AREA"]) as cur:

        for row in cur:

            bsmareaList[row[0]] = row[1]

    delbsm = []

    with arcpy.da.SearchCursor(xzkpath,["cskbsm","cskmianji"]) as cur:

        for row in cur:

            if abs(bsmareaList[row[0]] - row[1]) > 0.1 and row[0] not in delbsm:

                delbsm.append(row[0])

    return delbsm

def delBsm(xzkpath,lackbsmpath,delbsm):

    where_clause = " cskbsm in (%s)"%("'"+("','".join(delbsm)+"'"))

    arcpy.MakeFeatureLayer_management(xzkpath,"xzkpath")

    arcpy.SelectLayerByAttribute_management("xzkpath",where_clause=where_clause)

    count = int(arcpy.GetCount_management("xzkpath").getOutput(0))

    arcpy.AddMessage("����%s���ϱ����ݲ�ȫ��ͼ��"%count)

    arcpy.CopyFeatures_management("xzkpath",lackbsmpath)
    
    arcpy.DeleteFeatures_management("xzkpath")

if __name__ == "__main__":
    
    arcpy.AddMessage("6_��ʼ�����Щͼ��BSM��ȫ")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    lackbsmpath = 'lackbsmpath_6'
    dissolvepath = 'dissolvepath_6'

    arcpy.AddMessage("6_�ж���ЩBSMͼ�߲�ȫ")
    delbsm = judge(xzkpath,dissolvepath)
        
    arcpy.AddMessage("6_ɾ����ȫ����״��ͼ��")
    delBsm(xzkpath,lackbsmpath,delbsm)

    arcpy.SetParameterAsText(2,xzkpath)
    arcpy.AddMessage("6_���������Щͼ��BSM��ȫ")