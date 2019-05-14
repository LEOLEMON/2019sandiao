#!python
# -*- coding:utf-8 -*-

import arcpy,sys,os,datetime

def getName(xzqdm):
    """根据行政区代码获取行政区名"""

    if type(xzqdm) == unicode:

        xzqdm = xzqdm.encode('gbk')

    xianlist = [{'xzqdm':'440103','name':'荔湾区'},{'xzqdm':'440104','name':'越秀区'},{'xzqdm':'440105','name':'海珠区'},{'xzqdm':'440106','name':'天河区'},{'xzqdm':'440111','name':'白云区'},{'xzqdm':'440112','name':'黄埔区'},{'xzqdm':'440113','name':'番禺区'},{'xzqdm':'440114','name':'花都区'},{'xzqdm':'440115','name':'南沙区'},{'xzqdm':'440117','name':'从化区'},{'xzqdm':'440118','name':'增城区'},{'xzqdm':'440203','name':'武江区'},{'xzqdm':'440204','name':'浈江区'},{'xzqdm':'440205','name':'曲江区'},{'xzqdm':'440222','name':'始兴县'},{'xzqdm':'440224','name':'仁化县'},{'xzqdm':'440229','name':'翁源县'},{'xzqdm':'440232','name':'乳源瑶族自治县'},{'xzqdm':'440233','name':'新丰县'},{'xzqdm':'440281','name':'乐昌市'},{'xzqdm':'440282','name':'南雄市'},{'xzqdm':'440303','name':'罗湖区'},{'xzqdm':'440304','name':'福田区'},{'xzqdm':'440305','name':'南山区'},{'xzqdm':'440306','name':'宝安区'},{'xzqdm':'440307','name':'龙岗区'},{'xzqdm':'440308','name':'盐田区'},{'xzqdm':'440402','name':'香洲区'},{'xzqdm':'440403','name':'斗门区'},{'xzqdm':'440404','name':'金湾区'},{'xzqdm':'440507','name':'龙湖区'},{'xzqdm':'440511','name':'金平区'},{'xzqdm':'440512','name':'濠江区'},{'xzqdm':'440513','name':'潮阳区'},{'xzqdm':'440514','name':'潮南区'},{'xzqdm':'440515','name':'澄海区'},{'xzqdm':'440523','name':'南澳县'},{'xzqdm':'440604','name':'禅城区'},{'xzqdm':'440605','name':'南海区'},{'xzqdm':'440606','name':'顺德区'},{'xzqdm':'440607','name':'三水区'},{'xzqdm':'440608','name':'高明区'},{'xzqdm':'440703','name':'蓬江区'},{'xzqdm':'440704','name':'江海区'},{'xzqdm':'440705','name':'新会区'},{'xzqdm':'440781','name':'台山市'},{'xzqdm':'440783','name':'开平市'},{'xzqdm':'440784','name':'鹤山市'},{'xzqdm':'440785','name':'恩平市'},{'xzqdm':'440802','name':'赤坎区'},{'xzqdm':'440803','name':'霞山区'},{'xzqdm':'440804','name':'坡头区'},{'xzqdm':'440811','name':'麻章区'},{'xzqdm':'440823','name':'遂溪县'},{'xzqdm':'440825','name':'徐闻县'},{'xzqdm':'440881','name':'廉江市'},{'xzqdm':'440882','name':'雷州市'},{'xzqdm':'440883','name':'吴川市'},{'xzqdm':'440902','name':'茂南区'},{'xzqdm':'440904','name':'电白区'},{'xzqdm':'440981','name':'高州市'},{'xzqdm':'440982','name':'化州市'},{'xzqdm':'440983','name':'信宜市'},{'xzqdm':'441202','name':'端州区'},{'xzqdm':'441203','name':'鼎湖区'},{'xzqdm':'441223','name':'广宁县'},{'xzqdm':'441224','name':'怀集县'},{'xzqdm':'441225','name':'封开县'},{'xzqdm':'441226','name':'德庆县'},{'xzqdm':'441283','name':'高要市'},{'xzqdm':'441284','name':'四会市'},{'xzqdm':'441302','name':'惠城区'},{'xzqdm':'441303','name':'惠阳区'},{'xzqdm':'441322','name':'博罗县'},{'xzqdm':'441323','name':'惠东县'},{'xzqdm':'441324','name':'龙门县'},{'xzqdm':'441402','name':'梅江区'},{'xzqdm':'441403','name':'梅县区'},{'xzqdm':'441422','name':'大埔县'},{'xzqdm':'441423','name':'丰顺县'},{'xzqdm':'441424','name':'五华县'},{'xzqdm':'441426','name':'平远县'},{'xzqdm':'441427','name':'蕉岭县'},{'xzqdm':'441481','name':'兴宁市'},{'xzqdm':'441502','name':'城区'},{'xzqdm':'441521','name':'海丰县'},{'xzqdm':'441523','name':'陆河县'},{'xzqdm':'441581','name':'陆丰市'},{'xzqdm':'441602','name':'源城区'},{'xzqdm':'441621','name':'紫金县'},{'xzqdm':'441622','name':'龙川县'},{'xzqdm':'441623','name':'连平县'},{'xzqdm':'441624','name':'和平县'},{'xzqdm':'441625','name':'东源县'},{'xzqdm':'441702','name':'江城区'},{'xzqdm':'441704','name':'阳东区'},{'xzqdm':'441721','name':'阳西县'},{'xzqdm':'441781','name':'阳春市'},{'xzqdm':'441802','name':'清城区'},{'xzqdm':'441803','name':'清新区'},{'xzqdm':'441821','name':'佛冈县'},{'xzqdm':'441823','name':'阳山县'},{'xzqdm':'441825','name':'连山壮族瑶族自治县'},{'xzqdm':'441826','name':'连南瑶族自治县'},{'xzqdm':'441881','name':'英德市'},{'xzqdm':'441882','name':'连州市'},{'xzqdm':'441900','name':'东莞市'},{'xzqdm':'442000','name':'中山市'},{'xzqdm':'445102','name':'湘桥区'},{'xzqdm':'445103','name':'潮安区'},{'xzqdm':'445122','name':'饶平县'},{'xzqdm':'445202','name':'榕城区'},{'xzqdm':'445203','name':'揭东区'},{'xzqdm':'445222','name':'揭西县'},{'xzqdm':'445224','name':'惠来县'},{'xzqdm':'445281','name':'普宁市'},{'xzqdm':'445302','name':'云城区'},{'xzqdm':'445303','name':'云安区'},{'xzqdm':'445321','name':'新兴县'},{'xzqdm':'445322','name':'郁南县'},{'xzqdm':'445381','name':'罗定市'}]

    for xian in xianlist:

        if xian["xzqdm"] == xzqdm:

            return xian["name"]

    arcpy.AddMessage("不存在行政区划代码")

    sys.exit()

