from datetime import date
from flask import Flask, render_template, redirect, request, send_from_directory, session
import pyodbc
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
app.secret_key = 'gizli_anahtar' 
# Veritabanı bağlantısı
server = 'LAPTOP-NLQCE4VK'
database = 'havacılık_kurs_proje'
username = 'admin'
password = 'admin'
connection_string1 = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connect = pyodbc.connect(connection_string1)
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'C:\\Users\\erdem\\OneDrive\\Belgeler\\GitHub\\havacilikKurs\\proje güncel\\dekontlar'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/dekontlar')
def dekontlar():
    dekont_klasoru = app.config['UPLOAD_FOLDER']
    dekont_dosyalari = []

    for dosya_adi in os.listdir(dekont_klasoru):
        if os.path.isfile(os.path.join(dekont_klasoru, dosya_adi)):
            dekont_dosyalari.append(dosya_adi)

    return render_template('dekontlar.html', dekont_dosyalari=dekont_dosyalari)

@app.route('/dekontlar/goster/<path:dosya_adi>')
def dekont_goster(dosya_adi):
    dekont_klasoru = app.config['UPLOAD_FOLDER']
    return send_from_directory(dekont_klasoru, dosya_adi)

@app.route('/dekontlar/indir/<path:dosya_adi>')
def dekont_indir(dosya_adi):
    dekont_klasoru = app.config['UPLOAD_FOLDER']
    return send_from_directory(dekont_klasoru, dosya_adi, as_attachment=True)

# Kurs seçildiğinde ödeme sayfasına yönlendirme

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}  # Set the allowed file extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/kurslar')
def kurslar():
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurslar_ilan")
    kurslar_ilan = cursor.fetchall()
    cursor.close()
    return render_template("kurslar.html", kurslar_ilan=kurslar_ilan)


# Kurs ilanı ekleme
@app.route('/kurs_ekle', methods=['GET', 'POST'])
def kurs_ekle():
    if request.method == 'POST':
        # Retrieve form data
        kurs_adi = request.form.get('kurs_adi')
        kurs_veren_okul = request.form.get('kurs_veren_okul')
        kurs_admin_username = request.form.get('kurs_admin_username')
        kurs_aciklama = request.form.get('kurs_aciklama')
        kurs_tarih = request.form.get('kurs_tarih')
        kurs_kontenjan = request.form.get('kurs_kontenjan')
        kurs_fiyat = request.form.get('kurs_fiyat')

        try:
            cursor = connect.cursor()
            cursor.execute("""
                INSERT INTO kurslar_ilan (kurs_adi, kurs_veren_okul, kurs_admin_username, kurs_aciklama, kurs_tarih, kurs_kontenjan, kurs_fiyat)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (kurs_adi, kurs_veren_okul, kurs_admin_username, kurs_aciklama, kurs_tarih, kurs_kontenjan, kurs_fiyat))

            connect.commit()
            cursor.close()

            return redirect('/admin_panel')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Kurs eklenirken bir hata oluştu.');</script>"
    else:
        cursor = connect.cursor()
        cursor.execute("SELECT kurs_adi FROM kurs")
        kurslar = cursor.fetchall()
        cursor.close()
        return render_template("kurs_ekle.html", kurslar=kurslar)

@app.route('/kullanici_kurs_ekle/<string:username>', methods=['GET', 'POST'])
def kullanici_kurs_ekle(username):
    if request.method == 'POST':
        # Retrieve form data
        kurs_adi = request.form.get('kurs_adi')
        kurs_veren_okul = request.form.get('kurs_veren_okul')
        kurs_admin_username = username
        kurs_aciklama = request.form.get('kurs_aciklama')
        kurs_tarih = request.form.get('kurs_tarih')
        kurs_kontenjan = request.form.get('kurs_kontenjan')
        kurs_fiyat = request.form.get('kurs_fiyat')

        try:
            cursor = connect.cursor()
            cursor.execute("""
                INSERT INTO kurslar_ilan (kurs_adi, kurs_veren_okul, kurs_admin_username, kurs_aciklama, kurs_tarih, kurs_kontenjan, kurs_fiyat)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (kurs_adi, kurs_veren_okul, kurs_admin_username, kurs_aciklama, kurs_tarih, kurs_kontenjan, kurs_fiyat))

            connect.commit()
            cursor.close()

            return redirect('/kullanici_giris')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Kurs eklenirken bir hata oluştu.');</script>"
    else:
        cursor = connect.cursor()
        cursor.execute("SELECT kurs_adi FROM kurs")
        kurslar = cursor.fetchall()
        cursor.close()
        return render_template("kullanici_kurs_ekle.html", kurslar=kurslar,username=username)

