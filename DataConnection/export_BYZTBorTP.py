#!python
# -*- coding:utf-8 -*-

import arcpy


#获取输入-要素图层路径
def getfcIn(args1,args2):

    xzqdm = args1
    database = args2

    byztbfc = ''
    tpfc = ''

    if xzqdm in ['441202','441203','441223','441224','441225','441226','441702','441704','441721','441781','441825','441826','441882','445302','445303','445321','445322','445381','440902','440904','440981','440982','440983','440802','440803','440804','440811','440823','440825','440881','440882','440883','440785']:

        byztb_fcIn = database+'\GDSDWYXTKJK37.KJK_37\GDSDWYXTKJK37.SDJZ_BYZTB'
        
        tp_fcIn = database+'\GDSDWYXTKJK37.KJK_37\GDSDWYXTKJK37.SDJZ_TP'

    elif xzqdm in ['441283','441284','441302','441303','441322','441323','441324','441502','441521','441602','441621','441622','441623','441624','441625','441802','441803','441821','441823','442000','440703','440704','440705','440781','440783','440784','440604','440605','440606','440607','440608','440402','440403','440404','440303','440304','440305','440306','440307','440308','440203','440204','440205','440222','440224','440229','440232','440233','440281','440282','440103','440104','440105','440106','440111','440112','440113','440114','440115','440117','440118','441881']:

        byztb_fcIn = database+'\GDSDWYXTKJK38.KJK_38\GDSDWYXTKJK38.SDJZ_BYZTB'

        tp_fcIn = database+'\GDSDWYXTKJK38.KJK_38\GDSDWYXTKJK38.SDJZ_TP'

    elif xzqdm in ['441402','441403','441422','441423','441424','441426','441427','441481','441523','441581','440507','440511','440512','440513','440514','440515','440523','445103','445122','445202','445203','445222','445224','445281','441900','445102']:

        byztb_fcIn = database+'\GDSDWYXTKJK39.KJK_39\GDSDWYXTKJK39.SDJZ_BYZTB'

        tp_fcIn = database+'\GDSDWYXTKJK39.KJK_39\GDSDWYXTKJK39.SDJZ_TP'

    return byztb_fcIn,tp_fcIn

#获取输出-要素图层路径（避免和已存在图层重命名）
def getfcOut(args1,args2):

    xzqdm = args1
    outfc = args2

    arcpy.env.workspace = outfc

    fclist = arcpy.ListFeatureClasses()

    bdtbname = 'bdtb_'+xzqdm
    tpname = 'tp_'+xzqdm

    while bdtbname in fclist:

        bdtbname += '_1'

    while tpname in fclist:

        tpname += '_1'
        
    byztb_fcOut = outfc + '//' + bdtbname
    tp_fcOut = outfc + '//' + tpname
        
    return byztb_fcOut, tp_fcOut

#获取空白照片点图层
def getfcIn_blanktp(args1,args2):

    tp_fcIn = args1
    tp_fcOut = args2

    arcpy.env.workspace = 'C:/Users/JDZ/Documents/ArcGIS/Default.gdb'

    if '37' in tp_fcIn:

        arcpy.CopyFeatures_management ('blank_37', tp_fcOut)

    elif '38' in tp_fcIn:

        arcpy.CopyFeatures_management ('blank_38', tp_fcOut)

    elif '39' in tp_fcIn:

        arcpy.CopyFeatures_management ('blank_39', tp_fcOut)

    arcpy.ClearWorkspaceCache_management()
    
    return tp_fcOut

#导出图斑层
def exportBDTB(args1,args2,args3):

    xzqdm = args1
    byztb_fcIn = args2
    byztb_fcOut = args3

    byztb_Tempfc = 'byztb_tempfc'

    arcpy.MakeFeatureLayer_management (byztb_fcIn, byztb_Tempfc)

    arcpy.SelectLayerByAttribute_management (byztb_Tempfc, 'NEW_SELECTION', 'XZQDM LIKE \'{0}%\''.format(xzqdm))

    result = arcpy.GetCount_management(byztb_Tempfc)

    count = int(result.getOutput(0))

    arcpy.AddMessage('正在导出{0}个图斑'.format(count))

    arcpy.CopyFeatures_management(byztb_Tempfc, byztb_fcOut)
    
    return count, byztb_Tempfc

#导出照片层
def exportTP(args1,args2,args3):

    tp_fcIn = args1
    blanktp_fcIn = args2
    byztb_Tempfc = args3
    
    SearchCursor = arcpy.da.SearchCursor
    InsertCursor = arcpy.da.InsertCursor
    SetProgressorPosition = arcpy.SetProgressorPosition
    
    count = 0

    fields = ['BSM','YSDM','FHDM','TSTYBM','CJR','CJRQ','BZ','MC','LJ','JD','WD','DWMS','WXSL','FWJ','QCJ','FYJ','RKXH','RKSJ','FJLX','SFSS','MD5','CHECK_CODE','SHAPE']

    xfealist = SearchCursor(byztb_Tempfc,'TSTYBM')

    yfealist = InsertCursor(blanktp_fcIn,fields)
    
    insertRow = yfealist.insertRow

    for x in xfealist:

        zfealist = SearchCursor(tp_fcIn,fields,'TSTYBM=\'{0}\''.format(x[0]))

        for z in zfealist:

            insertRow(z)

        count += 1

        if count == 100:

            count = 0
            SetProgressorPosition()

    SetProgressorPosition()

if __name__ == '__main__':

    xzqdm = arcpy.GetParameterAsText(0)
    datatype = arcpy.GetParameterAsText(1)
    database = arcpy.GetParameterAsText(2)
    outfc = arcpy.GetParameterAsText(3)

    arcpy.AddMessage('开始')

    byztb_fcIn,tp_fcIn = getfcIn(xzqdm,database)

    byztb_fcOut,tp_fcOut = getfcOut(xzqdm,outfc)

    count,byztb_Tempfc = exportBDTB(xzqdm,byztb_fcIn,byztb_fcOut)

    if u'照片点' in datatype:

        arcpy.SetProgressor('step','更新进度',0,count,100)

        arcpy.AddMessage('正在提取{0}个图斑的照片点'.format(count))

        blanktp_fcIn = getfcIn_blanktp(tp_fcIn,tp_fcOut)

        exportTP(tp_fcIn,blanktp_fcIn,byztb_Tempfc)

    arcpy.AddMessage('完成')