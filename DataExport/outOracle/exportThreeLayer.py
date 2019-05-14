#!python
# -*- coding:utf-8 -*-

import arcpy,sys,os,datetime

def getName(xzqdm):
    """���������������ȡ��������"""

    if type(xzqdm) == unicode:

        xzqdm = xzqdm.encode('gbk')

    xianlist = [{'xzqdm':'440103','name':'������'},{'xzqdm':'440104','name':'Խ����'},{'xzqdm':'440105','name':'������'},{'xzqdm':'440106','name':'�����'},{'xzqdm':'440111','name':'������'},{'xzqdm':'440112','name':'������'},{'xzqdm':'440113','name':'��خ��'},{'xzqdm':'440114','name':'������'},{'xzqdm':'440115','name':'��ɳ��'},{'xzqdm':'440117','name':'�ӻ���'},{'xzqdm':'440118','name':'������'},{'xzqdm':'440203','name':'�佭��'},{'xzqdm':'440204','name':'䥽���'},{'xzqdm':'440205','name':'������'},{'xzqdm':'440222','name':'ʼ����'},{'xzqdm':'440224','name':'�ʻ���'},{'xzqdm':'440229','name':'��Դ��'},{'xzqdm':'440232','name':'��Դ����������'},{'xzqdm':'440233','name':'�·���'},{'xzqdm':'440281','name':'�ֲ���'},{'xzqdm':'440282','name':'������'},{'xzqdm':'440303','name':'�޺���'},{'xzqdm':'440304','name':'������'},{'xzqdm':'440305','name':'��ɽ��'},{'xzqdm':'440306','name':'������'},{'xzqdm':'440307','name':'������'},{'xzqdm':'440308','name':'������'},{'xzqdm':'440402','name':'������'},{'xzqdm':'440403','name':'������'},{'xzqdm':'440404','name':'������'},{'xzqdm':'440507','name':'������'},{'xzqdm':'440511','name':'��ƽ��'},{'xzqdm':'440512','name':'婽���'},{'xzqdm':'440513','name':'������'},{'xzqdm':'440514','name':'������'},{'xzqdm':'440515','name':'�κ���'},{'xzqdm':'440523','name':'�ϰ���'},{'xzqdm':'440604','name':'������'},{'xzqdm':'440605','name':'�Ϻ���'},{'xzqdm':'440606','name':'˳����'},{'xzqdm':'440607','name':'��ˮ��'},{'xzqdm':'440608','name':'������'},{'xzqdm':'440703','name':'���'},{'xzqdm':'440704','name':'������'},{'xzqdm':'440705','name':'�»���'},{'xzqdm':'440781','name':'̨ɽ��'},{'xzqdm':'440783','name':'��ƽ��'},{'xzqdm':'440784','name':'��ɽ��'},{'xzqdm':'440785','name':'��ƽ��'},{'xzqdm':'440802','name':'�࿲��'},{'xzqdm':'440803','name':'ϼɽ��'},{'xzqdm':'440804','name':'��ͷ��'},{'xzqdm':'440811','name':'������'},{'xzqdm':'440823','name':'��Ϫ��'},{'xzqdm':'440825','name':'������'},{'xzqdm':'440881','name':'������'},{'xzqdm':'440882','name':'������'},{'xzqdm':'440883','name':'�⴨��'},{'xzqdm':'440902','name':'ï����'},{'xzqdm':'440904','name':'�����'},{'xzqdm':'440981','name':'������'},{'xzqdm':'440982','name':'������'},{'xzqdm':'440983','name':'������'},{'xzqdm':'441202','name':'������'},{'xzqdm':'441203','name':'������'},{'xzqdm':'441223','name':'������'},{'xzqdm':'441224','name':'������'},{'xzqdm':'441225','name':'�⿪��'},{'xzqdm':'441226','name':'������'},{'xzqdm':'441283','name':'��Ҫ��'},{'xzqdm':'441284','name':'�Ļ���'},{'xzqdm':'441302','name':'�ݳ���'},{'xzqdm':'441303','name':'������'},{'xzqdm':'441322','name':'������'},{'xzqdm':'441323','name':'�ݶ���'},{'xzqdm':'441324','name':'������'},{'xzqdm':'441402','name':'÷����'},{'xzqdm':'441403','name':'÷����'},{'xzqdm':'441422','name':'������'},{'xzqdm':'441423','name':'��˳��'},{'xzqdm':'441424','name':'�廪��'},{'xzqdm':'441426','name':'ƽԶ��'},{'xzqdm':'441427','name':'������'},{'xzqdm':'441481','name':'������'},{'xzqdm':'441502','name':'����'},{'xzqdm':'441521','name':'������'},{'xzqdm':'441523','name':'½����'},{'xzqdm':'441581','name':'½����'},{'xzqdm':'441602','name':'Դ����'},{'xzqdm':'441621','name':'�Ͻ���'},{'xzqdm':'441622','name':'������'},{'xzqdm':'441623','name':'��ƽ��'},{'xzqdm':'441624','name':'��ƽ��'},{'xzqdm':'441625','name':'��Դ��'},{'xzqdm':'441702','name':'������'},{'xzqdm':'441704','name':'������'},{'xzqdm':'441721','name':'������'},{'xzqdm':'441781','name':'������'},{'xzqdm':'441802','name':'�����'},{'xzqdm':'441803','name':'������'},{'xzqdm':'441821','name':'�����'},{'xzqdm':'441823','name':'��ɽ��'},{'xzqdm':'441825','name':'��ɽ׳������������'},{'xzqdm':'441826','name':'��������������'},{'xzqdm':'441881','name':'Ӣ����'},{'xzqdm':'441882','name':'������'},{'xzqdm':'441900','name':'��ݸ��'},{'xzqdm':'442000','name':'��ɽ��'},{'xzqdm':'445102','name':'������'},{'xzqdm':'445103','name':'������'},{'xzqdm':'445122','name':'��ƽ��'},{'xzqdm':'445202','name':'�ų���'},{'xzqdm':'445203','name':'�Ҷ���'},{'xzqdm':'445222','name':'������'},{'xzqdm':'445224','name':'������'},{'xzqdm':'445281','name':'������'},{'xzqdm':'445302','name':'�Ƴ���'},{'xzqdm':'445303','name':'�ư���'},{'xzqdm':'445321','name':'������'},{'xzqdm':'445322','name':'������'},{'xzqdm':'445381','name':'�޶���'}]

    for xian in xianlist:

        if xian["xzqdm"] == xzqdm:

            return xian["name"]

    arcpy.AddMessage("������������������")

    sys.exit()

