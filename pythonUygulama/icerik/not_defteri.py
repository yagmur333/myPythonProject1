
from tkinter import *
from tkinter import messagebox
import sqlite3
import zipfile
import os
from datetime import datetime


def not_kaydet():
    baslik = entry0.get()
    icerik = entry1.get("1.0", END).strip()

    if not baslik or not icerik:
        messagebox.showwarning("Uyarı", "Başlık ve içerik boş olamaz.")
        return

    conn = sqlite3.connect("notlar.sqlite")
    cur = conn.cursor()
    cur.execute("INSERT INTO notlar (baslik, icerik) VALUES (?, ?)", (baslik, icerik))
    conn.commit()
    conn.close()
    messagebox.showinfo("Başarılı", "Not kaydedildi.")
    notlari_yukle()

def notlari_yukle():
    listbox.delete(0, END)
    conn = sqlite3.connect("notlar.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT id, baslik FROM notlar")
    for row in cur.fetchall():
        listbox.insert(END, f"{row[0]} - {row[1]}")
    conn.close()

def veritabani_yedekle():
    db_dosya = "notlar.sqlite"
    tarih = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_adi = f"yedek/notlar_yedek_{tarih}.zip"

    # "yedek" klasörü yoksa oluştur
    if not os.path.exists("yedek"):
        os.makedirs("yedek")

    with zipfile.ZipFile(zip_adi, 'w') as zipf:
        zipf.write(db_dosya, arcname="notlar.sqlite")

    messagebox.showinfo("Yedekleme Başarılı", f"Yedek oluşturuldu:\n{zip_adi}")


def not_guncelle():
    secilen = listbox.curselection()
    if not secilen:
        messagebox.showwarning("Uyarı", "Lütfen güncellenecek notu seçin.")
        return

    satir = listbox.get(secilen[0])
    not_id = int(satir.split(" - ")[0])

    yeni_baslik = entry0.get()
    yeni_icerik = entry1.get("1.0", END).strip()

    if not yeni_baslik or not yeni_icerik:
        messagebox.showwarning("Uyarı", "Başlık ve içerik boş olamaz.")
        return

    conn = sqlite3.connect("notlar.sqlite")
    cur = conn.cursor()
    cur.execute("UPDATE notlar SET baslik = ?, icerik = ? WHERE id = ?", (yeni_baslik, yeni_icerik, not_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Başarılı", "Not güncellendi.")
    notlari_yukle()

def not_sil():
    secilen = listbox.curselection()
    if not secilen:
        messagebox.showwarning("Uyarı", "Lütfen silinecek notu seçin.")
        return

    satir = listbox.get(secilen[0])
    not_id = int(satir.split(" - ")[0])

    cevap = messagebox.askyesno("Sil", "Bu notu silmek istediğinize emin misiniz?")
    if cevap:
        conn = sqlite3.connect("notlar.sqlite")
        cur = conn.cursor()
        cur.execute("DELETE FROM notlar WHERE id = ?", (not_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Silindi", "Not silindi.")
        notlari_yukle()
        entry0.delete(0, END)
        entry1.delete("1.0", END)

def on_note_select(event):
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        selected_note = listbox.get(index)
        not_id = int(selected_note.split(" - ")[0])

        conn = sqlite3.connect("notlar.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT baslik, icerik FROM notlar WHERE id = ?", (not_id,))
        note = cur.fetchone()
        conn.close()

        if note:
            entry0.delete(0, END)
            entry0.insert(0, note[0])
            entry1.delete("1.0", END)
            entry1.insert(END, note[1])

window = Tk()
window.geometry("900x700")
window.configure(bg="#ffffff")

canvas = Canvas(
    window,
    bg="#ffffff",
    height=700,
    width=900,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file="icerik/background.png")
background = canvas.create_image(450.0, 350.0, image=background_img)

entry0_img = PhotoImage(file="icerik/img_textBox0.png")
entry0_bg = canvas.create_image(561.0, 89.5, image=entry0_img)

entry0 = Entry(
    bd=0,
    bg="#d5d5d5",
    highlightthickness=0)
entry0.place(x=298.0, y=63.0, width=526.0, height=51)

entry1_img = PhotoImage(file="icerik/img_textBox1.png")
entry1_bg = canvas.create_image(561.0, 393.0, image=entry1_img)

entry1 = Text(
    bd=0,
    bg="#d5d5d5",
    highlightthickness=0)
entry1.place(x=298.0, y=179.0, width=526.0, height=426)

img2 = PhotoImage(file="icerik/img2.png")
b0 = Button(image=img2, borderwidth=0, highlightthickness=0, command=not_kaydet, relief="flat")
b0.place(x=713.0, y=624.0, width=121, height=37)

img1 = PhotoImage(file="icerik/img1.png")
b1 = Button(image=img1, borderwidth=0, highlightthickness=0, command=not_guncelle, relief="flat")
b1.place(x=561.0, y=624.0, width=121, height=37)

img0 = PhotoImage(file="icerik/img0.png")
b2 = Button(image=img0, borderwidth=0, highlightthickness=0, command=not_sil, relief="flat")
b2.place(x=288.0, y=624.0, width=121, height=37)

yedek_buton = Button(
    window,
    text="Yedek Al",
    command=veritabani_yedekle,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold")
)
yedek_buton.place(x=40, y=643, width=100, height=30)


listbox = Listbox(
    window,
    bd=0,
    bg="#e8e8e8",
    highlightthickness=0,
    font=("Arial", 10)
)
listbox.place(x=30, y=135, width=180, height=500)
listbox.bind('<<ListboxSelect>>', on_note_select)

notlari_yukle()

window.resizable(False, False)
window.mainloop()
