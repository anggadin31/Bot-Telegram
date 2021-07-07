from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import re
from openpyxl import load_workbook
import os
from pymongo import MongoClient, InsertOne
from collections import defaultdict
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def nestdict():
    return defaultdict(nestdict)        

class User():

    def __init__(self, username=''):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)


#@login.user_loader
def load_user(name):
    user = mongo.db.datax
    u = user.find_one({'name': name})
    if not u:
        return None
    return User(u['name'])


class Request():

    def __init__(self):
        client = MongoClient()
        self.db = client.daman
        self.coll = self.db.datarequest

    def get_data(self):
        return self.coll.find()
      

    def add_request(self, odp, pelanggan, id_user):
        # data = {'_id': ObjectId()}
        forupdate = {
            'ODP': odp,
            'PELANGGAN': pelanggan,

            'INPUT_BY': id_user,
            'last_modified': datetime.utcnow()+timedelta(hours=8),
            }
        return self.coll.update_one({ '_id':  ObjectId() },
                             {'$set': forupdate},
                             upsert=True)
    
    def delete_request(self,id_request):
        return self.coll.delete_one({ '_id':  ObjectId(id_request) })

class Userbot():

    def __init__(self):
        client = MongoClient()
        self.db = client.daman
        self.coll = self.db.userbot

    def get_data(self):
        return self.coll.find()

    def get_data_by_id(self,id_user):
        return self.coll.find_one({'_id':  ObjectId(id_user)})

    # def add_user(self, nik, nama,id_telegram):
    #     self.coll = self.db.userbot
    #     forupdate = {
    #         'NIK': nik,
    #         'NAMA': nama,
    #         'ID_TELEGRAM': id_telegram,
    #         'STATUS': 'NONAKTIF',
    #         'last_modified': datetime.utcnow()+timedelta(hours=8),
    #         }
    #     return self.coll.update_one({ '_id':  ObjectId() },
    #                          {'$set': forupdate},
    #                          upsert=True)

    # def get_id_user(self,id_telegram):
    #     self.coll = self.db.userbot
    #     return self.coll.find_one({'ID_TELEGRAM':id_telegram},{'_id':1})['_id']

    def activate(self, id_user):
        return self.coll.update_one({ '_id': ObjectId(id_user) },
                             {'$set': {'STATUS':'AKTIF',
                             'last_modified': datetime.utcnow()+timedelta(hours=8)}},
                             upsert=True)

    def deactivate(self, id_user):
        return self.coll.update_one({ '_id': ObjectId(id_user) },
                             {'$set': {'STATUS':'NONAKTIF',
                             'last_modified': datetime.utcnow()+timedelta(hours=8)}},
                             upsert=True)

    def delete_user(self,id_user):
        return self.coll.delete_one({ '_id':  ObjectId(id_user) })



class Dataodp():

    def __init__(self):
        client = MongoClient()
        self.db = client.daman
        self.coll = self.db.dataodpmaster

    def get_data(self):
        return self.coll.find()
    
    def get_data_by_id(self,id_odp):
        return self.coll.find_one({'_id':  ObjectId(id_odp)})

    def get_data_by_namaodp(self,namaodp):
        return self.coll.find_one({'NAMAODP':  namaodp})

    def get_data_by_layanan(self,layanan):
        return self.coll.find_one({'PORT.NO_LAYANAN': {'$regex': layanan, '$options':'i'}})

    def set_eksekutor(self, id_odp, eksekutor,statusuim):
        return self.coll.update_one({ '_id': ObjectId(id_odp) },
                             {'$set': {'EKSEKUTOR':eksekutor,'UIM':statusuim,
                             'last_modified': datetime.utcnow()+timedelta(hours=8)}},
                             upsert=True)

