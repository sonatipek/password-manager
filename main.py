from queue import Empty
import secrets
import string

from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
# from tkinter import ttk

import pyodbc

# *!Veritabanı Bağlantısı
db = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=SERVERNAME;'
        'Database=DBNAME;'
        'Trusted_Connection=True;'
)

imlec = db.cursor()

# *! Main Window 
mainWindow = ctk.CTk()
mainWindow.title("SSI Password Manager | Giriş Yap")
mainWindow.resizable("false","false")
mainWindow.geometry(f"{500}x{450}")
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Tipografi
headerFont = ctk.CTkFont(size=20, weight="bold")
commFont = ctk.CTkFont(size=14)
commFont2 = ctk.CTkFont(size=12, weight="bold")
infoFont = ctk.CTkFont(size=9)

# Tema değiştirme kodları
def changeUI(new_appearance_mode):
    ctk.set_appearance_mode(new_appearance_mode)

# Giriş yap butonuna tıklanıldığında tetiklenecek event
def girisYap():
    # Inputlardan girilen verilerin alınması
    girilen_eposta = ePosta_var.get()
    girilen_sifre = sifre_var.get()

    # Inputlar boşsa uyarı bildir, doluysa kayıt varlığını kontrol et
    if (girilen_eposta == "" or girilen_sifre == ""):
            messagebox.showinfo("Boş Alan Bırakılamaz","E-posta ve şifre alanları boş bırakılamaz!")
            
    else:
            imlec.execute(f"SELECT uye_id, e_posta, sifre FROM kayit_Tablosu WHERE e_posta = '{girilen_eposta}'")
            sonuc = imlec.fetchall()

            # Inputlardaki sorgu sonunda hiç kayıt yoksa uyaru, kayıt varsa doğruluğunu kontrol et
            if (len(sonuc) <= 0):
                    messagebox.showinfo("Hesap Bulunamadı","Bu e-postaya kayıtlı bir hesap yok")
                    
            else:
                    # Bu döngü ile veritabanındaki e-posta ve şifrenin bir değişkene atanması yapılıyor.
                    # Zaten kayıt aşamasında e-posta kontrolü yapıldığından 2 adet kayıt dönmesi muhtemel değil.
                    for i in sonuc:
                                global uyeID
                                uyeID = i[0]

                                e_posta = i[1]
                                sifre = i[2]

                    if (girilen_eposta == e_posta and girilen_sifre == sifre):
                                messagebox.showinfo("Giriş Başarılı","Giriş başarılı, yönlendiriliyorsunuz!")
                                mainWindow.destroy()
                                homepageUI()
    
                    else:
                                messagebox.showinfo("Giriş Başarısız","Girdiğiniz şifre ile uyuşan bir hesap yok!")




# *!Şifremi Unuttum Ekranı
def sifremiUnuttum():
    sifremiUnuttum = ctk.CTkToplevel()
    sifremiUnuttum.title("SSI Password Manager | Şifremi Unuttum")
    sifremiUnuttum.geometry("500x240+150+150")
    sifremiUnuttum.resizable("false","false")

    def sifreOgren():
        girilen_eposta = ePosta_var.get()
        girilen_cevap = guvenlikCevap_var.get()

        if (girilen_eposta == "" or girilen_cevap == ""):
            messagebox.showinfo("Boş Alan Bırakılamaz","E-posta ve güvenlik sorusu alanları boş bırakılamaz!")
            
        else:
                imlec.execute(f"SELECT e_posta, gs_cevap, sifre FROM kayit_Tablosu WHERE e_posta = '{girilen_eposta}'")
                sonuc = imlec.fetchall()

                if (len(sonuc) <= 0):
                        messagebox.showinfo("Hesap Bulunamadı","Bu e-postaya kayıtlı bir hesap yok")
                        
                else:
                        for i in sonuc:
                                e_posta = i[0]
                                gsCevap = i[1]
                                sifre = i[2]

                        if (girilen_eposta == e_posta and girilen_cevap == gsCevap):
                                messagebox.showinfo("İşlem Başarılı","Şifreniz klasöre oluşturulan 'sifre.txt' dosyasındadır.")
                                dosya = open("./sifre.txt","w",encoding="utf-8")
                                dosya.write(sifre)
                                dosya.close
                                sifremiUnuttum.destroy()
        
                        else:
                                messagebox.showinfo("İşlem Başarısız","Girdiğiniz güvenlik sorusu ile cevap uyuşmuyor! Şifrenizi öğrenmek için lütfen bizimle iletişime geçin")

    ctk.CTkLabel(sifremiUnuttum, text="Şifremi Unuttum", font=headerFont).place(x=150, y=30)

    ePosta_var = StringVar()
    ctk.CTkLabel(sifremiUnuttum, text="E-posta", font=infoFont).place(x=10, y=65)
    ctk.CTkEntry(sifremiUnuttum, textvariable=ePosta_var).place(x=10, y=90)

    guvenlikCevap_var = StringVar()
    ctk.CTkLabel(sifremiUnuttum, text="Güvenlik Sorunuzun Cevabı", font=infoFont).place(x=10, y=120)
    ctk.CTkEntry(sifremiUnuttum, textvariable=guvenlikCevap_var).place(x=10, y=145)

    ctk.CTkButton(sifremiUnuttum, text="Şifre Öğren", command=sifreOgren).place(x=10, y=200)
        
    sifremiUnuttum.mainloop()
