#!python
import arcpy,arcpyDeal

def setLINKTBS(xzkpath):
    """��linktbsָ���ͼ�ߵ�linktbs�ֶ���Ϊ�������bsm,û�а���LINKTBSָ���ͼ�߰���˳����"""

    arcpy.SetProgressor('step','6_����LINKTBSֵ',0,int(arcpy.GetCount_management(xzkpath).getOutput(0)),1)

    where_clause1 =  " LINKTBS <> ''"

    linktbsList = []
    tstybmList = []
    relationList = []

    with arcpy.da.SearchCursor(xzkpath,["LINKTBS","TSTYBM"],where_clause1) as cur:

        for row in cur:

            linktbsList.append(row[0])
            tstybmList.append(row[1])

    num = 0

    with arcpy.da.UpdateCursor(xzkpath,["BSM","LINKTBS","TSTYBM"]) as cur:

        for row in cur:

            BSM = row[0]
            LINKTBS = row[1]

            if BSM in linktbsList:

                row[1] = BSM
                index = linktbsList.index(BSM)
                relationList.append([row[2],tstybmList[index]])

            elif len(LINKTBS) !=18:

                row[1] = num

                num += 1

            cur.updateRow(row)

            arcpy.SetProgressorPosition()

    return tstybmList,relationList

def outputLINKTBS(xzkpath,tstybmList,dellinktbspath):
    """ɾ��LINKTBSͼ�߲����"""

    where_clause = " TSTYBM in (%s)"%("'"+("','".join(tstybmList)+"'"))

    # arcpy.AddMessage(where_clause)

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

        searchFields = ["TSTYBM","BSM","ZLDWDM","JZSJ","DLBM","WJZLX","CZCSXM","GDLX","TBXHDM","GDZZSXDM","LINKTBS","SJDLBM","cskbsm","cskzldwdm","cskdlbm","cskmianji","OLDTAG","ZZJZTB","width","SHAPE@"]

        arcpyDeal.checkField(outputxzkpath,searchFields)
        arcpyDeal.checkField(dellinktbspath,searchFields)

        insertrows = arcpy.da.InsertCursor(outputxzkpath,searchFields)

        with arcpy.da.SearchCursor(dellinktbspath,searchFields,where_clause=where_clause) as cur:

            for row in cur:

                insertrows.insertRow(row)

def createRelation(relationList,enviroment,relationpath,dellinktbspath):
    """�ں���Ƭ�������Ƭ"""

    arcpy.SetProgressor('step','6_����LINKTBSֵ',0,len(relationList),1)

    arcpy.CreateTable_management(enviroment,relationpath)

    newFields = ["oldfield","newfields"]

    arcpyDeal.ensureFields(relationpath,newFields)

    insertcur = arcpy.da.InsertCursor(relationpath,newFields)

    arcpy.MakeFeatureLayer_management(dellinktbspath, "dellinktbspath")

    for relation in relationList:

        arcpy.SelectLayerByAttribute_management("dellinktbspath",where_clause=" TSTYBM = '%s'"%(relation[0]))

        count = int(arcpy.GetCount_management("dellinktbspath").getOutput(0))

        if count > 0:

            insertcur.insertRow(relation)

        arcpy.SetProgressorPosition()

if __name__ == "__main__":
    
    arcpy.AddMessage("6_��ʼLinkTBS�ں�")

    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    relationpath = "relationpath_6"
    dissolvepath = "dissolvepath_6"
    dellinktbspath = "dellinktbspath_6"
    outputxzkpath = "outputxzkpath_6"
    nullTSTYBMpath = "nullTSTYBMpath_6"

    arcpy.AddMessage("6_����LINKTBSֵ")
    tstybmList,relationList = setLINKTBS(xzkpath)

    arcpy.AddMessage("6_�ں���ͬLINKTBS����")
    arcpy.Dissolve_management(xzkpath,dissolvepath,"LINKTBS","","SINGLE_PART","DISSOLVE_LINES")

    arcpy.AddMessage("6_ɾ������LINKTBS��ͼ��")
    outputLINKTBS(xzkpath,tstybmList,dellinktbspath)

    arcpy.AddMessage("6_�����Թ������ں�ͼ��")
    arcpy.SpatialJoin_analysis(target_features=dissolvepath, join_features=xzkpath,out_feature_class=outputxzkpath,join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",match_option="CONTAINS")

    arcpy.AddMessage("6_����Ƿ����û�й��������Ե�ͼ��")
    checkNone(outputxzkpath,dellinktbspath,nullTSTYBMpath)

    arcpy.AddMessage("6_�����Ƭ��ͼ��ͳһ�����ϵ")
    createRelation(relationList,enviroment,relationpath,dellinktbspath)

    arcpy.SetParameterAsText(2,outputxzkpath)
    arcpy.SetParameterAsText(3,relationpath)
    arcpy.AddMessage("6_����LinkTBS�ں�")