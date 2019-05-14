#!python
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import arcpy, sqlite3, os, requests, time
from myThread import MyThread


pic59 = ['4401','4402','4403','4404','4405','4406','4407']
pic60 = ['4408','4409','4410','4411','4412']
pic61 = ['4413','4414''4415','4416','4417']
          
xzqlist = {
    '440103':'荔湾区','440104':'越秀区','440105':'海珠区', '440233':'新丰县','440106':'天河区','440111':'白云区','440112':'黄埔区','440113':'番禺区','440229':'翁源县','440114':'花都区','440115':'南沙区','440117':'从化区','440118':'增城区','440203':'武江区','440204':'浈江区','440205':'曲江区','440222':'始兴县','440224':'仁化县','440232':'乳源瑶族自治县','440281':'乐昌市','440282':'南雄市','440303':'罗湖区','440304':'福田区','440305':'南山区','440306':'宝安区','440307':'龙岗区','440308':'盐田区','440402':'香洲区','440403':'斗门区','440404':'金湾区','440703':'蓬江区','440704':'江海区','440705':'新会区','440781':'台山市','440783':'开平区','440784':'鹤山市','441203':'鼎湖区','441284':'四会市','441302':'惠城区','441322':'博罗县','441323':'惠东县','441324':'龙门县','441502':'汕尾城区','441521':'海丰县','441602':'源城区','441621':'紫金县','441622':'龙川县','441624':'和平县','441623':'连平县','441625':'东源县','441803':'清新县','441821':'佛冈县','441823':'阳山县','441881':'英德市','441900':'东莞市','442000':'中山市','440607':'三水区','441303':'惠阳区','441802':'清城区','440507':'龙湖区','440511':'金平区','440512':'濠江区','440513':'潮阳区','440514':'潮南区','440515':'澄海区','440523':'南澳区','440604':'禅城区','440605':'南海区','440606':'顺德区','440608':'高明区','441402':'梅江区','441403':'梅县区','441422':'大埔区','441423':'丰顺县','441424':'五华县','441426':'平远县','441427':'蕉岭县','441481':'兴宁市','441523':'陆河县','441581':'陆丰市','445102':'湘桥区','445103':'潮安区','445122':'饶平县','445202':'榕城区','445203':'揭东区','445222':'揭西县','445224':'惠来县','445281':'普宁市','440785':'恩平市','440802':'赤坎区','440803':'霞山区','440804':'坡头区','440811':'麻章区','440823':'遂溪县','440825':'徐闻县','440881':'廉江市','440882':'雷州市','440883':'吴川市','440902':'茂南区','440904':'电白区','440981':'高州市','440982':'化州市','440983':'信宜市','441202':'端州区','441223':'广宁县','441224':'怀集县','441225':'封开县','441226':'德庆县','441283':'高要市','441702':'江城区','441704':'阳东区','441721':'阳西县','441781':'阳春市','441825':'连山壮族瑶族自治县','441826':'连南瑶族自治县','441882':'连州市','445302':'云城区','445303':'云安县','445321':'新兴县','445322':'郁南县','445381':'罗定市'
    }

sql_insertCCJZ = '''
INSERT INTO CCJZ(TBYBH,XZQDM,TBMJ,QSDWMC,QSXZ,YPDL,WYRDDL,SFJZ,BZ,JZRY,TBFW,PZD,XMC,XZB,YZB,SFXZ)
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
'''

sql_insertFJ = '''
INSERT INTO FJ(F_ID,TBYBH,XZQDM,TCBM,FJMC,FJLX,PSSJ,PSJD,PSRY,Longitude,Latitude,JYM,FJ,XZB,YZB,LYSB,TakeOffLon,TakeOffLat,TakeOffRelHeight,TakeOffAltitude,PSGD,PSFYJ,PSAltitude)
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
'''
     

def insertCCJZ(conn,parm1,parm2,parm3,parm4,parm5,parm6,parm7,parm8,parm9,parm10,parm11,parm12,parm13,parm14,parm15,parm16):

    conn.execute(sql_insertCCJZ,(parm1,parm2,parm3,parm4,parm5,parm6,parm7,parm8,parm9,parm10,parm11,parm12,parm13,parm14,parm15,parm16))


def insertFJ(conn,parm0,parm1,parm2,parm3,parm4,parm5,parm6,parm7,parm8,parm9,parm10,parm11,parm12,parm13,parm14,parm15,parm16,parm17,parm18,parm19,parm20,parm21,parm22):

    conn.execute(sql_insertFJ,(parm0,parm1,parm2,parm3,parm4,parm5,parm6,parm7,parm8,parm9,parm10,parm11,parm12,parm13,parm14,parm15,parm16,parm17,parm18,parm19,parm20,parm21,parm22))


