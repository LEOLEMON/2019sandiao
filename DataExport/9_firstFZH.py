#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json,arcpyDeal

if __name__ == "__main__":
    
    arcpy.AddMessage("9_初始分组")

    xzkPath = arcpy.GetParameterAsText(0)

    xzknum = int(arcpy.GetCount_management(xzkPath).getOutput(0))

    lstbsm = {}

    xzkcur = arcpy.da.SearchCursor(xzkPath,['cskbsm'])

    for row in xzkcur:

        cskbsm = row[0]
        
        if cskbsm in lstbsm:
        
            continue
        
        else:
        
            lstbsm[cskbsm] = 0

    arcpy.AddMessage('总共{0}个标识码'.format(len(lstbsm)))

    num = 0

    for x in lstbsm:

        num = num+1

        lstbsm[x] = num
        
    arcpyDeal.ensureFields(xzkPath,['xzkfzh'],'LONG')

    xzkcur = arcpy.da.UpdateCursor(xzkPath,['cskbsm','xzkfzh'])

    for row in xzkcur:

        cskbsm = row[0]

        row[1] = lstbsm[cskbsm]

        xzkcur.updateRow(row)
    
    arcpy.SetParameterAsText(1,xzkPath)
    arcpy.AddMessage('9_初始分组完成')