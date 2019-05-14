import arcpy

if __name__ == "__main__":
    
    env = arcpy.GetParameterAsText(0)
    name = arcpy.GetParameterAsText(1)
    tp = arcpy.GetParameterAsText(2)
    jzzp = arcpy.GetParameterAsText(3)

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = env

    arcpy.SpatialJoin_analysis(tp,jzzp,name,"JOIN_ONE_TO_ONE","KEEP_ALL","""MC "MC" true true false 100 Text 0 0 ,First,#,%s,MC,-1,-1;NAME "NAME" true true false 50 Text 0 0 ,First,#,%s,NAME,-1,-1;TBYBH "TBYBH" true true false 50 Text 0 0 ,First,#,%s,TBYBH,-1,-1"""%(tp,jzzp,jzzp),"INTERSECT","#","#")