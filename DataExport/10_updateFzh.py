#!python
import arcpy,arcpyDeal

def dissolveGetFzh(xzkPath,dissolvepath,outputxzkpath):
    """融合得到新分组号"""

    arcpy.MakeFeatureLayer_management(xzkPath,"xzkPath")

    arcpy.SelectLayerByAttribute_management("xzkPath",'NEW_SELECTION',"shpvary = 'Y'")

    arcpy.Dissolve_management("xzkPath",dissolvepath,'shpvary','','SINGLE_PART','UNSPLIT_LINES')

    arcpyDeal.ensureFields(dissolvepath,['relfzh'],"LONG")

    tmpcur = arcpy.da.UpdateCursor(dissolvepath,['relfzh'])

    num = 5000000

    for row in tmpcur:
        
        row[0] = num
        
        num = num + 1
        
        tmpcur.updateRow(row)
        
    arcpy.SpatialJoin_analysis(xzkPath,dissolvepath,outputxzkpath,join_operation= "JOIN_ONE_TO_ONE",join_type="KEEP_ALL",match_option="WITHIN")

def updateFzh(outputxzkpath):

    xzkcur = arcpy.da.UpdateCursor(outputxzkpath,['xzkfzh','relfzh'],'relfzh is not null')

    for row in xzkcur:

        row[0] = row[1]
        
        xzkcur.updateRow(row)

if __name__ == "__main__":
    
    arcpy.AddMessage("10_开始更新分组号范围")
    
    enviroment = arcpy.GetParameterAsText(0)
    xzkPath = arcpy.GetParameterAsText(1)

    arcpy.env.workspace = enviroment
    arcpy.env.overwriteOutput = True

    dissolvepath = 'dissolvepath_10'
    outputxzkpath = 'outputxzkpath_10'

    arcpy.AddMessage("10_融合得到新分组号")
    dissolveGetFzh(xzkPath,dissolvepath,outputxzkpath)
        
    arcpy.AddMessage("10_补充更新分组号")
    updateFzh(outputxzkpath)

    arcpy.SetParameterAsText(2,outputxzkpath)
    arcpy.AddMessage("10_结束更新分组号范围")