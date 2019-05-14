#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,dealNone,relation

def dealNull(xzkPath,cskPath):
    """清理空值并更新MC值"""

    searchFields = ['bsm','dlbm','dlmc','gdlx','tbxhdm','tbxhmc','gdzzsxdm','gdzzsxmc','czcsxm','wjzlx','LINKTBS']

    xzkcur = arcpy.da.UpdateCursor(xzkPath,searchFields)

    for row in xzkcur:
        
        #去除空值

        for i in range(len(searchFields)):
            
            if  row[i] != None and row[i] in (u"0"):

                row[i] = ""

            else:

                row[i] = dealNone.dealNoneAndBlank(row[i])

        #更新mc值

        dlbm = row[1]
        tbxhdm = row[4]
        gdzzsxdm = row[6]

        row[2] = relation.getMC(dlbm)
        row[5] = relation.getMC(tbxhdm)
        row[7] = relation.getMC(gdzzsxdm)

        xzkcur.updateRow(row)

        arcpy.SetProgressorPosition()

    searchFields = ['bsm','dlbm','czcsxm']

    cskcur = arcpy.da.UpdateCursor(cskPath,searchFields)

    for row in cskcur:
        
        for i in range(len(searchFields)):

            row[i] = dealNone.dealNoneAndBlank(row[i])
        
        cskcur.updateRow(row)

        arcpy.SetProgressorPosition()

if __name__ == "__main__":

    xzkPath = arcpy.GetParameterAsText(0)
    cskPath = arcpy.GetParameterAsText(1)

    arcpy.AddMessage("0_开始清理空值并更新MC值")
    arcpy.SetProgressor('step','0_开始清理空值并更新MC值',0,int(arcpy.GetCount_management(xzkPath).getOutput(0))+ int(arcpy.GetCount_management(cskPath).getOutput(0)),1)
    dealNull(xzkPath,cskPath)

    arcpy.SetParameterAsText(2,xzkPath)
    arcpy.SetParameterAsText(3,cskPath)
        