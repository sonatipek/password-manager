from queue import Empty

from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
# from tkinter import ttk

import pyodbc

# *!Veritabanı Bağlantısı
# Bağlantı mssql windows auth
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
infoFont = ctk.CTkFont(size=9)

# Tema değiştirme kodları
def changeUI(new_appearance_mode):
    ctk.set_appearance_mode(new_appearance_mode)

# Griş yap butonuna tıklanıldığında tetiklenecek event
def girisYap():
    # Inputlardan girilen verilerin alınması
    girilen_eposta = ePosta_var.get()
    girilen_sifre = sifre_var.get()

    # Inputlar boşsa uyarı bildir, doluysa kayıt varlığını kontrol et
    if (girilen_eposta == "" or girilen_sifre == ""):
            messagebox.showinfo("Boş Alan Bırakılamaz","E-posta ve şifre alanları boş bırakılamaz!")
            
    else:
            imlec.execute(f"SELECT e_posta, sifre FROM kayit_Tablosu WHERE e_posta = '{girilen_eposta}'")
            sonuc = imlec.fetchall()

            # Inputlardaki sorgu sonunda hiç kayıt yoksa uyaru, kayıt varsa doğruluğunu kontrol et
            if (len(sonuc) <= 0):
                    messagebox.showinfo("Hesap Bulunamadı","Bu e-postaya kayıtlı bir hesap yok")
                    
            else:
                    # Bu döngü ile veritabanındaki e-posta ve şifrenin bir değişkene atanması yapılıyor.
                    # Zaten kayıt aşamasında e-posta kontrolü yapıldığından 2 adet kayıt dönmesi muhtemel değil.
                    for i in sonuc:
                            e_posta = i[0]
                            sifre = i[1]

                    if (girilen_eposta == e_posta and girilen_sifre == sifre):
                            messagebox.showinfo("Giriş Başarılı","Giriş başarılı, yönlendiriliyorsunuz!")
                            mainWindow.destroy()
    
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
    kayıtOl.geometry("720x480+150+150")
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

        #!TODO: DOĞUM TARİHİNE YA TAKVİM KOY YA DA BİLGİLENDİRME MESAJI
    dogumTarihi_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="Doğum Tarihi", font=infoFont).place(x=10, y=120)
    ctk.CTkEntry(kayıtOl, textvariable=dogumTarihi_var).place(x=10, y=145)

    ePosta_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="E-posta", font=infoFont).place(x=10, y=175)
    ctk.CTkEntry(kayıtOl, textvariable=ePosta_var).place(x=10, y=200)

    sifre_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="Şifre", font=infoFont).place(x=10, y=235)
    ctk.CTkEntry(kayıtOl, textvariable=sifre_var, show="*").place(x=10, y=260)


    guvenlikSoru_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="Güvenlik Sorunuz*", font=infoFont).place(x=10, y=290)
    ctk.CTkEntry(kayıtOl, textvariable=guvenlikSoru_var).place(x=10, y=315)

    gsCevap_var = StringVar()
    ctk.CTkLabel(kayıtOl, text="Güvenlik Sorunuzun Cevabı*", font=infoFont).place(x=175, y=290)
    ctk.CTkEntry(kayıtOl, textvariable=gsCevap_var).place(x=175, y=315)


    ctk.CTkLabel(kayıtOl, text="*: Güvenlik sorunuzu ve cevabını saklayınız. Unuttuğunuz taktirde hesabınızı kaybedebilirsiniz.", font=infoFont).place(x=10, y=345)

    ctk.CTkButton(kayıtOl, text="Kayıt Ol", command=kayıtOlButton).place(x=10, y=400)



    kayıtOl.mainloop()
# *! Kaydol Ekranı Bitiş

# *! Kiralama Ekranı
# def kiralamaEkrani():
#     kiralamaEkranim = Toplevel()
#     kiralamaEkranim.title("Bergama Araç Kiralama | Araç Kiralama Ekranı")
#     kiralamaEkranim.geometry("720x480+100+100")
#     kiralamaEkranim.resizable("false", "false")

    
#     kiralamaEkranim.mainloop()

# *! Kiralama Ekranı Bitiş


# *! Listeleme Ekranı

# def ListeEkrani():
    
#     listeEkranim.mainloop()

# *! Listeleme Ekranı Bitiş

# *! Listeleme Ekranı

# def ListeEkrani():
    
#     listeEkranim.mainloop()

# *! Listeleme Ekranı Bitiş

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