@app.route('/ilanlar')
def ilanlar():
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurslar_ilan")
    ilanlar = cursor.fetchall()
    cursor.close()
    return render_template("ilanlar.html", ilanlar=ilanlar)

# Kurs ilanı düzenleme
@app.route('/kurs_duzenle/<int:kurs_ilan_id>', methods=['GET', 'POST'])
def kurs_duzenle(kurs_ilan_id):
    if request.method == 'POST':
        # Retrieve form data
        kurs_adi = request.form.get('kurs_adi')
        kurs_veren_okul = request.form.get('kurs_veren_okul')
        kurs_admin_username = request.form.get('kurs_admin_username')
        kurs_aciklama = request.form.get('kurs_aciklama')
        kurs_tarih = request.form.get('kurs_tarih')
        kurs_kontenjan = request.form.get('kurs_kontenjan')
        kurs_fiyat = request.form.get('kurs_fiyat')

        try:
            cursor = connect.cursor()
            cursor.execute("""
            UPDATE kurslar_ilan
            SET kurs_adi=?, kurs_veren_okul=?, kurs_admin_username=?, kurs_aciklama=?, kurs_tarih=?, kurs_kontenjan=?, kurs_fiyat=?
            WHERE kurs_ilan_id=?
            """, (kurs_adi, kurs_veren_okul, kurs_admin_username, kurs_aciklama, kurs_tarih, kurs_kontenjan, kurs_fiyat, kurs_ilan_id))

            connect.commit()
            cursor.close()

            return redirect('/kurslar')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Kurs ilanı düzenlenirken bir hata oluştu.');</script>"
    else:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM kurslar_ilan WHERE kurs_ilan_id=?", (kurs_ilan_id,))
        kurs = cursor.fetchone()
        cursor.close()
        return render_template("kurs_duzenle.html", kurs=kurs)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form.get('admin_username')
        admin_password = request.form.get('admin_password')

        cursor = connect.cursor()
        cursor.execute("""
            SELECT *
            FROM master_admin
            WHERE admin_username = ? AND admin_password = ?
        """, (admin_username, admin_password))
        admin = cursor.fetchone()
        cursor.close()

        if admin:
            return redirect('/admin_panel')
        else:
            return "<script>alert('Geçersiz kullanıcı adı veya şifre.');</script>"
    else:
        return render_template('admin_login.html')

@app.route('/admin_panel')
def admin_panel():
    dekont_klasoru = app.config['UPLOAD_FOLDER']
    dekont_dosyalari = []

    for dosya_adi in os.listdir(dekont_klasoru):
        if os.path.isfile(os.path.join(dekont_klasoru, dosya_adi)):
            dekont_dosyalari.append(dosya_adi)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurs")
    dersler = cursor.fetchall()
    
    
    cursor.execute("SELECT * FROM ogrenci")
    ogrenciler = cursor.fetchall()
    

    # İlanları al
    cursor.execute("SELECT * FROM kurslar_ilan")
    ilanlar = cursor.fetchall()

    # Rezervasyonları al
    cursor.execute("""
        SELECT r.rezervasyon_id, r.rezervasyon_tarih, o.ogrenci_isim, o.ogrenci_soyisim, r.kurs_ilan_id
        FROM rezervasyonlar r
        INNER JOIN ogrenci o ON r.ogrenci_id = o.ogrenci_id
    """)
    rezervasyonlar = cursor.fetchall()

    # Kullanıcıları al
    cursor.execute("SELECT * FROM kurs_admin")
    kullanici_listesi = cursor.fetchall()

    cursor.close()

    return render_template("admin_panel.html",ogrenciler=ogrenciler,dekont_dosyalari=dekont_dosyalari,dersler=dersler, ilanlar=ilanlar, rezervasyonlar=rezervasyonlar, kullanici_listesi=kullanici_listesi)
# Kullanıcı Ekle
@app.route('/kullanici_ekle', methods=['GET', 'POST'])
def kullanici_ekle():
    if request.method == 'POST':
        username = request.form.get('kurs_admin_username')
        password = request.form.get('kurs_admin_password')

        try:
            cursor = connect.cursor()
            cursor.execute("""
            INSERT INTO kurs_admin (kurs_admin_username, kurs_admin_password)
            VALUES (?, ?)
            """, (username, password))
            connect.commit()
            cursor.close()

            return redirect('/admin_panel')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Kullanıcı eklerken bir hata oluştu.');</script>"
    else:
        return render_template("kullanici_ekle.html")