class Excelreport():

    def __init__(self):
        client = MongoClient()
        self.db = client.daman
        self.coll = self.db.excelreport

    def get_started(self, tanggal):
        
        tanggal = str(tanggal)
        operations = []
        data = nestdict()
        pos = 0
          
        wb = load_workbook(filename = os.getcwd()+'/EXCEL REPORT_ODP_{}.xlsx'.format(tanggal), read_only=True, data_only=True)
        ws = wb['OCC']    
        data = [[cell.value for cell in each] for each in ws.iter_rows(min_col=1, max_col=16, min_row=2)]
        print (data[0])

        for x in data:
            try:
                odp = data[data.index(x)][2].split(' ')
            except:
                pass
            
            toinsert = {
                        'LON': x[0],
                        'LAT' : x[1],
                        'ODP' : odp[0],
                        'RESULT ODP': x[3],
                        'STO' : x[4],
                        'KAP' : x[5],
                        'USED' : x[6],
                        'AVAI' : x[7],
                        'PORT OLT' : x[8],
                        'HOSTNAME' : x[9],
                        'OCC' : x[10],
                        'TANGGAL R2C' : x[11],
                        'BULAN R2C' : x[12],
                        'MITRA' : x[13],
                        'KET' : x[14],
                        'STATUS SIIS' : x[15],
                        'TANGGAL' : tanggal
                        }
            operations.append(InsertOne(toinsert))
            pos +=1
        self.coll.delete_many({'TANGGAL':tanggal})
        self.coll.drop()
        result = self.coll.bulk_write(operations)
        return pos

    def get_odp(self):
        data = self.coll.find()
        return [each['ODP'] for each in data]

    def get_data(self, odp):
        data = self.coll.find_one({'ODP':{'$regex':odp}})
        return data

class IDPort():

    def __init__(self):
        self.data = []

    def read_data(self):
        path='D:\daman\ID Port OLT Banjarmasin (new update).xlsx'
        wb = load_workbook(path, data_only=True)
        ws = wb['Data']    
        self.data = [[cell.value for cell in each] for each in ws.iter_rows(min_col=1, max_col=6, min_row=2)]
        return self.data

    def get_ipolt(self,ipslotport):
        if any(ipslotport in sublist for sublist in self.data):
            return True
        else:
            return False

    def get_index(self,v):
        for i, x in enumerate(self.data):
            if v in x:
                return (i)

    def print_data(self,ipslotport):
        index = self.get_index(ipslotport)
        idport = self.data[index][4]
        return idport

class Golive():

    def __init__(self):
        self.data = []

    def read_data(self):
        path='D:\daman\CEK GOLIVE.xlsx'
        wb = load_workbook(path, data_only=True)
        ws = wb['Sheet2']    
        self.data = [[cell.value for cell in each] for each in ws.iter_rows(min_col=1, max_col=19, min_row=2)]
        return self.data

    def get_odp(self,odp):
        if any(odp in sublist for sublist in self.data):
            return True
        else:
            return False

    def get_index(self,v):
        for i, x in enumerate(self.data):
            if v in x:
                return (i)

    def print_data(self,odp):
        index = self.get_index(odp)
        result = (self.data[index][2:5]+self.data[index][14:16])
        return result

class QrOdp():

    def __init__(self):
        self.data = []

    def read_data(self):
        path='D:\daman\DATA_QR_ODP.xlsx'
        wb = load_workbook(path, data_only=True)
        ws = wb['QR ODP']    
        self.data = [[cell.value for cell in each] for each in ws.iter_rows(min_col=1, max_col=3, min_row=2)]
        return self.data

    def get_odp(self,nama_odp):
        if any(nama_odp in sublist for sublist in self.data):
            return True
        else:
            return False

    def get_index(self,v):
        for i, x in enumerate(self.data):
            if v in x:
                return (i)

    def print_data(self,nama_odp):
        index = self.get_index(nama_odp)
        result = (self.data[index])
        return result

class OdpUim():
    def __init__(self):
        self.data = []

    def read_data(self):
        path='D:\daman\DALAPA_VALIDASI_UIM.xlsx'
        wb = load_workbook(path, data_only=True)
        ws = wb['Sheet2']    
        self.data = [[cell.value for cell in each] for each in ws.iter_rows(min_col=1, max_col=15, min_row=2)]
        return self.data
        
    def print_data(self, odpuim):
        result = []
        if any(odpuim in sublist for sublist in self.data):
            for i, x in enumerate(self.data):
              if odpuim in x:
                  result.append((self.data[i][2:6]+self.data[i][8:12]))
            return result
        else:
            return False

