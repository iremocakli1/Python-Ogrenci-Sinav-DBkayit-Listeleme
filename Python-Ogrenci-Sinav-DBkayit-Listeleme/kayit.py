import sqlite3

class Ogrenci:
    def __init__(self, ad, soyad, vize, final):
        self.ad = ad
        self.soyad = soyad
        self.vize = vize
        self.final = final
        self.sonuc = ""

    def hesapla(self):
        ortalama = (self.vize + self.final) / 2
        if ortalama >= 50:
            self.sonuc = "G"
        else:
            self.sonuc = "K"

        conn = sqlite3.connect("sonuclar.db")
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students(
            ad CHAR(20) NOT NULL,
            soyad CHAR(20) NOT NULL,
            vize INTEGER NOT NULL,
            final INTEGER NOT NULL,
            sonuc CHAR(1)
        )''')

        cursor.execute('''
        INSERT INTO students(ad, soyad, vize, final, sonuc)
        VALUES (?, ?, ?, ?, ?)''', (self.ad, self.soyad, self.vize, self.final, self.sonuc))

        conn.commit()
        conn.close()

    def listele():
        conn = sqlite3.connect("sonuclar.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        if students:
            print("\n" + "-"*50)
            print(f"{'Ad':<20}{'Soyad':<20}{'Vize':<10}{'Final':<10}{'Sonuç':<10}")
            print("-"*50)
            for student in students:
                print(f"{student[0]:<20}{student[1]:<20}{student[2]:<10}{student[3]:<10}{student[4]:<10}")
            print("-"*50)
        else:
            print("Veritabanında kayıtlı öğrenci bulunmamaktadır.")

        conn.close()

while True:
    print("\n1 - Yeni öğrenci ekle")
    print("2 - Tüm öğrencileri listele")
    print("3 - Çık")

    secim = input("Bir seçenek girin (1, 2, 3): ")

    if secim == "1":
        ad = input("Öğrenci adı: ")
        if ad.lower() == 'q':
            print("Çıkılıyor...")
            break
        soyad = input("Öğrenci soyadı: ")
        vize = int(input("Öğrencinin vizeden aldığı puan: "))
        final = int(input("Öğrencinin finalden aldığı puan: "))

        ogrenci = Ogrenci(ad, soyad, vize, final)
        ogrenci.hesapla()
        print("Veriler veritabanına kaydedildi.")
    elif secim == "2":
        Ogrenci.listele()
    elif secim == "3":
        print("Çıkılıyor...")
        break
    else:
        print("Geçersiz seçim, tekrar deneyin.")
