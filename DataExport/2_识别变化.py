#!python


import arcpy,uuid

xzkPath = arcpy.GetParameterAsText(0)

xzknum = int(arcpy.GetCount_management(xzkPath).getOutput(0))

arcpy.AddField_management(xzkPath,'shuvary','TEXT')
arcpy.AddField_management(xzkPath,'shpvary','TEXT')

xzkcur = arcpy.da.UpdateCursor(xzkPath,['cskarea','shape_area','shpvary'])

for row in xzkcur:

    if abs(row[0]-row[1])<0.1:
    
        row[2] = 'N'
        
    else:
    
        row[2] = 'Y'
        
    xzkcur.updateRow(row)
    
    
xzkcur = arcpy.da.UpdateCursor(xzkPath,['dlbm','cskdlbm','shuvary'])

for row in xzkcur:

    if row[0] == row[1]:
    
        row[2] = 'N'
        
    else:
    
        row[2] = 'Y'   
        
    xzkcur.updateRow(row)   
    

arcpy.AddMessage('Íê³É')

#arcpy.SetParameterAsText(0,xzkPath)




