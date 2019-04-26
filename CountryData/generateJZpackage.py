# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy
import sqlite3,os
#import urllib2
import requests
from bs4 import BeautifulSoup
import  thread

class params():

    pic59=['4401','4402','4403','4404','4405','4406','4407']
    pic60=['4408','4409','4410','4411','4412']
    pic61=['4413','4414''4415','4416','4417']

    xzqlist = { '440103':'������','440104':'Խ����','440105':'������','440233':'�·���','440106':'�����','440111':'������',
                    '440112':'������','440113':'��خ��','440229':'��Դ��','440114':'������','440115':'��ɳ��','440117':'�ӻ���',
                    '440118':'������','440203':'�佭��','440204':'䥽���','440205':'������','440222':'ʼ����','440224':'�ʻ���',
                    '440232':'��Դ����������','440281':'�ֲ���','440282':'������','440303':'�޺���','440304':'������','440305':'��ɽ��',
                    '440306':'������','440307':'������','440308':'������','440402':'������','440403':'������','440404':'������',
                    '440703':'���','440704':'������','440705':'�»���','440781':'̨ɽ��','440783':'��ƽ��','440784':'��ɽ��','441203':'������',
                    '441284':'�Ļ���','441302':'�ݳ���','441322':'������','441323':'�ݶ���','441324':'������','441502':'��β����',
                    '441521':'������','441602':'Դ����','441621':'�Ͻ���','441622':'������','441624':'��ƽ��','441623':'��ƽ��',
                    '441625':'��Դ��','441803':'������','441821':'�����','441823':'��ɽ��','441881':'Ӣ����','441900':'��ݸ��',
                    '442000':'��ɽ��','440607':'��ˮ��','441303':'������','441802':'�����','440507':'������','440511':'��ƽ��',
                    '440512':'婽���','440513':'������','440514':'������','440515':'�κ���','440523':'�ϰ���','440604':'������','440605':'�Ϻ���',
                    '440606':'˳����','440608':'������','441402':'÷����','441403':'÷����','441422':'������','441423':'��˳��',
                    '441424':'�廪��','441426':'ƽԶ��','441427':'������','441481':'������','441523':'½����','441581':'½����','445102':'������',
                    '445103':'������','445122':'��ƽ��','445202':'�ų���','445203':'�Ҷ���','445222':'������','445224':'������','445281':'������',
                    '440785':'��ƽ��','440802':'�࿲��','440803':'ϼɽ��','440804':'��ͷ��','440811':'������', '440823':'��Ϫ��','440825':'������',
                    '440881':'������','440882':'������','440883':'�⴨��','440902':'ï����','440904':'�����','440981':'������','440982':'������',
                    '440983':'������','441202':'������', '441223':'������','441224':'������', '441225':'�⿪��','441226':'������','441283':'��Ҫ��',
                    '441702':'������','441704':'������','441721':'������','441781':'������','441825':'��ɽ׳������������','441826':'��������������',
                    '441882':'������','445302':'�Ƴ���','445303':'�ư���','445321':'������','445322':'������','445381':'�޶���'}

    sql_insertCCJZ='''
    INSERT INTO CCJZ(TBYBH,XZQDM,TBMJ,QSDWMC,QSXZ,YPDL,WYRDDL,SFJZ,BZ,JZRY,TBFW,PZD,XMC,XZB,YZB,SFXZ)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
    '''

    sql_insertFJ='''
    INSERT INTO FJ(TBYBH,XZQDM,TCBM,FJMC,FJLX,PSSJ,PSJD,PSRY,Longitude,Latitude,JYM,FJ,XZB,YZB)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);
    '''

def insertCCJZ(conn,parm1,parm2,parm3,parm4,parm5,parm6,parm7,parm8,parm9,parm10,parm11,parm12,parm13,parm14,parm15,parm16):

    conn.execute(params.sql_insertCCJZ,(parm1,parm2,parm3,parm4,parm5,parm6,parm7,parm8,parm9,parm10,parm11,parm12,parm13,parm14,parm15,parm16))

