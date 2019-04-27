#!python

import arcpy,uuid

xzkPath = arcpy.GetParameterAsText(0)

xzknum = int(arcpy.GetCount_management(xzkPath).getOutput(0))

lstbsm = {}

xzkcur = arcpy.da.UpdateCursor(xzkPath,['xzkfzh','relfzh'],'relfzh is not null')

for row in xzkcur:

    row[0] = row[1]
    
    xzkcur.updateRow(row)

arcpy.AddMessage('分组完成')
    
    

