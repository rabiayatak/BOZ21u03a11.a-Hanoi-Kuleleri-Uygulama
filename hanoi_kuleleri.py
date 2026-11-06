import tkinter as tk
from tkinter import messagebox

# Değişkenler
kule_sayisi = 3
halka_sayisi = 3
kuleler = []
secilen_kule = -1
hamle = 0

def cizimi_guncelle():
    canvas.delete("all")
    genislik = 800
    kule_araligi = genislik / kule_sayisi
    
    # Kuleleri (çubukları) çiz
    for i in range(kule_sayisi):
        x = (i + 0.5) * kule_araligi
        canvas.create_rectangle(x - 5, 100, x + 5, 350, fill="black")
        canvas.create_text(x, 370, text=f"Kule {i+1}", font=("Arial", 12, "bold"))
        
    # Halkaları çiz
    for i in range(kule_sayisi):
        x = (i + 0.5) * kule_araligi
        taban_y = 350
        for j, halka_boyutu in enumerate(kuleler[i]):
            halka_genisligi = 30 + (halka_boyutu * 25)
            y = taban_y - (j * 25)
            # Eğer halka seçiliyse rengini kırmızı yap
            renk = "red" if (secilen_kule == i and j == len(kuleler[i])-1) else "blue"
            canvas.create_rectangle(x - halka_genisligi/2, y - 20, 
                                    x + halka_genisligi/2, y, fill=renk)

def tiklama(event):
    global secilen_kule, hamle
    genislik = 800
    kule_araligi = genislik / kule_sayisi
    tiklanan_kule = int(event.x // kule_araligi)
    
    if tiklanan_kule < 0 or tiklanan_kule >= kule_sayisi:
        return

    if secilen_kule == -1:
        # Kule seçme ve en üstteki halkayı tutma
        if len(kuleler[tiklanan_kule]) > 0:
            secilen_kule = tiklanan_kule
            cizimi_guncelle()
    else:
        # Tutulan halkayı yeni kuleye bırakma
        if secilen_kule != tiklanan_kule:
            alinan_halka = kuleler[secilen_kule][-1]
            
            # Kural: Kule boş olmalı veya en üstteki halka bizimkinden büyük olmalı
            if len(kuleler[tiklanan_kule]) == 0 or kuleler[tiklanan_kule][-1] > alinan_halka:
                kuleler[tiklanan_kule].append(kuleler[secilen_kule].pop())
                hamle += 1
                bilgi_etiketi.config(text=f"Hamle: {hamle}")
                
                # Son kuleye hepsi dizildiyse kazanma uyarısı
                if len(kuleler[-1]) == halka_sayisi:
                    cizimi_guncelle()
                    messagebox.showinfo("Tebrikler", f"Oyunu {hamle} hamlede bitirdin!")
                    return
        
        secilen_kule = -1
        cizimi_guncelle()

def oyunu_baslat():
    global kuleler, secilen_kule, hamle, kule_sayisi, halka_sayisi
    
    # Kullanıcının girdiği değerleri al
    if int(kule_girdi.get()) >= 3 and int(halka_girdi.get()) >= 1:
        kule_sayisi = int(kule_girdi.get())
        halka_sayisi = int(halka_girdi.get())
        
    kuleler = [[] for _ in range(kule_sayisi)]
    
    # 1. kuleye halkaları büyükten küçüğe ekle
    for i in range(halka_sayisi, 0, -1):
        kuleler[0].append(i)
        
    secilen_kule = -1
    hamle = 0
    bilgi_etiketi.config(text=f"Hamle: {hamle}")
    cizimi_guncelle()

# Arayüzü oluştur
pencere = tk.Tk()
pencere.title("Hanoi Kuleleri")
pencere.geometry("850x550")

# Ayar menüsü
ust_cerceve = tk.Frame(pencere)
ust_cerceve.pack(pady=10)

tk.Label(ust_cerceve, text="Halka Sayısı:").pack(side=tk.LEFT)
halka_girdi = tk.Entry(ust_cerceve, width=5)
halka_girdi.insert(0, "3")
halka_girdi.pack(side=tk.LEFT, padx=5)

tk.Label(ust_cerceve, text="Kule Sayısı:").pack(side=tk.LEFT)
kule_girdi = tk.Entry(ust_cerceve, width=5)
kule_girdi.insert(0, "3")
kule_girdi.pack(side=tk.LEFT, padx=5)

tk.Button(ust_cerceve, text="Oyunu Başlat", command=oyunu_baslat).pack(side=tk.LEFT, padx=15)

bilgi_etiketi = tk.Label(pencere, text="Hamle: 0", font=("Arial", 14))
bilgi_etiketi.pack()

# Çizim alanı
canvas = tk.Canvas(pencere, width=800, height=450, bg="white")
canvas.pack(pady=10)
canvas.bind("<Button-1>", tiklama) # Fare ile tıklama algılayıcı

oyunu_baslat()
pencere.mainloop()