def insertFJ(conn,parm1,parm2,parm3,parm4,parm5,parm6,parm7,parm8,parm9,parm10,parm11,parm12,parm13,parm14):

    conn.execute(params.sql_insertFJ,(parm1,parm2,parm3,parm4,parm5,parm6,parm7,parm8,parm9,parm10,parm11,parm12,parm13,parm14))

def createDB(path):

    conn = sqlite3.connect(path)
    # ������
    sql_createFJ = '''
    CREATE TABLE 'FJ'('F_ID' INTEGER PRIMARY KEY AUTOINCREMENT,
    'TCBM' TEXT,
    'TBYBH' TEXT,
    'XZQDM' TEXT,
    'JKBSM' TEXT,
    'FJMC' TEXT,
    'FJLX' TEXT,
    'FJ' BLOB,
    'PSSJ' TEXT,
    'PSJD' INTEGER,
    'PSRY' TEXT,
    'Longitude' REAL,
    'Latitude' REAL,
    'XZB' REAL,
    'YZB' REAL,
    'metaRecord' TEXT,
    'JYM' TEXT
    )
    '''

    # �������
    sql_createZZBG = '''
    CREATE TABLE 'ZZBG'('TBYBH' TEXT NOT NULL PRIMARY KEY,
    'JKBSM' TEXT,
    'XZQDM' TEXT,
    'XMC' TEXT,
    'TBMJ' REAL,
    'XZB' REAL,
    'YZB' REAL,
    'NYBZ' TEXT,
    'PZD' TEXT,
    'BGDL' TEXT,
    'JZSM' TEXT,
    'BZ' TEXT,
    'JZRY' TEXT,
    'TBFW' TEXT
    )
    '''
    ##���ɼ��ͼ�߱�
    sql_createJCTB = '''
    CREATE TABLE 'JCTB'('JCBH' TEXT NOT NULL PRIMARY KEY,
    'TBLX' TEXT,
    'XZQDM' TEXT,
    'XMC' TEXT,
    'JCMJ' REAL,
    'QSX' TEXT,
    'HSX' TEXT,
    'XZB' REAL,
    'YZB' REAL,
    'TZ' TEXT,
    'PZD' TEXT,
    'BGDL' TEXT,
    'BGFW' TEXT,
    'WBGLX' TEXT,
    'BZ' TEXT,
    'JZRY' TEXT,
    'TBFW' TEXT
    )
    '''

    # ���߾�֤
    sql_createZXJZ = '''
    CREATE TABLE 'ZXJZ'('TBYBH' TEXT NOT NULL PRIMARY KEY,
    'JKBSM' TEXT,
    'XZQDM' TEXT,
    'XMC' TEXT,
    'TBMJ' REAL,
    'QSDWMC' TEXT,
    'QSXZ' TEXT,
    'XZB' REAL,
    'YZB' REAL,
    'DLBM' TEXT,
    'YPDL' TEXT,
    'NYBZ' TEXT,
    'PZD' TEXT,
    'DLYZX' TEXT,
    'WYRDDL' TEXT,
    'SFJZ' TEXT,
    'WJZLX' TEXT,
    'JZSM' TEXT,
    'BZ' TEXT,
    'JZRY' TEXT,
    'TBFW' TEXT
    )
    '''

    # ���ξ�֤
    sql_createCCJZ = '''
    CREATE TABLE 'CCJZ'('TBYBH' TEXT NOT NULL PRIMARY KEY,
    'JKBSM' TEXT,
    'XZQDM' TEXT,
    'XMC' TEXT,
    'TBMJ' REAL,
    'XZB' REAL,
    'YZB' REAL,
    'QSDWMC' TEXT,
    'QSXZ' TEXT,
    'DLBM' TEXT,
    'YPDL' TEXT,
    'NYBZ' TEXT,
    'PZD' TEXT,
    'DLYZX' TEXT,
    'WYRDDL' TEXT,
    'SFJZ' TEXT,
    'WJZLX' TEXT,
    'JZSM' TEXT,
    'BZ' TEXT,
    'JZRY' TEXT,
    'SFXZ' TEXT,
    'TBFW' TEXT
    )
    '''

    # �����֤
    sql_createBCJZ = '''
    CREATE TABLE 'BCJZ'('TBYBH' TEXT NOT NULL PRIMARY KEY,
    'JKBSM' TEXT,
    'XZQDM' TEXT,
    'XMC' TEXT,
    'TBMJ' REAL,
    'XZB' REAL,
    'YZB' REAL,
    'QSDWMC' TEXT,
    'QSXZ' TEXT,
    'DLBM' TEXT,
    'YPDL' TEXT,
    'NYBZ' TEXT,
    'PZD' TEXT,
    'DLYZX' TEXT,
    'WYRDDL' TEXT,
    'SFJZ' TEXT,
    'WJZLX' TEXT,
    'JZSM' TEXT,
    'BZ' TEXT,
    'JZRY' TEXT,
    'TBFW' TEXT
    )
    '''

    # ��������
    sql_createDLYB = '''
    CREATE TABLE 'DLYB'('TBYBH' TEXT NOT NULL PRIMARY KEY,
    'JKBSM' TEXT,
    'XZQDM' TEXT,
    'XMC' TEXT,
    'TBMJ' REAL,
    'XZB' REAL,
    'YZB' REAL,
    'YBDL' TEXT,
    'NYBZ' TEXT,
    'PZD' TEXT,
    'YBMS' TEXT,
    'JZRY' TEXT,
    'SFXZ' TEXT,
    'TBFW' TEXT,
    'DCBZ' TEXT
    )
    '''

    conn.execute(sql_createFJ)
    conn.execute(sql_createZZBG)
    conn.execute(sql_createJCTB)
    conn.execute(sql_createZXJZ)
    conn.execute(sql_createCCJZ)
    conn.execute(sql_createBCJZ)
    conn.execute(sql_createDLYB)
    print '�����ɹ�'
    conn.commit()
    #conn.close()
    return conn

