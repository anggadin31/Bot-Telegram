import sys
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import re
from models import *
from fuzzywuzzy import fuzz, process
from math import radians, cos, sin, asin, sqrt
from operator import itemgetter
import unicodedata
from pprint import pprint

class process_bot():

	def __init__(self):
		client = MongoClient()
		self.db = client.daman
		self.db_excelreport = Excelreport()
		self.code = self.db_excelreport.get_odp()
		self.db_idport = IDPort()
		self.db_odpuim = OdpUim()
		self.db_odplap = OdpLap()
		self.db_golive = Golive()
		self.db_qrodp = QrOdp()
		self.db_jadwal = Absen()

	def odpuim(self,text='WRONGCOMMAND'):
		if text in self.code:
			data = self.db_excelreport.get_data(text)
			lat = data['LAT']
			longi = data['LON']
			kap = data['KAP']
			used = data['USED']
			avai = data['AVAI']
			port_olt = data['PORT OLT']
			hostname = data['HOSTNAME']
			occ = data['OCC']
			tanggal_r2c = data['TANGGAL R2C']
			bulan_r2c = data['BULAN R2C']
			mitra = data['MITRA']
			status_siis = data['STATUS SIIS']
			tgl = data['TANGGAL']
			resp = \
			"{}\
			\nKAP----: {}\
			\nUSED--: {}\
			\nAVAI---: {}\
			\nPORT OLT--: {}\
			\nHOSTNAME-: {}\
			\nOCC----: {}%\
			\nTGL R2C--: {}\
			\nMITRA---: {}\
			\nSTATUS SIIS-: {}\
			\nLok-: {},{}\
			\nTgl Update: {}".format(text, kap, used, avai, port_olt, hostname, occ, tanggal_r2c, mitra, status_siis, lat, longi, tgl)
		else:
		    resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
		return resp

	def potong(self,text='WRONGCOMMAND'):
		s = text
		r=re.split("[^a-zA-Z\d]+",s)
		ans='_'.join([ i for i in r if len(i) > 0 ])
		resp=""
		if 'INTERNET' in ans:
			internet_index = ans.find('INTERNET')
			internet = ans[internet_index-22:internet_index+8]
			resp+=internet+"\n"
		if 'IPTV' in ans:
			iptv_index = ans.find('IPTV')
			iptv = ans[iptv_index-22:iptv_index+4]
			resp+=iptv+"\n"
		if 'VOICE' in ans:
			voice_index = ans.find('VOICE')
			voice = ans[voice_index-21:voice_index+5]
			resp+=voice
		return resp

	def cekOdpUim(self,text='WRONGCOMMAND'):
		if len(self.db_odpuim.data)<1:
			self.db_odpuim.read_data()
		if text.isnumeric():
			text = int(text)
		hasil = self.db_odpuim.print_data(text)
		if hasil == False:
			resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
		else:
			resp = \
			resp = "{}\nSTO|GPON|SLOT|PORT|NO. INET|ODP UIM|VALIDITAS\n".format(text)	
			for each in hasil:
				resp += "{}|{}|{}|{}|{}|{}|{}\n".format(each[0],each[1],each[2],each[3],each[4],
					each[6],each[7])
		return resp

	def cekOdpLap(self,text='WRONGCOMMAND'):
		if len(self.db_odplap.data)<1:
			self.db_odplap.read_data()
		if text.isnumeric():
			text = int(text)
		hasil = self.db_odplap.print_data(text)
		if hasil == False:
			resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
		else:
			resp = \
			resp = "{}\nSTO|GPON|SLOT|PORT|NO. INET|ODP LAP|VALIDITAS\n".format(text)	
			for each in hasil:
				resp += "{}|{}|{}|{}|{}|{}|{}\n".format(each[0],each[1],each[2],each[3],each[4],
					each[5],each[7])
		return resp

	def ipolt(self,text='WRONGCOMMAND'):
		if len(self.db_idport.data)<1:
			self.db_idport.read_data()
		if self.db_idport.get_ipolt(text):
			idport = self.db_idport.print_data(text)
			resp = \
			"{}\
			\nID Port: {}".format(text, idport)
		else:
		    resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
		return resp

	def cekGolive(self,text='WRONGCOMMAND'):
		if len(self.db_golive.data)<1:
			self.db_golive.read_data()
		if self.db_golive.get_odp(text):
			result = self.db_golive.print_data(text)
			resp = "{}\nODP_NAME : {}\
					  \nLAT,LON : {}, {}\
					  \nDATEL : {}\
					  \nSTO   : {}".format(text,result[0],result[1],result[2],result[3],result[4])
		else:
		    resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
		return resp

	def cekQR(self,text='WRONGCOMMAND'):
		if len(self.db_qrodp.data)<1:
			self.db_qrodp.read_data()
		if self.db_qrodp.get_odp(text):
			result = self.db_qrodp.print_data(text)
			resp = "NAMA ODP : {}\
					\nQR CODE ODP : {}".format(result[0],result[2])
		else:
		    resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
		return resp

	def cekJadwal(self, text='WRONGCOMMAND'):
		text = int(text)
		if len(self.db_jadwal.data)<1:
			self.db_jadwal.read_data()
		hasil = (self.db_jadwal.print_data(text))

		indexPagi = [i for i, x in enumerate(hasil) if x == 'P']
		indexSiang = [i for i, x in enumerate(hasil) if x == 'S']
		indexLibur = [i for i, x in enumerate(hasil) if x == 'L']
		indexCuti = [i for i, x in enumerate(hasil) if x == 'C']
		indexPiket = [i for i, x in enumerate(hasil) if x == 'PP']

		jadwalPagi = []
		jadwalSiang = []
		jadwalLibur = []
		jadwalCuti = []
		jadwalPiket = []

		for i in indexPagi:
			jadwalPagi.append(hasil[i-1])
		for i in indexPiket:
			jadwalPiket.append(hasil[i-1])
		for i in indexSiang:
			jadwalSiang.append(hasil[i-1])
		for i in indexLibur:
			jadwalLibur.append(hasil[i-1])
		for i in indexCuti:
			jadwalCuti.append(hasil[i-1])
		
		respPagi = "Masuk Pagi\n"+"------------------------------"+"\n"
		if len(jadwalPagi) != 0:
			for i in range(len(jadwalPagi)):
				respPagi += jadwalPagi[i]+"\n"
		else:
			respPagi += "-"

		respPiket = "Piket Pagi\n"+"------------------------------"+"\n"
		if len(jadwalPiket) != 0:
			for i in range(len(jadwalPiket)):
				respPiket += jadwalPiket[i]+"\n"
		else:
			respPagi += "-"

		respSiang = "Masuk Siang\n"+"------------------------------"+"\n"
		if len(jadwalSiang) != 0:
			for i in range(len(jadwalSiang)):
				respSiang += jadwalSiang[i]+"\n"
		else:
			respSiang += "-"

		respLibur = "Libur\n"+"------------------------------"+"\n"
		if len(jadwalLibur) != 0:
			for i in range(len(jadwalLibur)):
				respLibur += jadwalLibur[i]+"\n"
		else:
			respLibur += "-"

		respCuti = "Cuti\n"+"------------------------------"+"\n"
		if len(jadwalCuti) != 0:
			for i in range(len(jadwalCuti)):
				respCuti += jadwalCuti[i]+"\n"
		else:
			respCuti += "-"

		month = datetime.datetime.now().month
		year = datetime.datetime.now().year
		get_day = str(year)+"-"+str(month)+"-"+str(text)
		datem = datetime.datetime.strptime(get_day, "%Y-%m-%d")
		date = datetime.datetime.strftime(datem,"%A")
		if date == 'Monday':
			hari = 'Senin'
		elif date == 'Tuesday':
			hari = 'Selasa'
		elif date == 'Wednesday':
			hari = 'Rabu'
		elif date == 'Thursday':
			hari = 'Kamis'
		elif date == 'Friday':
			hari = 'Jumat'
		elif date == 'Saturday':
			hari = 'Sabtu'
		else:
			hari = 'Minggu'

		respHari = hari + datetime.datetime.strftime(datem,", %d %B %Y")+"\n"

		resp = \
        		"{}\
        		\n{}\
				\n{}\
				\n{}\
				\n{}\
				\n{}".format(respHari,respPagi,respPiket,respSiang,respLibur,respCuti)
		return resp

	def fotoodp(self,text,chat_id):
		nama_odp = text.replace('/','-')
		if sys.version[0] == '3':
			list_foto = os.listdir('D:\\mycode\\daman\\app\\static\\img')
		else:
			list_foto = os.listdir('D:\\daman\\app\\static\\img')
		res_foto =  [i for i in list_foto if str(nama_odp)+'-' in i or str(nama_odp)+'.' in i]
		return res_foto
		
	def handle_misvalue(self):
		resp = "Data tidak ditemukan. Perintah yang anda masukkan mungkin salah atau ODP belum R2C."
		return resp