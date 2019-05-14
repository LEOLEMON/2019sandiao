#-*- coding:utf-8 -*-
#encoding:utf-8
import arcpy,json

def getname(name,number,names):
    if name in names:

        return getname(name,number+1,names)

    else:
        newname = name+"000"[0:3-len(str(number))] + str(number)
        names.append(newname)
        return newname

if __name__ == "__main__":
    
    jzzp = arcpy.GetParameterAsText(0)

    names = []

    with arcpy.da.UpdateCursor(jzzp,["TBYBH","NAME","FJLX"],sql_clause  = (None,"ORDER TBYBH,FJLX")) as cur:

        for row in cur:

            NAME = getname(row[0]+"_"+row[2]+"_",1,names)

            row[1] = NAME

            cur.updateRow(row)