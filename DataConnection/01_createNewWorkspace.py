import arcpy,os,shutil

def createFolder(folder,name):

    rootdir = folder + "/" + name
    photodir = folder + "/" + name + u"/��֤��Ƭ"
    shapedir =  folder + "/" + name + u"/ʸ������"

    if os.path.exists(rootdir):

        arcpy.Delete_management(rootdir)

    os.mkdir(rootdir)
    os.mkdir(photodir)
    os.mkdir(shapedir)

    return shapedir,photodir

def createTempGBD(folder,name):

    name = "temp" + name + ".gdb"

    gdbpath = folder + "/" + name
    
    if os.path.exists(gdbpath):

        arcpy.Delete_management(gdbpath)

    arcpy.CreateFileGDB_management(folder, name)

    return folder+"/"+name

def start(folder,xiannname,xzqdm):

    name = xzqdm +xiannname

    arcpy.AddMessage("01_�����ļ���·��")
    shapedir,photodir = createFolder(folder,name)

    arcpy.AddMessage("01_������ʱGDB")
    tempgdb = createTempGBD(folder,name)

    return tempgdb,photodir,shapedir

if __name__ == "__main__":
    
    arcpy.AddMessage("01_�����滮Ժ�Խ�����")
    
    folder = arcpy.GetParameterAsText(0)
    xiannname = arcpy.GetParameterAsText(1)
    xzqdm = arcpy.GetParameterAsText(2)

    folder =folder.replace("\\","/")

    tempgdb,photodir,shapedir = start(folder,xiannname,xzqdm)

    arcpy.SetParameterAsText(3,shapedir)
    arcpy.SetParameterAsText(4,tempgdb)
    arcpy.SetParameterAsText(5,photodir)

    arcpy.AddMessage("01_����")