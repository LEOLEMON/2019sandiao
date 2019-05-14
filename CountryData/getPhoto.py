#-*- coding:utf-8 -*-
#encoding:utf-8
import sqlite3,os

if __name__ == "__main__":
    
    folder = arcpy.GetParameterAsText(0)
    db = arcpy.GetParameterAsText(1)

    conn = sqlite3.connect(db)

    photodir = folder + "/æŸ÷§’’∆¨"

    if os.path.exists(rootdir) == False:

        os.mkdir(photodir)

    c = conn.cursor()

    c.execute("SELECT FJMC ")