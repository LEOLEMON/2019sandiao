#-*- coding:utf-8 -*-
#coding:utf-8
relations = []

relations.append({'dm':'0303','mc':'�����ֵ�'})
relations.append({'dm':'0304','mc':'ɭ������'})
relations.append({'dm':'0306','mc':'�������'})
relations.append({'dm':'0402','mc':'����ݵ�'})
relations.append({'dm':'0603','mc':'����'})
relations.append({'dm':'1105','mc':'�غ�̲Ϳ'})
relations.append({'dm':'1106','mc':'��½̲Ϳ'})
relations.append({'dm':'1108','mc':'�����'})
relations.append({'dm':'0101','mc':'ˮ��'})
relations.append({'dm':'0102','mc':'ˮ����'})
relations.append({'dm':'0103','mc':'����'})
relations.append({'dm':'0201','mc':'��԰'})
relations.append({'dm':'0202','mc':'��԰'})
relations.append({'dm':'0203','mc':'��԰'})
relations.append({'dm':'0204','mc':'����԰��'})
relations.append({'dm':'0201K','mc':'�ɵ�����԰'})
relations.append({'dm':'0202K','mc':'�ɵ�����԰'})
relations.append({'dm':'0203K','mc':'�ɵ�����԰'})
relations.append({'dm':'0204K','mc':'�ɵ�������԰��'})
relations.append({'dm':'0301','mc':'��ľ�ֵ�'})
relations.append({'dm':'0302','mc':'���ֵ�'})
relations.append({'dm':'0305','mc':'��ľ�ֵ�'})
relations.append({'dm':'0307','mc':'�����ֵ�'})
relations.append({'dm':'0301K','mc':'�ɵ�����ľ�ֵ�'})
relations.append({'dm':'0302K','mc':'�ɵ������ֵ�'})
relations.append({'dm':'0307K','mc':'�ɵ��������ֵ�'})
relations.append({'dm':'0401','mc':'��Ȼ���ݵ�'})
relations.append({'dm':'0403','mc':'�˹����ݵ�'})
relations.append({'dm':'0404','mc':'�����ݵ�'})
relations.append({'dm':'0403K','mc':'�ɵ����˹����ݵ�'})
relations.append({'dm':'1001','mc':'��·�õ�'})
relations.append({'dm':'1002','mc':'�����ͨ�õ�'})
relations.append({'dm':'1003','mc':'��·�õ�'})
relations.append({'dm':'1004','mc':'������·�õ�'})
relations.append({'dm':'1005','mc':'��ͨ����վ�õ�'})
relations.append({'dm':'1006','mc':'ũ���·'})
relations.append({'dm':'1007','mc':'�����õ�'})
relations.append({'dm':'1008','mc':'�ۿ���ͷ�õ�'})
relations.append({'dm':'1009','mc':'�ܵ������õ�'})
relations.append({'dm':'1101','mc':'����ˮ��'})
relations.append({'dm':'1102','mc':'����ˮ��'})
relations.append({'dm':'1103','mc':'ˮ��ˮ��'})
relations.append({'dm':'1104','mc':'����ˮ��'})
relations.append({'dm':'1107','mc':'����'})
relations.append({'dm':'1109','mc':'ˮ�������õ�'})
relations.append({'dm':'1110','mc':'���������û�ѩ'})
relations.append({'dm':'1104A','mc':'��ֳ����'})
relations.append({'dm':'1104K','mc':'�ɵ�����ֳ����'})
relations.append({'dm':'1107A','mc':'����'})
relations.append({'dm':'1201','mc':'���е�'})
relations.append({'dm':'1202','mc':'��ʩũ�õ�'})
relations.append({'dm':'1203','mc':'�￲'})
relations.append({'dm':'1204','mc':'�μ��'})
relations.append({'dm':'1205','mc':'ɳ��'})
relations.append({'dm':'1206','mc':'������'})
relations.append({'dm':'1207','mc':'����ʯ����'})
relations.append({'dm':'201','mc':'����'})
relations.append({'dm':'202','mc':'������'})
relations.append({'dm':'203','mc':'��ׯ'})
relations.append({'dm':'204','mc':'���Ｐ�ɿ��õ�'})
relations.append({'dm':'205','mc':'�����õ�'})
relations.append({'dm':'201A','mc':'���ж�����ҵ�õ�'})
relations.append({'dm':'202A','mc':'�����������ҵ�õ�'})
relations.append({'dm':'203A','mc':'��ׯ������ҵ�õ�'})
relations.append({'dm':'0810','mc':'��԰���̵�'})
relations.append({'dm':'0810A','mc':'�㳡�õ�'})
relations.append({'dm':'1301','mc':'��ʱ�õ�'})
relations.append({'dm':'1302','mc':'�������'})
relations.append({'dm':'1303','mc':'������'})
relations.append({'dm':'1304','mc':'���δ����'})
relations.append({'dm':'HDGD','mc':'�ӵ�����'})
relations.append({'dm':'HQGD','mc':'��������'})
relations.append({'dm':'LQGD','mc':'��������'})
relations.append({'dm':'MQGD','mc':'��������'})
relations.append({'dm':'HHGD','mc':'ɳ�ĸ���'})
relations.append({'dm':'SMGD','mc':'ʯĮ������'})
relations.append({'dm':'LQYD','mc':'����԰��'})
relations.append({'dm':'GCCD','mc':'��Բݵ�'})
relations.append({'dm':'GZ','mc':'����'})
relations.append({'dm':'WG','mc':'δ����'})
relations.append({'dm':'YM','mc':'��ʱ��ֲ԰ľ'})
relations.append({'dm':'LM','mc':'��ʱ��ֲ��ľ'})
relations.append({'dm':'LH','mc':'�̻��ݵ�'})
relations.append({'dm':'MC','mc':'��ʱ��ֲ����'})
relations.append({'dm':'GSYY','mc':'����԰��'})
relations.append({'dm':'SSLM','mc':'������ľ'})
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