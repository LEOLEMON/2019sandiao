#-*- coding:utf-8 -*-
#coding:utf-8
relations = []

relations.append({'dm':'0303','mc':'红树林地'})
relations.append({'dm':'0304','mc':'森林沼泽'})
relations.append({'dm':'0306','mc':'灌丛沼泽'})
relations.append({'dm':'0402','mc':'沼泽草地'})
relations.append({'dm':'0603','mc':'盐田'})
relations.append({'dm':'1105','mc':'沿海滩涂'})
relations.append({'dm':'1106','mc':'内陆滩涂'})
relations.append({'dm':'1108','mc':'沼泽地'})
relations.append({'dm':'0101','mc':'水田'})
relations.append({'dm':'0102','mc':'水浇地'})
relations.append({'dm':'0103','mc':'旱地'})
relations.append({'dm':'0201','mc':'果园'})
relations.append({'dm':'0202','mc':'茶园'})
relations.append({'dm':'0203','mc':'橡胶园'})
relations.append({'dm':'0204','mc':'其他园地'})
relations.append({'dm':'0201K','mc':'可调整果园'})
relations.append({'dm':'0202K','mc':'可调整茶园'})
relations.append({'dm':'0203K','mc':'可调整橡胶园'})
relations.append({'dm':'0204K','mc':'可调整其他园地'})
relations.append({'dm':'0301','mc':'乔木林地'})
relations.append({'dm':'0302','mc':'竹林地'})
relations.append({'dm':'0305','mc':'灌木林地'})
relations.append({'dm':'0307','mc':'其他林地'})
relations.append({'dm':'0301K','mc':'可调整乔木林地'})
relations.append({'dm':'0302K','mc':'可调整竹林地'})
relations.append({'dm':'0307K','mc':'可调整其他林地'})
relations.append({'dm':'0401','mc':'天然牧草地'})
relations.append({'dm':'0403','mc':'人工牧草地'})
relations.append({'dm':'0404','mc':'其他草地'})
relations.append({'dm':'0403K','mc':'可调整人工牧草地'})
relations.append({'dm':'1001','mc':'铁路用地'})
relations.append({'dm':'1002','mc':'轨道交通用地'})
relations.append({'dm':'1003','mc':'公路用地'})
relations.append({'dm':'1004','mc':'城镇村道路用地'})
relations.append({'dm':'1005','mc':'交通服务场站用地'})
relations.append({'dm':'1006','mc':'农村道路'})
relations.append({'dm':'1007','mc':'机场用地'})
relations.append({'dm':'1008','mc':'港口码头用地'})
relations.append({'dm':'1009','mc':'管道运输用地'})
relations.append({'dm':'1101','mc':'河流水面'})
relations.append({'dm':'1102','mc':'湖泊水面'})
relations.append({'dm':'1103','mc':'水库水面'})
relations.append({'dm':'1104','mc':'坑塘水面'})
relations.append({'dm':'1107','mc':'沟渠'})
relations.append({'dm':'1109','mc':'水工建筑用地'})
relations.append({'dm':'1110','mc':'冰川及永久积雪'})
relations.append({'dm':'1104A','mc':'养殖坑塘'})
relations.append({'dm':'1104K','mc':'可调整养殖坑塘'})
relations.append({'dm':'1107A','mc':'干渠'})
relations.append({'dm':'1201','mc':'空闲地'})
relations.append({'dm':'1202','mc':'设施农用地'})
relations.append({'dm':'1203','mc':'田坎'})
relations.append({'dm':'1204','mc':'盐碱地'})
relations.append({'dm':'1205','mc':'沙地'})
relations.append({'dm':'1206','mc':'裸土地'})
relations.append({'dm':'1207','mc':'裸岩石砾地'})
relations.append({'dm':'201','mc':'城市'})
relations.append({'dm':'202','mc':'建制镇'})
relations.append({'dm':'203','mc':'村庄'})
relations.append({'dm':'204','mc':'盐田及采矿用地'})
relations.append({'dm':'205','mc':'特殊用地'})
relations.append({'dm':'201A','mc':'城市独立工业用地'})
relations.append({'dm':'202A','mc':'建制镇独立工业用地'})
relations.append({'dm':'203A','mc':'村庄独立工业用地'})
relations.append({'dm':'0810','mc':'公园与绿地'})
relations.append({'dm':'0810A','mc':'广场用地'})
relations.append({'dm':'1301','mc':'临时用地'})
relations.append({'dm':'1302','mc':'光伏板区'})
relations.append({'dm':'1303','mc':'推土区'})
relations.append({'dm':'1304','mc':'拆除未尽区'})
relations.append({'dm':'HDGD','mc':'河道耕地'})
relations.append({'dm':'HQGD','mc':'湖区耕地'})
relations.append({'dm':'LQGD','mc':'林区耕地'})
relations.append({'dm':'MQGD','mc':'牧区耕地'})
relations.append({'dm':'HHGD','mc':'沙荒耕地'})
relations.append({'dm':'SMGD','mc':'石漠化耕地'})
relations.append({'dm':'LQYD','mc':'林区园地'})
relations.append({'dm':'GCCD','mc':'灌丛草地'})
relations.append({'dm':'GZ','mc':'耕种'})
relations.append({'dm':'WG','mc':'未耕种'})
relations.append({'dm':'YM','mc':'临时种植园木'})
relations.append({'dm':'LM','mc':'临时种植林木'})
relations.append({'dm':'LH','mc':'绿化草地'})
relations.append({'dm':'MC','mc':'临时种植牧草'})
relations.append({'dm':'GSYY','mc':'观赏园艺'})
relations.append({'dm':'SSLM','mc':'速生林木'})
relations.append({'dm':'','mc':''})

def getDM(mc):

    if type(mc) == unicode:

        mc = mc.encode('gbk')

    for relation in relations:

        if mc == relation['mc']:

            return relation['dm']

    return ''

def getMC(dm):

    if type(dm) == unicode:

        dm = dm.encode('gbk')

    for relation in relations:

        if dm == relation['dm']:

            return relation['mc']

    return ''