import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="8. Sınıf İnkılap Tarihi", page_icon="🇹🇷", layout="centered")

# --- VERİTABANI BAĞLANTISI ---
conn = sqlite3.connect('ogrenci_sonuclari.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sonuclar 
             (ad TEXT, soyad TEXT, sube TEXT, unite TEXT, dogru INTEGER, yanlis INTEGER, bos INTEGER, tarih TEXT)''')
conn.commit()

# --- MÜFREDAT ÜNİTELERİ (Sıralı) ---
mufredat = [
    "1. Ünite: Bir Kahraman Doğuyor",
    "2. Ünite: Millî Uyanış",
    "3. Ünite: Ya İstiklal Ya Ölüm!",
    "4. Ünite: Atatürkçülük ve Çağdaşlaşan Türkiye",
    "5. Ünite: Demokratikleşme Çabaları",
    "6. Ünite: Atatürk Dönemi Türk Dış Politikası",
    "7. Ünite: Atatürk'ün Ölümü ve Sonrası"
]

# --- SORU HAVUZU ---
# Her ünite için 20 soruluk listeleri buraya ekleyeceksiniz. 
sorular_db = {
    "1. Ünite: Bir Kahraman Doğuyor": [
        # (Önceki mesajdaki 20 soruyu buraya yapıştırın)
    ],
    "2. Ünite: Millî Uyanış": [
        # (Aşağıda verdiğim 20 soruyu buraya yapıştırın)
    ]
    # Diğer üniteler eklendikçe buraya eklenecek
}

if 'ogrenci' not in st.session_state:
    st.session_state.ogrenci = None
if 'secilen_unite' not in st.session_state:
    st.session_state.secilen_unite = None
if 'sinav_bitti' not in st.session_state:
    st.session_state.sinav_bitti = False

# --- ADMİN PANELİ ---
with st.sidebar:
    st.header("⚙️ Admin Paneli")
    if st.text_input("Şifre", type="password") == "1923":
        df = pd.read_sql_query("SELECT * FROM sonuclar", conn)
        if not df.empty:
            st.success(f"Toplam Çözüm: {len(df)}")
            st.dataframe(df)
            st.download_button("📥 Excel İndir", df.to_csv(index=False).encode('utf-8'), "sonuclar.csv", "text/csv")
        else:
            st.info("Veri yok.")

# --- ANA EKRAN ---
if st.session_state.ogrenci is None:
    st.title("🎓 LGS İnkılap Tarihi Görevleri")
    with st.form("giris"):
        ad = st.text_input("Adınız", max_chars=30)
        soyad = st.text_input("Soyadınız", max_chars=30)
        sube = st.selectbox("Şube", ["Seçiniz", "8/A", "8/B", "8/C", "8/D", "8/E"])
        if st.form_submit_button("Giriş Yap 🚀") and ad and soyad and sube != "Seçiniz":
            st.session_state.ogrenci = {'ad': ad.capitalize(), 'soyad': soyad.upper(), 'sube': sube}
            st.rerun()

elif st.session_state.ogrenci and st.session_state.secilen_unite is None:
    ogr = st.session_state.ogrenci
    st.title(f"Hoş Geldin, {ogr['ad']} 👋")
    
    c.execute("SELECT unite FROM sonuclar WHERE ad=? AND soyad=? AND sube=?", (ogr['ad'], ogr['soyad'], ogr['sube']))
    cozulenler = [r[0] for r in c.fetchall()]
    
    # 7 Üniteyi Otomatik Döngüye Sokup Kilitleri Kontrol Eden Sistem
    for i, unite_adi in enumerate(mufredat):
        st.subheader(f"📚 {unite_adi}")
        
        # Eğer sorular_db'ye henüz bu ünitenin sorularını eklemediyseniz "Yapım Aşamasında" der
        if unite_adi not in sorular_db or len(sorular_db[unite_adi]) == 0:
            st.warning("🚧 Sorular yükleniyor...")
        elif unite_adi in cozulenler:
            st.success("✅ Tamamlandı.")
        else:
            # İlk ünite değilse ve bir önceki ünite çözülmemişse kilitle
            if i > 0 and mufredat[i-1] not in cozulenler:
                st.error("🔒 KİLİTLİ: Önceki üniteyi bitirmelisin!")
            else:
                st.info("🔓 Görev Açık!")
                if st.button("▶️ Sınava Başla", key=f"btn_{i}"):
                    st.session_state.secilen_unite = unite_adi
                    st.rerun()
        st.markdown("---")
        
    if st.button("🚪 Çıkış"):
        st.session_state.ogrenci = None
        st.rerun()

elif st.session_state.secilen_unite and not st.session_state.sinav_bitti:
    st.title(st.session_state.secilen_unite)
    sorular = sorular_db[st.session_state.secilen_unite]
    
    with st.form("sinav"):
        cevaplar = []
        for i, s in enumerate(sorular):
            st.markdown(f"**{i+1})** {s['soru']}")
            cevap = st.radio("Cevap:", s['secenekler'], key=f"s_{i}", index=None)
            cevaplar.append(cevap)
            st.write("---")
            
        if st.form_submit_button("Bitir ve Gönder 📤"):
            if None in cevaplar:
                st.error("Lütfen boş soru bırakmayın!")
            else:
                dogru = sum([1 for i, c in enumerate(cevaplar) if c == sorular[i]['cevap']])
                yanlis = len(sorular) - dogru
                tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ogr = st.session_state.ogrenci
                
                c.execute("INSERT INTO sonuclar VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (ogr['ad'], ogr['soyad'], ogr['sube'], st.session_state.secilen_unite, dogru, yanlis, 0, tarih))
                conn.commit()
                st.session_state.sinav_bitti = True
                st.session_state.sonuc = (dogru, yanlis)
                st.rerun()

elif st.session_state.sinav_bitti:
    d, y = st.session_state.sonuc
    st.success("🎉 Sınav kaydedildi!")
    st.info(f"✅ Doğru: {d} | ❌ Yanlış: {y}")
    if st.button("🔙 Görevlere Dön"):
        st.session_state.secilen_unite = None
        st.session_state.sinav_bitti = False
        st.rerun()
