# Restoran Otomasyon Sistemi

Bu proje, restoranlar için masa yönetimi, sipariş takibi ve hesap işlemlerini gerçekleştiren modern bir masaüstü uygulamasıdır. Python (PySide6) ve MSSQL veritabanı mimarisi kullanılarak geliştirilmiştir.

<div align="center">
  <table>
    <tr>
      <td style="text-align: center">
        <img src="https://github.com/user-attachments/assets/25e1cef2-a299-4a3d-a707-025e5af7fb1d" width="300" alt="Giriş Ekranı">
        <br>
        <em>Giriş Ekranı</em>
      </td>
      <td style="text-align: center">
        <img src="https://github.com/user-attachments/assets/d1064050-70ea-4837-8592-b669e336d453" width="500" alt="Ana Arayüz">
        <br>
        <em>Ana Arayüz</em>
      </td>
    </tr>
  </table>
</div>


## Özellikler

* **Güvenli Giriş:** Personel için şifreli giriş ekranı.
* **Sipariş Yönetimi:** Masa bazlı sipariş ekleme, güncelleme ve silme.
* **Otomatik Hesaplama:** Yemek ve içecek fiyatlarını otomatik toplayan algoritma.
* **Veritabanı Entegrasyonu:** MSSQL ile güvenli veri saklama.
* **Modern Arayüz:** CSS ile özelleştirilmiş, kullanıcı dostu tasarım.

## Teknolojiler

* **Dil:** Python 3.11
* **Arayüz:** PySide6 (Qt)
* **Veritabanı:** Microsoft SQL Server (MSSQL)
* **Sürücü:** PyODBC

  **Tabloları Oluşturma:**
SQL Server'ı kurduktan sonra aşağıdaki sorguyu çalıştırarak gerekli veritabanı ve tabloyu oluşturun:

```sql
CREATE DATABASE RestoranDB;
GO
USE RestoranDB;
GO
CREATE TABLE siparisler (
    id INT PRIMARY KEY IDENTITY(1,1),
    masa_no NVARCHAR(50),
    yemek_adi NVARCHAR(100),
    icecek_adi NVARCHAR(100),
    fiyat_yemek DECIMAL(10,2),
    fiyat_icecek DECIMAL(10,2),
    toplam_tutar DECIMAL(10,2)
);
Aynı zamanda main.py dosyasında bulunan "SERVER_NAME = r'DESKTOP-XXXXXX\SQLEXPRESS'" kısmına kendi sunucu adınızı giriniz.