def createDB(path):

    conn = sqlite3.connect(path)
    
    # 附件表
    sql_createFJ = '''
    CREATE TABLE 'FJ'('F_ID' TEXT NOT NULL PRIMARY KEY,
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
    'JYM' TEXT,
    'LYSB' TEXT,
    'TakeOffLon' REAL,
    'TakeOffLat' REAL,
    'TakeOffRelHeight' REAL,
    'TakeOffAltitude' REAL,
    'PSGD' REAL,
    'PSFYJ' REAL,
    'PSAltitude' REAL
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

    # 生成监测图斑表
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
    
    print ('Successfully create Database!')
    
    conn.commit()

    return conn


def createConn(XZQDM): #通过行政区代码生成不同的数据库

    XZQName = xzqlist[XZQDM]
    
    dir = "D:/test/test3/" + XZQName
    
    if(os.path.exists(dir.decode('utf-8')) == False):

        os.makedirs(dir.decode('utf-8'))
        
    db_path = dir + '/' +XZQDM + XZQName.decode('utf-8') + '.db'

    if(os.path.exists(db_path.decode('utf-8')) == False):
    
        with open(db_path.decode('utf-8'), 'w') as f:
            
            f.close()
            
        conn = createDB(db_path.decode('utf-8'))
        
        conn.text_factory = str
        
        print 'Successfully create ' + db_path.decode('utf-8') + '!'
    else:
    
        conn = sqlite3.connect(db_path.decode('utf-8'))
        
        conn.text_factory = str
        
    return conn


def main():

    arcpy.env.workspace = 'D:/test/清城.gdb'
    
    fields_BYZTB = ['DLBM','DLMC','QSXZ','QSDWDM','QSDWMC','TBMJ','SFJZ','XZQDM','TSTYBM','ZHXGR','SJDLBM','SHAPE@WKT','ZLDWDM','SHAPE@XY']
    
    fields_TP = ['SHAPE@XY','FJLX','TSTYBM','FWJ','CJR','CJRQ','MC','JD','WD','CHECK_CODE']
    
    #选择性消除属性访问，提高脚本效率
    SearchCursor = arcpy.da.SearchCursor
    local_insertFJ = insertFJ
    local_insertCCJZ = insertCCJZ
    
    cur_BYZTB = SearchCursor('BYZTB',fields_BYZTB)
    
    xzqdm = cur_BYZTB.next()[7]
    
    cur_BYZTB.reset()

    connnew = createConn(xzqdm) #通过游标获取该图层要素行政区代码，生成数据库
    
    if (xzqdm[0:4] in pic59):

        urlhost = "http://192.168.110.59/thumbnail/"
    elif (xzqdm[0:4] in pic60):

        urlhost = "http://192.168.101.60/thumbnail/"
    elif (xzqdm[0:4] in pic61):

        urlhost = "http://192.168.101.61/thumbnail/"
    else:

        urlhost = "http://192.168.101.62/thumbnail/"
    
    num = 0
    
    F_ID = 0
    
    def loop(url,temp,row2,F_ID,dic,LYSB):
    
        redictcontent = requests.get(url).content
        
        return redictcontent,temp,row2,F_ID,dic,LYSB
        
    result = []

    threads = []

    for row in cur_BYZTB:

        if row[6] != 'Y':
            
            SFJZ = 'N'
        else:
            
            SFJZ = 'Y'
            
        text = []
        
        cur_TP = SearchCursor('TP',fields_TP,"TSTYBM = '{0}'".format(row[8]))

        for row2 in cur_TP:
        
            F_ID += 1
        
            LYSB = '0'
        
            if row2[1] == 'W':
            
                LYSB = '1'
        
            dic = {}

            dic['type'] = row2[1]
            dic['x'], dic['y'] = row2[0]
            dic['radius'] = row2[3]
            
            text.append(dic)
            
            url = str(urlhost) + str(row[12]) + '/' + str(row[8]) + '/' + str(row2[6]) + "?real=True"
            
            temp = row[7]
            
            t = MyThread(loop,(url,temp,row2,F_ID,dic,LYSB),loop.__name__)
            threads.append(t)
            
        xzqmc = xzqlist[row[7]]
        coordX,coordY = row[13]
        SFXZ = '0'   #是否新增
        
        local_insertCCJZ(connnew, row[8], row[7], row[5], row[4], row[2], row[10], row[0], SFJZ, '', row[9], row[11],str(text).replace('\'','"'),xzqmc,coordX,coordY,SFXZ)

        num += 1
        
        loops = range(len(threads))
        
        if loops >= 1000:

            for i in loops:
                
                threads[i].start()
                
            for i in loops:
            
                threads[i].join()
                
                result.append(threads[i].get_result())

            for i in range(len(result)):
                
                local_insertFJ(connnew, str(result[i][3]),result[i][2][2], result[i][1], 'CCJZ', result[i][2][6], result[i][2][1], result[i][2][5], result[i][2][3], result[i][2][4],result[i][2][7], result[i][2][8], result[i][2][-1], result[i][0],result[i][4]['x'],result[i][4]['y'],result[i][5],0,0,0,0,0,0,0)
            
                # local_insertFJ(connnew, str(F_ID),row2[2], temp, 'CCJZ', row2[6], row2[1], row2[5], row2[3], row2[4],row2[7], row2[8], row2[-1], redictcontent,dic['x'],dic['y'],LYSB,0,0,0,0,0,0,0)

            threads = []
            result = []
        
        if num  == 1000:
            try:  
                connnew.commit()
                num = 0
            except Exception, e:
                print (e,num)
                
    for i in range(len(result)):
        
        local_insertFJ(connnew, str(result[i][3]),result[i][2][2], result[i][1], 'CCJZ', result[i][2][6], result[i][2][1], result[i][2][5], result[i][2][3], result[i][2][4],result[i][2][7], result[i][2][8], result[i][2][-1], result[i][0],result[i][4]['x'],result[i][4]['y'],result[i][5],0,0,0,0,0,0,0)
    
    connnew.commit()
    connnew.close()
    print ('恭喜发财！'.decode('utf-8'))


if __name__=='__main__':
    
    st = time.time()
    
    main()
    
    st2 = time.time()
    
    print (st2-st)