# *! ŞİFREMİ UNUTTUM EKRANI BİTİŞ


# *!Kaydol Ekranı
def kayıtOl():
    kayıtOl = ctk.CTkToplevel()
    kayıtOl.title("SSI Password Manager | Kaydol")
    kayıtOl.geometry("360x480+150+150")
    kayıtOl.resizable("false","false")

    def kayıtOlButton():
        global control
        control = False
        girilen_ad = ad_var.get()
        girilen_soyad = soyad_var.get()
        girilen_dt = dogumTarihi_var.get()
        girilen_eposta = ePosta_var.get()
        girilen_sifre = sifre_var.get()
        girilen_gs = guvenlikSoru_var.get()
        girilen_gsCevap = gsCevap_var.get()

        if (girilen_ad == "" or girilen_soyad == "" or girilen_dt == "" or girilen_eposta == "" or girilen_sifre == "" or girilen_gs == "" or girilen_gsCevap == "" ):
            messagebox.showinfo("Boş Alan Bırakılamaz","Kayıt girişlerinde boş alan bırakılamaz!")
        else:
                # https://github.com/sonatipek/emailController_py detaylı açıklamayı github'dan bulabilirsiniz
                for search in girilen_eposta:
                        if (search == "@"):
                                control = True
                                break

                if (control == False):
                        messagebox.showinfo("E-posta verisi bir e-posta değil"," Lütfen bir e-posta girin! (E-postada @ işareti olmalıdır.)")
                else:
                        temp = girilen_eposta.split(".")
                        if temp[-1] == "com":
                                temp = girilen_eposta.split("@")
                                temp = temp[-1].split(".com")
                        
                                if temp[0] != Empty:
                                        sorgu = f"INSERT INTO kayit_Tablosu(ad, soyad, dogum_tarihi, e_posta, sifre, guvenlik_sorusu, gs_cevap) VALUES(?,?,?,?,?,?,?)"
                                        values = (f'{girilen_ad}', f'{girilen_soyad}', f'{girilen_dt}',f'{girilen_eposta}',f'{girilen_sifre}',f'{girilen_gs}', f'{girilen_gsCevap}')
                                        ekle = imlec.execute(sorgu, values)
                                        db.commit()
                                        messagebox.showinfo("İşlem Başarılı"," Kayıt başarı ile oluşturuldu! Girişinizi yapabilirsiniz")
                                        kayıtOl.destroy()
                                        
                        else:      
                                messagebox.showinfo("E-posta verisi bir e-posta değil"," Lütfen bir e-posta girin! (E-postanın sonunda '.com' ve bir alt alan adı olmalıdır.)")


    ctk.CTkLabel(kayıtOl, text="Kayıt Ol", font=headerFont).place(x=150, y=30)

    ad_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="Ad", font=infoFont).place(x=10, y=65)
    ctk.CTkEntry(kayıtOl, textvariable=ad_var).place(x=10, y=90)

    soyad_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="Soyad", font=infoFont).place(x=175, y=65)
    ctk.CTkEntry(kayıtOl, textvariable=soyad_var).place(x=175, y=90)


    dogumTarihi_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="Doğum Tarihi*", font=infoFont).place(x=10, y=120)
    ctk.CTkEntry(kayıtOl, textvariable=dogumTarihi_var).place(x=10, y=145)

    ePosta_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="E-posta", font=infoFont).place(x=10, y=175)
    ctk.CTkEntry(kayıtOl, textvariable=ePosta_var).place(x=10, y=200)

    sifre_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="Şifre", font=infoFont).place(x=10, y=235)
    ctk.CTkEntry(kayıtOl, textvariable=sifre_var, show="*").place(x=10, y=260)


    guvenlikSoru_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="Güvenlik Sorunuz**", font=infoFont).place(x=10, y=290)
    ctk.CTkEntry(kayıtOl, textvariable=guvenlikSoru_var).place(x=10, y=315)

    gsCevap_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="Güvenlik Sorunuzun Cevabı**", font=infoFont).place(x=175, y=290)
    ctk.CTkEntry(kayıtOl, textvariable=gsCevap_var).place(x=175, y=315)


    ctk.CTkLabel(kayıtOl, text="*: Tarih değeri 'yyyy-aa-gg' şeklinde olmalıdır", font=infoFont).place(x=10, y=345)
    ctk.CTkLabel(kayıtOl, text="**: Güvenlik sorunuzu ve cevabını saklayınız.\nUnuttuğunuz taktirde hesabınızı kaybedebilirsiniz.", font=infoFont).place(x=10, y=375)

    ctk.CTkButton(kayıtOl, text="Kayıt Ol", command=kayıtOlButton).place(x=10, y=410)


    kayıtOl.mainloop()
