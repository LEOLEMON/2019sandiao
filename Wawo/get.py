#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,logging

def setLogger(folder,name):

    logger = logging.getLogger(__name__)

    logger.setLevel(level = logging.INFO)

    logpath = (folder+"\\"+name+".csv")

    f = open(logpath,'w')

    handler = logging.FileHandler(logpath)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

if __name__ == "__main__":
    
    arcpy.AddMessage("开始导出数据csv")

    folder = arcpy.GetParameterAsText(0)
    name = arcpy.GetParameterAsText(1)
    data = arcpy.GetParameterAsText(2)

    logger = setLogger(folder,name)

    fieldsList = [f.name for f in arcpy.ListFields(data)]

    logger.info(",".join(fieldsList))

    count = int(arcpy.GetCount_management(data).getOutput(0))
    arcpy.SetProgressor('step',"收集",0,count,1)

    with arcpy.da.SearchCursor(data,fieldsList) as cur:

        for row in cur:
            
            logger.info(",".join([s if type(s) == unicode else str(s) for s in row]))

            arcpy.SetProgressorPosition() 

    arcpy.AddMessage("结束导出数据")
    