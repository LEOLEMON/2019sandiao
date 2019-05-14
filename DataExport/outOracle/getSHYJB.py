import arcpy,cx_Oracle,dealNone,relation

if __name__ == "__main__":
    
    env = arcpy.GetParameterAsText(0)
    
    arcpy.env.workspace = env

    envname = arcpy.Describe(env).name.encode('gbk').split(".")[0]

    xzqdm = envname[0:6]

    conn =cx_Oracle.connect('')

    cur = conn.cursor()

    sql = """SELECT * from 
    (SELECT TSTYBM,SHDLBM,SHGDLX,SHTBXHMC,SHZZSXMC,row_number() Over(Partition by TSTYBM ORDER BY shsj) rank 
    from GDSDWYXTSXK.SH_YJB 
    WHERE ZLDWDM like '%s%s'  
    AND SHJL = '1'
    AND SHR like 'csy%s'
    ORDER BY ZLDWDM) 
    WHERE rank = '1'"""%(xzqdm,"%","%")

    cur.execute(sql)
    
    arcpy.AddMessage(sql)

    shyjList = cur.fetchall()

    cur.close()

    shyjDict = {}

    arcpy.SetProgressor('step','构造查询结果数据',0,len(shyjList),1)

    for i in range(len(shyjList)):

        TSTYBM = dealNone.dealNoneAndBlank(shyjList[i][0])
        SHDLBM = dealNone.dealNoneAndBlank(shyjList[i][1]) 
        SHGDLX = dealNone.dealNoneAndBlank(shyjList[i][2]) 
        SHTBXHMC = dealNone.dealNoneAndBlank(shyjList[i][3]) 
        SHZZSXMC = dealNone.dealNoneAndBlank(shyjList[i][4])

        SHTBXHDM = relation.getDM(SHTBXHMC)
        SHZZSXDM = relation.getDM(SHZZSXMC)

        shyjDict[TSTYBM] = {"SHDLBM":SHDLBM,"SHGDLX":SHGDLX,"SHTBXHDM":SHTBXHDM,"SHZZSXDM":SHZZSXDM}

        arcpy.SetProgressorPosition()

    arcpy.SetProgressor('step','更新数据',0,int(arcpy.GetCount_management("byztb").getOutput(0)),1)
    
    with arcpy.da.UpdateCursor("byztb",["TSTYBM","DLBM","GDLX","TBXHDM","GDZZSXDM"]) as cur:

        for row in cur:
        
            TSTYBM = row[0].encode('gbk')
            
            if TSTYBM not in shyjDict:
            
                continue

            shyj = shyjDict[TSTYBM]

            if shyj["SHDLBM"] != '':

                row[1] = shyj["SHDLBM"]

            if shyj["SHGDLX"] != '':

                row[2] = shyj["SHGDLX"]

            if shyj["SHTBXHDM"] != '':

                row[3] = shyj["SHTBXHDM"]

            if shyj["SHZZSXDM"] != '':

                row[4] = shyj["SHZZSXDM"]

            cur.updateRow(row)

            arcpy.SetProgressorPosition()



    