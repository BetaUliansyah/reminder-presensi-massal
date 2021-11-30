import requests
import re
from bs4 import BeautifulSoup
import datetime
from pytz import timezone
import urllib3
import json
from random import randint
import time
import pandas as pd
import numpy as np
from dotenv import load_dotenv

session = None
def google_drive():
    from google.colab import drive
    drive.mount('/content/drive')
    path = F"/content/drive/My Drive/Colab Notebooks/Monabsensi Massal/"
    filename = "pajak.csv"
    pajak = pd.read_csv(path+filename, error_bad_lines=False)

def set_global_session():
    global session
    if not session:
        session = requests.Session()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        session.verify = False

def get_token():
    with session.get('https://monabppk.kemenkeu.go.id/') as response:
        if response.status_code==200 and len(response.text) != 0:
            bsoup = BeautifulSoup(response.text, 'html.parser')
            csrf_value = bsoup.find("input", {"name":"csrf_test_name"})['value']
            return csrf_value

def login(csrf_value, username, password):
    with session.post('https://monabppk.kemenkeu.go.id/index.php/login',
                      data={'csrf_test_name': csrf_value, 'inputEmail': username , 'inputPassword': password}) as response:
        if response.status_code==200 and len(response.text) != 0 and username in response.text:
            return True

def logout():
    with session.get('https://monabppk.kemenkeu.go.id/index.php/login/logout') as response:
        if response.status_code==200:
            return True
        else:
            return False


def libur():
    libur = ['1-01-2021', # tahun baru
             '12-02-2021', # imlek
             '11-03-2021', # Isra' Mi'raj
             '14-03-2021', # Nyepi
             '2-04-2021',  # Wafat Isa
             '1-05-2021',  # Hari Buruh
             '13-05-2021', # Kenaikan Isa
             '13-05-2021', # Idul Fitri
             '14-05-2021', # Idul Fitri
             '26-05-2021', # Waisak
             '1-06-2021',  # pancasila
             '20-07-2021', # Idul Adha
             '11-08-2021', # Tahun Baru Hijriyah
             '17-08-2021', # Kemerdekaan RI
             '20-10-2021', # Maulid Nabi
             '25-12-2021', # Natal
             ]
    if datetime.datetime.now(timezone('Asia/Jakarta')).strftime("%-d-%m-%Y") in libur:
        return True
    return False

