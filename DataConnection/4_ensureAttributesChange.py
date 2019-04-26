#-*- coding:utf-8 -*-
#encoding:utf-8
#!python

import arcpy,json,arcpyDeal,dealNone,DCCGTBFieldsDEfined

def createFianllyAttributesFields(targetpath):
    """��������ȷ���ĵ�����룬������ֲ���Դ��룬�������ͣ�ͼ��ϸ������"""

    fields = ["exp_tbbh","exp_wjzlx","exp_czcsxm","bhlx","exp_dlbm","exp_dlmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc","DLBM_1","GDZZSXMC_1","GDLX_1","TBXHMC_1"]

    arcpyDeal.ensureFields(targetpath,fields)

def ensureValue(fieldname,value):
    """���ֵ�Ƿ���ֵ��Χ��"""

    fbool = False

    for valuesdefined in DCCGTBFieldsDEfined.FieldsGroup:

        if valuesdefined.fieldname == fieldname:

            #���������ֵװ��,��ֱ���жϴ����Ƿ���ֵ��Χ��
            if valuesdefined.relations == []:

                if value in valuesdefined.values:

                    fbool = True

            #�������ֵװ������������ֵת�����������ֵ����ֵװ���б��ڵ�ĳһ��ֵ�����жϴ���ֵ����ֵ��Χ��
            else:

                for relation in valuesdefined.relations:

                    if relation.oldValue == value or relation.newValue == value:

                        fbool = True

                        break

            break

    return fbool

def getBhlx(checkValue,nullValue,tempdlbm,exp_sjdlbm):
    """�жϱ仯����"""
       
    #���dlbm��gdzzsxmc��gdlx��tbxhmc�Ƿ���ֵ��Χ��
    bhlx = ""

    for value in checkValue:

        if value[1] not in nullValue:
            
            boolValue = ensureValue(value[0],value[1])

            if boolValue:

                bhlx = "1"

    if tempdlbm != exp_sjdlbm:

        bhlx = "1"
    
    if bhlx != "1":

        bhlx = ""

    return bhlx

def getAllNewValue(tempwjzlx,tempczcsxm,tempdlbm,tempgdzzsxmc,tempgdlx,temptbxhmc):
    """������ʱdlbm��gdzzsxmc,gdlx,tbxhmc��wjzlx,czcxmm�����ʽ����������"""

    exp_wjzlx,exp_czcsxm,exp_dlbm,exp_dlmc,exp_gdzzsxdm,exp_gdzzsxmc,exp_gdlx,exp_tbxhdm,exp_tbxhmc = "","","","","","","","",""

    #����������
    for relation in DCCGTBFieldsDEfined.FieldsValuesRelationGroup:

        if relation.field1 == "DLBM" and relation.field1Value == tempdlbm:

            exp_dlbm = tempdlbm
            exp_dlmc = relation.field2Value

            break

    #���������ֲ����
    for valuesdefined in DCCGTBFieldsDEfined.FieldsGroup:

        if valuesdefined.fieldname == "ZZSXMC":

            if tempgdzzsxmc in valuesdefined.values:

                exp_gdzzsxmc = tempgdzzsxmc

            else:

                for relation in valuesdefined.relations:

                    if relation.oldValue == tempgdzzsxmc:

                        exp_gdzzsxmc = relation.newValue

                        break
            break

    for relation in DCCGTBFieldsDEfined.FieldsValuesRelationGroup:

        if relation.field2 == "ZZSXMC" and relation.field2Value == exp_gdzzsxmc:

            exp_gdzzsxdm = relation.field1Value

            break

    #�����������
    for valuesdefined in DCCGTBFieldsDEfined.FieldsGroup:

        if valuesdefined.fieldname == "GDLXMC":

            if tempgdlx in valuesdefined.values:

                exp_gdlx = tempgdlx

            else:

                for relation in valuesdefined.relations:

                    if relation.oldValue == tempgdlx:

                        exp_gdlx = relation.newValue

                        break
            break

    #����ͼ��ϸ������
    for valuesdefined in DCCGTBFieldsDEfined.FieldsGroup:

        if valuesdefined.fieldname == "TBXHMC":

            if temptbxhmc in valuesdefined.values:

                exp_tbxhmc = temptbxhmc

            else:

                for relation in valuesdefined.relations:

                    if relation.oldValue == temptbxhmc:

                        exp_tbxhmc = relation.newValue

                        break
            break

    for relation in DCCGTBFieldsDEfined.FieldsValuesRelationGroup:

        if relation.field2 == "TBXHMC" and relation.field2Value == exp_tbxhmc:

            exp_tbxhdm = relation.field1Value

            break

    #����δ��֤����
    for valuesdefined in DCCGTBFieldsDEfined.FieldsGroup:

        if valuesdefined.fieldname == "WJZLX":

            if tempwjzlx in valuesdefined.values:

                exp_wjzlx = tempwjzlx

            else:

                for relation in valuesdefined.relations:

                    if relation.oldValue == tempwjzlx:

                        exp_wjzlx = relation.newValue

                        break
            break

    #��������������
    for valuesdefined in DCCGTBFieldsDEfined.FieldsGroup:

        if valuesdefined.fieldname == "CZCSXM":

            if tempczcsxm in valuesdefined.values:

                exp_czcsxm = tempczcsxm

            else:

                for relation in valuesdefined.relations:

                    if relation.oldValue == tempczcsxm:

                        exp_czcsxm = relation.newValue

                        break
            break


    return exp_wjzlx,exp_czcsxm,exp_dlbm,exp_dlmc,exp_gdzzsxdm,exp_gdzzsxmc,exp_gdlx,exp_tbxhdm,exp_tbxhmc

