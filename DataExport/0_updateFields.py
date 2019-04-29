#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,arcpyDeal,dealNone

def dealNull(xzkPath,cskPath):
    """�����ֵ"""

    searchFields = ['bsm','dlbm','dlmc','gdlx','tbxhdm','tbxhmc','gdzzsxdm','gdzzsxmc','czcsxm','wjzlx','LINKTBS']

    xzkcur = arcpy.da.UpdateCursor(xzkPath,searchFields)

    for row in xzkcur:

        arcpy.SetProgressorPosition()
        
        for i in range(len(searchFields)):
            
            if  row[i] != None and row[i] in (u"0",u"��"):

                row[i] = ""

            else:

                row[i] = dealNone.dealNoneAndBlank(row[i])

        xzkcur.updateRow(row)

    searchFields = ['bsm','dlbm','czcsxm']

    cskcur = arcpy.da.UpdateCursor(cskPath,searchFields)

    for row in cskcur:

        arcpy.SetProgressorPosition()
        
        for i in range(len(searchFields)):

            row[i] = dealNone.dealNoneAndBlank(row[i])
        
        cskcur.updateRow(row)

def dealSH(xzkPath):
    """�����������������������Ϊ��'DLBM_1','GDZZSXMC_1','GDLX_1','TBXHMC_1'�������Щ��������������Ϊ'DLBM_1','GDZZSXMC_1','GDLX_1','TBXHMC_1'"""

    searchFields = ["DLBM_1","GDZZSXMC_1","GDLX_1","TBXHMC_1","SH_DLBM","SH_GDZZSXMC","SH_GDLX","SH_TBXHMC"]

    arcpyDeal.ensureFields(xzkPath,searchFields)

    with arcpy.da.UpdateCursor(xzkPath,searchFields) as UpdateCursor:

        for row in UpdateCursor:

            row [4] = row[0]
            row [5] = row[1]
            row [6] = row[2]
            row [7] = row[3]

            UpdateCursor.updateRow(row)

if __name__ == "__main__":

    xzkPath = arcpy.GetParameterAsText(0)
    cskPath = arcpy.GetParameterAsText(1)

    arcpy.AddMessage("0_��ʼ�����ֵ")
    count = int(arcpy.GetCount_management(xzkPath).getOutput(0))+ int(arcpy.GetCount_management(cskPath).getOutput(0))
    arcpy.SetProgressor('step','0_��ʼ�����ֵ',0,count,1)
    dealNull(xzkPath,cskPath)

    arcpy.AddMessage("0_����������")
    # dealSH(xzkPath) ��ʱ������������
    
    arcpy.SetParameterAsText(2,xzkPath)
    arcpy.SetParameterAsText(3,cskPath)
        