def lihat_absensi_group(csrf_value, groupid=124):
    with session.post('https://monabppk.kemenkeu.go.id/index.php/absensi',
                      data={'csrf_test_name': csrf_value, 'groupid': str(groupid), 'submit': 'Tampilkan', 'example2_length': '100'}) as response:
        if response.status_code==200:
            bsoup = BeautifulSoup(response.text, 'html.parser')
            #print(bsoup)
            #nip = [[cell.text for cell in row("td")]
            #             for row in bsoup("tr")]
            # [[], ['1', '198409292006021002', 'ADHIPRADANA PRABU SWASITO', ''], ['2', '198408262006021001', 'AGUS BANDIYONO', ''], ['3', '197710231999031001', 'ANDRI MARFIANA', ''], ['4', '198212152009012009', 'ANISA FAHMI', ''], ['5', '197804202000011002', 'ANTONIUS RAGIL KUNCORO', ''], ['6', '198211092004121001', 'ARIEF BUDI WARDANA', ''], ['7', '198001192001121002', 'ARIF NUGRAHANTO', ''], ['8', '197401121995031001', 'BENNY GUNAWAN ARDIANSYAH', ''], ['9', '197904262000121001', 'BENNY SETIAWAN', ''], ['10', '196912201990032001', 'BUDIASIH WIDIASTUTI', ''], ['11', '198307142004121002', 'DHIAN ADHETIYA SAFITRA', ''], ['12', '197809082000011001', 'EDY RIYANTO', ''], ['13', '197606021999032002', 'EMIK SUYANI', ''], ['14', '198409052006021003', 'ERI WAHYUDI', ''], ['15', '196210101983021001', 'FADLIL USMAN', ''], ['16', '198502072006021001', 'FEBRIAN', ''], ['17', '198004202001121002', 'FERRY IRAWAN', ''], ['18', '197606151996022001', 'GUSTI AYU INDAH RATNASARI', ''], ['19', '198212312003122001', 'HANIK SUSILAWATI MUAMARAH', ''], ['20', '197010181995032001', 'HENI SULASTRI', ''], ['21', '197409111994021001', 'I GEDE KOMANG CHAHYA BAYU ANTA KUSUMA', ''], ['22', '197504261996021001', 'IMAM MUHASAN', ''], ['23', '197401081998031002', 'IRWAN ARIBOWO', ''], ['24', '197505241995032001', 'KHUSNAINI', ''], ['25', '197412251995111002', 'KRISTIAN AGUNG PRASETYO', ''], ['26', '196206281987031001', 'KUSMONO', ''], ['27', '197106101991031002', 'KUWAT SLAMET', ''], ['28', '197008251991031009', 'MUHAMMAD RIDHWAN GALELA', ''], ['29', '198202212003122002', 'NINA SABNITA', ''], ['30', '197502141999031001', 'NUGROHO YONIMURWANTO', ''], ['31', '197812162000011001', 'NUR ARIF NUGRAHA', ''], ['32', '198604142009012009', 'NUR FARIDA LIYANA', ''], ['33', '198403192006022002', 'NURHIDAYATI', ''], ['34', '197510031996021002', 'OKE WIBOWO', ''], ['35', '197809082000121007', 'PRIMANDITA FITRIANDI', ''], ['36', '197101231992031001', 'PURWANTO', ''], ['37', '197305011994021001', 'RACHMAD UTOMO', ''], ['38', '197605251996021002', 'RAHADI NUGROHO', ''], ['39', '196806271989031002', 'Rd. TATAN JAKA TRESNAJAYA', ''], ['40', '198811142009122002', 'RESA AKSARI', ''], ['41', '198311302009012008', 'RIANI BUDIARSIH', ''], ['42', '197305242002121001', 'RIKO RIANDOKO', ''], ['43', '198405312009011006', 'SONY HARTONO', ''], ['44', '197507241999031001', 'SUHUT TUMPAL SINAGA', ''], ['45', '197612091996021001', 'SULFAN', ''], ['46', '198201132002121001', 'SUPARNA WIJAYA', ''], ['47', '197903172000121001', 'SUPRIYADI', ''], ['48', '198510132007011002', 'TEGUH WARSITO', ''], ['49', '197410211995112001', 'TITIT WIDIASIH ASMANINGTYAS', ''], ['50', '198308172007011001', 'TRI WARSO NUGROHO', ''], ['51', '196801261994032001', 'VISSIA DEWI HAPTARI', ''], ['52', '198504102006022002', 'VITA APRILIASARI', ''], ['53', '197511051999031001', 'YADHY CAHYADY', '']]
            nip_table = pd.read_html(response.text)
            nip = nip_table[0]["NIP"]

            links = []
            for item in bsoup.select("button[onclick^=\"window.location=\"]"):
                # ... do stuff here, e.g.
                # thanks https://stackoverflow.com/questions/61462767/python-open-a-url-and-extract-location-href-value-from-onclick
                onclick = item["onclick"]
                href = onclick.split("=")[1]
                href = href.strip("'")
                #print(href)
                links.append(href)
            nip_links = pd.DataFrame(list(zip(nip, links)),
               columns =['nip', 'links'])
            return nip_links

def get_data_presensi_group(link, tanggal=datetime.datetime.now(timezone('Asia/Jakarta')).strftime("%-d-%m-%Y")):
    with session.get(link) as response:
        if response.status_code==200 and len(response.text) != 0:
            bsoup = BeautifulSoup(response.text, 'html.parser')
            #tgl_hari_ini = datetime.date.today().strftime("%-d-%m-%Y")
            hasil_presensi = bsoup.find('td', text = re.compile(tanggal))
            hari = hasil_presensi.find_previous_sibling('td')
            jam_masuk = hasil_presensi.findNext('td').findNext('td')
            jam_pulang = jam_masuk.findNext('td').findNext('td')
            keterangan = jam_pulang.findNext('td').findNext('td')
            nama = bsoup.find('h3', attrs = {'class': 'box-title pull-right'}).text.split(" -")[0]
            nip = bsoup.find('h3', attrs = {'class': 'box-title pull-right'}).text.split(" ")[-1]
            # <h3 class="box-title pull-right">Agus Bandiyono - 198408262006021001</h3>
            return [hari.text, tanggal, jam_masuk.text, jam_pulang.text, keterangan.text, nama, nip]

def cek_sudah_presensi_pagi_group(data_presensi):
    if data_presensi[2] != '00:00':
        return True

