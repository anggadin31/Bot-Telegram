# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:43:08 2017

@author: Hafiz
"""

import json
import requests
import time
import urllib
import re
from dbhelperodp import DBHelperODP
from dbhelperodp2 import DBHelperODP as DBHelperODP2
from dbhelperodp_valdat import DBHelperODP as DBHelperODP_valdat
from mongodb_dataodp import mongodbhelper_dataodp
from mongodb_dataservice import mongodbhelper_dataservice
from processbot import process_bot
import plotly
import plotly.graph_objs as go
from selenium import webdriver
import requests
from PIL import Image
db = DBHelperODP()
db2 = DBHelperODP2()
db_valdat = DBHelperODP_valdat()
db_dataodp = mongodbhelper_dataodp()
db_dataservice = mongodbhelper_dataservice()
processbot = process_bot()
import os 

# TOKEN = "387896555:AAFa_Q1XxMfVZHMr4W3Pd7ullhMUnViW2-8"
# TOKEN = "376444631:AAGAX2HaMBr4hBKlrW38yFyx0uFulmnaP9w"
TOKEN = "695625569:AAETfauv6v52r1jbJLmS_lwGX1AmLZ7xyUI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
# username = "@odp_report_kalsel3_bot".upper()
# username = "@odp_report_kalsel_bot".upper()
username = "@odpkalselbot".upper()
last_update = '07-Agustus-2018'
cwd = os.getcwd()
chart = 'file:///{}/temp-plot.html'.format(cwd)
warna = '#cc1414'
evenwarna = '#e5e5e5'

wavy = u'\U00003030'
altermark = u'\U0000303d'
circle = u'\U00002b55'
star = u'\U00002b50'
tower = u'\U0001f5fc'
emoji = altermark+tower

def crop(image_path, coords, saved_location):
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)

### Fungsi untuk mengambil respon dari URL yang kita akses
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

### Karena respon dari telegram memiliki format json, sehingga perlu diload supaya memudakan pembacaan di python 
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

### Fungsi untuk mendapatkan update yang masuk pada bot telegram
def get_updates(offset = None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

### Fungsi untuk mengambil id dari update terakhir
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def handle_help(chat):
    resp = "Masukkan query-ODP dengan format = [ODP]-[STO]-[ODC]/[NAMA ODP]\n\
Misal: ODP-BJM-FAS/032\n\
\n/data query-ODP (melihat data ODP format gambar)\
\nMisal: \
\n /data ODP-BJM-FAS/032\
\n\n/occuuim query-ODP (melihat data ODP format teks)\
\nMisal: \
\n /occuuim ODP-BJM-FAS/032\
\n\n/totalODP ODP-STO-ODC (melihat total ODP)\
\nMisal: /totalODP ODP-BJM-FAS\
\n\n/totalODC ODC-STO (melihat total ODC)\
\nMisal: /totalODC ODC-BBR\
\n\n/totalGCL GCL-STO (melihat total ODC di GCL)\
\nMisal: /totalGCL GCL-BBR\
\n\n/cari query (melihat daftar ODP)\
\nMisal: \
\n /cari ODP-BJM\
\n /cari ODP-BBR-FAV\
\n\n/kodeODP (melihat daftar kode ODP)\
\n/kodeSTO (melihat daftar kode STO)\
\n/kodeODC (melihat daftar kode ODC)\
\n/lis query-ODP (melihat daftar service pada ODP tsb)\
\n/tel query-nomor telepon (melihat data pelanggan)\
\n/odpuimlist query-ODP ()\
\n/odpuimplg query-ODP ()\
\n/foto query-ODP (untuk melihat foto ODP dari validasi lapangan)\
\nUntuk bantuan hubungi: @hafiz1401"
    send_message(resp, chat)

### Fungsi untuk mengirim pesan saat ada kesalahan command dari pengguna
def handle_misvalue(chat, notfound = ''):
    send_message("{}Perintah yang anda masukkan mungkin salah. Ketik /help untuk melihat petunjuk.".format(notfound), chat)

### Fungsi untuk mengembalika nilai true jika command tidak memiliki query tambahan
def handle_lesscommand(text = '', command=''):
    if text == command or text == command+username:
        return True
    
### Fungsi untuk menangani tanggapan pesan yang masuk ke telegram      
def handle_updates(updates):
    ## Untuk setiap update yang baru masuk
    for update in updates["result"]:
        try:
            # text menyimpan hasil kiriman pengguna telegram dalam huruf besar
            text = update["message"]["text"].upper()
            # chat menyimpan id yang akan digunakan untuk tujuan mengirim pesan
            chat = update["message"]["chat"]["id"]
            uname = update["message"]["chat"]["username"]
            if "first_name" in update["message"]["from"].keys():
                fname = update["message"]["from"]["first_name"]
            else:
                fname = ''
                
            if "last_name" in update["message"]["from"].keys():
                lname = update["message"]["from"]["last_name"]
            else:
                lname = ''
            log = fname +'|'+lname+'|'+str(chat)+'|@'+uname+': '+text
            send_message(log, '198205822')
            
            # code menyimpan seluruh nama ODP
            code = db.get_ODP()
            code2 = db_valdat.get_ODP()
            # Jika input berupa command untuk melihat data 
            if text.startswith("/OCCUUIM") or text.startswith("/OCCUUIM"+username):
                if handle_lesscommand(text, "/OCCUUIM"):
                    handle_misvalue(chat)
                else:
                    try:
                        query = text.split(' ')[1]
                        text = query
                    except:
                        text = 'WRONGCOMMAND'
                    if text in code:
                        lat = ''.join(db.get_items_lat(text))
                        longi = ''.join(db.get_items_lon(text))
                        kap = ''.join((db.get_items_kap(text)))
                        used = ''.join((db.get_items_used(text)))
                        avai = ''.join((db.get_items_avai(text)))
                        port_olt = ''.join((db.get_items_port_olt(text)))
                        olt = ''.join((db.get_items_olt(text)))
                        occ = ''.join((db.get_items_occ(text)))
                        tanggal_r2c = ''.join((db.get_items_tanggal_r2c(text)))
                        bulan_r2c = ''.join((db.get_items_bulan_r2c(text)))
                        mitra = ''.join((db.get_items_mitra(text)))
                        # ket = ''.join((db.get_items_ket(text)))
                        # ket = re.sub('IDLE', '-', ket)
                        status_siis = ''.join((db.get_items_status_siis(text)))
                        tgl = ''.join(db.get_items_tanggal(text))
                        resp = \
                        "{}\
                        \nKAP----: {}\
                        \nUSED--: {}\
                        \nAVAI---: {}\
                        \nPORT OLT--: {}\
                        \nOLT----: {}\
                        \nOCC----: {}%\
                        \nTGL R2C--: {}\
                        \nMITRA---: {}\
                        \nSTATUS SIIS-: {}\
                        \nLok-: {},{}\
                        \nTgl Update: {}".format(text, kap, used, avai, port_olt, olt, occ, tanggal_r2c, mitra, status_siis, lat, longi, tgl)
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
                        send_message(resp, chat)
                        send_location(chat, lat, longi)
                    else:
                        handle_misvalue(chat, "Data tidak ditemukan. ")

            elif text.startswith("/DATA") or text.startswith("/DATA"+username):
                if handle_lesscommand(text, "/DATA"):
                    handle_misvalue(chat)
                else:
                    try:
                        query = text.split(' ')[1]
                    except:
                        query = 'WRONGCOMMAND'
                    text = query
                    if text in code:
                        lat = ''.join(db.get_items_lat(text))
                        longi = ''.join(db.get_items_lon(text))
                        try:
                            kap = str(db_dataodp.get_items_kap(text)[0])
                        except:
                            kap = '-'
                        try:
                            used = ''.join((db_dataodp.get_items_used(text)[0]))
                        except:
                            used = '-'
                        try:
                            avai = int(kap) - int(used)
                        except:
                            avai = '-'
                            
                        port_olt = ''.join((db.get_items_port_olt(text)))
                        olt = ''.join((db.get_items_olt(text)))
                        occ_uim = ''.join((db.get_items_occ(text)))
                        tanggal_r2c = ''.join((db.get_items_tanggal_r2c(text)))
                        bulan_r2c = ''.join((db.get_items_bulan_r2c(text)))
                        mitra = ''.join((db.get_items_mitra(text)))
                        status_siis = ''.join((db.get_items_status_siis(text)))
                        try:
                            tgalsurvey = ''.join(db_dataodp.get_items_tgalsurvey(text)[0])
                        except:
                            tgalsurvey = '-'
                        try:
                            occ_lap = str(db_dataodp.get_items_occ(text)[0])
                        except:
                            occ_lap = '0'
                        # if int(occ) > 80:
                        #     warna = '#cc1414'
                        # elif int(occ) > 40 and int(occ) < 81:
                        #     warna = '#dddd00'
                        # elif int(occ) > 0 and int(occ) < 41:
                        #     warna = '#31b20e'
                        # elif int(occ) == 0:
                        #     warna = '#000000'
                        # print status_siis
                        # print occ_lap
                        warna = '#cc1414'
                        warna_lap = '#cc1414'
                        try:
                            if 'RED' in status_siis:
                                warna = '#cc1414'
                            elif 'YELLOW' in status_siis:
                                warna = '#dddd00'
                            elif 'GREEN' in status_siis:
                                warna = '#31b20e'
                            elif 'BLACK' in status_siis:
                                warna = '#000000'
                        except:
                            warna = '#cc1414'

                        try:
                            if float(occ_lap) > 80:
                                warna_lap = '#cc1414'
                            elif float(occ_lap) > 40 and float(occ_lap) < 81:
                                warna_lap = '#dddd00'
                            elif float(occ_lap) > 0 and float(occ_lap) < 41:
                                warna_lap = '#31b20e'
                            elif float(occ_lap) == 0:
                                warna_lap = '#000000'
                        except:
                            warna_lap = '#cc1414'
                        trace = go.Table(
                            type = 'table',
                            columnorder = [1,2],
                            columnwidth = [400,600],
                            header=dict(
                                values=['<b>NAMA ODP</b>','<b>'+text+'</b>'],
                                # line = dict(color='#25abd1'),
                                fill = dict(color='#25abd1'),
                                align = ['left','left'],
                                font = dict(color='white',size = 20),
                                height = 35
                                ),
                            cells=dict(
                                values=[["KAP","USED","AVAI","PORT OLT","OLT","OCCU UIM","OCCU LAP","TGL R2C","MITRA","LOKASI","SURVEY VALIDASI"],[kap,used,avai,port_olt,olt,'<b>'+occ_uim+"%"+'<b>','<b>'+occ_lap+'<b>',tanggal_r2c,mitra,lat+", "+longi,tgalsurvey]],
                                # line = dict(color=warna),
                                fill = dict(color=[[evenwarna,'white',evenwarna,'white',evenwarna,'white',evenwarna,'white',evenwarna,'white',evenwarna],[evenwarna,'white',evenwarna,'white',evenwarna,warna,warna_lap,'white',evenwarna,'white',evenwarna]]),
                                align = ['left','left'],
                                font = dict(color=[['black'],['black','black','black','black','black','white','white','black','black','black','black']], size=20),
                                height = 35
                                )
                            )
                        layout = dict(width=800, height = 800)


                        data = [trace]
                        fig = dict(data=data, layout=layout)
                        plotly.offline.plot(fig, auto_open=False)


                        driver = webdriver.Firefox()
                        driver.set_window_size(900, 300)
                        driver.get(chart)
                        driver.save_screenshot('dataodp.png')
                        print "saved"
                        driver.close()
                        crop('dataodp.png', (90,110,725,555), 'res_dataodp.png')
                        img = open('res_dataodp.png', 'rb')
                        lin = URL + 'sendPhoto'
                        requests.post(lin, data={'chat_id': chat}, files= {'photo': img})
                        img.close()
                        send_location(chat, lat, longi)
                    else:
                        handle_misvalue(chat, "Data tidak ditemukan. ")
            elif text.startswith("/ODPUIMPLG") or text.startswith("/ODPUIMPLG"+username):
                if handle_lesscommand(text, "/ODPUIMPLG"):
                    handle_misvalue(chat)
                else:
                    query = text.split(' ')[1]
                    text = query
                    try:
                        source = db2.get_data(text)
                        resp = "{} (Update: {})\nSTP PORT|SERVICE NUMBER|SERVICE ADMINSTATE|\n".format(text.upper(), last_update)
                        res_data = []
                        pos = 0
                        for each in source:
                            print each
                            pos+=1
                            s_number = ''.join(each[1])
                            s_adminstate = ''.join(each[2])
                            print pos
                            regex1 = 'PANEL.*'
                            if re.findall(regex1, each[5]):
                                stp_port = ''.join(re.findall(regex1, each[5])[0])
                            elif re.findall(regex1, each[6]):
                                stp_port = ''.join(re.findall(regex1, each[6])[0])
                            elif re.findall(regex1, each[7]):
                                stp_port = ''.join(re.findall(regex1, each[7])[0])
                            elif re.findall(regex1, each[8]):
                                stp_port = ''.join(re.findall(regex1, each[8])[0])
                            else:
                                stp_port = '-'
                            regex2 = '(?:GPON.*|DSLAM.*|2.SKIRBS.*|MCL.*|MDU.*|MSAN.*|)'
                            if re.findall(regex2, each[6]):
                                sp_target = ''.join(re.findall(regex2, each[6])[0])
                            elif re.findall(regex2, each[7]):
                                sp_target = ''.join(re.findall(regex2, each[7])[0])
                            elif re.findall(regex2, each[8]):
                                sp_target = ''.join(re.findall(regex2, each[8])[0])
                            elif re.findall(regex2, each[9]):
                                sp_target = ''.join(re.findall(regex2, each[9])[0])
                            else:
                                sp_target = '-'
                            cpe_sn = ''.join(each[10])
                            if s_adminstate == "IN_SERVICE":
                                s_adminstate = "IN SERVICE"
                            # resp = "{}===================\nSERVICE NUMBER----: {}\
                            # \nSERVICE ADMINSTATE--: {}\
                            # \nSTP PORT---: {}\
                            # \nSP TARGET--: {}\
                            # \nCPE SN----: {}".format(pos,s_number, s_adminstate, stp_port, sp_target, cpe_sn)
                            # resp = "{}{}{}{}{}".format(s_number, s_adminstate, stp_port, sp_target, cpe_sn)
                            # print resp
                            # send_message(resp, chat)

                            res_data.append([stp_port, s_number, s_adminstate])
                        res_data.sort()
                        for each in res_data:
                            resp += "{}|{}|{}\n".format(each[0],each[1],each[2])
                        send_message(resp, chat)
                        
                    except Exception as e:
                        print e
                        handle_misvalue(chat, "Data tidak ditemukan. ")
            elif text.startswith("/ODPUIMLIST") or text.startswith("/ODPUIMLIST"+username):
                if handle_lesscommand(text, "/ODPUIMLIST"):
                    handle_misvalue(chat)
                else:
                    try:
                        query = text.split(' ')[1]
                        text = query
                    except:
                        text = 'WRONGCOMMAND'
                    try:
                        resp = processbot.odpuimlist(text)
                            
                        send_message(resp, chat)
                            
                    except Exception as e:
                        print e
                        handle_misvalue(chat, "Data tidak ditemukan. ")
            elif text.startswith("/TELUIM") or text.startswith("/TELUIM"+username):
                if handle_lesscommand(text, "/TELUIM"):
                    handle_misvalue(chat)
                else:
                    try:
                        query = text.split(' ')[1]
                        text = query
                    except:
                        handle_misvalue(chat, "")
                        continue
                    try:
                        source = db_dataservice.get_teluim(text)
                        resp = "{} (Update: {})\n".format(text.upper(), source[0][7])
                        # resp = "{} (Update: {})\nSTATE|STP_PORT|SP_TARGET|SP_PORT|CPE_SN|SERVICE_STATUS\n".format(text.upper(), last_update)
                        res_data = []
                        # for each in source:
                            
                        #     res_data.append([id_odp, port_odp, service_name.replace('_','-')])
                        # res_data.sort(key=lambda x:x[1])
                        for each in source:
                            resp += "===\n{}\n{}\n{}\n{}\nSP-PORT--:{}\nCPE-SN---:{}\n{}\n".format(each[0].replace('_','-'),each[1].replace('_','-'),each[2].replace('_','-'),
                                each[3].replace('_','-'),each[4].replace('_','-'),each[5].replace('_','-'),each[6].replace('_','-'))
                            # resp += "====\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(each[0].replace('_','-'),each[1].replace('_','-'),each[2].replace('_','-'),
                            #     each[3],each[4],each[5],each[6])
                            
                        send_message(resp, chat)
                            
                    except Exception as e:
                        print e
                        handle_misvalue(chat, "Data tidak ditemukan. ")
            
            elif text.startswith("/VALDAT") or text.startswith("/VALDAT"+username):
                if handle_lesscommand(text, "/VALDAT"):
                    handle_misvalue(chat)
                else:
                    query = text.split(' ')[1]
                    text = query
                    try:
                        source = db_valdat.get_data(text)
                        pos = 0
                        res_data = []
                        for each in source:
                            print each
                            tgl_validasi = ''.join(each[0])
                            namaodp = ''.join(each[1])
                            lokasi = ''.join(each[2]).encode('ascii','ignore')
                            label = ''.join(each[3])
                            port = ''.join(each[4])
                            label_port = ''.join(each[5])
                            no_layanan = ''.join(each[6]).replace('_','-')
                            try:
                                nolayanan = re.findall(r"-\d+",no_layanan)[0].replace('-','')
                            except:
                                nolayanan = None
                            print nolayanan
                            if nolayanan is None:
                                if re.findall(r"/",no_layanan):
                                    nolayanan = '-'
                                else:
                                    try:
                                        nolayanan = re.findall(r"\d+",no_layanan)[0].replace('-','')
                                    except:
                                        nolayanan = '-'
                            print nolayanan
                            try:
                                res_no = db2.get_customer(nolayanan)
                                res_no = res_no[len(res_no)-1]  
                            except:
                                res_no = ['-','-']
                            label_dc = ''.join(each[7])
                            res_data.append([tgl_validasi,namaodp,lokasi,label,port,label_port,no_layanan,label_dc,res_no[0],res_no[1]])
                        
                        # res_data.sort()
                        resp = "{}\nTGL VALIDASI|LOKASI|LABEL|PORT|LABEL PORT|NO. LAYANAN|LABEL DC|CUST.|ALAMAT\n".format(res_data[0][1])
                        send_message(resp, chat)                        
                        for each in res_data:
                            resp = "{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(each[0],each[2],each[3],each[4],each[5],each[6],each[7],each[8],each[9])
                            send_message(resp, chat)

                    except Exception as e:
                        print e
                        handle_misvalue(chat, "Data tidak ditemukan. ")
            elif text.startswith("/LIS") or text.startswith("/LIS"+username):
                if handle_lesscommand(text, "/LIS"):
                    handle_misvalue(chat)
                else:
                    try:
                        query = text.split(' ')[1]

                        text = query
                        # try:
                        source = db_dataodp.get_data(text)[0]
                             
                        dataPort = ["Data Port"]
                        telp = ["Telp"]
                        namaPelanggan = ["Nama Pelanggan"]
                        alamatPelanggan = ["Alamat Pelanggan"]
                        for each in range(int(source['KAP'])):
                            index = each+1
                            no = source['PORT_'+str(index)]['NO_LAYANAN']
                            no_layanan = no.replace('_','-')
                            try:
                                if 'IDLE' in no_layanan.upper() or 'TIDAK' in no_layanan.upper():
                                    nolayanan = None
                                else:
                                    nolayanan = re.findall(r"-\d+",no_layanan)[0].replace('-','')
                            except:
                                nolayanan = None
                            if nolayanan is None:
                                # if re.findall(r"/",no_layanan):
                                #     nolayanan = '-'
                                # else:
                                try:
                                    if 'IDLE' in no_layanan.upper() or 'TIDAK' in no_layanan.upper():
                                        nolayanan = None
                                    else:
                                        nolayanan = re.findall(r"\d+",no_layanan)[0].replace('-','')
                                except:
                                    nolayanan = '-'
                            # print no_layanan
                            try:
                                cust = db_dataservice.get_customer(nolayanan)[0]
                            except:
                                cust = ['-','-']
                            # print cust
                            dataPort.append(index)
                            telp.append(no)
                            namaPelanggan.append(cust[0])
                            alamatPelanggan.append(cust[1])
                        trace = go.Table(
                            type = 'table',
                            columnorder = [1,2,3,4],
                            columnwidth = [30,150,100,150],
                            header=dict(
                                values=['<b>NAMA ODP</b>','<b>'+text+'</b>'],
                                # line = dict(color='#25abd1'),
                                fill = dict(color='#25abd1'),
                                align = ['left','left'],
                                font = dict(color='white',size = 20),
                                height = 35
                                ),
                            cells=dict(
                                values=[dataPort,telp,namaPelanggan,alamatPelanggan],
                                # line = dict(color=warna),
                                fill = dict(color=[['black','white',evenwarna,'white',evenwarna,'white',evenwarna,'white',evenwarna],
                                    ['black','white',evenwarna,'white',evenwarna,'white',evenwarna,'white',evenwarna],
                                    ['black','white',evenwarna,'white',evenwarna,'white',evenwarna,'white',evenwarna],
                                    ['black','white',evenwarna,'white',evenwarna,'white',evenwarna,'white',evenwarna]]),
                                align = ['left','left','left','left'],
                                font = dict(color=[['white','black'],['white','black'],['white','black'],['white','black']], size=17),
                                height = 35
                                )
                            )
                        layout = dict(width=1280, height = 2000)


                        data = [trace]
                        fig = dict(data=data, layout=layout)
                        plotly.offline.plot(fig,auto_open=False)


                        driver = webdriver.Firefox()
                        driver.set_window_size(1980, 2000)
                        driver.get(chart)
                        driver.save_screenshot('lisodp.png')
                        print "saved"
                        driver.close()
                        crop('lisodp.png', (90,110,1200,1000), 'res_lisodp.png')
                        img = open('res_lisodp.png', 'rb')
                        lin = URL + 'sendPhoto'
                        requests.post(lin, data={'chat_id': chat}, files= {'photo': img})
                        img.close()
                        # except Exception as e:
                        #     print e
                        #     resp = "ODP belum divalidasi"
                        #     send_message(resp, chat)
                            # handle_misvalue(chat, "Data tidak ditemukan. ")
                    except Exception as e:
                            print e
                            handle_misvalue(chat, "Data tidak ditemukan. ")
            elif text.startswith("/TEL") or text.startswith("/TEL"+username):
                if handle_lesscommand(text, "/TEL"):
                    handle_misvalue(chat)
                else:
                    try:
                        query = text.split(' ')[1]
                        text = query
                    except:
                        text = 'WRONG'
                    try:    
                        # try:
                            
                        #     res_no = db2.get_customer(text)
                        #     res_no = res_no[len(res_no)-1] 
                        # except:
                        #     res_no = ['-','-']

                        # with open('blacklist_odp.txt', 'r') as f:
                        #     x = f.read()
                        #     blacklist_odp = ''.join(x).split('\n')
                        #     source = db_valdat.get_items_customer(text)
                        #     source = source[len(source)-1] 
                        #     res_data = []
                        #     res_data.append([source[0],source[1],source[2],res_no[0],res_no[1],source[3]])
                        #     print res_data
                           
                        #     trace = go.Table(
                        #         type = 'table',
                        #         columnwidth = [150,450],
                        #         header=dict(
                        #             values=['<b>Nomor</b>','<b>'+text+'</b>'],
                        #             # line = dict(color='#25abd1'),
                        #             fill = dict(color='#25abd1'),
                        #             align = ['left','left'],
                        #             font = dict(color='white',size = 20),
                        #             height = 35
                        #             ),
                        #         cells=dict(
                        #             values=[["Nama ODP","Port","QR Code Port", "Nama Pelanggan", "Alamat Pelanggan", "Lokasi ODP"],
                        #             [source[0],source[1],source[2],res_no[0],res_no[1],source[3]]],
                        #             # line = dict(color=warna),
                        #             fill = dict(color=[[evenwarna,'white',evenwarna,'white',evenwarna,'white'],
                        #                 [evenwarna,'white',evenwarna,'white',evenwarna,'white']]),
                        #             align = ['left','left'],
                        #             font = dict(color=[['black'],['black']], size=20),
                        #             height = 35
                        #             )
                        #         )
                        #     layout = dict(width=1366, height = 768)


                        #     data = [trace]
                        #     fig = dict(data=data, layout=layout)
                        #     plotly.offline.plot(fig,auto_open=False)


                        #     driver = webdriver.Firefox()
                        #     driver.set_window_size(1366, 678)
                        #     driver.get(chart)
                        #     driver.save_screenshot('telodp.png')
                        #     print "saved"
                        #     driver.close()
                        #     crop('telodp.png', (90,110,1290,410), 'res_telodp.png')
                        #     img = open('res_telodp.png', 'rb')
                        #     lin = URL + 'sendPhoto'
                        #     requests.post(lin, data={'chat_id': chat}, files= {'photo': img})
                        #     img.close()
                        handle_misvalue(chat, "Mohon maaf untuk sementara command ini tidak dijalankan. \n")
                    except Exception as e:
                        print e
                        handle_misvalue(chat, "Data tidak ditemukan. ")
            # Jika input berupa command untuk meliht bantuan / petunjuk
            elif text == "/HELP" or text == "/HELP"+username:
                print "help"
                handle_help(chat)
            elif text.startswith("/FOTO") or text.startswith("/FOTO"+username):
                if handle_lesscommand(text, "/FOTO"):
                    print 'err'
                    handle_misvalue(chat)
                else:         
                    try:
                        query = text.split(' ')[1]
                        text = query
                        text = text.replace('/','-')
                        list_foto = os.listdir(os.getcwd()+'\\foto odp')
                        res_foto =  [i for i in list_foto if str(text) in i]
                        # print res_foto
                        for each in res_foto:
                            img = open('foto odp/{}'.format(each), 'rb')
                            lin = URL + 'sendPhoto'
                            requests.post(lin, data={'chat_id': chat}, files= {'photo': img})
                            img.close()
                    except Exception as e:
                        print e
                        handle_misvalue(chat, "Data tidak ditemukan. ")
            # Jika input berupa command untuk melihat total ODC
            # Jika input berupa command untuk melihat total ODP 
            elif text.startswith("/TOTALODP") or text.startswith("/TOTALODP"+username):
                if handle_lesscommand(text, "/TOTALODP"):
                    handle_misvalue(chat)
                else:         
                    # menggabung list odp menjadi satu string
                    string_code = '\n'.join(code)
                    # mengambil query dari kode ODP yang disertakan dalam command /totalODP
                    try:
                        cari = text.split(' ')[1]
                        text = "\\b{}\\b".format(cari)
                        hasil_cari = re.findall(text, string_code)
                        resp = "Total {} ODP".format(len(hasil_cari))
                        send_message(resp, chat)
                    except:
                        handle_misvalue(chat, "")
            # Jika input berupa command untuk melihat total ODC
            elif text.startswith("/TOTALODC") or text.startswith("/TOTALODC"+username):
                if handle_lesscommand(text, "/TOTALODC"):
                    handle_misvalue(chat)
                else:
                    subcode = []
                    regex = r"/.*"
                    for each in code:
                        subcode.append(re.sub(regex, "", each ))
                    set_s = set(subcode)
                    b = list(set_s)
                    list_odp = []
                    list_odp_keyboard = []
                             
                    string_code = '\n'.join(b)
                    cari = text.split(' ')[1]
                    carix = re.sub("ODC", "ODP", cari)
                    text = "\\b{}\\b".format(carix)
                    hasil_cari = re.findall(text, string_code)
                    resp = "Total {} ODC".format(len(hasil_cari))
                    send_message(resp, chat)
            # /totalgcl
            elif text.startswith("/TOTALGCL") or text.startswith("/TOTALGCL"+username):
                if handle_lesscommand(text, "/TOTALGCL"):
                   handle_misvalue(chat)
                else:
                    subcode = []
                    regex = r"/.*"
                    for each in code:
                        subcode.append(re.sub(regex, "", each ))
                    set_s = set(subcode)
                    b = list(set_s)
                    list_odp = []
                    list_odp_keyboard = []
                             
                    string_code = '\n'.join(b)
                    cari = text.split(' ')[1]
                    carix = re.sub("^.{0,3}", "GCL", cari)
                    text = "\\b{}\\b".format(carix)
                    hasil_cari = re.findall(text, string_code)
                    resp = "Total {} ODC".format(len(hasil_cari))
                    send_message(resp, chat)
            
            # Jika input berupa command untuk melihat daftar kode ODP
            elif text == "/KODEODP" or text.startswith("/KODEODP"+username):
                regex = r"^.{0,3}"
                result1 = []
                result1x = [] 
                for each in code:
                    result1.append(re.findall(regex,each))
                for each in result1:
                    result1x.append(''.join(each))                
                result1 = list(set(result1x))
                resp = "{} KODE ODP\n{}".format(len(result1), ' , '.join(result1))
                send_message(resp, chat)
            # Jika input berupa command untuk melihat daftar kode STO
            elif text == "/KODESTO" or text.startswith("/KODESTO"+username):
                regex = r"\-\w{3}."
                result2 = []
                result2x = []
                for each in code:
                    result2.append(re.findall(regex,each))
                for each in result2:
                    result2x.append(re.sub("-", "", ''.join(each)))
                result2 = list(set(result2x))
                resp = "{} KODE STO\n{}".format(len(result2), ' , '.join(result2))
                send_message(resp, chat)
            # Jika input berupa command untuk melihat daftar kode ODC
            elif text == "/KODEODC" or text.startswith("/KODEODC"+username):
                regex = r"\-\w{3}\-[A-Z]{2,3}\/"
                result3 = []
                result3x = []
                result3xx = []
                for each in code:
                    result3.append(re.findall(regex,each))
                for each in result3:
                    result3x.append(''.join(each)[1:])
                for each in result3x:
                    result3xx.append(re.sub("/", "", ''.join(each)))
                    
                result3 = list(set(result3xx))                
                resp = "{} KODE STO-ODC\n{}".format(len(result3), ' , '.join(result3))
                send_message(resp, chat)
            # Jika input berupa command untuk melakukan pencarian
            elif text.startswith("/CARI") or text.startswith("/CARI"+username):
                if handle_lesscommand(text, "/CARI"):
                    handle_misvalue(chat)
                else:
                    # Jika format command benar
                    try:
                        cari = text.split(' ')[1]
                        text = cari
                        list_odp = []
                        list_odp_keyboard = []
                        for each in code:
                            if each.startswith(text):
                              list_odp.append(each)
                              list_odp_keyboard.append('/OCCUUIM '+each)
                        list_odp.sort()
                        list_odp_keyboard.sort()
                        list_length = len(list_odp)
                        # Hitung jumlah karakter pesan
                        char_length = 0
                        for x in list_odp:
                            for y in x:
                                char_length+= 1
                        # Jika hasil pencarian terlalu banyak dengan jumlah karakter lebih dari 4096, maka cari subcodenya
                        if char_length > 4096:
                            subcode = []
                            regex = r"/.*"
                            for each in code:
                                subcode.append(re.sub(regex, "", each ))
                            set_subcode = set(subcode)
                            list_subcode = list(set_subcode)
                            list_odp = []
                            list_odp_keyboard = []
                            for each in list_subcode:
                                if each.startswith(''.join(text)):
                                  list_odp.append(each)
                                  list_odp_keyboard.append('/cari '+each+'/')
                            list_odp.sort()
                            list_odp_keyboard.sort()
                            list_length = len(list_odp)
                            char_length = 0
                            for x in list_odp:
                                for y in x:
                                    char_length+= 1
                            # Jika hasil pencarian masih terlalu banyak
                            if char_length >4096:
                                resp = "Hasil pencarian terlalu besar, tidak dapat ditampilkan. Silahkan tambahkan query. /help"
                            # Jika tidak, berikan respon sesuai hasil pencarian
                            else:
                                resp = search_sto_odc_odp(list_length, list_odp)
                            # Jika daftar pencarian mencapai lebih dari 128, berikan output hanya text
                            if list_length > 128:
                                send_message(resp, chat)
                            # Jika daftar pencarian tidak lebih dari 128, berikan output beserta tampilan keyboard
                            elif list_length <= 128:
                                keyboard = build_keyboard(list_odp_keyboard)
                                send_message(resp, chat, keyboard)
                                
                            
                        # Jika hasil pencarian tidak lebih dari 4096, maka tampilkan hasil pencarian
                        else:                        
                            if list_length ==0:
                                handle_misvalue(chat, "Data tidak ditemukan. ")
                            else:
                                resp = search_sto_odc_odp(list_length, list_odp)
                                if list_length > 128:
                                    send_message(resp, chat)
                                elif list_length <= 128:
                                    keyboard = build_keyboard(list_odp_keyboard)
                                    send_message(resp, chat,keyboard)
                    except:
                        handle_misvalue(chat, "")
            else:
                if text.startswith("/"):
                    send_message("/help", chat)
                
        except KeyError:
            pass

### Fungsi untuk melakukan pencarian entah pada tingkat STO, ODC, atau ODP
def search_sto_odc_odp(list_length = 0, list_odp = ''):
    regex = r".{0,3}\-.{0,3}\-"
    string_list_odp = ''.join(list_odp)
    result = re.search(regex, string_list_odp)
    desc = ''
    if (result):
        desc = "STO"
        regex = r".{0,3}\-.{0,3}\-.{0,3}"
        result = re.search(regex, string_list_odp)
        if (result):
            desc = "ODC"
            regex = r".{0,3}\-.{0,3}\-.{0,3}\/[0-9]{0,3}"
            result = re.search(regex, string_list_odp)
            if (result):
                desc = "ODP"
    resp = 'Terdapat {} item {}\n'.format(list_length, desc)+'\n'.join(list_odp)
    return resp

### Fungsi untuk mengirim pesan
def send_message(text, chat_id, reply_markup=None):
    text = urllib.quote_plus(text.encode('utf-8', 'strict'))
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)
### Fungsi untuk mengirim lokasi
def send_location(chat_id, latitude, longitude):
    url = URL + "sendLocation?chat_id={}&latitude={}&longitude={}".format(chat_id, latitude, longitude)
    get_url(url)

### Fungsi untuk membuat keyboard tambahan
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup, ensure_ascii = True)

## Fungsi utama yang memulai serangkaian perintah lainnya
def main():
    print 'odp report, in'
    last_update_id = None
    last_update = raw_input('Last Update: ')
    # last_update = '05-September-2018'
    db_dataservice.get_started(last_update)
    # tgl = raw_input('Tanggal Update: ')
    # db.get_started(tgl)
    # Melakukan looping tanpa henti
    while True:
        updates = get_updates(last_update_id)
    #         # Jika ada update maka,
        try:
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
    #             # Proses output sesuai input
    #            if updates["result"][0][]
    #            print updates['result'][0]['message']['chat']['id'].type
                #just me that can access
    #                if updates['result'][0]['message']['chat']['id'] == 198205822: 
    #                   print "yes"
                handle_updates(updates)
                last_update_id = get_last_update_id(updates) + 1
                time.sleep(0.5)
        except KeyError:
            print "KeyError"
            last_update_id = get_last_update_id(updates) + 1
            pass
#
if __name__ == '__main__':
    main()
