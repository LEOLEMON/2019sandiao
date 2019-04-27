#!python


import arcpy,uuid

xzkPath = arcpy.GetParameterAsText(0)

xzknum = int(arcpy.GetCount_management(xzkPath).getOutput(0))

lstbsm = {}

xzkcur = arcpy.da.SearchCursor(xzkPath,['bsm'])

for row in xzkcur:

    bsm = row[0]
    
    if bsm in lstbsm:
    
        continue
    
    else:
    
        lstbsm[bsm] = 0
        
    
arcpy.AddMessage('总共{0}个标识码'.format(len(lstbsm)))

num = 1
for x in lstbsm:

    lstbsm[x] = num
    num = num+1
    
arcpy.AddField_management(xzkPath,'xzkfzh','LONG')
    
xzkcur = arcpy.da.UpdateCursor(xzkPath,['bsm','xzkfzh'])

for row in xzkcur:

    bsm = row[0]
    row[1] = lstbsm[bsm]
    xzkcur.updateRow(row)
    
arcpy.AddMessage('分组完成')
    
    

