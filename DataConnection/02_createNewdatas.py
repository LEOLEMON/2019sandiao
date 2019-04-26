import arcpy,os,shutil

class FieldClass:

    name = ''
    aliasname = ''
    type = 'Text'
    length = 0
    canNull = 'NULLABLE'

    def __init__(self,name,aliasname,type,length,canNull):

        self.name = name
        self.aliasname = aliasname
        self.type = type
        self.length = length
        self.canNull = canNull

class DCCGTBFieldsClass:

    newTBFields=[]

    def __init__(self):

        self.newTBFields.append(FieldClass('BSM','标识码','Text',18,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('TBYBH','图斑预编号','Text',8,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('TBBH','图斑编号','Text',8,'NULLABLE'))
        self.newTBFields.append(FieldClass('ZLDWDM','坐落单位代码','Text',60,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('DLBM','地类编码','Text',5,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('DLMC','地类名称','Text',60,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('GDLXMC','耕地类型名称','Text',20,'NULLABLE'))
        self.newTBFields.append(FieldClass('TBXHDM','图斑细化代码','Text',4,'NULLABLE'))
        self.newTBFields.append(FieldClass('TBXHMC','图斑细化名称','Text',20,'NULLABLE'))
        self.newTBFields.append(FieldClass('ZZSXDM','种植属性代码','Text',4,'NULLABLE'))
        self.newTBFields.append(FieldClass('ZZSXMC','种植属性名称','Text',10,'NULLABLE'))
        self.newTBFields.append(FieldClass('CZCSXM','城镇村属性码','Text',4,'NULLABLE'))
        self.newTBFields.append(FieldClass('TBLX','图斑类型','Text',12,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('WYM','图斑唯一码','Text',36,'NULLABLE'))
        self.newTBFields.append(FieldClass('BHLX','变化类型','Text',6,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('WJZLX','未举证类型','Text',14,'NULLABLE'))
        self.newTBFields.append(FieldClass('FZH','分组号','Text',8,'NON_NULLABLE'))

class JZZPFieldsClass:

    newTBFields=[]

    def __init__(self):

        self.newTBFields.append(FieldClass('TBYBH','图斑预编号','Text',8,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('WYM','图斑唯一码','Text',36,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('NAME','照片名称','Text',14,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('WJZLX','未举证类型','Text',14,'NULLABLE'))
        self.newTBFields.append(FieldClass('PSSJ','拍摄时间','Date',20,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('PSR','拍摄人','Text',20,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('AZIM','方位角','DOUBLE',20,'NULLABLE'))
        self.newTBFields.append(FieldClass('ROLL','俯仰角','DOUBLE',20,'NULLABLE'))
        self.newTBFields.append(FieldClass('TILT','侧倾角','DOUBLE',20,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('PICX','X坐标','DOUBLE',20,'NULLABLE'))
        self.newTBFields.append(FieldClass('PICY','Y坐标','DOUBLE',20,'NULLABLE'))
        self.newTBFields.append(FieldClass('FJLX','附件类型','Text',1,'NON_NULLABLE'))
        self.newTBFields.append(FieldClass('FJFW','附件范围','Text',1024,'NULLABLE'))

def createGBD(shapedir,name):

    arcpy.CreateFileGDB_management(shapedir, name)

    return shapedir+"/"+name+".gdb"

def CreateFields(targetpath,fieldsInstance):
        
    fields = fieldsInstance.newTBFields

    for field in fields:
        
        name = field.name
        aliasname = field.aliasname
        type = field.type
        length = field.length
        canNull = field.canNull

        arcpy.AddField_management(targetpath,name,type,"","",length,aliasname,canNull)

        print "add "+name

def CreateDCCGTB(env,SpatialReference):

    DCCGTB = "DCCGTB"

    arcpy.CreateFeatureclass_management(env, "DCCGTB", "POLYGON","","","",SpatialReference)

    fieldsInstance = DCCGTBFieldsClass()

    CreateFields(DCCGTB,fieldsInstance)

    DCCGTB = arcpy.Describe(DCCGTB).catalogPath

    return DCCGTB

def CreateJZZP(env,SpatialReference):

    JZZP = "JZZP"

    arcpy.CreateFeatureclass_management(env, "JZZP", "POINT","","","",SpatialReference)

    fieldsInstance = JZZPFieldsClass()

    CreateFields(JZZP,fieldsInstance)

    JZZP = arcpy.Describe(JZZP).catalogPath

    return JZZP

def getSpatialReference(xzqdm):

    SpatialReference = None

    if xzqdm in ['441202','441203','441223','441224','441225','441226','441702','441704','441721','441781','441825','441826','441882','445302','445303','445321','445322','445381','440902','440904','440981','440982','440983','440802','440803','440804','440811','440823','440825','440881','440882','440883','440785']:

        SpatialReference = arcpy.SpatialReference("CGCS2000 3 Degree GK Zone 37")

    elif xzqdm in ['441283','441284','441302','441303','441322','441323','441324','441502','441521','441602','441621','441622','441623','441624','441625','441802','441803','441821','441823','442000','440703','440704','440705','440781','440783','440784','440604','440605','440606','440607','440608','440402','440403','440404','440303','440304','440305','440306','440307','440308','440203','440204','440205','440222','440224','440229','440232','440233','440281','440282','440103','440104','440105','440106','440111','440112','440113','440114','440115','440117','440118','441881']:

        SpatialReference = arcpy.SpatialReference("CGCS2000 3 Degree GK Zone 38")

    elif xzqdm in ['441402','441403','441422','441423','441424','441426','441427','441481','441523','441581','440507','440511','440512','440513','440514','440515','440523','445103','445122','445202','445203','445222','445224','445281','441900','445102']:

        SpatialReference = arcpy.SpatialReference("CGCS2000 3 Degree GK Zone 39")

    return SpatialReference

def createFeatureLayer(env,xzqdm):

    arcpy.env.workspace = env

    SpatialReference = getSpatialReference(xzqdm)

    if SpatialReference == "":

        arcpy.AddMessage("行政区代码错误，无法找到对应坐标系")

    DCCGTB = CreateDCCGTB(env,SpatialReference)
    JZZP = CreateJZZP(env,SpatialReference)

    return DCCGTB,JZZP

def start(shapedir,xiannname,xzqdm):

    name = xzqdm +xiannname

    arcpy.AddMessage("02_创建工作GDB")
    gdb = createGBD(shapedir,name)

    arcpy.AddMessage("02_图层")
    DCCGTB,JZZP = createFeatureLayer(gdb,xzqdm)

    return DCCGTB,JZZP

if __name__ == "__main__":
    
    arcpy.AddMessage("02_创建规划院对接数据")
    
    shapedir = arcpy.GetParameterAsText(0)
    xiannname = arcpy.GetParameterAsText(1)
    xzqdm = arcpy.GetParameterAsText(2)

    DCCGTB,JZZP = start(shapedir,xiannname,xzqdm)

    arcpy.SetParameterAsText(3,DCCGTB)
    arcpy.SetParameterAsText(4,JZZP)

    arcpy.AddMessage("02_结束")