# Kullanıcı Sil
@app.route('/kullanici_sil/<string:username>')
def kullanici_sil(username):
    try:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM kurs_admin WHERE kurs_admin_username=?", (username,))
        connect.commit()
        cursor.close()

        return redirect('/admin_panel')
    except Exception as e:
        print("Hata:", str(e))
        return "<script>alert('Kullanıcı silerken bir hata oluştu.');</script>"
# Eski kodlarınızın devamı...
@app.route('/ogrenciler')
def ogrenciler():
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM ogrenci")
    ogrenciler = cursor.fetchall()
    cursor.close()
    return render_template("ogrenciler.html", ogrenciler=ogrenciler)
# Eski kodlarınızın devamı...
@app.route('/ogrenci_ekle', methods=['GET', 'POST'])
def ogrenci_ekle():
    if request.method == 'POST':
        ogrenci_isim = request.form.get('ogrenci_isim')
        ogrenci_soyisim = request.form.get('ogrenci_soyisim')
        ogrenci_telefon = request.form.get('ogrenci_telefon')
        ogrenci_email = request.form.get('ogrenci_email')

        try:
            cursor = connect.cursor()
            cursor.execute("""
            INSERT INTO ogrenci (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon_no, ogrenci_email)
            VALUES (?, ?, ?, ?)
            """, (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon, ogrenci_email))

            connect.commit()
            cursor.close()

            return redirect('/ogrenciler')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Öğrenci eklenirken bir hata oluştu.');</script>"
    else:
        return render_template("ogrenci_ekle.html")

@app.route('/ogrenci_duzenle/<int:ogrenci_id>', methods=['GET', 'POST'])
def ogrenci_duzenle(ogrenci_id):
    if request.method == 'POST':
        ogrenci_isim = request.form.get('ogrenci_isim')
        ogrenci_soyisim = request.form.get('ogrenci_soyisim')
        ogrenci_telefon = request.form.get('ogrenci_telefon')
        ogrenci_email = request.form.get('ogrenci_email')

        try:
            cursor = connect.cursor()
            cursor.execute("""
            UPDATE ogrenci
            SET ogrenci_isim=?, ogrenci_soyisim=?, ogrenci_telefon_no=?, ogrenci_email=?
            WHERE ogrenci_id=?
            """, (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon, ogrenci_email, ogrenci_id))

            connect.commit()
            cursor.close()

            return redirect('/ogrenciler')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Öğrenci düzenlenirken bir hata oluştu.');</script>"
    else:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM ogrenci WHERE ogrenci_id=?", (ogrenci_id,))
        ogrenci = cursor.fetchone()
        cursor.close()
        return render_template("ogrenci_duzenle.html", ogrenci=ogrenci)

@app.route('/ogrenci_sil/<int:ogrenci_id>')
def ogrenci_sil(ogrenci_id):
    try:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM ogrenci WHERE ogrenci_id=?", (ogrenci_id,))

        connect.commit()
        cursor.close()

        return redirect('/ogrenciler')
    except Exception as e:
        print("Hata:", str(e))
        return "<script>alert('Öğrenci silme sırasında bir hata oluştu.');</script>"

# Kullanıcı Düzenle
@app.route('/kullanici_duzenle/<string:username>', methods=['GET', 'POST'])
def kullanici_duzenle(username):
    if request.method == 'POST':
        new_username = request.form.get('kurs_admin_username')
        new_password = request.form.get('kurs_admin_password')

        try:
            cursor = connect.cursor()
            cursor.execute("""
            UPDATE kurs_admin
            SET kurs_admin_username=?, kurs_admin_password=?
            WHERE kurs_admin_username=?
            """, (new_username, new_password, username))
            connect.commit()
            cursor.close()

            return redirect('/admin_panel')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Kullanıcı düzenlerken bir hata oluştu.');</script>"
    else:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM kurs_admin WHERE kurs_admin_username=?", (username,))
        kullanici = cursor.fetchone()
        cursor.close()
        return render_template("kullanici_duzenle.html", kullanici=kullanici)

