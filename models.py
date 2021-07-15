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
        ws = wb['validasi_odp_witel_KALSEL']    
        self.data = [[cell.value for cell in each] for each in ws.iter_rows(min_col=6, max_col=8, min_row=2)]
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
    def __init__(self):
        self.data = []
        self.tanggal = []

    def read_data(self):
        mydate = datetime.datetime.now()
        currentMonth = mydate.strftime("%B")
        currentYear = mydate.strftime("%Y")
        currentSheet = currentMonth[0:3]+"-"+currentYear[2:]
        path='D:\daman\JADWAL DESEMBER 2019.xlsx'
        wb = load_workbook(path, data_only=True)
        ws = wb[currentSheet]    
        self.data = [[cell.value for cell in each] for each in ws.iter_rows(min_col=4, max_col=35, min_row=4, max_row=18)]
        self.tanggal = self.data[0][1:]
        return self.data,self.tanggal
        
    def print_data(self,tgl):
        result = []
        data = self.data[1:]
        if tgl in self.tanggal:
          index = self.tanggal.index(tgl)+1
          for i, x in enumerate(data):
            result.append(data[i][0])
            result.append(data[i][index])
        return result

class isiAbsen():
    def __init__(self):
        self.scope = ['https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('absen-daman-1375d6c522b2.json', self.scope)
        self.client = gspread.authorize(self.creds)
        # self.sheet = self.client.open("MONITORING GOLIVE KALSEL").worksheet('GOLIVE 2019')
        self.sheet = self.client.open("dummy").worksheet(datetime.datetime.now().strftime("%b %Y"))
        
    def get_odp(self,odp):
        # odp = 'ODP-BJM-FAK/076'
        self.client.login()
        target = self.sheet.findall(odp)
        target_row = [self.sheet.row_values(each.row) for each in target]
        return target_row