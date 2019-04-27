#!python

import arcpy,uuid

xzkPath = arcpy.GetParameterAsText(0)
cskPath = arcpy.GetParameterAsText(1)

tmpPath = 't_'+str(uuid.uuid1())[0:8]

xzknum = int(arcpy.GetCount_management(xzkPath).getOutput(0))
csknum = int(arcpy.GetCount_management(cskPath).getOutput(0))

arcpy.AddField_management(xzkPath,'uninum','LONG')

arcpy.AddField_management(cskPath,'mianji','DOUBLE')


cskcur = arcpy.da.UpdateCursor(cskPath,['mianji','shape_area'])

for row in cskcur:

    row[0] = row[1]
    
    cskcur.updateRow(row)
    
    
cur = arcpy.da.UpdateCursor(xzkPath,['uninum'])

num = 0
for row in cur:

    num = num+1
    row[0] = num

    cur.updateRow(row)


arcpy.Intersect_analysis([xzkPath,cskPath],tmpPath,'ALL')


tmpnum = int(arcpy.GetCount_management(tmpPath).getOutput(0))


if xzknum != tmpnum:

    arcpy.AddMessage('现状库与初始库未套合，请检查')
    
else:
    
    fields = ['cskbsm','cskdlbm','cskczcsxm']
    
    for x in fields:
    
        arcpy.AddField_management(xzkPath,x,'TEXT','','',50)
        
    arcpy.AddField_management(xzkPath,'cskarea','DOUBLE')
    
    
    tmpcur = arcpy.da.SearchCursor(tmpPath,['uninum','BSM_1','DLBM_1','CZCSXM_1','mianji'])
   
    tmpval = {}
    
    for row in tmpcur:
    
        tmpval[row[0]] = [row[1],row[2],row[3],row[4]]
    
    
    xzkcur = arcpy.da.UpdateCursor(xzkPath,['uninum','cskbsm','cskdlbm','cskczcsxm','cskarea'])
    
    for row in xzkcur:
    
        uninum = row[0]
        row[1],row[2],row[3],row[4] = tmpval[uninum][0],tmpval[uninum][1],tmpval[uninum][2],tmpval[uninum][3]

        xzkcur.updateRow(row)
    
    
    arcpy.AddMessage('完成')
    
    #arcpy.SetParameterAsText(2,xzkPath)




