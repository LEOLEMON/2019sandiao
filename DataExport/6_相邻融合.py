#!python

import arcpy,uuid

xzkPath = arcpy.GetParameterAsText(0)
tarPath = 'tar_'+str(uuid.uuid1())[0:8]
disPath = 'dis_'+str(uuid.uuid1())[0:8]

xzknum = int(arcpy.GetCount_management(xzkPath).getOutput(0))

arcpy.AddField_management(xzkPath,'tmpshpvary','LONG')

xzkcur = arcpy.da.UpdateCursor(xzkPath,['shpvary','tmpshpvary'])

for row in xzkcur:
    
    if row[0] == 'Y':
        
        row[1] = 2
       
    elif row[0] == 'N':
    
        row[1] = 1
        
    xzkcur.updateRow(row)


arcpy.SelectLayerByAttribute_management(xzkPath,'CLEAR_SELECTION')

arcpy.Dissolve_management(xzkPath,tarPath,'dlbm;zldwdm;gdlx;tbxhdm;gdzzsxdm;xzkfzh','','SINGLE_PART','UNSPLIT_LINES')

#对融合的大图斑反向挂接原碎图斑信息

arcpy.SpatialJoin_analysis(target_features=tarPath, join_features=xzkPath, out_feature_class=disPath, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_COMMON", field_mapping="""TSTYBM "TSTYBM" true true false 1024 Text 0 0 ,Join,",",{0},TSTYBM,-1,-1;shpvary "shpvary" true true false 100 Text 0 0 ,Join,#,{1},shpvary,-1,-1""".format(xzkPath,xzkPath), match_option="CONTAINS", search_radius="", distance_field_name="")


arcpy.AddMessage('融合完成')
    
    