# *! Kaydol Ekranı Bitiş

# *! Homepage Ekranı    
def homepageUI():
        homepageUI = ctk.CTkToplevel()
        homepageUI.title("SSI Password Manager | Ana Sayfa")
        homepageUI.geometry("480x720+50+50")
        homepageUI.resizable("false", "false")

        def kayitEkle():
                kayitEkle = ctk.CTkToplevel()
                kayitEkle.title("SSI Password Manager | Şifre  Kayıt")
                kayitEkle.geometry("480x280+100+100")
                kayitEkle.resizable("false", "false")

                def dbYaz():
                        global uyeID
                        uygAdi =girilen_uygulamaAdi.get()
                        hesapAdi = girilen_hesapAdi.get()
                        hesapSifresi = girilen_hesapSifresi.get()
                        if (uygAdi == "" or hesapAdi == "" or hesapSifresi == ""):
                                messagebox.showinfo("Boş Alan Bırakılamaz","Kayıt girişlerinde boş alan bırakılamaz!")
                        else:
                                sorgu = f"INSERT INTO sifreler_Tablosu(uye_id, uygulama_adi, hesap_adi, hesap_sifresi) VALUES(?,?,?,?)"
                                values = (f'{uyeID}', f'{uygAdi}', f'{hesapAdi}',f'{hesapSifresi}')
                                ekle = imlec.execute(sorgu, values)
                                db.commit()
                                messagebox.showinfo("İşlem Başarılı","Şifreniz başarıyla eklendi!")
                                kayitEkle.destroy()

                ctk.CTkLabel(kayitEkle, text="Şifre Kayıt", font=headerFont).place(x=200, y=20)

                girilen_uygulamaAdi = StringVar()
                ctk.CTkLabel(kayitEkle, text="Şifresi kaydedilecek uygulama", font=infoFont).place(x=20, y=65)
                ctk.CTkEntry(kayitEkle, textvariable=girilen_uygulamaAdi).place(x=10, y=90)

                girilen_hesapAdi = StringVar()
                ctk.CTkLabel(kayitEkle, text="Hesap e-posta / kullanıcı adı", font=infoFont).place(x=20, y=120)
                ctk.CTkEntry(kayitEkle, textvariable=girilen_hesapAdi).place(x=10, y=145)

                girilen_hesapSifresi = StringVar()
                ctk.CTkLabel(kayitEkle, text="Hesap şifresi", font=infoFont).place(x=20, y=175)
                ctk.CTkEntry(kayitEkle, textvariable=girilen_hesapSifresi, show="*").place(x=10, y=200)
                
                ctk.CTkButton(kayitEkle, text="Şifreyi Kaydet", font=commFont, command=dbYaz).place(x=10, y=235)
             
                kayitEkle.mainloop()

        tabview = ctk.CTkTabview(homepageUI, width=480, height=720)
        tabview.place(x=0, y=0)

        tabview.add("Profil")
        tabview.add("Ana Sayfa")
        tabview.add("Şifrelerim")
        tabview.add("Şifre Oluştur")
        tabview.add("Ayarlar")
        tabview.add("Çıkış Yap")

        tabview.set("Ana Sayfa")

        # Ana Sayfa Görünümü
        ctk.CTkLabel(tabview.tab("Ana Sayfa"), text="Kayıtlı Hesaplarınız", font=headerFont).place(x=20, y=20)
        ctk.CTkButton(tabview.tab("Ana Sayfa"), text="+", font=headerFont, width=50, command=kayitEkle).place(x=400, y=600)


        global uyeID
        imlec.execute(f"SELECT uygulama_adi, hesap_adi FROM sifreler_Tablosu WHERE uye_id = '{uyeID}'")
        sonuc = imlec.fetchall()

        if (sonuc == []):
                ctk.CTkLabel(tabview.tab("Ana Sayfa"), text="Kayıtlı Hesabınız yok. Hemen bir tane ekleyin!", font=commFont).place(x=20, y=50)
        else:
                arttırma = 1
                for i in sonuc:
                        arttırma += 3
                        yDeger = 50 + (arttırma * 10) 
                        uygulama = i[0]
                        hesapAdi = i[1]
                
                        ctk.CTkLabel(tabview.tab("Ana Sayfa"), text=f"{uygulama}", font=commFont).place(x=30, y=yDeger)
                        ctk.CTkLabel(tabview.tab("Ana Sayfa"), text=f"{hesapAdi}", font=commFont).place(x=130, y=yDeger)

        def yenile():
                global uyeID
                imlec.execute(f"SELECT uygulama_adi, hesap_adi FROM sifreler_Tablosu WHERE uye_id = '{uyeID}'")
                sonuc = imlec.fetchall()

                if (sonuc == []):
                        ctk.CTkLabel(tabview.tab("Ana Sayfa"), text="Kayıtlı Hesabınız yok. Hemen bir tane ekleyin!", font=commFont).place(x=20, y=50)
                else:
                        arttırma = 1
                        for i in sonuc:
                                arttırma += 3
                                yDeger = 50 + (arttırma * 10) 
                                uygulama = i[0]
                                hesapAdi = i[1]
                        
                                ctk.CTkLabel(tabview.tab("Ana Sayfa"), text=f"{uygulama}", font=commFont).place(x=30, y=yDeger)
                                ctk.CTkLabel(tabview.tab("Ana Sayfa"), text=f"{hesapAdi}", font=commFont).place(x=130, y=yDeger)

        ctk.CTkButton(tabview.tab("Ana Sayfa"), text="Yenile", font=headerFont, width=50, command=yenile).place(x=10, y=600)

        # Profil Görünümü
        ctk.CTkLabel(tabview.tab("Profil"), text="Profil Bilgileri", font=headerFont).place(x=20, y=20)
        # global uyeID
        imlec.execute(f"select ad + ' ' +soyad, e_posta, kayit_tarihi, dogum_tarihi from kayit_Tablosu where uye_id = {uyeID}")
        sonuc = imlec.fetchall()

        adSoyad = sonuc[0][0]
        epostaBilgi = sonuc[0][1]
        kayitTarihBilgi = sonuc[0][2]
        dogumTarihBilgi = sonuc[0][3]

        ctk.CTkLabel(tabview.tab("Profil"), text="Ad - Soyad:", font=commFont2).place(x=20, y=50+20)
        ctk.CTkLabel(tabview.tab("Profil"), text=adSoyad, font=commFont).place(x=120, y=50+20)

        ctk.CTkLabel(tabview.tab("Profil"), text="E-posta:", font=commFont2).place(x=20, y=80+20)
        ctk.CTkLabel(tabview.tab("Profil"), text=epostaBilgi, font=commFont).place(x=120, y=80+20)

        ctk.CTkLabel(tabview.tab("Profil"), text="Kayıt Tarihi:", font=commFont2).place(x=20, y=100+30)
        ctk.CTkLabel(tabview.tab("Profil"), text=kayitTarihBilgi, font=commFont).place(x=120, y=100+30)

        ctk.CTkLabel(tabview.tab("Profil"), text="Doğum Tarihi:", font=commFont2).place(x=20, y=130+30)
        ctk.CTkLabel(tabview.tab("Profil"), text=dogumTarihBilgi, font=commFont).place(x=120, y=130+30)


        # Şifrelerim Görünümü
        ctk.CTkLabel(tabview.tab("Şifrelerim"), text="Şifrelerim", font=headerFont).place(x=200, y=10)

        ctk.CTkLabel(tabview.tab("Şifrelerim"), text="Uygulama", font=commFont2).place(x=30, y=50)
        ctk.CTkLabel(tabview.tab("Şifrelerim"), text="Kullanıcı Adı", font=commFont2).place(x=160, y=50)
        ctk.CTkLabel(tabview.tab("Şifrelerim"), text="Şifre", font=commFont2).place(x=290, y=50)
        ctk.CTkLabel(tabview.tab("Şifrelerim"), text="__________________________________________________", font=commFont2, text_color='#579BB1').place(x=30, y=80)

        imlec.execute(f"SELECT uygulama_adi, hesap_adi, hesap_sifresi FROM sifreler_Tablosu WHERE uye_id = '{uyeID}'")
        sonuc = imlec.fetchall()
        arttırma = 1
        for i in sonuc:
                arttırma += 3
                yDeger = 80 + (arttırma * 10) 
                uygulama = i[0]
                hesapAdi = i[1]
                sifre=i[2]

                ctk.CTkLabel(tabview.tab("Şifrelerim"), text=f"{uygulama}", font=commFont, fg_color='#579BB1', corner_radius=50).place(x=30, y=yDeger)
                ctk.CTkLabel(tabview.tab("Şifrelerim"), text=f"{hesapAdi}", font=commFont).place(x=160, y=yDeger)
                ctk.CTkLabel(tabview.tab("Şifrelerim"), text=f"{sifre}", font=commFont).place(x=290, y=yDeger)

        
        # Şifre Oluştur görünümü
        ctk.CTkLabel(tabview.tab("Şifre Oluştur"), text="Şifre Oluşturma", font=headerFont).place(x=150, y=10)
        ctk.CTkLabel(tabview.tab("Şifre Oluştur"), text="Şifre oluşturmak için karakter uzunluğu seçin ve\noluşturulan şifreyi kopyalayın.", font=commFont).place(x=30, y=220)

        def optionmenu_callback(uzunluk):
                letters = string.ascii_letters
                digits = string.digits
                special_chars = string.punctuation
                alphabet = letters + digits + special_chars
                pwd_length = int(uzunluk)
                pwd = ''
                for i in range(pwd_length):
                        pwd += ''.join(secrets.choice(alphabet))

                veri_var.set(pwd)

        
        ctk.CTkLabel(tabview.tab("Şifre Oluştur"), text="Oluşturulan Şifre:", font=commFont2).place(x=40, y=100)
        veri_var=StringVar()
        ctk.CTkEntry(tabview.tab("Şifre Oluştur"), textvariable=veri_var, font=commFont, width=300, state="readonly").place(x=30, y=130)

        ctk.CTkOptionMenu(tabview.tab("Şifre Oluştur"), values=["8", "12", "16", "24", "32"],command=optionmenu_callback, width=300).place(x=30,y=180)

        # Ayarlar
        def sifreGuncelle():
                sifreGuncelle = ctk.CTkToplevel()
                sifreGuncelle.title("SSI Password Manager | Şifre Güncelle")
                sifreGuncelle.geometry("480x280+100+100")
                sifreGuncelle.resizable("false", "false")

                def dbYaz():
                        global uyeID
                        eskiSifre = eskiSifre_var.get()
                        yeniSifre = yeniSifre_var.get()
                        
                        if (yeniSifre == "" or eskiSifre == "" ):
                                messagebox.showinfo("Boş Alan Bırakılamaz","Kayıt girişlerinde boş alan bırakılamaz!")
                        else:
                                imlec.execute(f"SELECT sifre FROM kayit_Tablosu WHERE uye_id = '{uyeID}'")
                                sonuc = imlec.fetchall()
                                dbEskiSifre = sonuc[0][0]
                                if (eskiSifre == dbEskiSifre):
                                        imlec.execute(f"UPDATE kayit_Tablosu SET sifre = '{yeniSifre}' WHERE uye_id = '{uyeID}'")
                                        db.commit()
                                        messagebox.showinfo("İşlem Başarılı","Şifreniz başarıyla değiştirildi!")
                                        sifreGuncelle.destroy()
                                else:
                                        messagebox.showinfo("İşlem Başarısız","Eski şifreniz uyuşmuyor!") 

                ctk.CTkLabel(sifreGuncelle, text="Şifre Değiştir", font=headerFont).place(x=200, y=20)

                eskiSifre_var = StringVar()
                ctk.CTkLabel(sifreGuncelle, text="Eski şifre", font=infoFont).place(x=20, y=65)
                ctk.CTkEntry(sifreGuncelle, textvariable=eskiSifre_var, show="*").place(x=10, y=90)

                yeniSifre_var = StringVar()
                ctk.CTkLabel(sifreGuncelle, text="Yeni şifre", font=infoFont).place(x=20, y=120)
                ctk.CTkEntry(sifreGuncelle, textvariable=yeniSifre_var, show="*").place(x=10, y=145)

                ctk.CTkButton(sifreGuncelle, text="Şifreyi Kaydet", font=commFont, command=dbYaz).place(x=10, y=235)
             

                sifreGuncelle.mainloop()

        def detay():
                detay = ctk.CTkToplevel()
                detay.title("SSI Password Manager | Uygulama Hakkında")
                detay.geometry("680x280+100+100")
                detay.resizable("false", "false")

                ctk.CTkLabel(detay, text="Uygulama Hakkında", font=headerFont).place(x=20, y=20)
                ctk.CTkLabel(detay, text="MS SQL Bağlantısı ile kullanıcıların şifrelerini saklamasına olanak sağlayan program.", font=commFont).place(x=40, y=50)

                
                ctk.CTkLabel(detay, text="İletişim", font=headerFont).place(x=20, y=120)
                ctk.CTkLabel(detay, text="github.com/sonatipek", font=commFont).place(x=40, y=150)
                ctk.CTkLabel(detay, text="instagram.com/sonatipek", font=commFont).place(x=40, y=150+25)
                ctk.CTkLabel(detay, text="twitter.com/sonatipek", font=commFont).place(x=40, y=150+50)
                ctk.CTkLabel(detay, text="www.sonatipek.com", font=commFont).place(x=40, y=150+75)

                detay.mainloop()
        ctk.CTkLabel(tabview.tab("Ayarlar"), text="Ayarlar", font=headerFont).place(x=150, y=10)

        # Güvenlik Section
        ctk.CTkButton(tabview.tab("Ayarlar"), text="Güvenlik", font=commFont2, command=None, border_width=2, fg_color="transparent",corner_radius=0, state="disabled",border_color=("#3B8ED0", "#1F6AA5"), text_color_disabled=("#144870", "white")).place(x=30, y=50)
        # Şifre Değiştir
        ctk.CTkButton(tabview.tab("Ayarlar"), text="Şifre Değiştir", font=commFont, command=sifreGuncelle, border_width=2,corner_radius=0,border_color=("#3B8ED0", "#1F6AA5"), text_color=("black", "#DCE4EE"), width=250).place(x=100, y=76)

        # Uygulama Hakkında Section
        ctk.CTkButton(tabview.tab("Ayarlar"), text="Uygulama Hakkında", font=commFont2, command=None, border_width=2, fg_color="transparent",corner_radius=0, state="disabled",border_color=("#3B8ED0", "#1F6AA5"), text_color_disabled=("#144870", "white")).place(x=30, y=150)
        # Version
        ctk.CTkButton(tabview.tab("Ayarlar"), text="v1.0.0", font=commFont, command=None, border_width=2, fg_color="transparent",corner_radius=0,border_color=("#3B8ED0", "#1F6AA5"), text_color=("black", "#DCE4EE"),text_color_disabled=("#144870", "white"), state="disabled", width=250).place(x=100, y=176)
        # Yazılımcı
        ctk.CTkButton(tabview.tab("Ayarlar"), text="Author: Sonat Saygın İpek - SSI", font=commFont, command=None, border_width=2, fg_color="transparent",corner_radius=0,border_color=("#3B8ED0", "#1F6AA5"), text_color=("black", "#DCE4EE"),text_color_disabled=("#144870", "white"), state="disabled", width=250).place(x=100, y=176+26)
        # Bilgi
        ctk.CTkButton(tabview.tab("Ayarlar"), text="Detaylı Bilgi ve İletişim", font=commFont, command=detay, border_width=2, corner_radius=0,border_color=("#3B8ED0", "#1F6AA5"), text_color=("black", "#DCE4EE"), width=250).place(x=100, y=176+26+26)


        # Delete account
        def deleteAcc():
                global uyeID
                soru = ctk.CTkInputDialog(text="Hesabınız silinecek!\nSilinmesini istiyorsanız ''evet'' yazın:", title="Hesabınız Silinecek!")

                cevap = soru.get_input()
                if (cevap == 'evet'):
                        imlec.execute(f"DELETE FROM kayit_Tablosu WHERE uye_id = '{uyeID}'")
                        db.commit()
                        imlec.execute(f"DELETE FROM sifreler_Tablosu WHERE uye_id = '{uyeID}'")
                        db.commit()
                        messagebox.showinfo("İşlem Başarılı","Silme işlemi başarılı! Silme işlemi tamamlandıktan sonra uygulamadan çıkacaktır.")
                        homepageUI.destroy()
                        



        ctk.CTkButton(tabview.tab("Ayarlar"), text="Hesabı Sil", font=commFont, command=deleteAcc, border_width=2, corner_radius=0,border_color=("#3B8ED0", "#1F6AA5"), text_color=("black", "#DCE4EE"), width=250).place(x=10, y=600)


        # Çıkış Yap
        ctk.CTkButton(tabview.tab("Çıkış Yap"), text="Uygulamadan Çıkış Yap", font=commFont2, width=450, command=homepageUI.destroy).place(x=10, y=5)

        homepageUI.mainloop()
