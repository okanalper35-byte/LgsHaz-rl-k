import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Mobil uyumlu görünüm ve sayfa ayarları
st.set_page_config(page_title="8. Sınıf İnkılap Tarihi Sınavı", page_icon="🇹🇷", layout="centered")

# Veritabanı bağlantısı (Sonuçları kaydetmek için)
conn = sqlite3.connect('ogrenci_sonuclari.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sonuclar 
             (ad TEXT, soyad TEXT, sube TEXT, dogru INTEGER, yanlis INTEGER, bos INTEGER, tarih TEXT)''')
conn.commit()

# 1. Ünite Soruları (Örnek olarak ilk 5 soruyu ekledim, dilediğiniz kadar uzatabilirsiniz)
sorular = [
    {
        "soru": "Soru 1: Sanayi İnkılabı ile Avrupa'da seri üretime geçilmiş... Buna göre hangisi Sanayi İnkılabı'nın Osmanlı Devleti'ne etkilerinden biri değildir?",
        "secenekler": ["A) Yerli esnafın rekabet gücünü kaybetmesi", "B) İthalatın artması", "C) Ekonomik bağımsızlığın güçlenmesi", "D) Ülkenin hammadde kaynağı olarak görülmesi"],
        "cevap": "C) Ekonomik bağımsızlığın güçlenmesi"
    },
    {
        "soru": "Soru 2: Fransız İhtilali'nin yaydığı milliyetçilik akımının Osmanlı Devleti'nde hangisine neden olduğu söylenebilir?",
        "secenekler": ["A) Demokratikleşme hareketlerinin tamamen durmasına", "B) Balkan uluslarının bağımsızlık isyanları çıkarmasına", "C) Padişahın yetkilerinin artmasına", "D) Ekonomik gelirlerin yükselmesine"],
        "cevap": "B) Balkan uluslarının bağımsızlık isyanları çıkarmasına"
    },
    {
        "soru": "Soru 3: Selanik; Türklerin, Rumların, Bulgarların bir arada yaşadığı bir şehirdi... Selanik ile ilgili hangisine ulaşılamaz?",
        "secenekler": ["A) Çok uluslu yapıya sahiptir.", "B) Kültürel zenginlik barındırır.", "C) Milliyetçilik akımından olumsuz etkilenmiştir.", "D) Şehrin yönetimi tamamen azınlıkların elindedir."],
        "cevap": "D) Şehrin yönetimi tamamen azınlıkların elindedir."
    },
    {
        "soru": "Soru 4: Selanik liman şehri olmasının yanında, demiryolu ile Avrupa'ya bağlıydı. Bu durumun Mustafa Kemal'e en büyük katkısı ne olmuştur?",
        "secenekler": ["A) Askerî yeteneklerinin gelişmesi", "B) Ekonomik tecrübe kazanması", "C) Avrupa'daki yeni fikirleri yakından takip edebilmesi", "D) Geleneksel eğitim alması"],
        "cevap": "C) Avrupa'daki yeni fikirleri yakından takip edebilmesi"
    },
    {
        "soru": "Soru 5: Mustafa'nın annesi geleneksel Mahalle Mektebi'ne, babası modern Şemsi Efendi Okulu'na gitmesini istiyordu. Bu durum neyi kanıtlar?",
        "secenekler": ["A) Eğitimde birlik olmadığını", "B) Karma eğitim yapıldığını", "C) Sadece askerî okulların başarılı olduğunu", "D) Eğitimin tamamen ücretsiz olduğunu"],
        "cevap": "A) Eğitimde birlik olmadığını"
    }
]

# --- ADMİN PANELİ (Yan Menü - Mobilde hamburger menü olarak görünür) ---
with st.sidebar:
    st.header("⚙️ Admin Girişi")
    admin_pass = st.text_input("Admin Şifresi", type="password")
    
    if admin_pass == "1923":  # Şifrenizi buradan değiştirebilirsiniz
        st.success("Admin Paneline Erişildi!")
        df = pd.read_sql_query("SELECT * FROM sonuclar", conn)
        
        if not df.empty:
            st.write(f"Toplam Çözen Öğrenci: {len(df)}")
            st.dataframe(df) # Excel benzeri tablo görünümü
            
            # Excel (CSV) olarak indirme butonu
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Sonuçları Excel (CSV) Olarak İndir",
                data=csv,
                file_name='sinav_istatistikleri.csv',
                mime='text/csv',
            )
        else:
            st.info("Henüz sınava giren öğrenci yok.")

# --- ÖĞRENCİ SINAV EKRANI ---
st.title("📝 8. Sınıf İnkılap Tarihi - 1. Ünite Sınavı")
st.markdown("Lütfen bilgilerinizi eksiksiz girin ve soruları yanıtlayın. Başarılar!")

if 'sinav_bitti' not in st.session_state:
    st.session_state.sinav_bitti = False

if not st.session_state.sinav_bitti:
    with st.form("sinav_formu"):
        st.subheader("Öğrenci Bilgileri")
        col1, col2, col3 = st.columns(3)
        with col1:
            ad = st.text_input("Adınız", max_chars=30)
        with col2:
            soyad = st.text_input("Soyadınız", max_chars=30)
        with col3:
            sube = st.selectbox("Şubeniz", ["Seçiniz", "8/A", "8/B", "8/C", "8/D"])
            
        st.markdown("---")
        st.subheader("Sorular")
        
        kullanici_cevaplari = []
        for i, soru in enumerate(sorular):
            st.markdown(f"**{soru['soru']}**")
            # Telefondan rahat tıklansın diye radio butonları kullanıyoruz
            cevap = st.radio("Seçeneğinizi işaretleyin:", soru['secenekler'], key=f"soru_{i}", index=None)
            kullanici_cevaplari.append(cevap)
            st.write("") # Boşluk
            
        submit_button = st.form_submit_button(label="Sınavı Bitir ve Gönder")
        
        if submit_button:
            if ad == "" or soyad == "" or sube == "Seçiniz":
                st.error("Lütfen ad, soyad ve şube bilgilerinizi eksiksiz doldurun!")
            elif None in kullanici_cevaplari:
                st.warning("Lütfen tüm soruları işaretlediğinizden emin olun!")
            else:
                # Puan Hesaplama
                dogru_sayisi = 0
                yanlis_sayisi = 0
                for i, cevap in enumerate(kullanici_cevaplari):
                    if cevap == sorular[i]["cevap"]:
                        dogru_sayisi += 1
                    else:
                        yanlis_sayisi += 1
                        
                tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Veritabanına Kayıt
                c.execute("INSERT INTO sonuclar (ad, soyad, sube, dogru, yanlis, bos, tarih) VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (ad.capitalize(), soyad.upper(), sube, dogru_sayisi, yanlis_sayisi, 0, tarih))
                conn.commit()
                
                st.session_state.sinav_bitti = True
                st.session_state.dogru = dogru_sayisi
                st.session_state.yanlis = yanlis_sayisi
                st.rerun()

# Sınav bittikten sonra öğrenciye gösterilecek ekran
if st.session_state.sinav_bitti:
    st.success("🎉 Sınavınız başarıyla kaydedildi!")
    st.balloons()
    st.info(f"**Sonucunuz:** {st.session_state.dogru} Doğru, {st.session_state.yanlis} Yanlış")
    st.write("Sınavı tamamladığınız için teşekkürler. Sayfayı kapatabilirsiniz.")