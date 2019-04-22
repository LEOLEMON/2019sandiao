import arcpy,arcpyDeal,json,pathArgs

def checkTBYBHAndTBWYM(data):

    if data['BHLX'] == "3" or data['BHLX'] == "0":

        data["WYM"] = ""
        data['TBYBH'] = ""

    return data

def check1234(data):

    #耕地
    if data["DLBM"][0:2] != "01":

        data["GDLXMC"] = ""

        if data["ZZSXDM"] in ['GZ','WG']:

            data["ZZSXDM"] = ""
            data["ZZSXMC"] = ""

        if data["TBXHDM"] in ['HDGD','HQGD','LQGD','MQGD','HHGD','SMGD']:

            data["TBXHDM"] = ""
            data["TBXHMC"] = ""

    #园地
    if data["DLBM"][0:2] != "02":

        if data["ZZSXDM"] in ['YM','GSYY']:

            data["ZZSXDM"] = ""
            data["ZZSXMC"] = ""

        if data["TBXHDM"] in ['LQYD']:

            data["TBXHDM"] = ""
            data["TBXHMC"] = ""

    #林地
    if data["DLBM"][0:2] != "03":

        if data["ZZSXDM"] in ['LM','SSLM']:

            data["ZZSXDM"] = ""
            data["ZZSXMC"] = ""

    #草地
    if data["DLBM"][0:2] != "04":

        if data["ZZSXDM"] in ['LH','MC']:

            data["ZZSXDM"] = ""
            data["ZZSXMC"] = ""

        if data["TBXHDM"] in ['GCCD']:

            data["TBXHDM"] = ""
            data["TBXHMC"] = ""

    return data

def checkWJZLX(data):

    if data['WJZLX'] != "":

        data["WYM"] = ""
        data["ZZSXDM"] = ""
        data["ZZSXMC"] = ""
        data["TBXHDM"] = ""
        data["TBXHMC"] = ""
        data["GDLXMC"] = ""

    return data

def checkdatas(dccgtb):

    datas = []
    newdatas = {}
    searchFields = ["objectid","TBYBH","WYM","BHLX","DLBM","ZZSXDM","ZZSXMC","TBXHDM","TBXHMC","GDLXMC"]
    tempFields = ["objectid","TBYBH","WYM","BHLX","DLBM","ZZSXDM","ZZSXMC","TBXHDM","TBXHMC","GDLXMC"]
    
    arcpyDeal.createTempDatas(searchFields,tempFields,dccgtb,datas)

    for data in datas:

        data = checkTBYBHAndTBWYM(data)

        data = check1234(data)

        newdatas[data["objectid"]] = data

        arcpy.SetProgressorPosition()

    return newdatas

def UpdateDats(dccgtb,newdatas):

    searchFields = ["objectid","TBYBH","WYM","DLBM","ZZSXDM","ZZSXMC","TBXHDM","TBXHMC","GDLXMC"]
    with arcpy.da.UpdateCursor(dccgtb,searchFields) as UpdateCursor:

        for updaterow in UpdateCursor:
            
            data = newdatas[updaterow[0]]

            updaterow[1] = data["TBYBH"]
            updaterow[2] = data["WYM"]
            updaterow[3] = data["DLBM"]
            updaterow[4] = data["ZZSXDM"]
            updaterow[5] = data["ZZSXMC"]
            updaterow[6] = data["TBXHDM"]
            updaterow[7] = data["TBXHMC"]
            updaterow[8] = data["GDLXMC"]
        
            UpdateCursor.updateRow(updaterow)

            arcpy.SetProgressorPosition()

def start(dccgtb):

    arcpy.AddMessage("31_开始检查")
    result = arcpy.GetCount_management(dccgtb)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step',"31_检查值域",0,count,1)

    newdatas = checkdatas(dccgtb)

    arcpy.AddMessage("31_更新数据")
    arcpy.SetProgressor('step',"31_更新数据",0,count,1)

    UpdateDats(dccgtb,newdatas)

if  __name__ == "__main__":
    
    arcpy.AddMessage("31_开始进行值域检查")

    dccgtb = arcpy.GetParameterAsText(0)

    start(dccgtb)

    arcpy.AddMessage("31_结束值域检查")