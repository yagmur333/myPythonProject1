from tkinter import *
from tkinter import messagebox
import subprocess
import sqlite3

# Veritabanı bağlantısı
db = sqlite3.connect("sifreler.sqlite")
im = db.cursor()

# Kullanıcı kontrol fonksiyonu
def kontrol():
    kull = k_Adi_v.get()
    sif = sifre_v.get()

    if not kull or not sif:
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
        return

    kontrol_sorgu = "SELECT * FROM kullanicilar WHERE username = ? AND password = ?"
    im.execute(kontrol_sorgu, (kull, sif))
    data = im.fetchone()

    if data:
        messagebox.showinfo("Başarılı", "Hoşgeldiniz!")
        window.destroy()
        subprocess.run(["python", "icerik/not_defteri.py"])  # Yol yapına göre ayarla
    else:
        messagebox.showerror("Hatalı Giriş", "Kullanıcı adı veya şifre yanlış!")

def kaydol():
    kull = k_Adi_v.get()
    sif = sifre_v.get()

    if not kull or not sif:
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
        return

    # Kullanıcı zaten var mı kontrol et
    kontrol = "SELECT * FROM kullanicilar WHERE username = ?"
    im.execute(kontrol, (kull,))
    if im.fetchone():
        messagebox.showerror("Hata", "Bu kullanıcı adı zaten kayıtlı!")
        return

    # Yeni kullanıcıyı ekle
    im.execute("INSERT INTO kullanicilar (username, password) VALUES (?, ?)", (kull, sif))
    db.commit()
    messagebox.showinfo("Başarılı", "Kayıt başarıyla oluşturuldu!")


window = Tk()

window.geometry("994x616")
window.configure(bg="#ffffff")
canvas = Canvas(
    window,
    bg="#ffffff",
    height=616,
    width=994,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file="giris/background.png")
background = canvas.create_image(
    497.0, 308.0,
    image=background_img)

entry0_img = PhotoImage(
    file="giris/img_textBox0.png")
entry0_bg = canvas.create_image(
    736.5, 245.5,
    image=entry0_img)

k_Adi_v = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0)

k_Adi_v.place(
    x=594.0, y=224.0,
    width=285.0,
    height=41)

entry1_img = PhotoImage(
    file="giris/img_textBox1.png")
entry1_bg = canvas.create_image(
    736.5, 356.5,
    image=entry1_img)

sifre_v = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0,
    show="*")

sifre_v.place(
    x=594.0, y=335.0,
    width=285.0,
    height=41)

img0 = PhotoImage(file="giris/img0.png")
b0 = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=kontrol,
    relief="flat")

b_kaydol = Button(
    text="Kayıt Ol",
    command=kaydol,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold")
)
b_kaydol.place(x=594.0, y=412.0, width=135, height=43)


b0.place(
    x=759.0, y=412.0,
    width=135,
    height=43)

window.resizable(False, False)
window.mainloop()
