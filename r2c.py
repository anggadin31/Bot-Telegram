import sys
reload(sys)   
sys.setdefaultencoding('utf-8')
import time
import telepot
# import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import per_chat_id, create_open, pave_event_space,include_callback_query_chat_id 
from models import *
import logging
from datetime import datetime, timedelta

# from dbhelperodpr2c import dbhelperodp_mongo
# from mongodb_dataodp import mongodbhelper_dataodp
# from mongodb_dataservice import mongodbhelper_dataservice
from processbot import process_bot
import unicodedata
# db_dataodp = mongodbhelper_dataodp()
# db_dataservice = mongodbhelper_dataservice()

# db_dataodpokupansi = Dataodpokupansi()
db_dataodp = Dataodp()
processbot = process_bot()
db_r2cnoss = r2cnoss()
logging.basicConfig(filename="botr2c.log", level=logging.INFO)

class ODPKalsel(telepot.helper.ChatHandler):
    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                    #InlineKeyboardButton(text='Cek R2C', callback_data='r2c'),
                    #InlineKeyboardButton(text='Request R2C', callback_data='request'),
                    ],
                    [
                    InlineKeyboardButton(text='CEK GOLIVE', callback_data='golive'),
                    ],
                    [
                    InlineKeyboardButton(text='CEK IP OLT', callback_data='odpuim'),
                    #InlineKeyboardButton(text='List ODP', callback_data='cari'),
                    # InlineKeyboardButton(text='Lihat Data', callback_data='lihat_data'),
                    ],
                    [
                    InlineKeyboardButton(text='CEK PEL UIM', callback_data='odpuimlist'),
                    InlineKeyboardButton(text='CEK PEL LAP', callback_data='odplaplist'),
                    ],
                    [                  
                    InlineKeyboardButton(text='CEK LABEL QR ODP', callback_data='cekqr'),
                    ],
                    [
                    # InlineKeyboardButton(text='Layanan UIM', callback_data='layananuim'),
                    # InlineKeyboardButton(text='Layanan LAP', callback_data='layananlap'),
                    ],
                    [
                    InlineKeyboardButton(text='SERVICE NAME 1054', callback_data='service'),
                    #InlineKeyboardButton(text='Feasibility', callback_data='feasibility'),
                    ],
                    [
                    InlineKeyboardButton(text='HELP', callback_data='help'),
                    InlineKeyboardButton(text='Foto ODP', callback_data='fotoodp'),
                    ],
                                        [
                    InlineKeyboardButton(text='ID SERVICE PORT', callback_data='ipolt'),
                    ],
                    [
                    InlineKeyboardButton(text='CEK JADWAL DAMAN', callback_data='jadwal'),
                    ],
                    ]
                )

    keyboard_daftar = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [InlineKeyboardButton(text='Daftar', callback_data='daftar'),
                    ],
                    [],
                    [],
                    [],
                    ]
                )

    def __init__(self, *args, **kwargs):
        super(ODPKalsel, self).__init__(*args, **kwargs)
        self._count = 0
        self._state = ''
        self._state_input = ''
        self.data = {}
        self.data_user = {}
        self._editor = ''
        self._status_member = '' 
        self._id_member = ''

    def _cancel_last(self):
        if self._editor:
            self._editor.deleteMessage()
            self._editor = None
            self._edit_msg_ident = None

    def _cancel_markup(self):
        if self._editor:
            self._editor.editMessageReplyMarkup(reply_markup=None)
            self._editor = None
            self._edit_msg_ident = None

    def split_msg(self,text):
        split = -(-len(text)//2)
        return text[:split],text[split:]

    def _send_message(self,text,markup=None):
        sent = self.sender.sendMessage(text,reply_markup=markup)
        self._editor = telepot.helper.Editor(self.bot, sent)

    def on_chat_message(self, msg):
        self._count += 1
        # self.sender.sendMessage(self._count)
        content_type, chat_type, chat_id = telepot.glance(msg)
        # if self._id_member == '':
        member = processbot.get_user_by_id(chat_id)
        if member:
            self._id_member = member['_id']
            self._status_member = member['STATUS']
            # print (self._id_member,self._status_member)
        if self._status_member == 'NONAKTIF':
            self._send_message('Akun anda belum aktif, hubungi @Calling_Man')

            # self._cancel_last()
            self.close()
        elif self._status_member == 'AKTIF':
            text_input = msg['text'].upper()
            # self.bot.sendMessage(198205822,'@{},{},{}'.format(msg['chat'].get('username'),self._state,text_input))
            logging.info('{}::@{},{},{}'.format(datetime.utcnow()+timedelta(hours=8),msg['chat'].get('username'),self._state,text_input))
            # print(msg['text'].upper())
            # if msg['text'] == 'Daftar':
            if text_input.startswith("/LBL"):
                # if handle_lesscommand(text, "/LBL"):
                    # processbot.handle_misvalue(chat)
                # else:
                    # Jika format command benar
                try:
                    text = text_input.split(' ')[1]
                    resp = processbot.cari_label(text)
                    if resp[0][1] == resp[1][1] and resp[1][1] and resp[2][1]:
                        skor = resp[0][1]
                        msg = ''
                        for each in resp:
                            if each[1] == skor:
                                msg += '{} - {}\n'.format(each[0],each[1])
                                skor = each[1]
                            else:
                                msg += '{} - {}\n'.format(each[0],each[1])
                                skor = each[1]
                                break
                        self._send_message(msg)
                    else:
                        self._send_message('{} - {}\n{} - {}\n{} - {}'.format(resp[0][0],resp[0][1],resp[1][0],resp[1][1],resp[2][0],resp[2][1]))
                except:
                    self._send_message('Perintah yang anda masukkan salah.\nContoh: /LBL T4T047H15R4F')
            elif self._state == 'r2c':
                data = db_dataodpokupansi.get_data(text_input)
                try:
                    occ_lap =str(db_dataodp.get_data_by_namaodp(text_input)['OCCU'])
                except:
                    occ_lap = '0'
                try:
                    tgl_lap =str(db_dataodp.get_data_by_namaodp(text_input)['TGAL_SURVEY'])
                except:
                    tgl_lap = '0'
                # print(data[0])
                res = len(data)
                if res > 0:
                    resp = '{}\nSudah R2C\nSTATUS: {}\nKAP: {}\nISI:{}\nAVAI: {}\nOCCU UIM: {}\nOCCU LAP: {}\nTGL SURVAI: {}\nLok: {},{}\nUpdate: {}\nUpdate Database: {}'.format(data[0]['ODP_NAME'],data[0]['STATUS'],\
                        data[0]['IS_TOTAL'],data[0]['ISI'],data[0]['AVAI'],data[0]['OCCU'],occ_lap,tgl_lap,\
                        data[0]['LATITUDE'],data[0]['LONGITUDE'],data[0]['UPDATE_DATE\n'],data[0]['TANGGAL'])
                else:
                    resp = processbot.handle_misvalue()
                self._send_message(resp,self.keyboard)
                # self.sender.sendLocation(data[0]['LATITUDE'],data[0]['LONGITUDE'])
                # self._cancel_last()
            elif self._state == 'r2cnoss':
                data = db_r2cnoss.get_odp(text_input)
                res = len(data)
                resp = ''
                if res > 0:
                    for each in data:
                        # if not each[2] or not each[3] or not each[37]:
                        #     resp = 'Sedang validasi abd.'
                        # else:
                        #     resp += 'TA--------------: {}\nPORT OLT---: {}\nNAMA ODP-: {}\nMITRA--------: {}\nGOLIVE COMPLETED: {}\n~~~~~~~~~\n'.format(each[2],each[3],each[29],each[31],each[37])
                        # resp += 'NAMA ODP-: {}\nMITRA--------: {}'.format(each[29],each[31])
                        if each[11] is None:
                            # r2c = 'Belum R2C'
                            resp += 'NAMA ODP: {}\nMITRA: {}\nALAMAT: {}\nKOORDINAT: {}\nPROJECT: {}\nTANGGAL ORDER: {}\nKETERANGAN: {}\n'.format(each[3],each[0],each[2],each[5],each[6],each[9],'Belum R2C')
                        elif each[11] == 'OK':
                            # r2c = 'Sudah R2C'
                            resp += 'NAMA ODP: {}\nMITRA: {}\nALAMAT: {}\nKOORDINAT: {}\nPROJECT: {}\nTANGGAL ORDER: {}\nKETERANGAN: {}\n'.format(each[3],each[0],each[2],each[5],each[6],each[9],'Sudah R2C')
                        elif each[7] == 'STTF 4 2019':
                            resp += 'NAMA ODP: {}\nMITRA: {}\nALAMAT: {}\nKOORDINAT: {}\nPROJECT: {}\nTANGGAL ORDER: {}\nKETERANGAN: {}\nABD: {}\nESTIMASI: {}'.format(each[3],each[0],each[2],each[5],each[6],each[9],'Belum R2C',each[12],each[13])
                        elif each[7] == 'PT2 STTF 3 2019 SATUI' and each[11] == '#N/A':
                            resp += 'NAMA ODP: {}\nMITRA: {}\nALAMAT: {}\nKOORDINAT: {}\nPROJECT: {}\nTANGGAL ORDER: {}\nKETERANGAN: {}\nABD: {}\nESTIMASI: {}\n'.format(each[3],each[0],each[2],each[5],each[6],each[9],'Belum R2C',each[12],each[13])
                        elif each[7] == 'PT2 STTF 3 2019 PLE' and each[11] == '#N/A':
                            resp += 'NAMA ODP: {}\nMITRA: {}\nALAMAT: {}\nKOORDINAT: {}\nPROJECT: {}\nTANGGAL ORDER: {}\nKETERANGAN: {}\nABD: {}\nESTIMASI: {}\n'.format(each[3],each[0],each[2],each[5],each[6],each[9],'Belum R2C',each[12],each[13])
                        else:
                            # r2c = 'Belum R2C /', each[12]
                            resp += 'NAMA ODP: {}\nMITRA: {}\nALAMAT: {}\nKOORDINAT: {}\nPROJECT: {}\nTANGGAL ORDER: {}\nKETERANGAN: {}{}\nABD: {}\nESTIMASI: {}\n'.format(each[3],each[0],each[2],each[5],each[6],each[9],'Belum R2C / ',each[14],each[11],each[12])
                else:
                    resp = 'Data yang anda cari tidak ditemukan atau belum setor abd.'
                    # resp = processbot.handle_misvalue()
                self._send_message(resp,self.keyboard)
                # self._cancel_last()
            elif self._state == 'odpuim':
                resp = processbot.odpuim(text_input)
                self._send_message(resp,self.keyboard)
                # self._cancel_last()
            elif self._state == 'ipolt':
                resp = processbot.ipolt(text_input)
                self._send_message(resp,self.keyboard)
            elif self._state == 'service':
                resp = processbot.potong(text_input)
                self._send_message(resp,self.keyboard)
            elif self._state == 'cari':
                resp = processbot.cari(text_input)
                self._send_message(resp,self.keyboard)
                # self._cancel_last()
            elif self._state == 'golive':
                resp = processbot.cekGolive(text_input)
                self._send_message(resp,self.keyboard)
            elif self._state == 'cekqr':
                resp = processbot.cekQR(text_input)
                self._send_message(resp,self.keyboard)
            elif self._state == 'odpuimlist':
                resp = processbot.cekOdpUim(text_input)
                self._send_message(resp,self.keyboard)
                # self._cancel_last()
            elif self._state == 'odplaplist':
                resp = processbot.cekOdpLap(text_input)
                self._send_message(resp,self.keyboard)
                # self._cancel_last()
            elif self._state == 'jadwal':
                resp = processbot.cekJadwal(text_input)
                self._send_message(resp,self.keyboard)
                # self._cancel_last()
            elif self._state == 'portodplap':
                resp = processbot.portodplap(text_input)
                resp1 = resp.splitlines()
                self._send_message(resp,self.keyboard)
            elif self._state == 'layananuim':
                resp = processbot.layananuim(text_input)
                self._send_message(resp,self.keyboard)
                # self._cancel_last()
            elif self._state == 'layananlap':
                resp = processbot.layananlap(text_input)
                self._send_message(resp,self.keyboard)
                # self._cancel_last()
            elif self._state == 'unsc':
                resp = processbot.cekunsc(text_input)
                self._send_message(resp,self.keyboard)

            elif self._state == 'feasibility':
                resp = processbot.cekfeasibility(text_input)
                # print()
                self._send_message(resp,self.keyboard)
                # print(text_input)
                # text_input = float(u'{}'.format(text_input))
                # a = type(text_input)
 

                # print(type(a))
                # resp1,resp2 = self.split_msg(resp)
                # self._send_message(resp1)
                # self._send_message(resp,self.keyboard)
            elif self._state == 'request':
                if self._state_input =='request':
                    self._cancel_last()
                    self.data['odp'] = text_input
                    self._send_message('Masukkan jumlah potensi pelanggan:\nContoh: 2')
                    self._state_input = 'odp'
                elif self._state_input == 'odp':
                    self.data['pelanggan']= text_input
                    self._cancel_last()
                    if self.data['odp'] and self.data['pelanggan']:
                        odp = self.data['odp']
                        pelanggan = self.data['pelanggan']
                        id_user = processbot.get_user_by_id(chat_id)['_id']
                        nama = processbot.get_user_by_id(chat_id)['NAMA']
                        add_request = processbot.add_request(odp,pelanggan,nama)
                        self._send_message('Data tersimpan.',self.keyboard)
                        self._state = ''
                        self._state_input = 'pelanggan'
            
            elif self._state == 'fotoodp':
                res_foto = processbot.fotoodp(text_input,chat_id)
                if res_foto:
                    for each in res_foto:
                        if sys.version[0] == '3':
                            img = open('D:\\mycode\\daman\\app\\static\\img\\{}'.format(each), 'rb')
                        else:
                            img = open('D:\\daman\\app\\static\\img\\{}'.format(each), 'rb')
                        self.sender.sendPhoto(img)
                        img.close()
                    self._send_message(':D',self.keyboard)
                else:
                    self._send_message('Tidak terdapat foto untuk ODP tersebut atau pesan yang anda masukkan salah.',self.keyboard)
                self._state = ''
                # sent = self.sender.sendPhoto(foto)
                # self._editor = telepot.helper.Editor(self.bot, sent)
                # self._send_message(resp,self.keyboard)
                # self._cancel_last()

            elif self._state == 'ceksid':
                res_foto = processbot.ceksid(text_input,chat_id)
                resp = processbot.ceksidodp(text_input,chat_id)
                # self._send_message(resp,self.keyboard)
                # print('-----')
                # res_foto = res_foto.replace('[]','')
                # print(res_foto)
                # print('......')
                # print(resp)
                if res_foto == 'Data tidak ada':
                    self._send_message('Tidak terdapat foto untuk No SID tersebut atau pesan yang anda masukkan salah.',self.keyboard)
                else:
                    for each in res_foto:
                        if sys.version[0] == '3':
                            img = open('E:\\daman1\\app\\static\\img\\{}'.format(each), 'rb')
                        else:
                            img = open('D:\\daman\\app\\static\\img\\{}'.format(each), 'rb')
                        self.sender.sendPhoto(img)
                        img.close()
                    self._send_message(resp,self.keyboard)
            
                    

            # elif self._state == 'daftar':
            #     # print (msg)
            #     if self._state_input == 'nik':                
            #         nik = db.get_all_nik()
            #         if not db.contains(msg['text'], nik):
            #             self.data_user['nik'] = msg['text']
            #             self._editor.deleteMessage()
            #             # self.sender.sendMessage('NIK anda '+msg['text'])
            #             sent = self.sender.sendMessage(
            #             '\
            #             NIK------------:{}\nPassword---:{}\nNama--------:{}\nLoker---------:{}'.format(self.data_user.get('nik'),
            #             self.data_user.get('password'),self.data_user.get('nama'),self.data_user.get('loker')),
            #             reply_markup=self.reg_keyboard
            #             )
            #             self._editor = telepot.helper.Editor(self.bot, sent)

            #     elif self._state_input == 'password':
            #         self.data_user['password'] = msg['text']
            #         self._editor.deleteMessage()
            #         # self.sender.sendMessage('Password anda '+msg['text'])
            #         sent = self.sender.sendMessage(
            #         '\
            #         NIK------------:{}\nPassword---:{}\nNama--------:{}\nLoker---------:{}'.format(self.data_user.get('nik'),
            #         self.data_user.get('password'),self.data_user.get('nama'),self.data_user.get('loker')),
            #         reply_markup=self.reg_keyboard
            #         )
            #         self._editor = telepot.helper.Editor(self.bot, sent)
             
            else:
                self._send_message('Halo kaka...',self.keyboard)

                # self._cancel_last()
                self.close()

        elif self._state == 'daftar':
                if self._state_input == 'daftar': 
                    self._cancel_last()
                    self.data_user['nik'] = msg['text']
                    # if db.get_user('nik',self.data_user['nik']):
                        # self._send_message('NIK anda sudah terdaftar.',self.bind_keyboard)
                    # else:
                    self._send_message('Masukkan Nama anda:')
                    self._state_input = 'nik'
                elif self._state_input == 'nik':
                    self._cancel_last()
                    self.data_user['nama'] = msg['text']
                    self._send_message('Masukkan Loker anda:')
                    self._state_input = 'nama'
                elif self._state_input == 'nama':
                    self._cancel_last()
                    self.data_user['loker'] = msg['text']
                    if self.data_user['nik'] and self.data_user['nama'] and self.data_user['loker']:
                        # id_user = 'u{}'.format(314)
                        # if not db.get_user('nik',self.data_user['nik']):
                        nik = self.data_user['nik']
                        nama = self.data_user['nama']
                        loker = self.data_user['loker']
                        username = msg['chat'].get('username')
                        nama_telegram = msg['chat'].get('first_name')
                        add_user = processbot.add_user(nik,nama,loker,chat_id,username,nama_telegram)
                        self._send_message('Data anda tersimpan.')
                        self._state = ''
                        self._state_input = 'loker'

                        # else:
                        #     print(7)
                        #     sent = self.sender.sendMessage('Data nik anda telah . {}'.format(insert_user))

        else:
            self._send_message('Akun anda belum terdaftar. Klik daftar.',self.keyboard_daftar)

            # self._cancel_last()
            self.close()
    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        # if query_data == 'daftar':
        #     self._state = 'daftar'
        #     self.sender.sendMessage(
        #         'Klik',
        #         reply_markup=self.reg_keyboard
        #     )
        # print(self._state)
        if query_data == 'r2c':
            self._state = 'r2c'
            # self._cancel_last()
            self._send_message('Masukkan nama ODP: \nContoh: ODP-BJM-FAK/005')
        elif query_data == 'request':
            self._state = 'request'
            self._state_input = 'request'
            self._send_message('*Fitur ini masih dalam tahap percobaan.\nMasukkan nama ODP: \nContoh: ODP-BJM-FAK/005')
        elif query_data == 'r2cnoss':
            self._state = 'r2cnoss'
            self._state_input = 'r2cnoss'
            self._send_message('Masukkan nama ODP: \nContoh: ODP-ULI-FK/036')
        elif query_data == 'odpuim':
            self._state = 'odpuim'
            # self._cancel_last()
            self._send_message('Masukkan nama ODP: \nContoh: ODP-BJM-FAK/005')
        elif query_data == 'ipolt':
            self._state = 'ipolt'
            # self._cancel_last()
            self._send_message('Masukkan nama IP OLT Slot-Port: \nContoh: 172.20.166.75 2-7')
        elif query_data == 'service':
            self._state = 'service'
            # self._cancel_last()
            self._send_message('Masukkan Text: \nContoh: The TT is created for CRM order ID: SC501260618_3-318428317401 OSM ID: 163574376. Service ID is 50565311_162214304058_INTERNET,50565311_162214304058_IPTV')
        elif query_data == 'cari':
            self._state = 'cari'
            # self._cancel_last()
            self._send_message('Masukkan query: \nContoh: ODP-BJM-FAK/')
        elif query_data == 'odpuimlist':
            self._state = 'odpuimlist'
            # self._cancel_last()
            self._send_message('Masukkan nama ODP atau No. Inet: \nContoh: ODP-KPL-FAA/004 atau 162223901881')
        
        elif query_data == 'odplaplist':
            self._state = 'odplaplist'
            # self._cancel_last()
            self._send_message('Masukkan nama ODP atau No. Inet: \nContoh: ODP-KPL-FAA/004 atau 162223901881')
        elif query_data == 'golive':
            self._state = 'golive'
            # self._cancel_last()
            self._send_message('Masukkan nama ODP: \nContoh: ODP-BLC-FW/097')
        elif query_data == 'cekqr':
            self._state = 'cekqr'
            # self._cancel_last()
            self._send_message('Masukkan nama ODP atau QR CODE ODP: \nContoh: ODP-BJM-FAJ/161 atau T4T08G4OEE73')
        elif query_data == 'jadwal':
            self._state = 'jadwal'
            # self._cancel_last()
            self._send_message('Masukkan Tanggal: \nContoh: 20')
        elif query_data == 'portodplap':
            self._state = 'portodplap'
            # self._cancel_last()
            self._send_message('Masukkan nama ODP: \nContoh: ODP-BJM-FAK/005')
        elif query_data == 'layananuim':
            self._state = 'layananuim'
            # self._cancel_last()
            self._send_message('Masukkan nomor layanan: \nContoh: 161202208981')
        elif query_data == 'layananlap':
            self._state = 'layananlap'
            # self._cancel_last()
            self._send_message('Masukkan nomor layanan: \nContoh: 161202208981')
        elif query_data == 'unsc':
            self._state = 'unsc'
            self._send_message('Masukkan nama ODP: \nContoh: ODP-BJM-FAK/005')
        elif query_data == 'feasibility':
            self._state = 'feasibility'
            self._send_message('Masukkan koordinat: \nContoh: -3.337965,114.582247')
        elif query_data == 'ceksid':
            self._state = 'ceksid'
            # self._cancel_last()
            self._send_message('Masukkan nomor layanan: \nContoh: 161202208981')
        # elif query_data == 'updateunsc':
            # resp = processbot.updateunsc()
            # self._send_message(resp,self.keyboard)
        elif query_data == 'fotoodp':
            self._state = 'fotoodp'
            # self._cancel_last()
            self._send_message('Masukkan nama ODP: \nContoh: ODP-BJM-FAK/005')
        elif query_data == 'lihat_data':
            data = processbot.get_user_by_id(from_id)
            sent = self.sender.sendMessage('\
                NIK------:{}\nNama---:{}\nStatus--:{}'.format(data.get('NIK'),
                data.get('NAMA'),data.get('STATUS')))
        elif query_data == 'daftar':
            self._cancel_last()
            # if not db.get_user_telegram(from_id):
            self._send_message('Masukkan NIK/ID anda:')
            self._state = 'daftar'
            self._state_input = 'daftar'
            # else:  
                # self._state = None
                # id_user = db.get_user_telegram(from_id)
                # nik = db.get_user('id_user',id_user[0][1])[0][1]
                # self._send_message('Akun Telegram anda telah terhubung dengan NIK: {}'.format(nik),self.unbind_keyboard)
        elif query_data == 'help':
            self._send_message('\
                Cek R2C: Melihat okupansi ODP berdasarkan UIM dan survey lapangan\n\
Request R2C: -\n\
R2C NOSS 2018: -\n\
ODP UIM: Detail informasi ODP berdasarkan UIM\n\
List ODP: Melakukan pencarian ODP\n\
Isi ODP UIM: Daftar pelanggan berdasarkan UIM\n\
Isi ODP LAP: Daftar pelanggan berdasarkan Lapangan\n\
Layanan UIM: Informasi layanan berdasarkan UIM\n\
Layanan LAP: Posisi nomor layanan berdasarkan survey lapangan\n\
Foto ODP: Foto ODP hasil survai tim validasi data\n\
                ',self.keyboard)
       

# TOKEN = sys.argv[1]  # get token from command-line

if sys.version[0] == '3':
    #bot developmentdamanbot
    TOKEN = '694699130:AAG4S3Tb9uxxxPHjbl5fP-QiNsjOehOhieM'
else:
    #bot r2c on
    TOKEN = '1700736876:AAFbW1nhZcgKlKm3vtisZrIIpQMf4OqsrZA'
bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
    pave_event_space())(
        per_chat_id(), create_open, ODPKalsel, timeout=100
    ),
])


MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