def createTempGBD(folder,name):
    """创建临时GDB"""

    name =  name + ".gdb"

    gdbpath = folder + "/" + name
    
    if os.path.exists(gdbpath):

        arcpy.Delete_management(gdbpath)

    arcpy.CreateFileGDB_management(folder, name)

    return gdbpath

def getCSK(csk,outputcsk,xzqdm):
    """根据行政区代码获取初始库"""

    where_clause = " XZQDM = '%s'"%xzqdm

    arcpy.MakeFeatureLayer_management(csk,"c")

    arcpy.SelectLayerByAttribute_management("c",where_clause=where_clause)

    arcpy.CopyFeatures_management("c",outputcsk)
    
def getBYZTB(byztb,outputbyztb,xzqdm):
    """根据行政区代码获取不一致图斑"""

    where_clause = " XZQDM = '%s'"%xzqdm

    arcpy.MakeFeatureLayer_management(byztb,"b")

    arcpy.SelectLayerByAttribute_management("b",where_clause=where_clause)

    arcpy.CopyFeatures_management("b",outputbyztb)
    
def getTP(env,outputbyztb,tp,outputtp):
    """获取照片点"""
    
    arcpy.SetProgressor('step','获取照片点',0,int(arcpy.GetCount_management(outputbyztb).getOutput(0)),1)

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

    arcpy.AddMessage("根据行政区代码获取行政区名")
    name = getName(xzqdm)

    arcpy.AddMessage("创建临时GDB")
    arcpy.env.workspace = createTempGBD(folder,xzqdm+name)

    arcpy.AddMessage("根据行政区代码获取初始库")
    getCSK(csk,outputcsk,xzqdm)

    arcpy.AddMessage("根据行政区代码获取不一致图斑")
    getBYZTB(byztb,outputbyztb,xzqdm)

    arcpy.AddMessage("获取照片点")
    getTP(arcpy.env.workspace,outputbyztb,tp,outputtp)

    arcpy.SetParameterAsText(5,arcpy.env.workspace)