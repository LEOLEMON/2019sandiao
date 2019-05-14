import arcpy

if __name__ == "__main__":
    
    table = arcpy.GetParameterAsText(0)

    arcpy.env.overwriteOutput = True

    baseName = arcpy.Describe(table).baseName

    arcpy.TableToTable_conversion(table,"C:/Users/HCD/Desktop/JDZ/Í¼°ß±í",baseName+u".dbf","#","""Join_Count "Join_Count" true true false 4 Long 0 0 ,First,#,C:/Users/HCD/Documents/ArcGIS/Default.gdb/"""+baseName+""",Join_Count,-1,-1;TARGET_FID "TARGET_FID" true true false 4 Long 0 0 ,First,#,C:/Users/HCD/Documents/ArcGIS/Default.gdb/"""+baseName+""",TARGET_FID,-1,-1;TSTYBM "TSTYBM" true true false 50 Text 0 0 ,First,#,C:/Users/HCD/Documents/ArcGIS/Default.gdb/"""+baseName+""",TSTYBM,-1,-1;TBYBH_1 "TBYBH_1" true true false 50 Text 0 0 ,First,#,C:/Users/HCD/Documents/ArcGIS/Default.gdb/"""+baseName+""",TBYBH_1,-1,-1;TBYBH "TBYBH" true true false 50 Text 0 0 ,First,#,C:/Users/HCD/Documents/ArcGIS/Default.gdb/"""+baseName+""",TBYBH,-1,-1;SHAPE_Leng "SHAPE_Leng" false true true 8 Double 0 0 ,First,#,C:/Users/HCD/Documents/ArcGIS/Default.gdb/"""+baseName+""",SHAPE_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,C:/Users/HCD/Documents/ArcGIS/Default.gdb/"""+baseName+""",SHAPE_Area,-1,-1""","#")