class OdpLap():
    def __init__(self):
        self.data = []

    def read_data(self):
        path='D:\daman\DALAPA_VALIDASI_LAPANGAN.xlsx'
        wb = load_workbook(path, data_only=True)
        ws = wb['Sheet2']    
        self.data = [[cell.value for cell in each] for each in ws.iter_rows(min_col=1, max_col=15, min_row=2)]
        return self.data
        
    def print_data(self, odplap):
        result = []
        if any(odplap in sublist for sublist in self.data):
            for i, x in enumerate(self.data):
              if odplap in x:
                  result.append((self.data[i][2:6]+self.data[i][8:12]))
            return result
        else:
            return False

class Absen():
    def read_data(self):
        mydate = datetime.datetime.now()
        currentMonth = mydate.strftime("%B")
        currentYear = mydate.strftime("%Y")
        currentSheet = currentMonth[0:3]+"-"+currentYear[2:]
        path='D:\daman\JADWAL DESEMBER 2019.xlsx'
        wb = load_workbook(path, data_only=True)
        ws = wb[currentSheet]    
        data = [[cell.value for cell in each] for each in ws.iter_rows(min_col=4, max_col=35, min_row=4, max_row=18)]
        tanggal = data[0][1:]
        return data,tanggal
        
    def print_data(self,tgl):
        data,tanggal= self.read_data()
        result = []
        data = data[1:]
        if tgl in tanggal:
          index = tanggal.index(tgl)+1
          for i, x in enumerate(data):
            result.append(data[i][0])
            result.append(data[i][index])
        return result

class Datalabel():

    def __init__(self):
        client = MongoClient()
        self.db = client.daman
        self.coll = self.db.datalabel

    def get_started(self, tanggal):
        
        tanggal = str(tanggal)
        operations = []
        data = nestdict()
        pos = 0
            

        wb = load_workbook(filename = os.getcwd()+'/Database Qrcode Kalsel {}.xlsx'.format(tanggal), read_only=True, data_only=True)
        ws = wb.active
        data = [[cell.value for cell in each] for each in ws.iter_rows(min_col=1, max_col=3, min_row=2)]
        print (data[0])

        for x in data:           
            toinsert = {
                        'LABELCODE': x[0],
                        'NO' : x[1],
                        'LABEL_ID' : x[2],
                        'TANGGAL' : tanggal
                        }
            operations.append(InsertOne(toinsert))
            pos +=1
        self.coll.delete_many({'TANGGAL':tanggal})
        self.coll.drop()
        result = self.coll.bulk_write(operations)
        return pos

    def get_label(self):

        data = self.coll.find()
        return [each['LABELCODE'] for each in data]

# class Dataodpokupansi():

#     def __init__(self):
#         self.client = MongoClient()
#         self.db = self.client.dataocc
#         self.coll = self.db.dataokupansi

#     def get_all(self):
#         coll_update = self.db.data_update.find_one({'_id':'last_update'})
#         query = self.coll.find({'TANGGAL':coll_update['Tanggal']})
#         return [x for x in query] 

#     def get_odp(self):
#         coll_update = self.db.data_update.find_one({'_id':'last_update'})
#         query = self.coll.find({'TANGGAL':coll_update['Tanggal']})
#         return [x['ODP_NAME'] for x in query] 

#     def get_data(self, namaodp, tanggal=datetime.now().strftime('%Y%m%d')):
#     # def get_data(self, namaodp, tanggal='20180925'):
#         coll_update = self.db.data_update.find_one({'_id':'last_update'})['Tanggal']
#         query = self.coll.find({'ODP_NAME': namaodp, 'TANGGAL':coll_update})
#         return [x for x in query]

#     def get_items_occ(self, namaodp):
#         query = self.coll.find({'NAMAODP': namaodp})
#         return [x['OCCU'] for x in query]

