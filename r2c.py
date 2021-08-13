import sys
import os
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import per_chat_id, create_open, pave_event_space,include_callback_query_chat_id 
from models import *
from processbot import process_bot

processbot = process_bot()

class ODPKalsel(telepot.helper.ChatHandler):
    keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                    InlineKeyboardButton(text='CEK GOLIVE', callback_data='golive'),
                    ],
                    [
                    InlineKeyboardButton(text='CEK IP OLT', callback_data='odpuim'),
                    ],
                    [
                    InlineKeyboardButton(text='CEK PEL UIM', callback_data='odpuimlist'),
                    InlineKeyboardButton(text='CEK PEL LAP', callback_data='odplaplist'),
                    ],
                    [                  
                    InlineKeyboardButton(text='CEK LABEL QR ODP', callback_data='cekqr'),
                    ],
                    [
                    InlineKeyboardButton(text='SERVICE NAME 1054', callback_data='service'),
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
                    [
                    InlineKeyboardButton(text='UPDATE DATABASE', callback_data='update'),
                    ],
                    ]
                )
    keyboardUpdate = InlineKeyboardMarkup(
                    inline_keyboard=[
                    [
                    InlineKeyboardButton(text='DATABASE GOLIVE', callback_data='database_golive'),
                    ],
                    [
                    InlineKeyboardButton(text='DATABASE IP OLT', callback_data='database_odpuim'),
                    ],
                    [
                    InlineKeyboardButton(text='DATABASE PEL UIM', callback_data='database_odpuimlist'),
                    InlineKeyboardButton(text='DATABASE PEL LAP', callback_data='database_odplaplist'),
                    ],
                    [                  
                    InlineKeyboardButton(text='DATABASE LABEL QR ODP', callback_data='database_cekqr'),
                    ],
                    [
                    InlineKeyboardButton(text='DATABASE SERVICE PORT', callback_data='database_ipolt'),
                    ],
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
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'document':
            file_id = msg['document']['file_id']
        else:
            text_input = msg['text'].upper()
        if self._state == '':
            self._send_message('Halo kaka...',self.keyboard)
            self.close()
        elif self._state == 'odpuim':
            resp = processbot.odpuim(text_input)
            self._send_message(resp,self.keyboard)
        elif self._state == 'ipolt':
            resp = processbot.ipolt(text_input)
            self._send_message(resp,self.keyboard)
        elif self._state == 'service':
            resp = processbot.potong(text_input)
            self._send_message(resp,self.keyboard)
        elif self._state == 'golive':
            resp = processbot.cekGolive(text_input)
            self._send_message(resp,self.keyboard)
        elif self._state == 'cekqr':
            resp = processbot.cekQR(text_input)
            self._send_message(resp,self.keyboard)
        elif self._state == 'odpuimlist':
            resp = processbot.cekOdpUim(text_input)
            self._send_message(resp,self.keyboard)
        elif self._state == 'odplaplist':
            resp = processbot.cekOdpLap(text_input)
            self._send_message(resp,self.keyboard)
        elif self._state == 'jadwal':
            resp = processbot.cekJadwal(text_input)
            self._send_message(resp,self.keyboard)
        elif self._state == 'database_odpuimlist':
            os.remove("D:\daman\DALAPA_VALIDASI_UIM.xlsx")
            file_name = "DALAPA_VALIDASI_UIM.xlsx" # or look up from msg
            bot.download_file(file_id, os.path.join('D:\daman', file_name))
            self._send_message('Database sedang diupdate mohon tunggu sebentar')
            resp = processbot.updateOdpUim()
            self._send_message(resp,self.keyboard)
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif self._state == 'database_odplaplist':
            os.remove("D:\daman\DALAPA_VALIDASI_LAPANGAN.xlsx")
            file_name = "DALAPA_VALIDASI_LAPANGAN.xlsx" # or look up from msg
            bot.download_file(file_id, os.path.join('D:\daman', file_name))
            self._send_message('Database sedang diupdate mohon tunggu sebentar')
            resp = processbot.updateOdpLap()
            self._send_message(resp,self.keyboard)
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif self._state == 'database_golive':
            os.remove("D:\daman\CEK GOLIVE.xlsx")
            file_name = "CEK GOLIVE.xlsx" # or look up from msg
            bot.download_file(file_id, os.path.join('D:\daman', file_name))
            self._send_message('Database sedang diupdate mohon tunggu sebentar')
            resp = processbot.updateGolive()
            self._send_message(resp,self.keyboard)
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif self._state == 'database_odpuim':
            os.remove("D:\daman\EXCEL REPORT_ODP.xlsx")
            file_name = "EXCEL REPORT_ODP.xlsx" # or look up from msg
            bot.download_file(file_id, os.path.join('D:\daman', file_name))
            self._send_message('Database sedang diupdate mohon tunggu sebentar')
            resp = processbot.updateExcelReport()
            self._send_message(resp,self.keyboard)
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif self._state == 'database_ipolt':
            os.remove("D:\daman\ID Port OLT Banjarmasin (new update).xlsx")
            file_name = "ID Port OLT Banjarmasin (new update).xlsx" # or look up from msg
            bot.download_file(file_id, os.path.join('D:\daman', file_name))
            self._send_message('Database sedang diupdate mohon tunggu sebentar')
            resp = processbot.updateIdPort()
            self._send_message(resp,self.keyboard)
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif self._state == 'database_cekqr':
            os.remove("D:\daman\DATA_QR_ODP.xlsx")
            file_name = "DATA_QR_ODP.xlsx" # or look up from msg
            bot.download_file(file_id, os.path.join('D:\daman', file_name))
            self._send_message('Database sedang diupdate mohon tunggu sebentar')
            resp = processbot.updateQrCode()
            self._send_message(resp,self.keyboard)
            os.execl(sys.executable, sys.executable, *sys.argv)
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

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        if query_data == 'odpuim':
            self._state = 'odpuim'
            self._send_message('Masukkan nama ODP: \nContoh: ODP-BJM-FAK/005')
        elif query_data == 'ipolt':
            self._state = 'ipolt'
            self._send_message('Masukkan nama IP OLT Slot-Port: \nContoh: 172.20.166.75 2-7')
        elif query_data == 'service':
            self._state = 'service'
            self._send_message('Masukkan Text: \nContoh: The TT is created for CRM order ID: SC501260618_3-318428317401 OSM ID: 163574376. Service ID is 50565311_162214304058_INTERNET,50565311_162214304058_IPTV')
        elif query_data == 'odpuimlist':
            self._state = 'odpuimlist'
            self._send_message('Masukkan nama ODP atau No. Inet: \nContoh: ODP-KPL-FAA/004 atau 162223901881')
        elif query_data == 'odplaplist':
            self._state = 'odplaplist'
            self._send_message('Masukkan nama ODP atau No. Inet: \nContoh: ODP-KPL-FAA/004 atau 162223901881')
        elif query_data == 'golive':
            self._state = 'golive'
            self._send_message('Masukkan nama ODP: \nContoh: ODP-BLC-FW/097')
        elif query_data == 'cekqr':
            self._state = 'cekqr'
            self._send_message('Masukkan nama ODP atau QR CODE ODP: \nContoh: ODP-BJM-FAJ/161 atau T4T08G4OEE73')
        elif query_data == 'jadwal':
            self._state = 'jadwal'
            self._send_message('Masukkan Tanggal: \nContoh: 20')
        elif query_data == 'update':
            self._state = 'update'
            self._send_message('Pilih database yang ingin diupdate',self.keyboardUpdate)
        elif query_data == 'database_odpuimlist':
            self._state = 'database_odpuimlist'
            self._send_message('Kirim file dengan nama DALAPA_VALIDASI_UIM dan pastikan format sudah sesuai') 
        elif query_data == 'database_odplaplist':
            self._state = 'database_odplaplist'
            self._send_message('Kirim file dengan nama DALAPA_VALIDASI_LAPANGAN dan pastikan format sudah sesuai') 
        elif query_data == 'database_golive':
            self._state = 'database_golive'
            self._send_message('Kirim file dengan nama CEK GOLIVE dan pastikan format sudah sesuai')
        elif query_data == 'database_odpuim':
            self._state = 'database_odpuim'
            self._send_message('Kirim file dengan nama EXCEL REPORT_ODP dan pastikan format sudah sesuai')
        elif query_data == 'database_ipolt':
            self._state = 'database_ipolt'
            self._send_message('Kirim file dengan nama ID Port OLT Banjarmasin (new update) dan pastikan format sudah sesuai')
        elif query_data == 'database_cekqr':
            self._state = 'database_cekqr'
            self._send_message('Kirim file dengan nama DATA_QR_ODP dan pastikan format sudah sesuai')
        elif query_data == 'fotoodp':
            self._state = 'fotoodp'
            self._send_message('Masukkan nama ODP: \nContoh: ODP-BJM-FAK/005')
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

TOKEN = '1838698997:AAFpae5AxmpNMuI0la3GFLokT4DOF50UmZU'
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