def updateDatas(targetpath):
    """����ͼ���ϸ�����������ֵ"""

    searchFields = ['DLBM_1',"WJZLX","CZCSXM_1",'exp_sjdlbm','GDLX','TBXHDM','TBXHMC','GDZZSXDM','GDZZSXMC',"DLBM_12","GDZZSXMC_1","GDLX_1","TBXHMC_1","exp_wjzlx","exp_czcsxm",'bhlx',"exp_dlbm","exp_dlmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc"]
    tempFields = ['dlbm',"wjzlx","czcsxm",'exp_sjdlbm','gdlx','tbxhdm','tbxhmc','gdzzsxdm','gdzzsxmc',"dlbm_1","gdzzsxmc_1","gdlx_1","tbxhmc_1","exp_wjzlx","exp_czcsxm",'bhlx',"exp_dlbm","exp_dlmc","exp_gdzzsxdm","exp_gdzzsxmc","exp_gdlx","exp_tbxhdm","exp_tbxhmc"]

    arcpyDeal.checkField(targetpath,searchFields)

    list = [field.name for field in arcpy.ListFields(targetpath)]

    with arcpy.da.UpdateCursor(targetpath,searchFields) as UpdateCursor:

        for updaterow in UpdateCursor:

            data = dict(zip(tempFields,updaterow))

            dlbm = dealNone.dealNoneAndBlank(data['dlbm'])
            exp_sjdlbm = dealNone.dealNoneAndBlank(data['exp_sjdlbm'])
            czcsxm = dealNone.dealNoneAndBlank(data['czcsxm'])
            wjzlx = dealNone.dealNoneAndBlank(data['wjzlx'])
            gdlx = dealNone.dealNoneAndBlank(data['gdlx'])
            tbxhdm = dealNone.dealNoneAndBlank(data['tbxhdm'])
            tbxhmc = dealNone.dealNoneAndBlank(data['tbxhmc'])
            gdzzsxdm = dealNone.dealNoneAndBlank(data['gdzzsxdm'])
            gdzzsxmc = dealNone.dealNoneAndBlank(data['gdzzsxmc'])
            dlbm_1 = dealNone.dealNoneAndBlank(data['dlbm_1'])
            gdzzsxmc_1 = dealNone.dealNoneAndBlank(data['gdzzsxmc_1'])
            gdlx_1 = dealNone.dealNoneAndBlank(data['gdlx_1'])
            tbxhmc_1 = dealNone.dealNoneAndBlank(data['tbxhmc_1'])

            #������ʱֵ�����ʡ����������ݣ����ʡ�������Ϣ���
            
            nullValue = ["",None,u"��","0"]

            tempwjzlx = wjzlx
            tempczcsxm = czcsxm
            tempdlbm = dlbm if dlbm_1 in nullValue else dlbm_1
            tempgdzzsxmc = gdzzsxmc if gdzzsxmc_1 in nullValue else gdzzsxmc_1
            tempgdlx = gdlx if gdlx_1 in nullValue else gdlx_1
            temptbxhmc = tbxhmc if tbxhmc_1 in nullValue else tbxhmc_1

            #��ȡ�仯����
            
            checkValue = [["ZZSXMC",tempgdzzsxmc],["GDLXMC",tempgdlx],["TBXHMC",temptbxhmc]]

            bhlx = getBhlx(checkValue,nullValue,tempdlbm,exp_sjdlbm)

            #������ʱֵ��ԭ��������

            exp_wjzlx,exp_czcsxm,exp_dlbm,exp_dlmc,exp_gdzzsxdm,exp_gdzzsxmc,exp_gdlx,exp_tbxhdm,exp_tbxhmc = getAllNewValue(tempwjzlx,tempczcsxm,tempdlbm,tempgdzzsxmc,tempgdlx,temptbxhmc)

            #����

            updaterow[-10] = exp_wjzlx
            updaterow[-9] = exp_czcsxm
            updaterow[-8] = bhlx
            updaterow[-7] = exp_dlbm
            updaterow[-6] = exp_dlmc
            updaterow[-5] = exp_gdzzsxdm
            updaterow[-4] = exp_gdzzsxmc
            updaterow[-3] = exp_gdlx
            updaterow[-2] = exp_tbxhdm
            updaterow[-1] = exp_tbxhmc

            UpdateCursor.updateRow(updaterow)

            arcpy.SetProgressorPosition()

def start(targetpath):

    arcpy.AddMessage("4_��������ȷ�������ֶ�")
    createFianllyAttributesFields(targetpath)

    arcpy.AddMessage("4_��������")

    result = arcpy.GetCount_management(targetpath)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step','4_���Ա仯����',0,count,1)

    updateDatas(targetpath)

if __name__ == "__main__":
    
    arcpy.AddMessage("4_��ʼ�ж������Ƿ�仯")

    targetpath = arcpy.GetParameterAsText(0)

    start(targetpath)

    arcpy.SetParameterAsText(1,targetpath)

    arcpy.AddMessage("4_�����ж������Ƿ�仯")