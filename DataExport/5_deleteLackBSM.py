#!python
import arcpy,arcpyDeal

def judge(xzkpath,dissolvepath):
    """������ͬ��ʼ������ںϣ��ռ��ں�������ʼ������������ͼ��"""

    arcpy.Dissolve_management(xzkpath,dissolvepath,'cskbsm','','SINGLE_PART','UNSPLIT_LINES')

    bsmareaList = {}

    with arcpy.da.SearchCursor(dissolvepath,["cskbsm","SHAPE@AREA"]) as cur:

        for row in cur:

            bsmareaList[row[0]] = row[1]

    delbsm = []

    with arcpy.da.SearchCursor(xzkpath,["cskbsm","cskmianji"]) as cur:

        for row in cur:

            if abs(row[1] - bsmareaList[row[0]]) > 0.15 and row[0] not in delbsm:

                delbsm.append(row[0])

    return delbsm

def delBsm(xzkpath,notfullpath,delbsm):
    """ɾ����ʼ��ͼ�߷�Χ�ڵ���״��ͼ�ߺϲ������ԭ�����������״��ͼ��"""

    where_clause = " cskbsm in (%s)"%("'"+("','".join(delbsm)+"'"))

    arcpy.MakeFeatureLayer_management(xzkpath,"xzkpath")

    arcpy.SelectLayerByAttribute_management("xzkpath",where_clause=where_clause)

    count = int(arcpy.GetCount_management("xzkpath").getOutput(0))

    arcpy.AddMessage("����%s���ϱ����ݲ�ȫ��ͼ��"%count)

    arcpy.CopyFeatures_management("xzkpath",notfullpath)
    
    arcpy.DeleteFeatures_management("xzkpath")

if __name__ == "__main__":
    
    arcpy.AddMessage("5_��ʼ�����Щͼ��δռ��ԭ��ʼ�ⷶΧ")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    dissolvepath = 'dissolvepath_5'
    notfullpath = 'notfullpath_5'

    arcpy.AddMessage("5_�ж���Щͼ��δռ��ԭ��ʼ�ⷶΧ")
    delbsm = judge(xzkpath,dissolvepath)
        
    arcpy.AddMessage("5_ɾ����ʼ��ͼ�߷�Χ�ڵ���״��ͼ�ߺϲ������ԭ�����������״��ͼ��")
    delBsm(xzkpath,notfullpath,delbsm)

    arcpy.SetParameterAsText(2,xzkpath)
    arcpy.AddMessage("5_���������Щͼ��δռ��ԭ��ʼ�ⷶΧ")