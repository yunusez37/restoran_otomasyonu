import sys
import subprocess
import os

def kutuphane_kontrol_ve_yukle():
    gerekli_paketler = ["pyodbc", "PySide6"]
    for paket in gerekli_paketler:
        try:
            __import__(paket)
        except ImportError:
            print(f"Modül eksik: {paket}. Sisteme yükleniyor, lütfen bekleyin...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", paket])
                print(f"{paket} başarıyla yüklendi!")
            except Exception as e:
                print(f"HATA: {paket} yüklenemedi. Detay: {e}")

kutuphane_kontrol_ve_yukle()

import pyodbc
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QGroupBox, QMessageBox, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

SERVER_NAME = r'DESKTOP-NFQ6RHC\SQLEXPRESS'
DATABASE_NAME = 'RestoranDB'

class GirisEkrani(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personel Girişi")
        self.setFixedSize(450, 550)

        self.setStyleSheet("""
            QWidget { background-color: #2c3e50; font-family: 'Segoe UI'; }
            QLabel { color: #ecf0f1; }
            QLineEdit {
                background-color: #ecf0f1; border: 2px solid #bdc3c7;
                border-radius: 20px; padding: 10px; font-size: 16px; color: #2c3e50;
            }
            QLineEdit:focus { border: 2px solid #e67e22; }
            QPushButton {
                background-color: #e67e22; color: white; border-radius: 20px;
                padding: 10px; font-weight: bold; font-size: 16px;
            }
            QPushButton:hover { background-color: #d35400; }
        """)
        self.arayuz_olustur()

    def arayuz_olustur(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        baslik = QLabel("ZEYTİNLİ\nRESTORAN")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(baslik)

        card = QFrame()
        card.setStyleSheet("background-color: #34495e; border-radius: 15px;")
        card.setFixedSize(350, 300)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0,0,0,80))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout()
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(30,30,30,30)

        lbl_info = QLabel("Giriş Şifresi: 1234")
        lbl_info.setStyleSheet("color: #bdc3c7; font-size: 14px;")
        lbl_info.setAlignment(Qt.AlignCenter)

        self.txt_sifre = QLineEdit()
        self.txt_sifre.setPlaceholderText("****")
        self.txt_sifre.setEchoMode(QLineEdit.Password)
        self.txt_sifre.setAlignment(Qt.AlignCenter)

        self.btn_giris = QPushButton("GİRİŞ YAP")
        self.btn_giris.setCursor(Qt.PointingHandCursor)
        self.btn_giris.clicked.connect(self.kontrol_et)

        card_layout.addWidget(lbl_info)
        card_layout.addWidget(self.txt_sifre)
        card_layout.addWidget(self.btn_giris)
        card.setLayout(card_layout)

        layout.addWidget(card)
        self.setLayout(layout)

    def kontrol_et(self):
        if self.txt_sifre.text() == "1234":
            self.ana_sayfa = RestoranOtomasyon()
            self.ana_sayfa.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Hatalı Şifre!")