#     def get_items_kap(self, namaodp):
#         query = self.coll.find({'NAMAODP': namaodp})
#         return [x['KAP'] for x in query]

#     def get_items_used(self, namaodp):
#         query = self.coll.find({'NAMAODP': namaodp})
#         return [x['USED'] for x in query]
        
#     def get_items_tgalsurvey(self, namaodp):
#         query = self.coll.find({'NAMAODP': namaodp})
#         return [x['TGAL_SURVEY'] for x in query] 

class Dataservice():
    def __init__(self):
        client = MongoClient()
        db = client.daman
        self.coll = db.serviceinfo

### Fungsi untuk melakukan pembacaan file data dari excel untuk dimasukkan ke dalam basis data *.db
    def get_started(self, tgl):
        self.coll.drop()
        operations = []
        pos = 1
        with open(os.getcwd()+'\\SERVICE_INFO_R6_WITEL_KALSEL.txt', 'r') as f:
            for line in f:
                print (pos)
                if pos == 1:
                    pos +=1
                    continue
                pos +=1
                print("ini temp_data")
                temp_data = line.split('";"')

                # temp_data = line.split(';')
                operations.append(
                        InsertOne({
                                'REGIONAL': temp_data[0],
                                'WITEL': temp_data[1],
                                'DATEL': temp_data[2],
                                'STO': temp_data[3],
                                'STO_NAME': temp_data[4],   
                                'SERVICE_ID': temp_data[5],
                                'SERVICE_NAME': temp_data[6],   
                                'SERVICE_NUMBER': temp_data[7],
                                'SERVICE_TYPE': temp_data[8],
                                'SERVICE_ADMINSTATE': temp_data[9],
                                'SERVICE_PARTY': temp_data[10],
                                'SERVICE_PARTY_NAME': temp_data[11],
                                'SERVICE_CONTACT': temp_data[12],
                                'ADDRESS': temp_data[13],
                                'CFS_VERSION': temp_data[14],
                                'RFS_VERSION': temp_data[15],
                                'TECHNOLOGY': temp_data[16],
                                'ID_ODP': temp_data[17],
                                'STP_TARGET': temp_data[18],
                                'STP_PORT': temp_data[19],
                                'SP_TARGET': temp_data[20],
                                'SP_PORT': temp_data[21],
                                'CPE_SN': temp_data[41],
                                'SERVICE_STATUS': temp_data[43],
                                'last_update': tgl
                                })
                        )
            result = self.coll.bulk_write(operations)
        print ("Database updated")

    def get_data(self, ODP):
        ODP = '^'+ODP+' '
        query = self.coll.find({
            'STP_PORT': {'$regex': ODP,'$options': 'i'},
            'SERVICE_ADMINSTATE': {'$in':['IN_SERVICE','SUSPENDED','PENDING','PENDING_DISCONNECT','CANCEL_PENDING_CONNECT','PENDING_CANCEL']}
            })
        return [x for x in query]

    def get_list(self, ODP):
        ODP = '^'+ODP+' '
        query = self.coll.find({
            'STP_PORT': {'$regex': ODP,'$options': 'i'},
            'SERVICE_ADMINSTATE': {'$in':['IN_SERVICE','SUSPENDED']}
            })
        return [x for x in query]

    def get_id_odp(self, ODP):
        ODP = '^'+ODP+' '
        query = self.coll.find({
            'STP_PORT': {'$regex': ODP,'$options': 'i'},
            'SERVICE_ADMINSTATE': {'$in':['IN_SERVICE','SUSPENDED']}
            })
        return [x['ID_ODP'] for x in query]

    def get_port_odp(self, ODP):
        ODP = '^'+ODP+' '
        query = self.coll.find({
            'STP_PORT': {'$regex': ODP,'$options': 'i'},
            'SERVICE_ADMINSTATE': {'$in':['IN_SERVICE','SUSPENDED']}
            })
        return [x['STP_PORT'] for x in query]

    def get_service_name(self, ODP):
        ODP = '^'+ODP+' '
        query = self.coll.find({
            'STP_PORT': {'$regex': ODP,'$options': 'i'},
            'SERVICE_ADMINSTATE': {'$in':['IN_SERVICE','SUSPENDED']}
            })
        return [x['SERVICE_NAME'] for x in query]
    
    def get_odpuimlist(self, ODP):
        ODP = '^'+ODP+''
        query = self.coll.find({
            'STP_TARGET': {'$regex': ODP,'$options': 'i'},
            'SERVICE_ADMINSTATE': {'$in':['IN_SERVICE','SUSPENDED']}
            })
        return [[x['ID_ODP'],x['STP_PORT'],x['SERVICE_NAME'],x['SERVICE_ADMINSTATE'],x['last_update']] for x in query]

    def get_layananuim(self, tel):
        query = self.coll.find({
            'SERVICE_NAME': {'$regex': tel,'$options': 'i'},
            'SERVICE_ADMINSTATE': {'$in':['IN_SERVICE','SUSPENDED']}
            })
        return [[x['SERVICE_NAME'],x['SERVICE_ADMINSTATE'],x['STP_PORT'],x['SP_TARGET'],x['SP_PORT'],x['CPE_SN'],x['SERVICE_STATUS'],x['last_update']] for x in query]

    def get_customer(self, nolayanan):
        query = self.coll.find({
            'SERVICE_NAME': {'$regex': nolayanan,'$options': 'i'},
            # 'SERVICE_ADMINSTATE': {'$in':['IN_SERVICE','SUSPENDED']}
            })
        return [[x['SERVICE_PARTY_NAME'],x['ADDRESS']] for x in query]

    def get_odp_customer(self, nolayanan):
        query = self.coll.find({
            'SERVICE_NAME': {'$regex': nolayanan,'$options': 'i'},
            # 'SERVICE_ADMINSTATE': {'$in':['IN_SERVICE','SUSPENDED']}
            })
        return [x['STP_PORT'] for x in query]

