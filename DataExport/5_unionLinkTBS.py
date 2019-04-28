#!python
import arcpy,arcpyDeal

def setLINKTBS(xzkpath):
    """��linktbsָ���ͼ�ߵ�linktbs�ֶ���Ϊ�������bsm,û�а���LINKTBSָ���ͼ�߰���˳����"""

    where_clause1 =  " LINKTBS <> ''"

    linktbsList = []
    tstybmList = []

    with arcpy.da.SearchCursor(xzkpath,["LINKTBS","TSTYBM"],where_clause1) as cur:

        for row in cur:

            linktbsList.append(row[0])
            tstybmList.append(row[1])

    num = 0

    with arcpy.da.UpdateCursor(xzkpath,["BSM","LINKTBS"]) as cur:

        for row in cur:

            BSM = row[0]
            LINKTBS = row[1]

            if BSM in linktbsList:

                row[1] = BSM

            elif len(LINKTBS) !=18:

                row[1] = num

                num += 1

            cur.updateRow(row)

            arcpy.SetProgressorPosition()

    return tstybmList

def outputLINKTBS(xzkpath,tstybmList,dellinktbspath):
    """ɾ��LINKTBSͼ�߲����"""

    where_clause = " TSTYBM in (%s)"%("'"+("','".join(tstybmList)+"'"))

    arcpy.AddMessage(where_clause)

    arcpy.MakeFeatureLayer_management(xzkpath,"xzkpath")

    arcpy.SelectLayerByAttribute_management("xzkpath",where_clause=where_clause)

    count = int(arcpy.GetCount_management("xzkpath").getOutput(0))

    arcpy.AddMessage("����%s������LINKTBS��ͼ��"%count)

    arcpy.CopyFeatures_management("xzkpath",dellinktbspath)

    arcpy.DeleteFeatures_management("xzkpath")

def checkNone(outputxzkpath,dellinktbspath,nullTSTYBMpath):

    where_clause = "TSTYBM is null"

    arcpy.MakeFeatureLayer_management(outputxzkpath,"outputxzkpath")

    arcpy.SelectLayerByAttribute_management("outputxzkpath",where_clause=where_clause)

    count = int(arcpy.GetCount_management("outputxzkpath").getOutput(0))

    arcpy.AddMessage("����%s��û�й��������Ե�ͼ��"%count)

    if count > 0:

        arcpy.SpatialJoin_analysis("outputxzkpath",dellinktbspath,nullTSTYBMpath,"JOIN_ONE_TO_ONE","KEEP_ALL","TSTYBM \"TSTYBM\" true true false 255 Text 0 0 ,First,#,\"outputxzkpath\",TSTYBM,-1,-1;TSTYBM_1 \"TSTYBM_1\" true true false 50 Text 0 0 ,First,#,"+dellinktbspath+",TSTYBM,-1,-1","CONTAINS","#","#")

        arcpy.DeleteFeatures_management("outputxzkpath")

        tstybmList = []

        with arcpy.da.SearchCursor(nullTSTYBMpath,["TSTYBM_1"]) as cur:

            for row in cur:

                tstybmList.append(row[0])

        where_clause = " TSTYBM in (%s)"%("'"+("','".join(tstybmList)+"'"))

        searchFields = ["TSTYBM","BSM","ZLDWDM","JZSJ","DLBM","WJZLX","CZCSXM","GDLX","TBXHDM","GDZZSXDM","LINKTBS","SJDLBM","cskbsm","cskzldwdm","cskdlbm","cskmianji","shuvary","shpvary","error","repetitive","SHAPE@"]

        arcpyDeal.checkField(outputxzkpath,searchFields)
        arcpyDeal.checkField(dellinktbspath,searchFields)

        insertrows = arcpy.da.InsertCursor(outputxzkpath,searchFields)

        with arcpy.da.SearchCursor(dellinktbspath,searchFields,where_clause=where_clause) as cur:

            for row in cur:

                insertrows.insertRow(row)

if __name__ == "__main__":
    
    arcpy.AddMessage("5_��ʼLinkTBS�ں�")

    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    dissolvepath = "dissolvepath_5"
    dellinktbspath = "dellinktbspath_5"
    outputxzkpath = "outputxzkpath_5"
    nullTSTYBMpath = "nullTSTYBMpath_5"

    arcpy.AddMessage("5_����LINKTBSֵ")
    count = int(arcpy.GetCount_management(xzkpath).getOutput(0))
    arcpy.SetProgressor('step','5_����LINKTBSֵ',0,count,1)
    tstybmList = setLINKTBS(xzkpath)

    arcpy.AddMessage("5_�ں���ͬLINKTBS����")
    arcpy.Dissolve_management(xzkpath,dissolvepath,"LINKTBS","","SINGLE_PART","DISSOLVE_LINES")

    arcpy.AddMessage("5_ɾ������LINKTBS��ͼ��")
    outputLINKTBS(xzkpath,tstybmList,dellinktbspath)

    arcpy.AddMessage("5_�����Թ������ں�ͼ��")
    arcpy.SpatialJoin_analysis(target_features=dissolvepath, join_features=xzkpath,out_feature_class=outputxzkpath,join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",match_option="CONTAINS")

    arcpy.AddMessage("5_����Ƿ����û�й��������Ե�ͼ��")
    checkNone(outputxzkpath,dellinktbspath,nullTSTYBMpath)

    arcpy.SetParameterAsText(2,outputxzkpath)
    arcpy.AddMessage("5_����LinkTBS�ں�")