def createConn(folder,XZQName,xzqdm):   #ͨ���������������ɲ�ͬ�����ݿ�
    """�������ݿ�"""

    dir = folder + XZQName

    if(os.path.exists(dir) == False):

        os.makedirs(dir)

    db_path = dir + '/' + xzqdm + XZQName + '.db'

    if(os.path.exists(db_path) == False):

        with open(db_path, 'w') as f:
            
            f.close()

        conn = createDB(db_path)

        conn.text_factory = str

        arcpy.AddMessage("����" + db_path + "�ɹ�!")
    else:

        conn = sqlite3.connect(db_path)

        conn.text_factory = str

    return conn

def getZl(byztb):
    """��ȡ�������������뼰����"""
    
    cursor = arcpy.da.SearchCursor(byztb,["XZQDM","ZLDWDM"])

    row = cursor.next()

    xzqdm = row[0]
    zldwdm = row[1]

    name = params.xzqlist[xzqdm]

    return name,xzqdm,zldwdm

def insertdatas(byztb,conn):
    """����CCJZ��"""

    searchFields = ['DLBM', 'DLMC', 'QSXZ', 'QSDWDM', 'QSDWMC', 'TBMJ', 'BZ', 'SFJZ', 'XZQDM', 'TSTYBM', 'ZHXGR', 'SJDLBM', 'SHAPE@', 'ZLDWDM','SHAPE@XY']

    cursor = arcpy.da.SearchCursor(byztb,searchFields)

    number = 0

    for row in cursor:

        test()

        data = dict(zip(searchFields,row))

        conn.execute(params.sql_insertCCJZ,(parm1,parm2,parm3,parm4,parm5,parm6,parm7,parm8,parm9,parm10,parm11,parm12,parm13,parm14,parm15,parm16))

        (data['TSTYBM'], data["XZQDM"], data["TBMJ"], data["QSDWMC"], data["QSXZ"], data["SJDLBM"], data["DLBM"], data["SFJZ"], data["BZ"], data["ZHXGR"], data["SHAPE@"],str(test),xzqmc,coordX,coordY,SFXZ)