class r2cnoss():
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)
        self.client = gspread.authorize(self.creds)
        # self.sheet = self.client.open("MONITORING GOLIVE KALSEL").worksheet('GOLIVE 2019')
        self.sheet = self.client.open("MONITORING GOLIVE").worksheet('Booking ODP')
        
    def get_odp(self,odp):
        # odp = 'ODP-BJM-FAK/076'
        self.client.login()
        target = self.sheet.findall(odp)
        target_row = [self.sheet.row_values(each.row) for each in target]
        return target_row

class Dataunsc():

    # def __init__(self):
    #     client = MongoClient()
    #     db = client.daman
    #     self.coll = db.dataunsc

    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_report.json', self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open("REKAP ENTRY ULANG UNSC").worksheet('6.FWFM REVOKE')
        client = MongoClient()
        db = client.unsc
        self.coll = db.sditomman

    # def update_data(self):
    #     operations = []
    #     data = nestdict()
    #     pos = 0
    #     wb = load_workbook(filename = os.getcwd()+'/dataunsc.xlsx', read_only=True, data_only=True)
    #     ws = wb.active    
    #     data = [[cell.value for cell in each] for each in ws.iter_rows(min_col=1, max_col=28, min_row=1)]
    #     for x in data:
    #         print(pos)
    #         if pos == 0:
    #             pos +=1
    #             continue
    #         pos +=1
    #         toinsert = {}
    #         for indx in range(len(data[0])):
    #             toinsert[data[0][indx]] = x[indx]
    #         operations.append(InsertOne(toinsert))
    #     self.coll.drop()
    #     result = self.coll.bulk_write(operations)
    #     return pos

    def get_all(self):
        # data = self.coll.find()
        # return [x for x in data] 
        self.client.login()
        koor = self.sheet.col_values(18)
        unsc = self.sheet.col_values(22)
        ket = self.sheet.col_values(25)
        return koor,unsc,ket

    def get_sc_sdi(self,sc):
        data = self.coll.find_one({'sc': int(sc)})
        return data