def createTempGBD(folder,name):
    """������ʱGDB"""

    name =  name + ".gdb"

    gdbpath = folder + "/" + name
    
    if os.path.exists(gdbpath):

        arcpy.Delete_management(gdbpath)

    arcpy.CreateFileGDB_management(folder, name)

    return gdbpath

def getCSK(csk,outputcsk,xzqdm):
    """���������������ȡ��ʼ��"""

    where_clause = " XZQDM = '%s'"%xzqdm

    arcpy.MakeFeatureLayer_management(csk,"c")

    arcpy.SelectLayerByAttribute_management("c",where_clause=where_clause)

    arcpy.CopyFeatures_management("c",outputcsk)
    
def getBYZTB(byztb,outputbyztb,xzqdm):
    """���������������ȡ��һ��ͼ��"""

    where_clause = " XZQDM = '%s'"%xzqdm

    arcpy.MakeFeatureLayer_management(byztb,"b")

    arcpy.SelectLayerByAttribute_management("b",where_clause=where_clause)

    arcpy.CopyFeatures_management("b",outputbyztb)
    
def getTP(env,outputbyztb,tp,outputtp):
    """��ȡ��Ƭ��"""
    
    arcpy.SetProgressor('step','��ȡ��Ƭ��',0,int(arcpy.GetCount_management(outputbyztb).getOutput(0)),1)

    SpatialReference = arcpy.Describe(tp).spatialReference

    arcpy.CreateFeatureclass_management(env,outputtp, "Point","","","",SpatialReference)

    for field in arcpy.ListFields(tp):
    
        aliasName = field.aliasName
        baseName = field.baseName
        length = field.length
        type = field.type
        
        if baseName.lower() in ["objectid","shape"]:
        
            continue
        
        arcpy.AddField_management(outputtp,baseName,type,field_length=length,field_alias=aliasName)

    fields = ['BSM','YSDM','FHDM','TSTYBM','CJR','CJRQ','BZ','MC','LJ','JD','WD','DWMS','WXSL','FWJ','QCJ','FYJ','RKXH','RKSJ','FJLX','SFSS','MD5','CHECK_CODE','SHAPE@']

    insertCur = arcpy.da.InsertCursor(outputtp,fields)

    starttime = datetime.datetime.now()

    limit = 200

    tstybms = []

    with arcpy.da.SearchCursor(outputbyztb,"TSTYBM") as cur:

        for r in cur:

            TSTYBM = r[0].encode('gbk')

            tstybms.append(TSTYBM)

            if len(tstybms) == limit:

                where_clause = " TSTYBM in (%s) "%("'"+"','".join(tstybms)+"'")

                tstybms = []

                with arcpy.da.SearchCursor(tp,fields,where_clause = where_clause) as tpcur:

                    for tprow in tpcur:
                        
                        insertCur.insertRow(tprow)
    
            arcpy.SetProgressorPosition()
            
    if len(tstybms) > 0:
    
        where_clause = " TSTYBM in (%s) "%("'"+"','".join(tstybms)+"'")
        
        with arcpy.da.SearchCursor(tp,fields,where_clause = where_clause) as tpcur:

            for tprow in tpcur:
                
                insertCur.insertRow(tprow)

    endtime = datetime.datetime.now()

    arcpy.AddMessage(endtime-starttime)
    
if __name__ == "__main__":
    
    xzqdm = arcpy.GetParameterAsText(0)
    folder = arcpy.GetParameterAsText(1)
    csk = arcpy.GetParameterAsText(2)
    byztb = arcpy.GetParameterAsText(3)
    tp = arcpy.GetParameterAsText(4)
    
    arcpy.env.overwriteOutput = True

    outputcsk = "csk"
    outputbyztb = "byztb"
    outputtp = "tp"

    arcpy.AddMessage("���������������ȡ��������")
    name = getName(xzqdm)

    arcpy.AddMessage("������ʱGDB")
    arcpy.env.workspace = createTempGBD(folder,xzqdm+name)

    arcpy.AddMessage("���������������ȡ��ʼ��")
    getCSK(csk,outputcsk,xzqdm)

    arcpy.AddMessage("���������������ȡ��һ��ͼ��")
    getBYZTB(byztb,outputbyztb,xzqdm)

    arcpy.AddMessage("��ȡ��Ƭ��")
    getTP(arcpy.env.workspace,outputbyztb,tp,outputtp)

    arcpy.SetParameterAsText(5,arcpy.env.workspace)