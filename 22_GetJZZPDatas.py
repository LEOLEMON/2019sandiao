#-*- coding:utf-8 -*-
import arcpy,arcpyDeal,os,json

def getname(name,number):

    names = []

    if name in names:

        return getname(name,number+1)

    else:
        newname = name+"000"[0:3-len(str(number))] + str(number)
        names.append(newname)
        return newname

def join(dccgtb,sourcePath):
    """��������ɹ�ͼ�ߺ���Ƭ��ͼ��,�õ���������"""

    baseName1 = arcpy.Describe(sourcePath).baseName
    baseName2 = arcpy.Describe(dccgtb).baseName

    arcpy.AddMessage("22_������ʱͼ��")

    arcpy.MakeFeatureLayer_management ( sourcePath, baseName1)
    arcpy.MakeFeatureLayer_management ( dccgtb, baseName2)

    arcpy.AddMessage("22_ͼ�����")

    arcpy.AddJoin_management(baseName1,"TSTYBM",baseName2,"WYM")

    where_clause = " %s.WYM is not null and %s.WJZLX = ''"%(baseName2,baseName2)

    datas = []
    tempFields =['CJRQ','CJR','FWJ','QCJ','FYJ','FJLX','MC']
    searchFields =[baseName1+"."+f for f in tempFields]

    tempFields1 = ['SHAPE@X','SHAPE@Y','SHAPE@']
    searchFields1 = ['SHAPE@X','SHAPE@Y','SHAPE@']

    tempFields2 =['TBYBH','WYM']
    searchFields2 =[baseName2+"."+f for f in tempFields2]

    tempFields.extend(tempFields1)
    tempFields.extend(tempFields2)
    searchFields.extend(searchFields1)
    searchFields.extend(searchFields2)

    arcpy.AddMessage("22_��Ƭ�����ݻ�ȡ")

    arcpyDeal.createTempDatas(searchFields,tempFields,baseName1,datas,where_clause=where_clause)

    return datas

def updateDatas(jzzp,photopath,datas):
    """�������ݵ���֤��Ƭ��"""

    insertrows = arcpy.da.InsertCursor(jzzp,['TBYBH','WYM','NAME','PSSJ','PSR','AZIM','ROLL','TILT','PICX','PICY','FJLX','FJFW','SHAPE@'])

    for data in datas:

        WYM = data['WYM']
        TBYBH = data['TBYBH']
        PSSJ = data['CJRQ']
        PSR = data['CJR']
        AZIM = data['FWJ']
        TILT = data['QCJ']
        ROLL = data['FYJ']
        FJLX = data['FJLX']
        PICX = data['SHAPE@X']
        PICY = data['SHAPE@Y']
        shp = data['SHAPE@']
        mc = data['MC']
        FJFW = ''
        
        NAME = getname(TBYBH+"_"+FJLX+"_",1)

        # urllib.urlretrieve(photoUrl+"/"+ZLDWDM+"/"+WYM+""+mc,photopath+"/"+TBYBH+"/"+NAME+".jpg")

        # file = open(photopath+"/"+TBYBH+"/"+NAME+".jpg","w")
        # file.seek(5000)
        # file.close()

        insertrows.insertRow([TBYBH,WYM,NAME,PSSJ,PSR,AZIM,ROLL,TILT,PICX,PICY,FJLX,FJFW,shp])

        arcpy.SetProgressorPosition()

def collectWJZLX(dccgtb):

    datas = []
    searchFields =['TBYBH','WJZLX','SHAPE@X','SHAPE@Y']
    tempFields =['TBYBH','WJZLX','SHAPE@X','SHAPE@Y']

    where_clause = " WJZLX <> ''"

    arcpyDeal.createTempDatas(searchFields,tempFields,dccgtb,datas,where_clause=where_clause)

    return datas

def insertWJZLX(photopath,datas):

    insertrows = arcpy.da.InsertCursor(jzzp,['TBYBH','WJZLX','SHAPE@'])

    for data in datas:

        TBYBH = data['TBYBH']
        WJZLX = data['WJZLX']

        point = arcpy.Point(data['SHAPE@X'],data['SHAPE@Y'])

        insertrows.insertRow([TBYBH,WJZLX,point])
        
        arcpy.SetProgressorPosition()

def start(dccgtb,jzzp,sourcePath,photopath):

    arcpy.AddMessage("22_��ȡ����")
    datas = join(dccgtb,sourcePath)
    arcpy.AddMessage(len(datas))

    arcpy.AddMessage("22_��������")
    result = arcpy.GetCount_management(dccgtb)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','22_������Ƭ��',0,count,1)

    arcpyDeal.createIndex(sourcePath,["TSTYBM"])

    updateDatas(jzzp,photopath,datas)

    arcpy.AddMessage("22_�ռ�δ��֤����")
    datas = collectWJZLX(dccgtb)

    arcpy.AddMessage("22_����δ��֤��������")
    count = len(datas)
    arcpy.SetProgressor('step','22_����δ��֤��������',0,count,1)

    insertWJZLX(photopath,datas)

if __name__ == "__main__":
    
    arcpy.AddMessage("22_��ȡ��֤��Ƭ")
    
    dccgtb = arcpy.GetParameterAsText(0)
    jzzp = arcpy.GetParameterAsText(1)
    sourcePath = arcpy.GetParameterAsText(2)
    photopath = arcpy.GetParameterAsText(3)

    start(dccgtb,jzzp,sourcePath,photopath)

    arcpy.SetParameterAsText(4,jzzp)

    arcpy.AddMessage("22_����")