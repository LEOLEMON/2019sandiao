#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,json

def dissolve1(xzkpath,dissolvepath,outputxzkpath):
    """�ں���ͬ���ԣ�bsmһ�µ�ͼ��,��ֻ֤�����Ա仯��ͼ�����ܱ�ͼ�߲���ͬһ���������"""

    arcpy.CheckGeometry_management(xzkpath,"dissolvepath_7_CheckGeometry")

    searchFields = ['cskbsm','dlbm','zldwdm','gdlx','tbxhdm','gdzzsxdm']

    arcpy.AddMessage("�ں��ֶΣ�"+';'.join(searchFields))

    arcpy.Dissolve_management(xzkpath,dissolvepath,"ZLDWDM;DLBM;GDLX;TBXHDM;GDZZSXDM;cskbsm","#","SINGLE_PART","UNSPLIT_LINES")

    arcpyDeal.deleteFields(dissolvepath,searchFields)

    arcpy.SpatialJoin_analysis(dissolvepath,xzkpath,outputxzkpath,join_operation= "JOIN_ONE_TO_ONE",join_type="KEEP_ALL",match_option="CONTAINS",field_mapping="""
        DLBM "DLBM" true true false 5 Text 0 0 ,First,#,%s,DLBM,-1,-1;
        ZLDWDM "ZLDWDM" true true false 19 Text 0 0 ,First,#,%s,ZLDWDM,-1,-1;
        GDLX "GDLX" true true false 2 Text 0 0 ,First,#,%s,GDLX,-1,-1;
        TBXHDM "TBXHDM" true true false 4 Text 0 0 ,First,#,%s,TBXHDM,-1,-1;
        GDZZSXDM "GDZZSXDM" true true false 8 Text 0 0 ,First,#,%s,GDZZSXDM,-1,-1;
        LINKTBS "LINKTBS" true true false 254 Text 0 0 ,First,#,%s,LINKTBS,-1,-1;
        TBXHMC "TBXHMC" true true false 20 Text 0 0 ,First,#,%s,TBXHMC,-1,-1;
        GDZZSXMC "GDZZSXMC" true true false 20 Text 0 0 ,First,#,%s,GDZZSXMC,-1,-1;
        CZCSXM "CZCSXM" true true false 4 Text 0 0 ,First,#,%s,CZCSXM,-1,-1;
        TSTYBM "TSTYBM" true true false 100 Text 0 0 ,First,#,%s,TSTYBM,-1,-1;
        SJDLBM "SJDLBM" true true false 100 Text 0 0 ,First,#,%s,SJDLBM,-1,-1;
        OLDTAG "OLDTAG" true true false 20 Text 0 0 ,First,#,%s,OLDTAG,-1,-1;
        JZSJ "JZSJ" true true false 8 Date 0 0 ,First,#,%s,JZSJ,-1,-1;
        BSM "BSM" true true false 18 Text 0 0 ,First,#,%s,BSM,-1,-1;
        ZZJZTB "ZZJZTB" true true false 1 Text 0 0 ,First,#,%s,ZZJZTB,-1,-1;
        WJZLX "WJZLX" true true false 8 Text 0 0 ,First,#,%s,WJZLX,-1,-1;
        cskmianji "cskmianji" true true false 8 Double 0 0 ,First,#,%s,cskmianji,-1,-1;
        cskbsm "cskbsm" true true false 255 Text 0 0 ,First,#,%s,cskbsm,-1,-1;
        cskzldwdm "cskzldwdm" true true false 255 Text 0 0 ,First,#,%s,cskzldwdm,-1,-1;
        cskdlbm "cskdlbm" true true false 255 Text 0 0 ,First,#,%s,cskdlbm,-1,-1;
        cskczcsxm "cskczcsxm" true true false 255 Text 0 0 ,First,#,%s,cskczcsxm,-1,-1;
        tstybmlist "tstybmlist" true true false 2000 Text 0 0 ,Join,",",%s,TSTYBM,-1,-1;"""%(xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath,xzkpath))

def getRelation(outputxzkpath,enviroment,relationpath):
    """�����¾�ͼ��ͳһ�����ϵ"""
    
    relationList = []

    count = int(arcpy.GetCount_management(outputxzkpath).getOutput(0))

    arcpy.SetProgressor('step','7_��ȡ��Ƭ���ں�',0,count,1)

    with arcpy.da.SearchCursor(outputxzkpath,["TSTYBM","tstybmlist"]) as cur:

        for row in cur:

            if len(row[1]) > 36:

                tstybmlist = row[1].split(",")

                for oldtstybm in tstybmlist:

                    relationList.append([oldtstybm,row[0]])

            arcpy.SetProgressorPosition()

    arcpy.CreateTable_management(enviroment,relationpath)

    newFields = ["oldfield","newfields"]

    arcpyDeal.ensureFields(relationpath,newFields)

    insertcur = arcpy.da.InsertCursor(relationpath,newFields)

    for relation in relationList:

        insertcur.insertRow(relation)

        arcpy.SetProgressorPosition()

if __name__ == "__main__":
    """�ں���ͬ��ʼ��BSM������һ�µ�ͼ��,���û�з������α仯��ͼ��"""
    
    arcpy.AddMessage("7_��ʼ�ں�")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    relationpath = "relationpath_7"
    dissolvepath = "dissolvepath_7"
    outputxzkpath = "outputxzkpath_7"

    arcpy.AddMessage("7_�޸�����")
    arcpy.RepairGeometry_management (xzkpath, "KEEP_NULL")

    arcpy.AddMessage("7_�ں���ͬ��ʼ��BSM������һ�µ�ͼ��")
    dissolve1(xzkpath,dissolvepath,outputxzkpath)

    arcpy.AddMessage("7_��ȡ�ں���Ƭ��")
    getRelation(outputxzkpath,enviroment,relationpath)
        
    arcpy.SetParameterAsText(2,outputxzkpath)
    arcpy.SetParameterAsText(3,relationpath)
    arcpy.AddMessage("7_�����ں�")