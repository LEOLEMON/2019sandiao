import arcpy,uuid

xzkPath = arcpy.GetParameterAsText(0)

tmpPath = 'dissolve'+str(uuid.uuid1())[0:8]

fzhPath = 'fzh'+str(uuid.uuid1())[0:8]

xzknum = int(arcpy.GetCount_management(xzkPath).getOutput(0))

arcpy.DeleteField_management(xzkPath,'relfzh')

arcpy.SelectLayerByAttribute_management(xzkPath,'NEW_SELECTION',"shpvary = 'Y'")

arcpy.Dissolve_management(xzkPath,tmpPath,'shpvary','','SINGLE_PART','UNSPLIT_LINES')

arcpy.AddField_management(tmpPath,'relfzh','LONG')

tmpcur = arcpy.da.UpdateCursor(tmpPath,['relfzh'])

num = 5000000
for row in tmpcur:
    
    row[0] = num
    num = num + 1
    
    tmpcur.updateRow(row)
    
    
arcpy.SpatialJoin_analysis(xzkPath,tmpPath,fzhPath,"JOIN_ONE_TO_ONE","KEEP_COMMON","uninum 'uninum' true true false 4 Long 0 0 ,First,#,{0},uninum,-1,-1;relfzh 'relfzh' true true false 4 Long 0 0 ,First,#,{1},relfzh,-1,-1".format(xzkPath,tmpPath),"INTERSECT","","")


fzhcur =  arcpy.da.SearchCursor(fzhPath,['uninum','relfzh'])
    
lstfzh = {}

for row in fzhcur:

    lstfzh[row[0]] = row[1]
    
    
arcpy.AddField_management(xzkPath,'relfzh','LONG')
    
xzkcur = arcpy.da.UpdateCursor(xzkPath,['uninum','relfzh'])


for row in xzkcur:

    if (row[0] in lstfzh):
    
        row[1] = lstfzh[row[0]]
        xzkcur.updateRow(row)
        
    else:
        continue
    
arcpy.AddMessage('Íê³É')
    
    

    
