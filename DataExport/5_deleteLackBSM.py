#!python
import arcpy,arcpyDeal

def judge(xzkpath,dissolvepath):
    """根据相同初始库进行融合，收集融合面积与初始库面积相差过大的图斑"""

    arcpy.Dissolve_management(xzkpath,dissolvepath,'cskbsm','','SINGLE_PART','UNSPLIT_LINES')

    bsmareaList = {}

    with arcpy.da.SearchCursor(dissolvepath,["cskbsm","SHAPE@AREA"]) as cur:

        for row in cur:

            bsmareaList[row[0]] = row[1]

    delbsm = []

    with arcpy.da.SearchCursor(xzkpath,["cskbsm","cskmianji"]) as cur:

        for row in cur:

            if abs(row[1] - bsmareaList[row[0]]) > 0.15 and row[0] not in delbsm:

                delbsm.append(row[0])

    return delbsm

def delBsm(xzkpath,notfullpath,delbsm):
    """删除初始库图斑范围内的现状库图斑合并面积与原面积不符的现状库图斑"""

    where_clause = " cskbsm in (%s)"%("'"+("','".join(delbsm)+"'"))

    arcpy.MakeFeatureLayer_management(xzkpath,"xzkpath")

    arcpy.SelectLayerByAttribute_management("xzkpath",where_clause=where_clause)

    count = int(arcpy.GetCount_management("xzkpath").getOutput(0))

    arcpy.AddMessage("共有%s个上报数据不全的图斑"%count)

    arcpy.CopyFeatures_management("xzkpath",notfullpath)
    
    arcpy.DeleteFeatures_management("xzkpath")

if __name__ == "__main__":
    
    arcpy.AddMessage("5_开始检查哪些图斑未占满原初始库范围")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkpath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    dissolvepath = 'dissolvepath_5'
    notfullpath = 'notfullpath_5'

    arcpy.AddMessage("5_判断哪些图斑未占满原初始库范围")
    delbsm = judge(xzkpath,dissolvepath)
        
    arcpy.AddMessage("5_删除初始库图斑范围内的现状库图斑合并面积与原面积不符的现状库图斑")
    delBsm(xzkpath,notfullpath,delbsm)

    arcpy.SetParameterAsText(2,xzkpath)
    arcpy.AddMessage("5_结束检查哪些图斑未占满原初始库范围")