# Kurs ilanı silme
@app.route('/kurs_sil/<int:kurs_ilan_id>')
def kurs_sil(kurs_ilan_id):
    try:
        cursor = connect.cursor()

        # İlgili kurs ilanını kontrol et
        cursor.execute("SELECT * FROM kurslar_ilan WHERE kurs_ilan_id=?", (kurs_ilan_id,))
        ilan = cursor.fetchone()

        if ilan:
            # İlgili rezervasyonları sil
            cursor.execute("DELETE FROM rezervasyonlar WHERE kurs_ilan_id=?", (kurs_ilan_id,))
            connect.commit()

            # Kurs ilanını sil
            cursor.execute("DELETE FROM kurslar_ilan WHERE kurs_ilan_id=?", (kurs_ilan_id,))
            connect.commit()

            cursor.close()

            return redirect('/kurslar')
        else:
            return "<script>alert('İlgili kurs ilanı bulunamadı.');</script>"
    except Exception as e:
        print("Hata:", str(e))
        return "<script>alert('Kurs ilanı silme sırasında bir hata oluştu.');</script>"

@app.route('/odeme/<int:kurs_ilan_id>', methods=['GET', 'POST'])
def odeme(kurs_ilan_id):
    if request.method == 'POST':
        isim_soyisim = request.form.get('ogrenci_bilgileri')
        
        dekont = request.files['dekont']
        if dekont and allowed_file(dekont.filename):
            # Dosya adını kurs_ilan_id ve isim_soyisim ile birlikte kaydet
            filename = secure_filename(f"{kurs_ilan_id}_{isim_soyisim}.{dekont.filename.rsplit('.', 1)[1].lower()}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            dekont.save(filepath)

        return redirect('/kurs_detay/' + str(kurs_ilan_id))
    else:
        return render_template('odeme.html', kurs_ilan_id=kurs_ilan_id)

@app.route('/kurs_detay/<int:kurs_ilan_id>')
def kurs_detay(kurs_ilan_id):
    
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurslar_ilan WHERE kurs_ilan_id=?", (kurs_ilan_id,))
    kurs = cursor.fetchone()
    cursor.close()

    return render_template("kurs_detay.html", kurs=kurs)

@app.route('/rezervasyon/<int:kurs_ilan_id>', methods=["GET", "POST"])
def rezervasyon(kurs_ilan_id):
    if request.method == 'POST':
        try:
            # Form verilerini al
            ogrenci_isim = request.form.get('ogrenci_isim')
            ogrenci_soyisim = request.form.get('ogrenci_soyisim')
            ogrenci_telefon = request.form.get('ogrenci_telefon')
            ogrenci_email = request.form.get('ogrenci_email')

            cursor = connect.cursor()

            # Öğrencinin ogrenci tablosunda zaten var olup olmadığını kontrol et
            cursor.execute("""
                SELECT ogrenci_id FROM ogrenci
                WHERE ogrenci_isim = ? AND ogrenci_soyisim = ? 
                AND ogrenci_telefon_no = ? AND ogrenci_email = ?
            """, (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon, ogrenci_email))
            
            existing_student = cursor.fetchone()

            if existing_student:
                ogrenci_id = existing_student[0]
            else:
                # Yeni öğrenciyi ogrenci tablosuna ekle
                cursor.execute("""
                    INSERT INTO ogrenci (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon_no, ogrenci_email)
                    OUTPUT inserted.ogrenci_id
                    VALUES (?, ?, ?, ?)
                """, (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon, ogrenci_email))
                row = cursor.fetchone()  # Son eklenen satırı al
                ogrenci_id = row[0]  # Öğrenci ID'sini al

            connect.commit()

            # Rezervasyon için gerekli bilgileri al ve rezervasyon yap
            cursor.execute("SELECT * FROM kurslar_ilan WHERE kurs_ilan_id=?", (kurs_ilan_id,))
            ilan = cursor.fetchone()

            today = date.today()
            rezervasyon_tarih = today.strftime("%Y-%m-%d")

            cursor.execute("""
                INSERT INTO rezervasyonlar (kurs_ilan_id, ogrenci_id, rezervasyon_tarih)
                VALUES (?, ?, ?)
                """, (kurs_ilan_id, ogrenci_id, rezervasyon_tarih))
            connect.commit()

            # Kurs kontenjanını azalt
            cursor.execute("""
                UPDATE kurslar_ilan
                SET kurs_kontenjan = kurs_kontenjan - 1
                WHERE kurs_ilan_id = ?
                AND kurs_kontenjan > 0
            """, (kurs_ilan_id,))
            connect.commit()

            cursor.close()

            # Başarılı rezervasyon için şablonu döndür
            return render_template("rezervasyon_basarili.html", ogrenci_isim=ogrenci_isim, ogrenci_soyisim=ogrenci_soyisim,
                                   ogrenci_telefon=ogrenci_telefon, ogrenci_email=ogrenci_email,
                                   kurs_ilan_id=ilan.kurs_ilan_id, kurs_adi=ilan.kurs_adi, aciklama=ilan.kurs_aciklama)
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Rezervasyon sırasında bir hata oluştu.');</script>"
    else:
        # Sayfayı göster
        return render_template("rezervasyon.html")



# Rezervasyonları listeleme
@app.route('/rezervasyonlar')
def rezervasyonlar():
    cursor = connect.cursor()
    cursor.execute("""
        SELECT r.rezervasyon_id, r.rezervasyon_tarih, o.ogrenci_isim, o.ogrenci_soyisim, k.kurs_adi, k.kurs_veren_okul, k.kurs_admin_username, k.kurs_kontenjan
        FROM rezervasyonlar r
        INNER JOIN ogrenci o ON r.ogrenci_id = o.ogrenci_id
        INNER JOIN kurslar_ilan k ON r.kurs_ilan_id = k.kurs_ilan_id
    """)
    rezervasyonlar = cursor.fetchall()
    cursor.close()

    fully_booked_kurslar = [rezervasyon for rezervasyon in rezervasyonlar if rezervasyon.kurs_kontenjan <= 0]
    available_kurslar = [rezervasyon for rezervasyon in rezervasyonlar if rezervasyon.kurs_kontenjan > 0]

    return render_template("rezervasyonlar.html", fully_booked_kurslar=fully_booked_kurslar, available_kurslar=available_kurslar)


@app.route('/rezervasyon_sil/<int:rezervasyon_id>')
def rezervasyon_sil(rezervasyon_id):
    try:
        cursor = connect.cursor()
        
        # Rezervasyon bilgilerini al
        cursor.execute("SELECT kurs_ilan_id FROM rezervasyonlar WHERE rezervasyon_id=?", (rezervasyon_id,))
        rezervasyon = cursor.fetchone()
        kurs_ilan_id = rezervasyon.kurs_ilan_id
        
        # Rezervasyonu sil
        cursor.execute("DELETE FROM rezervasyonlar WHERE rezervasyon_id=?", (rezervasyon_id,))
        
        # Kurs kontenjanını güncelle
        cursor.execute("""
            UPDATE kurslar_ilan
            SET kurs_kontenjan = kurs_kontenjan + 1
            WHERE kurs_ilan_id = ?
        """, (kurs_ilan_id,))
        
        connect.commit()
        cursor.close()

        return redirect('/rezervasyonlar')
    except Exception as e:
        print("Hata:", str(e))
        return "<script>alert('Rezervasyon silme sırasında bir hata oluştu.');</script>"

@app.route('/rezervasyon_duzenle/<int:rezervasyon_id>', methods=['GET', 'POST'])
def rezervasyon_duzenle(rezervasyon_id):
    if request.method == 'POST':
        # Retrieve form data
        ogrenci_isim = request.form.get('ogrenci_isim')
        ogrenci_soyisim = request.form.get('ogrenci_soyisim')
        kurs_adi = request.form.get('kurs_adi')
        rezervasyon_tarih = request.form.get('rezervasyon_tarih')

        # Perform database updates
        cursor = connect.cursor()

        # Update 'ogrenci' table
        cursor.execute("""
            UPDATE ogrenci
            SET ogrenci_isim=?, ogrenci_soyisim=?
            WHERE ogrenci_id IN (
                SELECT ogrenci_id
                FROM rezervasyonlar
                WHERE rezervasyon_id=?
            )
        """, (ogrenci_isim, ogrenci_soyisim, rezervasyon_id))

        # Update 'kurslar_ilan' table
        cursor.execute("""
            UPDATE kurslar_ilan
            SET kurs_adi=?
            WHERE kurs_ilan_id IN (
                SELECT kurs_ilan_id
                FROM rezervasyonlar
                WHERE rezervasyon_id=?
            )
        """, (kurs_adi, rezervasyon_id))

        connect.commit()
        cursor.close()

        return redirect('/rezervasyonlar')


    else:
        cursor = connect.cursor()
        cursor.execute("""
            SELECT r.rezervasyon_id, r.rezervasyon_tarih, o.ogrenci_isim, o.ogrenci_soyisim, k.kurs_adi
            FROM rezervasyonlar r
            INNER JOIN ogrenci o ON r.ogrenci_id = o.ogrenci_id
            INNER JOIN kurslar_ilan k ON r.kurs_ilan_id = k.kurs_ilan_id
            WHERE r.rezervasyon_id=?
        """, (rezervasyon_id,))
        rezervasyon = cursor.fetchone()
        cursor.close()
        return render_template("rezervasyon_duzenle.html", rezervasyon=rezervasyon)
@app.route('/kullanicilar')
def kullanicilar():
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurs_admin")
    kullanici_listesi = cursor.fetchall()
    cursor.close()
    return render_template("kullanicilar.html", kullanici_listesi=kullanici_listesi)
@app.route('/kullanici_giris', methods=['GET', 'POST'])
def kullanici_giris():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Kullanıcı adı ve şifreyi kontrol et
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM kurs_admin WHERE kurs_admin_username = ? AND kurs_admin_password = ?", (username, password))
        kullanici = cursor.fetchone()
            # Kullanıcının ilanlarını getir
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM kurslar_ilan WHERE kurs_admin_username = ?", (username,))
        ilanlar = cursor.fetchall()
            # Kullanıcının rezervasyonlarını getir
        cursor.execute("""
        SELECT o.ogrenci_isim, o.ogrenci_soyisim, k.kurs_adi, k.kurs_aciklama, r.rezervasyon_tarih
        FROM rezervasyonlar r
        INNER JOIN ogrenci o ON r.ogrenci_id = o.ogrenci_id
        INNER JOIN kurslar_ilan k ON r.kurs_ilan_id = k.kurs_ilan_id
        WHERE k.kurs_admin_username = ?
        """, (username))

        rezervasyonlar = cursor.fetchall()

        cursor.close()

        if kullanici:
            
            return render_template('/kullanici_panel.html',username=username,ilanlar=ilanlar,rezervasyonlar=rezervasyonlar)
        else:
            return "<script>alert('Geçersiz kullanıcı adı veya şifre.');</script>"
    else:
        return render_template('kullanici_giris.html')
@app.route('/kullanici_panel')
def kullanici_panel():
    return render_template('kullanici_panel.html')
@app.route('/ders_ekle', methods=['GET', 'POST'])
def ders_ekle():
    if request.method == 'POST':
        # Form verilerini al
        kurs_adi = request.form.get('kurs_adi')
        kurs_aciklama = request.form.get('kurs_aciklama')

        try:
            cursor = connect.cursor()
            cursor.execute("""
            INSERT INTO kurs (kurs_adi, kurs_aciklama)
            VALUES (?, ?)
            """, (kurs_adi, kurs_aciklama))

            connect.commit()
            cursor.close()

            return redirect('/admin_panel')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Ders eklenirken bir hata oluştu.');</script>"
    else:
        return render_template("ders_ekle.html")
# Ders düzenleme
@app.route('/ders_duzenle/<int:kurs_id>', methods=['GET', 'POST'])
def ders_duzenle(kurs_id):
    if request.method == 'POST':
        kurs_adi = request.form.get('kurs_adi')
        kurs_aciklama = request.form.get('kurs_aciklama')

        try:
            cursor = connect.cursor()
            cursor.execute("""
            UPDATE kurs
            SET kurs_adi=?, kurs_aciklama=?
            WHERE kurs_id=?
            """, (kurs_adi, kurs_aciklama, kurs_id))

            connect.commit()
            cursor.close()

            return redirect('/dersler')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Ders düzenlenirken bir hata oluştu.');</script>"
    else:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM kurs WHERE kurs_id=?", (kurs_id,))
        ders = cursor.fetchone()
        cursor.close()
        return render_template("ders_duzenle.html", ders=ders)

# Ders silme
@app.route('/ders_sil/<int:kurs_id>')
def ders_sil(kurs_id):
    try:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM kurs WHERE kurs_id=?", (kurs_id,))

        connect.commit()
        cursor.close()

        return redirect('/dersler')
    except Exception as e:
        print("Hata:", str(e))
        return "<script>alert('Ders silme sırasında bir hata oluştu.');</script>"
# Dersleri listeleme
@app.route('/dersler')
def dersler():
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurs")
    dersler = cursor.fetchall()
    cursor.close()
    return render_template("dersler.html", dersler=dersler)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