def main(folder,byztb,tp):

    arcpy.AddMessage("��ȡ�����������������������")
    name,xzqdm,zldwdm = getZl(byztb)

    arcpy.AddMessage("�������ݻ���")
    conn = createConn(folder,name,xzqdm)

    arcpy.AddMessage("")
    insertCCJZ(byztb,conn)

    cursor = arcpy.da.SearchCursor(byztb,
                                   ['DLBM', 'DLMC', 'QSXZ', 'QSDWDM', 'QSDWMC', 'TBMJ', 'BZ', 'SFJZ', 'XZQDM', 'TSTYBM',
                                    'ZHXGR',
                                    'SJDLBM', 'SHAPE@', 'ZLDWDM','SHAPE@XY'])

    cursorPic = arcpy.da.SearchCursor(tp, ['SHAPE@XY', 'FJLX', 'TSTYBM', 'FWJ', 'CJR', 'CJRQ', 'MC', 'JD', 'WD',
                                                  'CHECK_CODE'])
    listpic = []
    for picrow in cursorPic:
        dicpic = {}
        dicpic["X"], dicpic["Y"] = picrow[0]
        dicpic["FJLX"] = picrow[1]
        dicpic["TSTYBM"] = picrow[2]
        dicpic["FWJ"] = picrow[3]
        dicpic["CJR"] = picrow[4]
        dicpic["CJRQ"] = picrow[5]
        dicpic["MC"] = picrow[6]
        dicpic["JD"] = picrow[7]
        dicpic["WD"] = picrow[8]
        dicpic["CHECK_CODE"] = picrow[9]
        listpic.append(dicpic)
    del picrow
    del cursorPic

    num =0 #��������������һǧ�����ֹͣ
    for row in cursor:
        TBFW = row[12].WKT
        test = []
        #if (num >3):
            #return
        if (row[8] != '' and row[8] != None):
            connnew = createConn(row[8])
        else:
            print '����ʧ��'
            return
        for i in listpic:
            dictest = {}
            if (i['TSTYBM'] == row[9]):
                dictest['type'] = i["FJLX"]
                dictest['x'] = i["X"]
                dictest['y'] = i["Y"]
                dictest['radius'] = i["FWJ"]
                test.append(dictest)
                if (row[8][0:4] in params.pic59):
                    #print '59'
                    urlhost = "http://192.168.110.59/thumbnail/"
                    urlcache = "http://192.168.110.59"
                elif (row[8][0:4] in params.pic60):
                    #print '60'
                    urlhost = "http://192.168.101.60/thumbnail/"
                    urlcache = "http://192.168.101.60"
                elif (row[8][0:4] in params.pic61):
                    #print '61'
                    urlhost = "http://192.168.101.61/thumbnail/"
                    urlcache = "http://192.168.101.61"
                else:
                    #print '62'
                    urlhost = "http://192.168.101.62/thumbnail/"
                    urlcache = "http://192.168.101.62"

                url = str(urlhost) + str(row[13]) + '/' + str(row[9]) + '/' + str(i["MC"]) + "?real=True"
                #print url
                #try:

                redictcontent = requests.get(url).content

                insertFJ(connnew, i["TSTYBM"], row[8], 'CCJZ', i["MC"], i["FJLX"], i["CJRQ"], i["FWJ"], i["CJR"],
                             i["JD"], i["WD"], i["CHECK_CODE"], redictcontent,i["X"],i["Y"])
                #except:
                    #print 'fail'
        xzqmc = params.xzqlist[row[8]]
        coordX,coordY = row[14]
        SFXZ = '0'   #�Ƿ�����
        insertCCJZ(connnew, row[9], row[8], row[5], row[4], row[2], row[11], row[0], row[7], row[6], row[10], TBFW,str(test),xzqmc,coordX,coordY,SFXZ)
        connnew.commit()
        #num +=1
    del row
    del cursor
    #connnew.commit()
    connnew.close()

if __name__=='__main__':

    arcpy.AddMessage("�ύ����DB��������")

    folder = arcpy.GetParameterAsText(0)
    byztb = arcpy.GetParameterAsText(1)
    tp = arcpy.GetParameterAsText(2)

    main(folder,byztb.tp)

    arcpy.AddMessage("���")

