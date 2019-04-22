import arcpy,arcpyDeal,json,dealNone

def UpdateDats(jzzp):

    updateCurosr = arcpy.da.UpdateCursor(jzzp,['WJZLX','NAME','PSR','AZIM','ROLL','TILT','PICX','PICY','FJLX','FJFW'])

    for updateRow in updateCurosr:

        WJZLX = dealNone.dealNoneAndBlank(updateRow[0])

        if WJZLX == "":

            updateRow[0] = ""

        else:

            updateRow[1] = ""
            updateRow[2] = ""
            updateRow[3] = 0
            updateRow[4] = 0
            updateRow[5] = 0
            updateRow[6] = 0
            updateRow[7] = 0
            updateRow[8] = ""
            updateRow[9] = ""

        updateCurosr.updateRow(updateRow)

        arcpy.SetProgressorPosition()

def start(jzzp):

    arcpy.AddMessage("32_开始检查")
    result = arcpy.GetCount_management(jzzp)
    count = int(result.getOutput(0))
    arcpy.SetProgressor('step',"32_检查值域",0,count,1)

    UpdateDats(jzzp)


if  __name__ == "__main__":
    
    arcpy.AddMessage("32_开始进行照片值域检查")

    jzzp = arcpy.GetParameterAsText(0)

    start(jzzp)

    arcpy.AddMessage("32_结束照片值域检查")