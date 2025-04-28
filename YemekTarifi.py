import tkinter as tk
from tkinter import messagebox

class Malzeme:
    def __init__(self, ad, miktar):
        self.ad = ad
        self.miktar = miktar

class Tarif:
    def __init__(self, ad, malzemeler, icerik):
        self.ad = ad
        self.malzemeler = malzemeler
        self.icerik = icerik
        self.puanlar = []

    def puan_ekle(self, puan):
        self.puanlar.append(puan)

    def puan_ortalamasi(self):
        if self.puanlar:
            return sum(self.puanlar) / len(self.puanlar)
        else:
            return 0

class TarifUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Yemek Tarifi Uygulaması")
        self.tarifler = []

        tk.Label(root, text="Tarif Adı:").grid(row=0, column=0)
        self.entry_tarif_adi = tk.Entry(root)
        self.entry_tarif_adi.grid(row=0, column=1)

        tk.Label(root, text="Malzemeler (virgülle ayır):").grid(row=1, column=0)
        self.entry_malzemeler = tk.Entry(root)
        self.entry_malzemeler.grid(row=1, column=1)

        tk.Label(root, text="İçerik:").grid(row=2, column=0)
        self.entry_icerik = tk.Entry(root)
        self.entry_icerik.grid(row=2, column=1)

        self.btn_tarif_ekle = tk.Button(root, text="Tarif Ekle", command=self.tarif_ekle)
        self.btn_tarif_ekle.grid(row=3, column=0, columnspan=2)

        tk.Label(root, text="Ara:").grid(row=4, column=0)
        self.entry_arama = tk.Entry(root)
        self.entry_arama.grid(row=4, column=1)
        self.entry_arama.bind("<KeyRelease>", self.tarif_ara)

        self.lst_sonuclar = tk.Listbox(root, width=50)
        self.lst_sonuclar.grid(row=5, column=0, columnspan=2)

        tk.Label(root, text="Puan (1-5):").grid(row=6, column=0)
        self.entry_puan = tk.Entry(root)
        self.entry_puan.grid(row=6, column=1)

        self.btn_puanla = tk.Button(root, text="Puan Ver", command=self.puan_ver)
        self.btn_puanla.grid(row=7, column=0, columnspan=2)

    def tarif_ekle(self):
        ad = self.entry_tarif_adi.get()
        malzemeler_text = self.entry_malzemeler.get()
        icerik = self.entry_icerik.get()

        if ad and malzemeler_text and icerik:
            malzeme_listesi = [Malzeme(m.strip(), "Belirtilmedi") for m in malzemeler_text.split(",")]
            yeni_tarif = Tarif(ad, malzeme_listesi, icerik)
            self.tarifler.append(yeni_tarif)
            messagebox.showinfo("Başarılı", "Tarif eklendi!")
            self.entry_tarif_adi.delete(0, tk.END)
            self.entry_malzemeler.delete(0, tk.END)
            self.entry_icerik.delete(0, tk.END)
            self.guncelle_tarif_listesi()  # Tüm tarifleri göster
        else:
            messagebox.showerror("Hata", "Tüm alanları doldurun!")

    def guncelle_tarif_listesi(self, filtre=""):
        self.lst_sonuclar.delete(0, tk.END)
        for tarif in self.tarifler:
            if filtre.lower() in tarif.ad.lower():
                ortalama_puan = tarif.puan_ortalamasi()
                malzeme_text = ", ".join([m.ad for m in tarif.malzemeler])
                self.lst_sonuclar.insert(tk.END, f"{tarif.ad} | Malzemeler: {malzeme_text} | Puan: {ortalama_puan:.1f}")

    def tarif_ara(self, event=None):
        aranan = self.entry_arama.get()
        self.guncelle_tarif_listesi(aranan)

    def puan_ver(self):
        secim = self.lst_sonuclar.curselection()
        if secim:
            try:
                puan = int(self.entry_puan.get())
                if puan < 1 or puan > 5:
                    raise ValueError
                secili_tarif_ad = self.lst_sonuclar.get(secim[0]).split(" | ")[0]
                for tarif in self.tarifler:
                    if tarif.ad == secili_tarif_ad:
                        tarif.puan_ekle(puan)
                        messagebox.showinfo("Başarılı", "Puan eklendi!")
                        self.tarif_ara()
                        break
            except ValueError:
                messagebox.showerror("Hata", "Lütfen 1 ile 5 arasında bir sayı girin!")
        else:
            messagebox.showerror("Hata", "Lütfen bir tarif seçin!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TarifUygulamasi(root)
    root.mainloop()
