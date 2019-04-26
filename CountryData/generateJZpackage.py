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

    xzqlist = { '440103':'荔湾区','440104':'越秀区','440105':'海珠区','440233':'新丰县','440106':'天河区','440111':'白云区',
                    '440112':'黄埔区','440113':'番禺区','440229':'翁源县','440114':'花都区','440115':'南沙区','440117':'从化区',
                    '440118':'增城区','440203':'武江区','440204':'浈江区','440205':'曲江区','440222':'始兴县','440224':'仁化县',
                    '440232':'乳源瑶族自治县','440281':'乐昌市','440282':'南雄市','440303':'罗湖区','440304':'福田区','440305':'南山区',
                    '440306':'宝安区','440307':'龙岗区','440308':'盐田区','440402':'香洲区','440403':'斗门区','440404':'金湾区',
                    '440703':'蓬江区','440704':'江海区','440705':'新会区','440781':'台山市','440783':'开平区','440784':'鹤山市','441203':'鼎湖区',
                    '441284':'四会市','441302':'惠城区','441322':'博罗县','441323':'惠东县','441324':'龙门县','441502':'汕尾城区',
                    '441521':'海丰县','441602':'源城区','441621':'紫金县','441622':'龙川县','441624':'和平县','441623':'连平县',
                    '441625':'东源县','441803':'清新县','441821':'佛冈县','441823':'阳山县','441881':'英德市','441900':'东莞市',
                    '442000':'中山市','440607':'三水区','441303':'惠阳区','441802':'清城区','440507':'龙湖区','440511':'金平区',
                    '440512':'濠江区','440513':'潮阳区','440514':'潮南区','440515':'澄海区','440523':'南澳区','440604':'禅城区','440605':'南海区',
                    '440606':'顺德区','440608':'高明区','441402':'梅江区','441403':'梅县区','441422':'大埔区','441423':'丰顺县',
                    '441424':'五华县','441426':'平远县','441427':'蕉岭县','441481':'兴宁市','441523':'陆河县','441581':'陆丰市','445102':'湘桥区',
                    '445103':'潮安区','445122':'饶平县','445202':'榕城区','445203':'揭东区','445222':'揭西县','445224':'惠来县','445281':'普宁市',
                    '440785':'恩平市','440802':'赤坎区','440803':'霞山区','440804':'坡头区','440811':'麻章区', '440823':'遂溪县','440825':'徐闻县',
                    '440881':'廉江市','440882':'雷州市','440883':'吴川市','440902':'茂南区','440904':'电白区','440981':'高州市','440982':'化州市',
                    '440983':'信宜市','441202':'端州区', '441223':'广宁县','441224':'怀集县', '441225':'封开县','441226':'德庆县','441283':'高要市',
                    '441702':'江城区','441704':'阳东区','441721':'阳西县','441781':'阳春市','441825':'连山壮族瑶族自治县','441826':'连南瑶族自治县',
                    '441882':'连州市','445302':'云城区','445303':'云安县','445321':'新兴县','445322':'郁南县','445381':'罗定市'}

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
    # 附件表
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

    # 自主变更
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
    ##生成监测图斑表
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

    # 在线举证
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

    # 初次举证
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

    # 补充举证
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

    # 地类样本
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
    print '创建成功'
    conn.commit()
    #conn.close()
    return conn

def createConn(folder,XZQName,xzqdm):   #通过行政区代码生成不同的数据库
    """创建数据库"""

    dir = folder + XZQName

    if(os.path.exists(dir) == False):

        os.makedirs(dir)

    db_path = dir + '/' + xzqdm + XZQName + '.db'

    if(os.path.exists(db_path) == False):

        with open(db_path, 'w') as f:
            
            f.close()

        conn = createDB(db_path)

        conn.text_factory = str

        arcpy.AddMessage("创建" + db_path + "成功!")
    else:

        conn = sqlite3.connect(db_path)

        conn.text_factory = str

    return conn

def getZl(byztb):
    """获取数据行政区代码及名字"""
    
    cursor = arcpy.da.SearchCursor(byztb,["XZQDM","ZLDWDM"])

    row = cursor.next()

    xzqdm = row[0]
    zldwdm = row[1]

    name = params.xzqlist[xzqdm]

    return name,xzqdm,zldwdm

def insertdatas(byztb,conn):
    """插入CCJZ表"""

    searchFields = ['DLBM', 'DLMC', 'QSXZ', 'QSDWDM', 'QSDWMC', 'TBMJ', 'BZ', 'SFJZ', 'XZQDM', 'TSTYBM', 'ZHXGR', 'SJDLBM', 'SHAPE@', 'ZLDWDM','SHAPE@XY']

    cursor = arcpy.da.SearchCursor(byztb,searchFields)

    number = 0

    for row in cursor:

        test()

        data = dict(zip(searchFields,row))

        conn.execute(params.sql_insertCCJZ,(parm1,parm2,parm3,parm4,parm5,parm6,parm7,parm8,parm9,parm10,parm11,parm12,parm13,parm14,parm15,parm16))

        (data['TSTYBM'], data["XZQDM"], data["TBMJ"], data["QSDWMC"], data["QSXZ"], data["SJDLBM"], data["DLBM"], data["SFJZ"], data["BZ"], data["ZHXGR"], data["SHAPE@"],str(test),xzqmc,coordX,coordY,SFXZ)

def main(folder,byztb,tp):

    arcpy.AddMessage("获取数据行政区代码和行政区名")
    name,xzqdm,zldwdm = getZl(byztb)

    arcpy.AddMessage("创建数据环境")
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

    num =0 #计数器，当插入一千条后就停止
    for row in cursor:
        TBFW = row[12].WKT
        test = []
        #if (num >3):
            #return
        if (row[8] != '' and row[8] != None):
            connnew = createConn(row[8])
        else:
            print '创建失败'
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
        SFXZ = '0'   #是否新增
        insertCCJZ(connnew, row[9], row[8], row[5], row[4], row[2], row[11], row[0], row[7], row[6], row[10], TBFW,str(test),xzqmc,coordX,coordY,SFXZ)
        connnew.commit()
        #num +=1
    del row
    del cursor
    #connnew.commit()
    connnew.close()

if __name__=='__main__':

    arcpy.AddMessage("提交国家DB数据生成")

    folder = arcpy.GetParameterAsText(0)
    byztb = arcpy.GetParameterAsText(1)
    tp = arcpy.GetParameterAsText(2)

    main(folder,byztb.tp)

    arcpy.AddMessage("结果")

