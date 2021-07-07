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
# import string
# import inspect
from pprint import pprint

class process_bot():

	def __init__(self):
		client = MongoClient()
		self.db = client.daman
		self.db_dataodp = Dataodp()
		self.db_dataservice = Dataservice()
		self.db_excelreport = Excelreport()
		self.db_datalabel = Datalabel()
		self.code = self.db_excelreport.get_odp()
		self.label = self.db_datalabel.get_label()
		# self.db_dataodpokupansi = Dataodpokupansi()
		self.db_dataunsc = Dataunsc()
		self.db_idport = IDPort()
		self.db_odpuim = OdpUim()
		self.db_odplap = OdpLap()
		self.db_golive = Golive()
		self.db_qrodp = QrOdp()
		self.db_jadwal = Absen()
		# self.ipolt_code = self.db_idport.get_ipolt()

	def cari_label(self,text):
	    daftar_label = self.label
	    return process.extract(text,daftar_label,limit=30)

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
			# ket = (dblite.get_items_ket(text)))
			# ket = re.sub('IDLE', '-', ket)
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
				# resp = \
				# text+"\
				# \nKAP"+emoji+kap+"\
				# \nUSED"+emoji+used+"\
				# \nAVAI"+emoji+avai+"\
				# \nPORT OLT"+emoji+port_olt+"\
				# \nOLT"+emoji+olt+"\
				# \nOCC"+emoji+occ+"%\
				# \nTGL R2C"+emoji+tanggal_r2c+"\
				# \nMITRA"+emoji+mitra+"\
				# \nSTATUS SIIS"+emoji+status_siis+"\
				# \nLok"+emoji+lat+","+longi+"\
				# \nTgl Update"+emoji+tgl
			
			# send_location(chat, lat, longi)
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

		month = datetime.now().month
		year = datetime.now().year
		get_day = str(year)+"-"+str(month)+"-"+str(text)
		datem = datetime.strptime(get_day, "%Y-%m-%d")

		respHari = datetime.strftime(datem,"%A, %d %B %Y")+"\n"

		resp = \
        		"{}\
        		\n{}\
				\n{}\
				\n{}\
				\n{}\
				\n{}".format(respHari,respPagi,respPiket,respSiang,respLibur,respCuti)
		return resp

	# def odpuimlist(self,text='WRONGCOMMAND'):
	# 	try:
	# 		if 'PAR' in text[4:7]:
	# 			text += '|'+text.replace('PAR','PGN')
	# 		elif 'PGN' in text[4:7]:
	# 			text += '|'+text.replace('PGN','PAR')
	# 		elif 'ULN' in text[4:7]:
	# 			text += '|'+text.replace('ULN','ULI')
	# 		elif 'ULI' in text[4:7]:
	# 			text += '|'+text.replace('ULI','ULN')
	# 		elif 'KYI' in text[4:7]:
	# 			text += '|'+text.replace('KYI','KYG')
	# 		elif 'KYG' in text[4:7]:
	# 			text += '|'+text.replace('KYG','KYI')
	# 		elif 'LDU' in text[4:7]:
	# 			text += '|'+text.replace('LDU','LUL')
	# 		elif 'LUL' in text[4:7]:
	# 			text += '|'+text.replace('LUL','LDU')
	# 		source = self.db_dataservice.get_odpuimlist(text)
	# 		resp = "{} (Update FTP: {})\nID ODP|PORT|SERVICE NAME\n".format(text, source[0][4])

	# 		res_data = []
	# 		for each in source:
	# 			# print (each)
	# 			regex1 = 'PANEL.*'
	# 			id_odp = each[0]
	# 			port_odp = re.findall(regex1, each[1])[0]
	# 			service_name = each[2]
	         
	            
	# 			res_data.append([id_odp, port_odp, service_name.replace('_','-')])
	# 		res_data.sort(key=lambda x:x[1])
	# 		for each in res_data:
	# 			resp += "{}|{}|{}\n".format(each[0],each[1],each[2])
	# 		return resp
	# 	except Exception as e:
	# 		print(e)
	# 		return 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'

	# def odplaplist(self,text='WRONGCOMMAND'):
	# 	odp = self.db_dataodp.get_data_by_namaodp(text)
	# 	if odp:
	# 		resp = "{} (TGL SURVEY: {})\n LABEL ODP: {}\nPORT|LABEL PORT|STATUS|NO. LAYANAN|LABEL DC\n".format(text, odp['TGAL_SURVEY'], odp['LABEL'])	
	# 		for each in odp['PORT']:
	# 			resp += "{}|{}|{}|{}|{}\n".format(each['NO_PORT'],each['LABEL_PORT'],each['STATUS'],each['NO_LAYANAN'],each['LABEL_DROPCORE'])
	# 	else:
	# 		return 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
	# 	return resp

	# def portodplap(self,text='WRONGCOMMAND'):
	# 	odp = self.db_dataodp.get_data_by_namaodp(text)
	# 	if odp:
	# 		resp = "{} (LABEL ODP: {}) \n".format(text,odp['LABEL'])	
	# 		for each in odp['PORT']:
	# 			resp += "{}|{}\n".format(each['NO_PORT'],each['LABEL_PORT'])
	# 	else:
	# 		return 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
	# 	return resp

	# def layananuim(self,text='WRONGCOMMAND'):
	# 	if 'PAR' in text[4:7]:
	# 		text = '|'+text.replace('PAR','PGN')
	# 	elif 'PGN' in text[4:7]:
	# 		text = '|'+text.replace('PGN','PAR')
	# 	elif 'ULN' in text[4:7]:
	# 		text = '|'+text.replace('ULN','ULI')
	# 	elif 'ULI' in text[4:7]:
	# 		text = '|'+text.replace('ULI','ULN')
	# 	elif 'KYI' in text[4:7]:
	# 		text = '|'+text.replace('KYI','KYG')
	# 	elif 'KYG' in text[4:7]:
	# 		text = '|'+text.replace('KYG','KYI')
	# 	elif 'LDU' in text[4:7]:
	# 		text = '|'+text.replace('LDU','LUL')
	# 	elif 'LUL' in text[4:7]:
	# 		text = '|'+text.replace('LUL','LDU')
	# 	source = self.db_dataservice.get_layananuim(text)
	# 	if source:
	# 		resp = "{} (Update: {})\n".format(text.upper(), source[0][7])
	# 		res_data = []
	# 		for each in source:
	# 		    resp += "===\n{}\n{}\n{}\n{}\nSP-PORT--:{}\nCPE-SN---:{}\n{}\n".format(each[0].replace('_','-'),each[1].replace('_','-'),each[2].replace('_','-'),
	#         each[3].replace('_','-'),each[4].replace('_','-'),each[5].replace('_','-'),each[6].replace('_','-'))
	# 	else:
	# 		resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
	# 	return resp

	# def layananlap(self,text='WRONGCOMMAND'):
	# 	odp = self.db_dataodp.get_data_by_layanan(text)
	# 	if odp:
	# 		resp = "{} (TGL SURVEY: {})\nPORT|LABEL PORT|STATUS|NO. LAYANAN|LABEL DC\n".format(odp['NAMAODP'], odp['TGAL_SURVEY'])	
	# 		for each in odp['PORT']:
	# 			resp += "{}|{}|{}|{}|{}\n".format(each['NO_PORT'],each['LABEL_PORT'],each['STATUS'],each['NO_LAYANAN'],each['LABEL_DROPCORE'])
	# 	else:
	# 		resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
	# 	return resp

	# def cekfeasibility(self,text):
		
	# 	latplg,lonplg = text.split(',')
	# 	odp = self.db_dataodpokupansi.get_all()
	# 	resp = 'ODP|OCCU UIM|OCCU LAP|SURVAI\n'
	# 	result = []
	# 	for each in odp:
	# 		latodp = each['LATITUDE']
	# 		lonodp = each['LONGITUDE']
	# 		jarakx = self.check_radius(latplg,lonplg,latodp,lonodp)
			
	# 		try:
	# 			if jarakx >= 0 and jarakx < 0.25:
	# 				nama_odp = each['ODP_NAME']
	# 				occu_uim = str(each['OCCU'])
	# 				try:
	# 					occu_lap =str(self.db_dataodp.get_data_by_namaodp(nama_odp)['OCCU'])
	# 				except:
	# 					occu_lap = '-'
	# 				try:
	# 					tgl_lap =str(self.db_dataodp.get_data_by_namaodp(nama_odp)['TGAL_SURVEY'])
	# 				except:
	# 					tgl_lap = '-'
	# 				# result+= '{}|{}|{}|{}\n'.format(nama_odp,occu_uim,occu_lap,tgl_lap)
	# 				toresult = [nama_odp,occu_uim,occu_lap,tgl_lap]
					
	# 				result.append(toresult)
	# 			else:
	# 				print("ini")
	# 		except:
	# 			pass
	# 	result = sorted(result, key=itemgetter(3),reverse=True)
	# 	resp+='\n'.join(['|'.join(x) for x in result])
	# 	return resp

	# def cekunsc(self,text):
	# 	# print("ini")
	# 	odp = self.db_excelreport.get_data(text)
	# 	if odp:
	# 		latodp = odp['LAT'] 
	# 		lonodp = odp['LON'] 
	# 	else:
	# 		latodp = 0
	# 		lonodp = 0
	# 	koor,unsc,ket = self.db_dataunsc.get_all()
	# 	result = 'SC|LOKER|PROGRESS UN|KET\n'
	# 	pos=-1
	# 	for each in koor:
	# 		pos+=1
	# 		try:
	# 			latunsc,lonunsc = each.split(',')
	# 			jarakx = self.check_radius(latunsc,lonunsc,latodp,lonodp)
	# 			if jarakx >= 0 and jarakx < 0.4:
	# 				loker = ''
	# 				progressun = ''
	# 				if unsc[pos]:
	# 					data = self.db_dataunsc.get_sc_sdi(str(unsc[pos]))					
	# 					if data:
	# 						loker = data['loker']
	# 						progressun = data['progressun']

	# 				result+= '{}|{}|{}|{}\n'.format(str(unsc[pos]),loker,progressun,ket[pos])
	# 		except Exception as e:
	# 			# print(type(unsc))
	# 			# print(unsc[pos])
	# 			pass
	# 	return result
		# return '-\n'.join([str(x) for x in jarak if x < 0.5 and x >= 0 ])
		# return sum(x < 0.5 and x >= 0 for x in jarak)

	# def check_string(self,check_point_lat,check_point_long,center_point_lat,center_point_long):
	# 	try:
	# 		float(center_point_lat)
	# 		print('true')
	# 	except:
	# 		print('false')

	# def check_radius(self,check_point_lat,check_point_long,center_point_lat,center_point_long):
		
	# 	lat1 = ""
	# 	lon1 = ""
	# 	for x in list(check_point_lat):
	# 		lat1+= x
	# 	for y in list(check_point_long):
	# 		lon1+= y
	# 	lat1 = float(lat1)
	# 	lon1 = float(lon1)
	# 	# lat2 = float(check_point_lat)
	# 	# lon2 = float(check_point_long)
	# 	# try:
	# 	# lat1 = float(center_point_lat)
	# 	# lon1 = float(center_point_long)
	# 	# a = str(center_point_long)

	# 	# b = str(center_point_lat)
	# 	# print(type(center_point_lat))
	# 	# lat1 = float(b)
	# 	# lat1 = center_point_lat
	# 	# lon1 = center_point_long
	# 	# print(type(check_point_lat))
	# 	lat2 = float(check_point_lat)
	# 	lon2 = float(check_point_long)
	# 	# print("lat 1 {}").format(type(lat1))
	# 	# print("lon 1 {}").format(type(lon1))
	# 	# print("lat 2 {}").format(type(lat2))
	# 	# print("lon 2 {}").format(type(lon2))
	# 	jarak = self.haversine(lon1, lat1, lon2, lat2)
	# 	# print(jarak)
	# 	return jarak

		# except (ValueError, TypeError):
		# 	print("ini")
		# 	return 0.0
		# print(lat1)
		# print(type(lat1))
		
		

	# def haversine(self, lon1, lat1, lon2, lat2):
	# 	"""
	# 	pr=
	# 	Calculate the great circle distance between two points 
	# 	on the earth (specified in decimal degrees)
	# 	"""
	# 	# convert decimal degrees to radians 
	# 	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# 	# haversine formula 
	# 	dlon = lon2 - lon1 
	# 	dlat = lat2 - lat1 
	# 	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	# 	c = 2 * asin(sqrt(a)) 
	# 	r = 6371 # Radius of earth in kilometers. Use 3956 for miles
	# 	return c * r

	# def updateunsc(self):
		# return self.db_dataunsc.update_data()

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

	# def search_sto_odc_odp(self,list_length = 0, list_odp = ''):
	#     regex = r".{0,3}\-.{0,3}\-"
	#     string_list_odp = ''.join(list_odp)
	#     result = re.search(regex, string_list_odp)
	#     desc = ''
	#     if (result):
	#         desc = "STO"
	#         regex = r".{0,3}\-.{0,3}\-.{0,3}"
	#         result = re.search(regex, string_list_odp)
	#         if (result):
	#             desc = "ODC"
	#             regex = r".{0,3}\-.{0,3}\-.{0,3}\/[0-9]{0,3}"
	#             result = re.search(regex, string_list_odp)
	#             if (result):
	#                 desc = "ODP"
	#     resp = 'Terdapat {} item {}\n'.format(list_length, desc)+'\n'.join(list_odp)
	#     return resp

	# def cari(self, query):
	# 	text = query
	# 	list_odp = []
	# 	code = self.db_dataodpokupansi.get_odp()
	# 	for each in code:
	# 	    if each.startswith(text):
	# 	      list_odp.append(each)
	# 	list_odp.sort()
	# 	list_length = len(list_odp)
	# 	# Hitung jumlah karakter pesan
	# 	char_length = 0
	# 	for x in list_odp:
	# 	    for y in x:
	# 	        char_length+= 1
	# 	# Jika hasil pencarian terlalu banyak dengan jumlah karakter lebih dari 4096, maka cari subcodenya
	# 	if char_length > 4096:
	# 	    subcode = []
	# 	    regex = r"/.*"
	# 	    for each in code:
	# 	        subcode.append(re.sub(regex, "", each ))
	# 	    set_subcode = set(subcode)
	# 	    list_subcode = list(set_subcode)
	# 	    list_odp = []
	# 	    for each in list_subcode:
	# 	        if each.startswith(''.join(text)):
	# 	          list_odp.append(each)
	# 	    list_odp.sort()
	# 	    list_length = len(list_odp)
	# 	    char_length = 0
	# 	    for x in list_odp:
	# 	        for y in x:
	# 	            char_length+= 1
	# 	    # Jika hasil pencarian masih terlalu banyak
	# 	    if char_length >4096:
	# 	        resp = "Hasil pencarian terlalu besar, tidak dapat ditampilkan. Silahkan tambahkan query. /help"
	# 	    # Jika tidak, berikan respon sesuai hasil pencarian
	# 	    else:
	# 	        resp = self.search_sto_odc_odp(list_length, list_odp)
	# 	    return resp
		        
	# 	# Jika hasil pencarian tidak lebih dari 4096, maka tampilkan hasil pencarian
	# 	else:                        
	# 		if list_length ==0:
	# 		    resp = self.handle_misvalue()
	# 		else:
	# 		    resp = self.search_sto_odc_odp(list_length, list_odp)
	# 		return resp



	def add_request(self, odp, pelanggan, nama):
		self.coll = self.db.datarequest
		# data = {'_id': ObjectId()}
		forupdate = {
			'ODP': odp,
			'PELANGGAN': pelanggan,

			'INPUT_BY': nama,
			'last_modified': datetime.utcnow()+timedelta(hours=8),
			}
		return self.coll.update_one({ '_id':  ObjectId() },
					   		 {'$set': forupdate},
					   		 upsert=True)

	def add_user(self,nik,nama,loker,id_telegram,username,nama_telegram):
		self.coll = self.db.userbot
		forupdate = {
			'NIK': nik,
			'NAMA': nama,
			'LOKER': loker,
			'ID_TELEGRAM': id_telegram,
			'USERNAME': username,
			'NAMA_TELEGRAM': nama_telegram,
			'STATUS': 'NONAKTIF',
			'last_modified': datetime.utcnow()+timedelta(hours=8),
			}
		return self.coll.update_one({ '_id':  ObjectId() },
					   		 {'$set': forupdate},
					   		 upsert=True)

	def get_user_by_id(self,id_telegram):
		self.coll = self.db.userbot
		return self.coll.find_one({'ID_TELEGRAM':id_telegram})

	def ceksid(self,text,chat_id):
		odp = self.db_dataodp.get_data_by_layanan(text)
		if odp is None:
			res_foto = "Data tidak ada"
		else:
			nama = odp['NAMAODP']
			nama_odp = nama.replace('/','-')
			# print(nama)
			# print(nama_odp)

			if sys.version[0] == '3':
				list_foto = os.listdir('E:\\daman1\\app\\static\\img')
			else:
				list_foto = os.listdir('D:\\daman\\app\\static\\img')

			res_foto =  [i for i in list_foto if str(nama_odp)+'-' in i or str(nama_odp)+'.' in i]
			# resp = "NAMA ODP : {}".format(nama)	
		return res_foto
		# return resp

	def ceksidodp(self,text,chat_id):
		odp = self.db_dataodp.get_data_by_layanan(text)
		if odp is None:
			resp ="Data tidak ada"
		else:
			nama = odp['NAMAODP']
			nama_odp = nama.replace('/','-')

			print(nama)
			print(nama_odp)

			# bb = odp['PORT']
			# result = ''
			
			# for each in bb:
			# 	n = re.findall(text,each['NO_LAYANAN'])
			# 	print(n)
			# 	if n:
			# 		result+= each['NO_PORT']
			# print(result)
			# print(".......................")

			if sys.version[0] == '3':
				list_foto = os.listdir('E:\\daman1\\app\\static\\img')
			else:
				list_foto = os.listdir('D:\\daman\\app\\static\\img')

			res_foto =  [i for i in list_foto if str(nama_odp)+'-' in i or str(nama_odp)+'.' in i]
			bb = odp['PORT']
			resp = ''
			for each in bb:
				n = re.findall(text,each['NO_LAYANAN'])
				# print(n)
				if n:
					resp = "NAMA ODP : {}\nKoordinat : {}\nPORT|LABEL PORT|STATUS|NO. LAYANAN|LABEL DC\n".format(nama,odp['LONGLAT'])
					# result+= each['NO_PORT']
					resp += "{}|{}|{}|{}|{}\n".format(each['NO_PORT'],each['LABEL_PORT'],each['STATUS'],each['NO_LAYANAN'],each['LABEL_DROPCORE'])
					hasil = "ada"
					break
				else:
					hasil = "tidak ada"
			if hasil == "tidak ada":
				return "Data tidak ada"
		return resp
		# if odp:
		# 	resp = "NAMA ODP : {}\nKoordinat : {}\nPORT|LABEL PORT|STATUS|NO. LAYANAN|LABEL DC\n".format(nama,odp['LONGLAT'])
		# 	for each in odp['PORT']:
			# for each in n:
				# resp += "{}|{}|{}|{}|{}\n".format(each['NO_PORT'],each['LABEL_PORT'],each['STATUS'],each['NO_LAYANAN'],each['LABEL_DROPCORE'])
		# resp = "NAMA ODP : {}\nKoordinat : {}".format(nama,odp['LONGLAT'])
		# else:
		# 	resp = "Data tidak ada"
		# print('=======')
		# print(resp)
		# res_foto = res.replace('[]','')
		# tgal = odp['TGAL_SURVEY']
		# for each in odp['PORT']:
		# # 	nolayanan = each['NO_LAYANAN']
		# if odp:
		# 	resp = "{} (TGL SURVEY: {})\nPORT|LABEL PORT|STATUS|NO. LAYANAN|LABEL DC\n".format(odp['NAMAODP'], odp['TGAL_SURVEY'])	
		# 	for each in odp['PORT']:
		# 		resp += "{}|{}|{}|{}|{}\n".format(each['NO_PORT'],each['LABEL_PORT'],each['STATUS'],each['NO_LAYANAN'],each['LABEL_DROPCORE'])
		# else:
		# 	resp = 'Data tidak ditemukan. Perintah yang anda masukkan mungkin salah.'
		# return resp,res_foto
		
		# return res_foto
		# return resp