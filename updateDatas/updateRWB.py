import arcpy,cx_Oracle,psycopg2

if __name__ == "__main__":
    
    arcpy.AddMessage("开始更新任务表")

    pgconn = psycopg2.connect(host='',port='',database='',user='',password='')

    pgcursor = pgconn.cursor()

    pgcursor.execute("SELECT \"SBSJ\" from \"SH_RWB\" ORDER BY \"SBSJ\" DESC LIMIT 1")

    time = pgcursor.fetchone()[0]

    arcpy.AddMessage("任务表数据最新到：%s"%time)  

    orconn = cx_Oracle.connect('')

    orcursor = orconn.cursor()
    
    sql = "select count(*) FROM GDSDWYXTSXK.SH_RWB WHERE SBSJ >= \"TO_DATE\"('%s','yyyy-MM-dd hh24:mi:ss' )"%time

    count = orcursor.execute(sql).fetchone()[0]
    # count = 1

    arcpy.SetProgressor('step',"有%s条数据需要更新"%count,0,count,1000)

    # sql1 = "select * FROM GDSDWYXTSXK.SH_RWB WHERE SBSJ >= \"TO_DATE\"('%s','yyyy-MM-dd hh24:mi:ss') and ROWNUM <=1 ORDER BY SBSJ"%time
    sql1 = "select * FROM GDSDWYXTSXK.SH_RWB WHERE SBSJ >= \"TO_DATE\"('%s','yyyy-MM-dd hh24:mi:ss') ORDER BY SBSJ"%time

    orcursor.execute(sql1)

    arcpy.AddMessage(count)
    arcpy.AddMessage(sql1)

    exists = True

    number = 0

    while exists == True:

        number += 1

        arcpy.AddMessage("fetchmany : " + str(number))

        list0 = orcursor.fetchmany(numRows=1000)

        for i in range(len(list0)):

            list0[i] = list(list0[i])

            list0[i].pop()
            list0[i].pop()

            # arcpy.AddMessage(list0[i])

            for v in range(len(list0[i])):

                if type(list0[i][v]) == unicode:

                    list0[i][v] = list0[i][v].encode("gbk")

                    list0[i][v] = list0[i][v].replace("'","")

                    list0[i][v] = "'"+list0[i][v]+"'"

                elif list0[i][v] == None or list0[i][v] == "NULL":

                    list0[i][v] = "NUll"

                elif type(list0[i][v]) == float:
                    
                    list0[i][v] = str(list0[i][v])  
                else:

                    list0[i][v] = str(list0[i][v])

                    list0[i][v] = list0[i][v].replace("'","")

                    list0[i][v] = "'"+list0[i][v]+"'"

            # arcpy.AddMessage(list0[i])

            values = ",".join(list0[i])

            values = values.decode("gbk")
            
            insertSql = u"""INSERT INTO \"SH_RWB\" VALUES (%s)"""%values

            try:
                pgcursor.execute(insertSql)

            except Exception,e:
                
                arcpy.AddMessage(insertSql)
                arcpy.AddMessage(e.message)

                exists = False

                break

        if len(list0) < 1000:

            exists = False

        arcpy.SetProgressorPosition()

        pgconn.commit()


            