def cek_sudah_presensi_sore_group(data_presensi):
    if data_presensi[3] != '00:00':
        return True

def nusasms_kirim_wa(tujuan, pesan, test=0, apikey="110C9015F177631FDF2FD8042CA1A040"):
    if (test):
        BASE_URL = 'https://dev.nusasms.com/nusasms_api/1.0'
    else:
        BASE_URL = 'https://api.nusasms.com/nusasms_api/1.0'

    HEADERS = {
        "Accept": "application/json",
        "APIKey": apikey
    }
    PAYLOADS = {
        'destination': tujuan,
        'message': pesan
    }

    with session.post(f'{BASE_URL}/whatsapp/message',
                      headers=HEADERS,
                      json=PAYLOADS) as response:
        if response.status_code==200:
            return True

def wachat_send_message(tujuan, pesan, sender, apikey):
    HEADERS = {
        "Accept": "application/json",
        "APIKey": apikey
    }
    PAYLOADS = {
        # 'destination': '628194804439',
        'destination': tujuan,
        'sender': sender,
        'message': pesan
    }

    r = requests.post(
        'https://api.wachat-api.com/wachat_api/1.0/message',
        headers=HEADERS,
        json=PAYLOADS,
        # Skip SSL Verification
        # verify=False
    )

def load_data_pegawai():
    pegawai = [
              ["Adhipradana Prabu Swasito", "198409292006021002", "6281932041277"],
              ["Agus Bandiyono", "198408262006021001", "6281316119900"],
              ["Andri Marfiana", "197710231999031001", "6281291271077"],
              ["Anisa Fahmi", "198212152009012009", "6285220039446"],
              ["Antonius Ragil Kuncoro", "197804202000011002", "6285867831000"],
              ["Arief Budi Wardana", "198211092004121001", "6281542526291"],
              ["Arif Nugrahanto", "198001192001121002", "6281318009961"],
              ["Benny Gunawan Ardiansyah", "197401121995031001", "62811970040"],
              ["Benny Setiawan", "197904262000121001", "6285890067729"],
              ["Budiasih Widiastuti", "196912201990032001", "6285216946634"],
              ["Dhian Adhetiya Safitra", "198307142004121002", "62811454465"],
              ["Edy Riyanto", "197809082000011001", "6281310301061"],
              ["Emik Suyani", "197606021999032002"],
              ["Eri Wahyudi", "198409052006021003", "6281804473231"],
              ["Fadlil Usman", "196210101983021001", "628164801198"],
              ["Febrian", "198502072006021001","628194804439"],
              ["Ferry Irawan", "198004202001121002", "6287776002029"],
              ["Gusti Ayu Indah Ratnasari", "197606151996022001", "6281247058030"],
              ["Hanik Susilawati Muamarah", "198212312003122001", "628151860135"],
              ["Heni Sulastri", "197010181995032001", "628974743601"],
              ["I Gede Komang Chahya Bayu Anta Kusuma", "197409111994021001","628161342015"],
              ["Imam Muhasan", "197504261996021001", "6281281117248"],
              ["Irwan Aribowo", "197401081998031002", "6281585145266"],
              ["Khusnaini", "197505241995032001", "6287887888636"],
              ["Kristian Agung P", "197412251995111002", "6285215291580"],
              ["Kusmono", "196206281987031001", "628129909228"],
              ["Kuwat Slamet, S.e., M.si.", "197106101991031002", "6281584984317"],
              ["Muhammad Ridhwan Galela", "197008251991031009", "62817877162"],
              ["Nina Sabnita", "198202212003122002", "6281295683763"],
              ["Nugroho Yonimurwanto", "197502141999031001", "6281298072083"],
              ["Nur Arif Nugraha", "197812162000011001", "62817272778"],
              ["Nur Farida Liyana", "198604142009012009", "6281286629363"],
              ["Nurhidayati", "198403192006022002", "6281510584137"],
              ["Oke Wibowo, Sst., Ak.", "197510031996021002", "6288227716171"],
              ["Primandita Fitriandi", "197809082000121007", "628129502938"],
              ["Purwanto", "197101231992031001", "6281519209667"],
              ["Rachmad Utomo", "197305011994021001", "628179920900"],
              ["Rahadi Nugroho", "197605251996021002", "6281381204811"],
              ["Rd. Tatan Jaka Tresnajaya", "196806271989031002", "6281212246888"],
              ["Resa Aksari", "198811142009122002", "6281266442812"],
              ["Riani Buadiarsih", "198311302009012008", "6285641955528"],
              ["Riko Riandoko", "197305242002121001", "62811122612"],
              ["Sony Hartono", "198405312009011006", "6281328731969"],
              ["Suhut Tumpal Sinaga", "197507241999031001", "628111805191"],
              ["Sulfan", "197612091996021001","628129353689"],
              ["Suparna Wijaya", "198201132002121001", "6287780663168"],
              ["Supriyadi", "197903172000121001","6281296615127"],
              ["Teguh Warsito", "198510132007011002", "6285921535499"],
              ["Titit Widiasih Asmaningtyas", "197410211995112001","6281383410431"],
              ["Tri Warso Nugroho", "198308172007011001","6281283357474"],
              ["Vissia Dewi Haptari", "196801261994032001", "6281293610106"],
              ["Vita Apriliasari", "198504102006022002","62817613050"],
              ["Yadhy Cahyady", "197511051999031001","6282125125025"]
              ]
    return pegawai