class RestoranOtomasyon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restoran Yönetim Sistemi (MSSQL Bağlantılı)")
        self.setGeometry(100, 100, 1100, 750)
        self.secili_siparis_id = None
        self.baglanti = None

        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; }
            QLabel { color: #ecf0f1; font-family: 'Segoe UI'; font-weight: 500; }
            QLineEdit {
                background-color: #ecf0f1; border: 2px solid #bdc3c7; border-radius: 8px;
                padding: 8px; font-size: 14px; color: #2c3e50;
            }
            QGroupBox {
                color: #e67e22; font-weight: bold; border: 2px solid #34495e;
                border-radius: 15px; margin-top: 25px; background-color: #34495e;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 20px; padding: 0 5px; }
            QTableWidget {
                background-color: #ecf0f1; color: #2c3e50; gridline-color: #bdc3c7;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #2c3e50; color: white; padding: 8px; font-weight: bold;
            }
            QTableWidget::item:selected { background-color: #e67e22; color: white; }
        """)

        if self.veritabani_baglan():
            self.arayuz_olustur()
            self.verileri_yukle()

    def veritabani_baglan(self):
        try:
            connection_string = (
                f'DRIVER={{SQL Server}};'
                f'SERVER={SERVER_NAME};'
                f'DATABASE={DATABASE_NAME};'
                f'Trusted_Connection=yes;'
            )
            self.baglanti = pyodbc.connect(connection_string)
            self.imlec = self.baglanti.cursor()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Bağlantı Hatası",
                                 f"MSSQL'e bağlanılamadı!\n\nSunucu: {SERVER_NAME}\nVeritabanı: {DATABASE_NAME}\n\nHata: {str(e)}\n\nLütfen SQL Server'da 'RestoranDB' veritabanını oluşturduğunuzdan emin olun.")
            return False

    def arayuz_olustur(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        ana_layout = QVBoxLayout()

        ust_panel = QHBoxLayout()

        grp_sol = QGroupBox(" Masa & Sipariş ")
        lay_sol = QVBoxLayout()
        self.txt_masa = self.input_yap("Masa No:", lay_sol)
        self.txt_yemek = self.input_yap("Yemek:", lay_sol)
        self.txt_icecek = self.input_yap("İçecek:", lay_sol)

        self.btn_ekle = QPushButton("SİPARİŞ EKLE")
        self.btn_stil(self.btn_ekle, "#e67e22", "#d35400")
        self.btn_ekle.clicked.connect(self.siparis_ekle)
        lay_sol.addWidget(self.btn_ekle)
        grp_sol.setLayout(lay_sol)
        ust_panel.addWidget(grp_sol)

        grp_orta = QGroupBox(" Fiyatlandırma ")
        lay_orta = QVBoxLayout()
        self.txt_fyemek = self.input_yap("Yemek Fiyat:", lay_orta)
        self.txt_ficecek = self.input_yap("İçecek Fiyat:", lay_orta)

        lay_orta.addWidget(QLabel("TOPLAM:"))
        self.txt_toplam = QLineEdit()
        self.txt_toplam.setReadOnly(True)
        lay_orta.addWidget(self.txt_toplam)

        self.btn_hesapla = QPushButton("HESAPLA")
        self.btn_stil(self.btn_hesapla, "#e67e22", "#d35400")
        self.btn_hesapla.clicked.connect(self.hesapla)
        lay_orta.addWidget(self.btn_hesapla)
        grp_orta.setLayout(lay_orta)
        ust_panel.addWidget(grp_orta)

        grp_sag = QGroupBox(" İşlemler ")
        lay_sag = QVBoxLayout()

        btn_guncelle = QPushButton("GÜNCELLE")
        self.btn_stil(btn_guncelle, "#f39c12", "#e67e22")
        btn_guncelle.clicked.connect(self.siparis_guncelle)

        btn_sil = QPushButton("SİL")
        self.btn_stil(btn_sil, "#c0392b", "#a93226")
        btn_sil.clicked.connect(self.siparis_sil)

        btn_temizle = QPushButton("TEMİZLE")
        self.btn_stil(btn_temizle, "#7f8c8d", "#95a5a6")
        btn_temizle.clicked.connect(self.temizle)

        lay_sag.addWidget(btn_guncelle)
        lay_sag.addWidget(btn_sil)
        lay_sag.addWidget(btn_temizle)
        grp_sag.setLayout(lay_sag)
        ust_panel.addWidget(grp_sag)

        ana_layout.addLayout(ust_panel)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7)
        self.tablo.setHorizontalHeaderLabels(["ID", "Masa", "Yemek", "İçecek", "Y. Fiyat", "İ. Fiyat", "Toplam"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.cellClicked.connect(self.satir_secildi)
        ana_layout.addWidget(self.tablo)

        central_widget.setLayout(ana_layout)

    def input_yap(self, label, layout):
        lbl = QLabel(label)
        txt = QLineEdit()
        layout.addWidget(lbl)
        layout.addWidget(txt)
        return txt

    def btn_stil(self, btn, color, hover):
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"QPushButton {{ background-color: {color}; color: white; border-radius: 10px; padding: 10px; font-weight:bold; }} QPushButton:hover {{ background-color: {hover}; }}")

    def hesapla(self):
        try:
            f1 = float(self.txt_fyemek.text()) if self.txt_fyemek.text() else 0
            f2 = float(self.txt_ficecek.text()) if self.txt_ficecek.text() else 0
            toplam = f1 + f2
            self.txt_toplam.setText(f"{toplam:.2f}")
            return toplam
        except:
            return 0

    def siparis_ekle(self):
        toplam = self.hesapla()
        try:
            query = "INSERT INTO siparisler (masa_no, yemek_adi, icecek_adi, fiyat_yemek, fiyat_icecek, toplam_tutar) VALUES (?, ?, ?, ?, ?, ?)"
            val = (self.txt_masa.text(), self.txt_yemek.text(), self.txt_icecek.text(), self.txt_fyemek.text(), self.txt_ficecek.text(), toplam)
            self.imlec.execute(query, val)
            self.baglanti.commit()
            self.verileri_yukle()
            self.temizle()
            QMessageBox.information(self, "Bilgi", "Sipariş Eklendi!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def verileri_yukle(self):
        self.tablo.setRowCount(0)
        try:
            self.imlec.execute("SELECT * FROM siparisler")
            for row_idx, row_data in enumerate(self.imlec.fetchall()):
                self.tablo.insertRow(row_idx)
                for col_idx, col_data in enumerate(row_data):
                    self.tablo.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            print("Veri yükleme hatası:", e)

    def satir_secildi(self, row, col):
        self.secili_siparis_id = self.tablo.item(row, 0).text()
        self.txt_masa.setText(self.tablo.item(row, 1).text())
        self.txt_yemek.setText(self.tablo.item(row, 2).text())
        self.txt_icecek.setText(self.tablo.item(row, 3).text())
        self.txt_fyemek.setText(self.tablo.item(row, 4).text())
        self.txt_ficecek.setText(self.tablo.item(row, 5).text())
        self.txt_toplam.setText(self.tablo.item(row, 6).text())

    def siparis_guncelle(self):
        if not self.secili_siparis_id: return
        toplam = self.hesapla()
        try:
            query = "UPDATE siparisler SET masa_no=?, yemek_adi=?, icecek_adi=?, fiyat_yemek=?, fiyat_icecek=?, toplam_tutar=? WHERE id=?"
            val = (self.txt_masa.text(), self.txt_yemek.text(), self.txt_icecek.text(), self.txt_fyemek.text(), self.txt_ficecek.text(), toplam, self.secili_siparis_id)
            self.imlec.execute(query, val)
            self.baglanti.commit()
            self.verileri_yukle()
            QMessageBox.information(self, "Bilgi", "Güncellendi!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def siparis_sil(self):
        if self.secili_siparis_id:
            if QMessageBox.question(self, "Onay", "Silinsin mi?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
                try:
                    self.imlec.execute("DELETE FROM siparisler WHERE id=?", (self.secili_siparis_id,))
                    self.baglanti.commit()
                    self.verileri_yukle()
                    self.temizle()
                except Exception as e:
                    QMessageBox.critical(self, "Hata", str(e))

    def temizle(self):
        self.txt_masa.clear()
        self.txt_yemek.clear()
        self.txt_icecek.clear()
        self.txt_fyemek.clear()
        self.txt_ficecek.clear()
        self.txt_toplam.clear()
        self.secili_siparis_id = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    giris = GirisEkrani()
    giris.show()
    sys.exit(app.exec())
