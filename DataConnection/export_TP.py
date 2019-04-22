#!python
# -*- coding:utf-8 -*-

import arcpy,time

def total(fcA):

    with arcpy.da.SearchCursor(fcA,'OBJECTID') as fealist:

        count = 0

        for x in fealist:
        
            count = count+1

        arcpy.AddMessage('待更新图斑{0}条'.format(count))

        arcpy.SetProgressor('step','更新进度',0,count,100)
        
def main(fcA,fcB,fcC):

    with arcpy.da.SearchCursor(fcA,'TSTYBM') as xfealist:

        count = 0

        fields = ['BSM','YSDM','FHDM','TSTYBM','CJR','CJRQ','BZ','MC','LJ','JD','WD','DWMS','WXSL','FWJ','QCJ','FYJ','RKXH','RKSJ','FJLX','SFSS','MD5','CHECK_CODE','SHAPE']

        zfealist = arcpy.da.InsertCursor(fcC,fields)

        for x in xfealist:

            yfealist = arcpy.da.SearchCursor(fcB,fields,'TSTYBM=\'{0}\''.format(x[0]))

            for y in yfealist:
                
                zfealist.insertRow(y)

            count += 1

            if count == 100:

                count = 0
                arcpy.SetProgressorPosition()

        arcpy.SetProgressorPosition()

if __name__ == '__main__':

    fcA = arcpy.GetParameterAsText(0)
    fcB = arcpy.GetParameterAsText(1)
    fcC = arcpy.GetParameterAsText(2)
    
    arcpy.AddMessage('开始')

    total(fcA)

    main(fcA,fcB,fcC)

    arcpy.AddMessage('完成')