def no_wa(nip, pegawai):
    wa = np.where()
    # belum kepake 

if __name__ == "__main__":
    if load_dotenv():
        WACHAT_APIKEY = os.getenv('WACHAT_APIKEY')
        USERNAME_MONABSENSI = os.getenv('USERNAME_MONABSENSI')
        PASSWORD_MONABSENSI = os.getenv('PASSWORD_MONABSENSI')
    else:
        exit('Tidak ada file .env')


    set_global_session()
    # google_drive()
    pegawai = pd.DataFrame(load_data_pegawai(), columns=['nama', 'nip', 'mobile'])
    pegawai[(pegawai != None).all(1)]

    start_time = datetime.datetime.now()
    print("Start script presensi " + datetime.datetime.now(timezone('Asia/Jakarta')).strftime("%-d-%m-%Y") + " at " + str(start_time))
    if libur() == False:
        if login(get_token(), USERNAME_MONABSENSI, PASSWORD_MONABSENSI):
            print("Berhasil Login")
            dataweb = lihat_absensi_group(get_token(), groupid=124)
            gabung = pd.concat([pegawai, dataweb], axis=1)
            gabung.dropna(how="any", inplace=True) # hapus data tanpa no HP

            for index, data in gabung.iterrows():
                data_presensi = get_data_presensi_group(data['links'])
                hari = data_presensi[0]
                tanggal = data_presensi[1]
                presensi_pagi = data_presensi[2]
                presensi_sore = data_presensi[3]
                status_presensi = data_presensi[4]
                nama = data_presensi[5]

                if presensi_pagi == '00:00':
                    pesan_pagi = "Anda belum presensi pagi. Segera lakukan presensi pagi di https://monabppk.kemenkeu.go.id/\n"
                else:
                    pesan_pagi = "Anda sudah presensi pagi pada pukul " + presensi_pagi +"\n"
                if presensi_sore == '00:00':
                    pesan_sore = "Anda belum presensi sore. Segera lakukan presensi sore di https://monabppk.kemenkeu.go.id/\n"
                else:
                    pesan_sore = "Anda sudah presensi sore pada pukul " + presensi_sore +"\n"

                pesan = '*INFO PRESENSI*\n'
                pesan = pesan + "Hari: " + hari + ", tanggal " + tanggal +"\n"
                pesan = pesan + "Nama: " + nama +"\n"
                pesan = pesan + pesan_pagi
                if datetime.datetime.now(timezone('Asia/Jakarta')).hour >= 17:
                    pesan = pesan + pesan_sore
                pesan = pesan + "Status presensi hari ini: " + status_presensi +"\n"
                pesan = pesan + "\nPesan dikirim pada: " + str(datetime.datetime.now(timezone("Asia/Jakarta")))
                #pesan = pesan + "\nSelama masa percobaan, harap forward pesan ini ke wa.me/628567074554 (Beta Uliansyah). Terima kasih."
                #nusasms_kirim_wa(str(data['mobile']), pesan)
                wachat_send_message(str(data['mobile']), pesan, sender='6282189096866', WACHAT_APIKEY)
                print("Kirim WA ke " + nama + ", nomor " + str(data['mobile']) +"\n")
                print("Isi pesan: " + pesan)
            if (logout()):
                print("Berhasil logout")

    duration = datetime.datetime.now() - start_time
    print("Duration: " + str(duration))