# *! Homepage Ekranı Bitiş



ctk.CTkLabel(mainWindow, text="SSI Password Manager", font=headerFont).place(x=150, y=30)

ePosta_var = StringVar()
ctk.CTkLabel(mainWindow, text="E-posta", font=infoFont).place(x=210, y=65)
ctk.CTkEntry(mainWindow, textvariable=ePosta_var).place(x=200, y=90)

sifre_var = StringVar()
ctk.CTkLabel(mainWindow, text="Şifre", font=infoFont).place(x=210, y=120)
ctk.CTkEntry(mainWindow, textvariable=sifre_var, show="*").place(x=200, y=145)

ctk.CTkButton(mainWindow, text="Giriş Yap", command=girisYap).place(x=200, y=180)
ctk.CTkButton(mainWindow, text="Şifremi Unuttum", command=sifremiUnuttum).place(x=200, y=210)



ctk.CTkButton(mainWindow, text="Hesabın yok mu? Kaydol!", command=kayıtOl).place(x=330, y=380)

ctk.CTkLabel(mainWindow, text="Tema").place(x=5,y=355)
ctk.CTkOptionMenu(mainWindow, values=["Dark", "Light", "System"], command=changeUI).place(x=5, y=380)



ctk.CTkLabel(mainWindow, text="© 2022 Sonat Saygın İpek | Bergama MYO Bilgisayar Programcılığı 2.Sınıf", font=infoFont).place(x=150, y=420)


mainWindow.mainloop()
