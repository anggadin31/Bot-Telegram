import sys
import os
from pymongo import MongoClient
from datetime import datetime
import re
from models import *
from pprint import pprint

class process_bot():

	def __init__(self):
		client = MongoClient()
		self.dbnames = client.list_database_names()
		self.db = client.daman
		self.db_excelreport = Excelreport()
		self.code = self.db_excelreport.get_odp()
		self.db_idport = IDPort()
		self.db_odpuim = OdpUim()
		self.code_odpuim= self.db_odpuim.get_odp()
		self.code_inetuim= self.db_odpuim.get_inet()
		self.db_odplap = OdpLap()
		self.code_odplap= self.db_odplap.get_odp()
		self.code_inetlap= self.db_odplap.get_inet()
		self.db_golive = Golive()
		self.code_golive = self.db_golive.get_odp()
		self.code_idport = self.db_idport.get_ipslotport()
		self.db_qrodp = QrOdp()
		self.code_qrodp = self.db_qrodp.get_odp()
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
			\nLok-: {},{}".format(text, kap, used, avai, port_olt, hostname, occ, tanggal_r2c, mitra, status_siis, lat, longi)
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
		if text.isnumeric():
			text = int(text)
			if text in self.code_inetuim:
				data = self.db_odpuim.get_data_inet(text)
				resp = "{}\nSTO|GPON|SLOT|PORT|NO. INET|ODP UIM|VALIDITAS\n".format(text)	
				for each in data:
					sto = each[0]
					gpon = each[1]
					slot = each[2]
					port = each[3]
					inet = each[4]
					odp = each[5]
					valid = each[6]
					resp += "{}|{}|{}|{}|{}|{}|{}\n".format(sto,gpon,slot,port,inet,
					odp,valid)
			else:
				resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'

		else:
			if text in self.code_odpuim:
				data = self.db_odpuim.get_data_odp(text)
				resp = "{}\nSTO|GPON|SLOT|PORT|NO. INET|ODP UIM|VALIDITAS\n".format(text)	
				for each in data:
					sto = each[0]
					gpon = each[1]
					slot = each[2]
					port = each[3]
					inet = each[4]
					odp = each[5]
					valid = each[6]
					resp += "{}|{}|{}|{}|{}|{}|{}\n".format(sto,gpon,slot,port,inet,
					odp,valid)
			else:
				resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
		return resp

	def cekOdpLap(self,text='WRONGCOMMAND'):
		if text.isnumeric():
			text = int(text)
			if text in self.code_inetuim:
				data = self.db_odpuim.get_data_inet(text)
				resp = "{}\nSTO|GPON|SLOT|PORT|NO. INET|ODP UIM|VALIDITAS\n".format(text)	
				for each in data:
					sto = each[0]
					gpon = each[1]
					slot = each[2]
					port = each[3]
					inet = each[4]
					odp = each[5]
					valid = each[6]
					resp += "{}|{}|{}|{}|{}|{}|{}\n".format(sto,gpon,slot,port,inet,
					odp,valid)
			else:
				resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'

		else:
			if text in self.code_odpuim:
				data = self.db_odpuim.get_data_odp(text)
				resp = "{}\nSTO|GPON|SLOT|PORT|NO. INET|ODP UIM|VALIDITAS\n".format(text)	
				for each in data:
					sto = each[0]
					gpon = each[1]
					slot = each[2]
					port = each[3]
					inet = each[4]
					odp = each[5]
					valid = each[6]
					resp += "{}|{}|{}|{}|{}|{}|{}\n".format(sto,gpon,slot,port,inet,
					odp,valid)
			else:
				resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
		return resp

	def ipolt(self,text='WRONGCOMMAND'):
		if text in self.code_idport:
			data = self.db_idport.get_data(text)
			idport = data['ID PORT']
			resp = "{}\nID PORT : {}".format(text,idport)
		else:
		    resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
		return resp

	def cekGolive(self,text='WRONGCOMMAND'):
		if text in self.code_golive:
			data = self.db_golive.get_data(text)
			odp_name = data['ODP_NAME']
			lat = data['LAT']
			lon = data['LON']
			datel = data['DATEL']
			sto = data['STO']
			resp = "{}\nODP_NAME : {}\
					  \nLAT,LON : {}, {}\
					  \nDATEL : {}\
					  \nSTO   : {}".format(text,odp_name,lat,lon,datel,sto)
		else:
		    resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
		return resp

	def cekQR(self,text='WRONGCOMMAND'):
		if text in self.code_qrodp:
			data = self.db_qrodp.get_data(text)
			odp_name = data['ODP_NAME']
			qr = data['QR CODE']
			resp = "ODP_NAME : {}\
					\nQR CODE ODP : {}".format(odp_name,qr)
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

	def updateOdpUim(self):
		self.db_odpuim.get_started()
		return "Database sudah diupdate"

	def updateOdpLap(self):
		self.db_odplap.get_started()
		return "Database sudah diupdate"	
	
	def updateGolive(self):
		self.db_golive.get_started()
		return "Database sudah diupdate"
	
	def updateExcelReport(self):
		self.db_excelreport.get_started()
		return "Database sudah diupdate"

	def updateIdPort(self):
		self.db_idport.get_started()
		return "Database sudah diupdate"

	def updateQrCode(self):
		self.db_qrodp.get_started()
		return "Database sudah diupdate"
		
	def handle_misvalue(self):
		resp = "Data tidak ditemukan. Perintah yang anda masukkan mungkin salah atau ODP belum R2C."
		return resp