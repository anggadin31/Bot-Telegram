# Bot-Telegram
Digunakan untuk mengambil data dari database berdasarkan yang dicari dan menampilkannya di telegram
Menu awal yang ditampilkan oleh bot yaitu sebagai berikut, dimana bot akan menampilkan beberapa pilihan yang bisa digunakan
<p align="center">
  <img src="https://github.com/anggadin31/Bot-Telegram/blob/main/Screenshot/main.PNG?raw=true" width="350" title="hover text">
</p>
Untuk menu Cek Golive sendiri digunakan untuk mengetahui lokasi dari suatu ODP, berdasarkan nama ODP yang diinput oleh user seperti pada gambar di bawah
<p align="center">
  <img src="https://github.com/anggadin31/Bot-Telegram/blob/main/Screenshot/golive.PNG?raw=true" width="350" title="hover text">
</p>
Data yang digunakan oleh menu Cek Golive diambil dari file CEK GOLIVE.xlsx yang bisa dilihat pada folder Database
Untuk menu kedua ada Cek IP OLT yang digunakan untuk mengetahui detail informasi ODP dari UIM. User bisa mengetahui detail dengan menginputkan nama ODP yang ingin dicari
<p align="center"> 
  <img src="https://github.com/anggadin31/Bot-Telegram/blob/main/Screenshot/ip_olt.PNG?raw=true" width="350" title="hover text"> 
</p>
 Data yang digunakan oleh menu Cek IP OLT diambil dari file Excel yang ada pada server
 
 Untuk menu Cek Pel UIM dan Cek Pel Lap sendiri fungsinya kurang lebih sama, yaitu untuk mengecek data ODP yang ada di sistem UIM dan yang ada di lapangan. Data ODP sendiri bisa lebih dari satu karena1 ODP bisa memiliki beberapa No. Internet Berbeda. User bisa mengambil data ODP dengan menginputkan nama ODP ataupun nomor internet
 <p align="center"> 
  <img src="https://github.com/anggadin31/Bot-Telegram/blob/main/Screenshot/pel_lap.PNG?raw=true" width="350" title="hover text"> 
 </p>
 <p align="center"> 
  <img src="https://github.com/anggadin31/Bot-Telegram/blob/main/Screenshot/pel_uim.PNG?raw=true" width="350" title="hover text"> 
 </p>
 Data yang digunakan oleh menu Cek Pel UIM dan Cek Pel Lap diambil dari file DALAPA_VALIDASI_LAPANGAN.xlsx dan DALAPA_VALIDASI_UIM.xlsx yang bisa dilihat pada folder Database
 
 Untuk menu Cek Label QR ODP digunakan untuk mengetahui kode QR dari suatu ODP. User dapat mengambil data QR berdasarkan nama ODP yang diinput
 <p align="center"> 
  <img src="https://github.com/anggadin31/Bot-Telegram/blob/main/Screenshot/label_qr.PNG?raw=true" width="350" title="hover text"> 
 </p>
 Data yang digunakan oleh menu Cek Label QR ODP diambil dari file DATA_QR_ODP.xlsx yang dapat dilihat di folder Database
 
 Untuk menu Service Name 1054 digunakan untuk memotong text yang diinput oleh user, sehingga user akan mendapatkan info mengenai Service ID
 <p align="center"> 
  <img src="https://github.com/anggadin31/Bot-Telegram/blob/main/Screenshot/service_name.PNG?raw=true" width="350" title="hover text"> 
 </p>
 Untuk hasil output dari pemotongan text harus sesuai seperti gambar di bawah
  <p align="center"> 
  <img src="https://github.com/anggadin31/Bot-Telegram/blob/main/Screenshot/service.PNG?raw=true" width="350" title="hover text"> 
 </p>
 
 Untuk menu Foto ODP digunakan untuk mengambil foto dari nama ODP yang telah diinput user, seperti pada gambar di bawah
 <p align="center"> 
  <img src="https://github.com/anggadin31/Bot-Telegram/blob/main/Screenshot/foto_odp.PNG?raw=true" width="350" title="hover text"> 
 </p>
 Data yang digunakan oleh menu Foto ODP diambil dari folder gambar yang ada pada server
 
 Untuk menu ID Service Port digunakan untuk mengetahui ID Port dari suatu IP dengan Slot dan Port tertentu. Untuk mengetahui ID Port tersebut, user harus menginputkan alamat IP beserta slot dan port yang ingin diketahui seperti pada gambar di bawah
 <p align="center"> 
  <img src="https://github.com/anggadin31/Bot-Telegram/blob/main/Screenshot/service_port.PNG?raw=true" width="350" title="hover text"> 
 </p>
 Data yang digunakan oleh menu ID Service Port diambil dari file ID Port OLT Banjarmasin new (update).xlsx yang dapat dilihat pada folder Database
 
 Untuk menu Cek Jadwal Daman digunakan untuk mengetahui jadwal karyawan pada tanggal tertentu seperti siapa yang masuk pagi, piket pagi, masuk siang, cuti, ataupun libur. Untuk mengetahui jadwal tersebut user harus menginputkan tanggal yang ingin diketahui seperti pada gambar di bawah
 <p align="center"> 
  <img src="https://github.com/anggadin31/Bot-Telegram/blob/main/Screenshot/jadwal.PNG?raw=true" width="350" title="hover text"> 
 </p>
 Data yang digunakan oleh menu Cek Jadwal Daman ini diambil dari file JADWAL DESEMBER 2019.xlsx yang dapat dilihat pada folder Database
 Untuk menu terakhir yaitu menu Absensi masih dalam tahap pengembangan.
