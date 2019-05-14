import arcpy

if __name__ == "__main__":
    
    env = arcpy.GetParameterAsText(0)
    name = arcpy.GetParameterAsText(1)
    byztb = arcpy.GetParameterAsText(2)
    dccgtb = arcpy.GetParameterAsText(3)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = env

    arcpy.SpatialJoin_analysis(byztb,dccgtb,name,"JOIN_ONE_TO_ONE","KEEP_ALL","""TSTYBM "TSTYBM" true true false 50 Text 0 0 ,First,#,%s,TSTYBM,-1,-1;TBYBH_1 "TBYBH_1" true true false 50 Text 0 0 ,First,#,%s,TBYBH,-1,-1;TBYBH "TBYBH" true true false 50 Text 0 0 ,First,#,%s,TBYBH,-1,-1"""%(byztb,byztb,dccgtb),"CONTAINS","#","#")