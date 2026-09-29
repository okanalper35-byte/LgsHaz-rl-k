import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LGS İnkılap Tarihi Sınav Sistemi", page_icon="🇹🇷", layout="wide")

# --- VERİTABANI BAĞLANTISI ---
conn = sqlite3.connect('ogrenci_sonuclari_v3.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sonuclar 
             (ad TEXT, soyad TEXT, sube TEXT, unite TEXT, puan INTEGER, dogru INTEGER, yanlis INTEGER, detaylar TEXT, tarih TEXT)''')
conn.commit()

# --- MÜFREDAT VE 7 ÜNİTE ---
mufredat = [
    "1. Ünite: Bir Kahraman Doğuyor",
    "2. Ünite: Millî Uyanış",
    "3. Ünite: Ya İstiklal Ya Ölüm!",
    "4. Ünite: Atatürkçülük ve Çağdaşlaşan Türkiye",
    "5. Ünite: Demokratikleşme Çabaları",
    "6. Ünite: Türk Dış Politikası",
    "7. Ünite: Atatürk'ün Ölümü ve Sonrası"
]

# --- SORU HAVUZU (70 SORU TAMAMI) ---
sorular_db = {
    "1. Ünite: Bir Kahraman Doğuyor": [
        {"soru": "Sanayi İnkılabı ile hammadde ve pazar ihtiyacı artmış, sömürgecilik yarışı hızlanmıştır. Bu durumun Osmanlı'ya en belirgin etkisi nedir?", "secenekler": ["A) Ekonomik bağımsızlığını kaybetmesi ve açık pazar olması", "B) Topraklarının genişlemesi", "C) Demokratikleşmesi", "D) Yeni fabrikalar kurması"], "cevap": "A) Ekonomik bağımsızlığını kaybetmesi ve açık pazar olması"},
        {"soru": "Fransız İhtilali'nin yaydığı milliyetçilik akımı Osmanlı Devleti'nde neye yol açmıştır?", "secenekler": ["A) Ekonomik kalkınmaya", "B) Azınlık isyanlarına ve toprak kayıplarına", "C) Meşrutiyetin iptaline", "D) Halifeliğin güçlenmesine"], "cevap": "B) Azınlık isyanlarına ve toprak kayıplarına"},
        {"soru": "Selanik'in farklı milletlerin bir arada yaşadığı, Avrupa'ya demiryolu ile bağlı bir liman kenti olması Mustafa Kemal'e nasıl bir katkı sağlamıştır?", "secenekler": ["A) Sadece askerî becerilerini geliştirmiştir", "B) Farklı kültürleri tanımasını ve yenilikleri takip etmesini sağlamıştır", "C) Geleneksel yapısını korumasını sağlamıştır", "D) Ekonomik zenginlik katmıştır"], "cevap": "B) Farklı kültürleri tanımasını ve yenilikleri takip etmesini sağlamıştır"},
        {"soru": "Mustafa Kemal'in Manastır Askerî İdadisinde okurken arkadaşı Ömer Naci'den edebiyat, öğretmeni Mehmet Tevfik'ten tarih sevgisi alması neyin göstergesidir?", "secenekler": ["A) Çevresinin fikir hayatını şekillendirdiğinin", "B) Sadece savaş sanatına ilgi duyduğunun", "C) Siyasi hayata erken atıldığının", "D) Yabancı dilinin zayıf olduğunun"], "cevap": "A) Çevresinin fikir hayatını şekillendirdiğinin"},
        {"soru": "Mustafa Kemal'in Namık Kemal'den vatan sevgisi, Ziya Gökalp'ten milliyetçilik, Montesquieu'den eşitlik konularında etkilenmesi onun hangi özelliğini yansıtır?", "secenekler": ["A) Teslimiyetçiliğini", "B) Sadece yerli düşünürleri okuduğunu", "C) Çok yönlü ve yenilikçi fikir yapısını", "D) Gelenekçi olduğunu"], "cevap": "C) Çok yönlü ve yenilikçi fikir yapısını"},
        {"soru": "31 Mart İsyanı'nı bastıran Hareket Ordusu'nda Kurmay Başkanı olarak görev yapması, Mustafa Kemal'in hangi özelliğini gösterir?", "secenekler": ["A) Padişahı tahttan indirmek istediğini", "B) Yeniliklerin ve meşrutiyet rejiminin koruyucusu olduğunu", "C) Yabancı devletlerle anlaştığını", "D) İsyancılara destek verdiğini"], "cevap": "B) Yeniliklerin ve meşrutiyet rejiminin koruyucusu olduğunu"},
        {"soru": "Trablusgarp Savaşı'nda Mustafa Kemal'in yerel halkı İtalyanlara karşı bir araya getirerek direniş başlatması onun hangi becerisini kanıtlar?", "secenekler": ["A) Teşkilatçılık ve liderlik", "B) Diplomatik arabuluculuk", "C) Ekonomik planlama", "D) İnkılapçılık"], "cevap": "A) Teşkilatçılık ve liderlik"},
        {"soru": "Balkan Savaşları sonucunda Osmanlı'nın Balkanlardaki topraklarını kaybetmesiyle Anadolu'ya büyük göçler yaşanmıştır. Bu durum Anadolu'da neye neden olmuştur?", "secenekler": ["A) Ekonomik zenginliğe", "B) Türk nüfusunun artmasına", "C) Sınırların genişlemesine", "D) Azınlık isyanlarının bitmesine"], "cevap": "B) Türk nüfusunun artmasına"},
        {"soru": "Mustafa Kemal'in Sofya'da askerî ataşe iken Avrupa devletlerinin diplomatlarıyla görüşmesi ona hangi alanda tecrübe kazandırmıştır?", "secenekler": ["A) Dini eğitim", "B) Uluslararası diplomasi ve dış politika", "C) Sağlık yönetimi", "D) Mühendislik"], "cevap": "B) Uluslararası diplomasi ve dış politika"},
        {"soru": "Birinci Dünya Savaşı öncesinde 'Gelecekte savaşların sonucunu hava kuvvetleri belirleyecektir' demesi Mustafa Kemal'in hangi yönünü gösterir?", "secenekler": ["A) İleri görüşlülüğünü", "B) Karamsarlığını", "C) Gelenekçiliğini", "D) Tevazusunu"], "cevap": "A) İleri görüşlülüğünü"}
    ],
    "2. Ünite: Millî Uyanış": [
        {"soru": "I. Dünya Savaşı'nın çıkmasında devletler arası silahlanma yarışı ve hammadde arayışı etkilidir. Bu durumun temel nedeni nedir?", "secenekler": ["A) Milliyetçilik Akımı", "B) Sanayi İnkılabı", "C) Fransız İhtilali", "D) Aydınlanma Çağı"], "cevap": "B) Sanayi İnkılabı"},
        {"soru": "Osmanlı Devleti'nin I. Dünya Savaşı'na girerken kapitülasyonları kaldırdığını ilan etmesinin amacı nedir?", "secenekler": ["A) Ekonomik bağımsızlığını sağlamak", "B) Askerî gücünü artırmak", "C) Yeni sınırlar çizmek", "D) Halifeliği korumak"], "cevap": "A) Ekonomik bağımsızlığını sağlamak"},
        {"soru": "Kafkas Cephesi'nde Mustafa Kemal'in Muş ve Bitlis'i Ruslardan geri alması onun hangi özelliğini gösterir?", "secenekler": ["A) Barışçıllığını", "B) Askerî yeteneğini", "C) Uzlaşmacılığını", "D) İnkılapçılığını"], "cevap": "B) Askerî yeteneğini"},
        {"soru": "Çanakkale Zaferi'nin I. Dünya Savaşı'nın süresini uzatması ve Rusya'da rejim değişikliğine neden olması bu zaferin hangi sonucudur?", "secenekler": ["A) Bölgesel", "B) Sadece askerî", "C) Ekonomik", "D) Uluslararası"], "cevap": "D) Uluslararası"},
        {"soru": "Mondros Ateşkes Antlaşması'nın 7. maddesinin (Güvenliği tehdit eden yerler işgal edilecek) asıl amacı nedir?", "secenekler": ["A) Ülkeye barış getirmek", "B) Yapılacak işgallere hukuki zemin hazırlamak", "C) Azınlıkları korumak", "D) Osmanlı ordusunu terhis etmek"], "cevap": "B) Yapılacak işgallere hukuki zemin hazırlamak"},
        {"soru": "Kuvâ-yı Millîye'nin düşmanı durduramayıp sadece yavaşlatması neyin eksikliğini gösterir?", "secenekler": ["A) Vatanseverliğin", "B) Düzenli ve disiplinli bir ordunun", "C) Cesaretin", "D) Silah üretiminin"], "cevap": "B) Düzenli ve disiplinli bir ordunun"},
        {"soru": "Amasya Genelgesi'nde yer alan 'Vatanın bütünlüğü, milletin bağımsızlığı tehlikededir' maddesi Milli Mücadele'nin nesidir?", "secenekler": ["A) Yöntemi", "B) Gerekçesi (Nedeni)", "C) Amacı", "D) Sonucu"], "cevap": "B) Gerekçesi (Nedeni)"},
        {"soru": "Erzurum Kongresi'nde alınan 'Milli sınırlar içinde vatan bir bütündür' kararı neyin göstergesidir?", "secenekler": ["A) Bölgesel kalındığının", "B) Manda ve himayenin kabul edildiğinin", "C) Ülke bütünlüğünün ve ulusal amacın", "D) Saltanatın desteklendiğinin"], "cevap": "C) Ülke bütünlüğünün ve ulusal amacın"},
        {"soru": "Sivas Kongresi'nde tüm cemiyetlerin tek çatı altında birleştirilmesinin amacı nedir?", "secenekler": ["A) Milli Mücadeleyi tek merkezden yönetmek", "B) İsyan çıkarmak", "C) İtilaf devletleri ile anlaşmak", "D) Yeni bir başkent bulmak"], "cevap": "A) Milli Mücadeleyi tek merkezden yönetmek"},
        {"soru": "TBMM'nin açılmasıyla 'Egemenlik kayıtsız şartsız milletindir' ilkesinin benimsenmesi neyi ifade eder?", "secenekler": ["A) Padişahlığın devamını", "B) Milli iradeye (demokrasiye) dayalı yeni bir devletin kurulduğunu", "C) Kapitülasyonların onaylandığını", "D) Ekonomik bağımsızlığı"], "cevap": "B) Milli iradeye (demokrasiye) dayalı yeni bir devletin kurulduğunu"}
    ],
    "3. Ünite: Ya İstiklal Ya Ölüm!": [
        {"soru": "Ermenilerle imzalanan Gümrü Antlaşması ile TBMM'nin varlığı uluslararası alanda ilk kez tanınmıştır. Bu durum neyi gösterir?", "secenekler": ["A) Askeri zaferin siyasi bir başarı getirdiğini", "B) Batı cephesinin kapandığını", "C) Kurtuluş Savaşı'nın sona erdiğini", "D) İtilaf devletleriyle uzlaşıldığını"], "cevap": "A) Askeri zaferin siyasi bir başarı getirdiğini"},
        {"soru": "I. İnönü Zaferi'nden sonra İstiklal Marşı'nın kabul edilmesi ve Teşkilat-ı Esasiye'nin ilan edilmesi neyin kanıtıdır?", "secenekler": ["A) Yeni bir Türk devletinin temellerinin sağlamlaştığının", "B) Savaşın tamamen bittiğinin", "C) Sadece askeri konulara odaklanıldığının", "D) Padişahın yetkilerinin arttığının"], "cevap": "A) Yeni bir Türk devletinin temellerinin sağlamlaştığının"},
        {"soru": "Tekalif-i Milliye Emirleri ile halktan orduya silah ve erzak yardımı istenmiştir. Bu durum Türk halkının hangi özelliğini yansıtır?", "secenekler": ["A) Çaresizliğini", "B) Milli dayanışma ve fedakarlığını", "C) Teslimiyetçiliğini", "D) Zenginliğini"], "cevap": "B) Milli dayanışma ve fedakarlığını"},
        {"soru": "Sakarya Meydan Muharebesi'nde Mustafa Kemal'in 'Hattı müdafaa yoktur, sathı müdafaa vardır' emri neyi ifade eder?", "secenekler": ["A) Sadece belli bir çizginin korunmasını", "B) Topyekün (bütünsel) vatan savunmasını", "C) Geri çekilme planını", "D) Saldırı taktiğini"], "cevap": "B) Topyekün (bütünsel) vatan savunmasını"},
        {"soru": "Fransızların Ankara Antlaşması'nı imzalayarak Anadolu'yu terk etmesi neyin sonucudur?", "secenekler": ["A) Sakarya Zaferi'nin siyasi bir sonucudur", "B) Mudanya'nın sonucudur", "C) I. İnönü savaşının sonucudur", "D) Gümrü antlaşmasının sonucudur"], "cevap": "A) Sakarya Zaferi'nin siyasi bir sonucudur"},
        {"soru": "Mudanya Ateşkes Antlaşması ile İstanbul ve Boğazlar savaş yapılmadan TBMM'ye bırakılmıştır. Bu durum neyi kanıtlar?", "secenekler": ["A) Osmanlı Devleti'nin hukuken sona erdiğini", "B) İtilaf devletlerinin güçlendiğini", "C) Kurtuluş Savaşı'nın kaybedildiğini", "D) Saltanatın kaldırıldığını"], "cevap": "A) Osmanlı Devleti'nin hukuken sona erdiğini"},
        {"soru": "Lozan Barış Antlaşması'nda kapitülasyonların kesin olarak kaldırılması hangi ilke ile ilgilidir?", "secenekler": ["A) Siyasi eşitlik", "B) Tam ve ekonomik bağımsızlık", "C) Laiklik", "D) Çok partili hayat"], "cevap": "B) Tam ve ekonomik bağımsızlık"},
        {"soru": "Kütahya-Eskişehir Savaşlarındaki yenilgi sırasında Mustafa Kemal'in Maarif Kongresi'ni toplaması neyi gösterir?", "secenekler": ["A) Eğitime savaştan daha çok önem verdiğini", "B) Eğitim ve cehaletle mücadeleye savaş kadar önem verdiğini", "C) Savaşın kaybedileceğini anladığını", "D) Öğretmenleri askere almak istediğini"], "cevap": "B) Eğitim ve cehaletle mücadeleye savaş kadar önem verdiğini"},
        {"soru": "Büyük Taarruz ile düşmanın Anadolu'dan atılması Kurtuluş Savaşı'nın hangi safhasını bitirmiştir?", "secenekler": ["A) Diplomasi safhasını", "B) Hazırlık safhasını", "C) Askeri safhasını (sıcak çatışma)", "D) Kongreler safhasını"], "cevap": "C) Askeri safhasını (sıcak çatışma)"},
        {"soru": "Güney Cephesi'nde Fransızlara karşı Şahin Bey, Sütçü İmam gibi yerel kahramanlar savaşmıştır. Bu neyi gösterir?", "secenekler": ["A) Güneyde halkın Kuvâ-yı Millîye ruhuyla direndiğini", "B) Düzenli ordunun güneyde yenildiğini", "C) Fransızların barış istediğini", "D) Padişahın bölgeye destek gönderdiğini"], "cevap": "A) Güneyde halkın Kuvâ-yı Millîye ruhuyla direndiğini"}
    ],
    "4. Ünite: Atatürkçülük ve Çağdaşlaşan Türkiye": [
        {"soru": "Cumhuriyetin ilanı ile devletin rejiminin ve adının belirlenmesi hangi sorunu çözmüştür?", "secenekler": ["A) Eğitim sistemindeki karışıklığı", "B) Devlet başkanlığı ve rejim krizini", "C) Ekonomik kalkınmayı", "D) Dış borçları"], "cevap": "B) Devlet başkanlığı ve rejim krizini"},
        {"soru": "Tevhid-i Tedrisat Kanunu ile tüm okullar MEB'e bağlanmıştır. Bu durumun en önemli sonucu nedir?", "secenekler": ["A) Karma eğitime geçilmesi", "B) Eğitimde ikiliğin ortadan kalkması ve çağdaşlaşma", "C) Okuma yazma oranının düşmesi", "D) Üniversitelerin kapatılması"], "cevap": "B) Eğitimde ikiliğin ortadan kalkması ve çağdaşlaşma"},
        {"soru": "Türk Medeni Kanunu kadınlara hangi hakkı VERMEMİŞTİR?", "secenekler": ["A) Mirastan eşit pay alma", "B) Siyasi seçme ve seçilme", "C) Resmi nikah zorunluluğu", "D) İstediği meslekte çalışma"], "cevap": "B) Siyasi seçme ve seçilme"},
        {"soru": "Şapka İnkılabı, Kılık Kıyafet Kanunu ve Takvim, Saat değişikliklerinin ortak amacı nedir?", "secenekler": ["A) Siyasi alanı düzenlemek", "B) Toplumsal hayatta çağdaşlaşmayı ve batı ile uyumu sağlamak", "C) Eğitim sistemini değiştirmek", "D) Tarımı geliştirmek"], "cevap": "B) Toplumsal hayatta çağdaşlaşmayı ve batı ile uyumu sağlamak"},
        {"soru": "Soyadı Kanunu ile unvan ve lakapların yasaklanması Atatürk'ün hangi ilkesiyle ilgilidir?", "secenekler": ["A) Laiklik", "B) Devletçilik", "C) Halkçılık (Eşitlik)", "D) Cumhuriyetçilik"], "cevap": "C) Halkçılık (Eşitlik)"},
        {"soru": "Atatürk'ün Milliyetçilik ilkesi ırkçı değildir; kendini Türk hisseden herkesi Türk sayar. Bu durum neyi gösterir?", "secenekler": ["A) Birleştirici ve bütünleştirici olduğunu", "B) Ayrımcı olduğunu", "C) Ümmetçi olduğunu", "D) Gelenekçi olduğunu"], "cevap": "A) Birleştirici ve bütünleştirici olduğunu"},
        {"soru": "Özel sektörün sermaye yetersizliği nedeniyle devletin fabrikalar kurması hangi ilke ile ilgilidir?", "secenekler": ["A) Cumhuriyetçilik", "B) İnkılapçılık", "C) Devletçilik", "D) Laiklik"], "cevap": "C) Devletçilik"},
        {"soru": "Halifeliğin kaldırılması ve Medeni Kanun'un kabulü Atatürk'ün hangi temel ilkesi doğrultusundadır?", "secenekler": ["A) Laiklik", "B) Milliyetçilik", "C) Devletçilik", "D) Cumhuriyetçilik"], "cevap": "A) Laiklik"},
        {"soru": "Harf İnkılabı'nın yapılması ve Millet Mekteplerinin açılmasının temel amacı nedir?", "secenekler": ["A) Okuma yazma oranını artırmak ve eğitimi kolaylaştırmak", "B) Yabancı dilleri unutturmak", "C) Siyasi partiler kurmak", "D) Avrupa'ya öğrenci göndermek"], "cevap": "A) Okuma yazma oranını artırmak ve eğitimi kolaylaştırmak"},
        {"soru": "İzmir İktisat Kongresi'nde yerli malı kullanımının teşvik edilmesinin amacı nedir?", "secenekler": ["A) Dışa bağımlılığı azaltarak ekonomik bağımsızlığı sağlamak", "B) Tarımı bitirmek", "C) Özel sektörü yasaklamak", "D) Yabancı okulları kapatmak"], "cevap": "A) Dışa bağımlılığı azaltarak ekonomik bağımsızlığı sağlamak"}
    ],
    "5. Ünite: Demokratikleşme Çabaları": [
        {"soru": "Atatürk döneminde farklı fırkaların (partilerin) kurulması neyin göstergesidir?", "secenekler": ["A) Saltanata geri dönülmek istendiğinin", "B) Çok partili demokratik hayata geçilmeye çalışıldığının", "C) Ekonominin kötü olduğunun", "D) Dış politikanın başarısızlığının"], "cevap": "B) Çok partili demokratik hayata geçilmeye çalışıldığının"},
        {"soru": "Demokrasilerde farklı siyasi partilerin bulunması mecliste neyi sağlar?", "secenekler": ["A) Tek fikir etrafında birleşmeyi", "B) Farklı görüşlerin yansımasını ve hükümetin denetlenmesini", "C) Yargı bağımsızlığını", "D) Sınırların genişlemesini"], "cevap": "B) Farklı görüşlerin yansımasını ve hükümetin denetlenmesini"},
        {"soru": "Terakkiperver Cumhuriyet Fırkası'nın Şeyh Sait isyanı sonrası kapatılması neyi gösterir?", "secenekler": ["A) Türkiye'nin henüz çok partili hayata hazır olmadığını", "B) Demokrasinin tamamen yerleştiğini", "C) Partinin seçimi kazandığını", "D) İnkılapların tamamlandığını"], "cevap": "A) Türkiye'nin henüz çok partili hayata hazır olmadığını"},
        {"soru": "Şeyh Sait İsyanı iç politikada Türkiye'yi zorlarken dış politikada hangi kaybımıza neden olmuştur?", "secenekler": ["A) Hatay sorunu", "B) Boğazlar sorunu", "C) Musul sorunu", "D) Nüfus mübadelesi"], "cevap": "C) Musul sorunu"},
        {"soru": "İzmir Suikastı girişimi, doğrudan neyi hedef almıştır?", "secenekler": ["A) Cumhuriyet rejimini ve inkılapları", "B) Ekonomik yatırımları", "C) Sınır komşularımızı", "D) Düzenli orduyu"], "cevap": "A) Cumhuriyet rejimini ve inkılapları"},
        {"soru": "Mustafa Kemal İzmir Suikastı sonrası 'Benim naçiz vücudum...' sözüyle neyi vurgulamıştır?", "secenekler": ["A) Suikastçıları affettiğini", "B) Cumhuriyetin kalıcılığını ve kişilere bağlı olmadığını", "C) Ordunun siyasete girmesi gerektiğini", "D) Yeni bir parti kuracağını"], "cevap": "B) Cumhuriyetin kalıcılığını ve kişilere bağlı olmadığını"},
        {"soru": "Serbest Cumhuriyet Fırkası kapandıktan hemen sonra hangi gerici ayaklanma çıkmıştır?", "secenekler": ["A) 31 Mart Vakası", "B) Menemen (Kubilay) Olayı", "C) Şeyh Sait İsyanı", "D) Çerkez Ethem İsyanı"], "cevap": "B) Menemen (Kubilay) Olayı"},
        {"soru": "Menemen Olayı'nda Kubilay'ın şehit edilmesine halkın tepki göstermesi neyi kanıtlar?", "secenekler": ["A) Halkın inkılapları benimsediğini", "B) Eski düzene dönülmek istendiğini", "C) Eğitim sisteminin çöktüğünü", "D) Ordunun zayıfladığını"], "cevap": "A) Halkın inkılapları benimsediğini"},
        {"soru": "Çok partili hayat denemelerinin başarısız olması nedeniyle kesintisiz çok partili yaşama ne zaman geçildi?", "secenekler": ["A) 1923", "B) 1930", "C) 1938", "D) 1945 sonu / 1946"], "cevap": "D) 1945 sonu / 1946"},
        {"soru": "Erkan-ı Harbiye vekâletinin kaldırılarak Genelkurmay Başkanlığı'nın kurulması hangi ilkeyi korur?", "secenekler": ["A) Milliyetçilik", "B) Cumhuriyetçilik (Demokrasi)", "C) Devletçilik", "D) Laiklik"], "cevap": "B) Cumhuriyetçilik (Demokrasi)"}
    ],
    "6. Ünite: Türk Dış Politikası": [
        {"soru": "Musul'un Şeyh Sait İsyanı nedeniyle Irak'a (İngiltere) bırakılması neyi gösterir?", "secenekler": ["A) İç sorunların dış politikayı olumsuz etkilediğini", "B) İngiltere ile müttefik olduğumuzu", "C) Misak-ı Milli'den taviz verilmediğini", "D) Musul'da petrol bulunmadığını"], "cevap": "A) İç sorunların dış politikayı olumsuz etkilediğini"},
        {"soru": "Türkiye'nin 'Yurtta sulh, cihanda sulh' ilkesini benimsemesinin amacı nedir?", "secenekler": ["A) Topraklarını savaşarak genişletmek", "B) Barışçı bir tutumla güvenliğini sağlamak", "C) Sömürgecilik faaliyetlerine katılmak", "D) İç işlere karışmak"], "cevap": "B) Barışçı bir tutumla güvenliğini sağlamak"},
        {"soru": "1936 Montrö Boğazlar Sözleşmesi ile Boğazların tam denetiminin Türkiye'ye geçmesi neyi sağlamıştır?", "secenekler": ["A) Egemenlik haklarımızın güçlenmesini ve tam bağımsızlığı", "B) Boğazların ticarete kapatılmasını", "C) Yeni savaşların çıkmasını", "D) Osmanlı'nın yeniden kurulmasını"], "cevap": "A) Egemenlik haklarımızın güçlenmesini ve tam bağımsızlığı"},
        {"soru": "Türkiye'nin dünya barışına katkıda bulunmak amacıyla 1932 yılında katıldığı kuruluş hangisidir?", "secenekler": ["A) NATO", "B) Birleşmiş Milletler", "C) Milletler Cemiyeti", "D) Avrupa Birliği"], "cevap": "C) Milletler Cemiyeti"},
        {"soru": "Türkiye, batı sınırını güvence altına almak için Balkan Antantı'nı imzalamıştır. Bunun nedeni nedir?", "secenekler": ["A) İtalya ve Almanya'nın saldırgan politikası", "B) İngiltere'nin baskısı", "C) Rusya'nın tehdidi", "D) Fransa'nın işgalleri"], "cevap": "A) İtalya ve Almanya'nın saldırgan politikası"},
        {"soru": "İran, Irak ve Afganistan ile Sadabat Paktı'nı (1937) imzalamamız Atatürk'ün hangi özelliğini gösterir?", "secenekler": ["A) Gelenekçi yapısını", "B) İleri görüşlülüğünü ve barışçılığını", "C) Karamsarlığını", "D) Teslimiyetçiliğini"], "cevap": "B) İleri görüşlülüğünü ve barışçılığını"},
        {"soru": "Yabancı okullar sorununun 'Bu benim iç meselemdir' denilerek çözülmesi Türkiye'nin hangi hassasiyetidir?", "secenekler": ["A) Ekonomik bağımlılık", "B) Bağımsız devlet anlayışı", "C) Laiklik", "D) Çağdaşlaşma"], "cevap": "B) Bağımsız devlet anlayışı"},
        {"soru": "Yunanistan ile yaşanan Nüfus Mübadelesi sorununun çözülmesi hangi antlaşmanın pürüzünü gidermiştir?", "secenekler": ["A) Ankara", "B) Gümrü", "C) Lozan", "D) Mondros"], "cevap": "C) Lozan"},
        {"soru": "Mustafa Kemal'in 'Kırk asırlık Türk yurdu düşman elinde esir kalamaz' diyerek şahsi meselesi gördüğü yer neresidir?", "secenekler": ["A) Kıbrıs", "B) Batum", "C) Musul", "D) Hatay"], "cevap": "D) Hatay"},
        {"soru": "Hatay'ın anavatana katılması Türkiye'nin dış politikada hangi hedefine ulaştığını gösterir?", "secenekler": ["A) Sömürge elde etme", "B) Misak-ı Milli'yi gerçekleştirme yönünde büyük bir adım", "C) Yayılmacı politika izleme", "D) Sınırlarını küçültme"], "cevap": "B) Misak-ı Milli'yi gerçekleştirme yönünde büyük bir adım"}
    ],
    "7. Ünite: Atatürk'ün Ölümü ve Sonrası": [
        {"soru": "Atatürk'ün 'Cumhuriyet ilelebet payidar kalacaktır' sözü neyi ifade eder?", "secenekler": ["A) Vefat edeceğini bildiğini", "B) Bütün inkılapların bittiğini", "C) Cumhuriyetin kişilere değil milletin iradesine dayandığını", "D) Yerine geçecek kişiyi seçtiğini"], "cevap": "C) Cumhuriyetin kişilere değil milletin iradesine dayandığını"},
        {"soru": "Atatürk'ün vefatının sömürge altındaki milletlerde de büyük üzüntü yaratmasının nedeni nedir?", "secenekler": ["A) Ekonomik yardımlar yapması", "B) Dünyadaki tek lider olması", "C) Bağımsızlık savaşını kazanarak mazlum milletlere örnek olması", "D) Yabancı dil bilmesi"], "cevap": "C) Bağımsızlık savaşını kazanarak mazlum milletlere örnek olması"},
        {"soru": "Atatürk'ün yazdığı Nutuk'un (1919-1927) yazılış amacı nedir?", "secenekler": ["A) Şiir yeteneğini göstermek", "B) İnkılapların nasıl yapıldığını nesillere aktarmak ve ders verdirmek", "C) Sadece savaşı anlatmak", "D) Kendi hayatını övmek"], "cevap": "B) İnkılapların nasıl yapıldığını nesillere aktarmak ve ders verdirmek"},
        {"soru": "İkinci Dünya Savaşı sırasında erkek nüfusun askere alınması Türkiye'ye nasıl etki etmiştir?", "secenekler": ["A) Sanayinin gelişmesi", "B) Tarımsal üretimin düşmesi ve ekonomik sıkıntılar", "C) Nüfusun artması", "D) Sınırların genişlemesi"], "cevap": "B) Tarımsal üretimin düşmesi ve ekonomik sıkıntılar"},
        {"soru": "İkinci Dünya Savaşı'nda çıkarılan Varlık Vergisi ve Milli Korunma Kanunu hangi Atatürk ilkesiyle örtüşür?", "secenekler": ["A) Laiklik", "B) İnkılapçılık", "C) Devletçilik", "D) Cumhuriyetçilik"], "cevap": "C) Devletçilik"},
        {"soru": "İkinci Dünya Savaşı'ndan sonra 1946 yılında Türkiye'de hangi siyasi gelişme yaşanmıştır?", "secenekler": ["A) Saltanatın geri gelmesi", "B) Çok partili siyasi hayata kesin olarak geçilmesi", "C) Kadınlara seçme hakkı", "D) Anayasanın kaldırılması"], "cevap": "B) Çok partili siyasi hayata kesin olarak geçilmesi"},
        {"soru": "1938'de Cumhurbaşkanı seçilen ve II. Dünya Savaşı'nda Türkiye'yi savaştan uzak tutan devlet adamı kimdir?", "secenekler": ["A) Celal Bayar", "B) Fevzi Çakmak", "C) İsmet İnönü", "D) Adnan Menderes"], "cevap": "C) İsmet İnönü"},
        {"soru": "1945'te Birleşmiş Milletler'e (BM) kurucu üye olabilmek için Türkiye'nin attığı adım nedir?", "secenekler": ["A) Almanya ve Japonya'ya kağıt üzerinde savaş ilan etmesi", "B) İngiltere'ye asker göndermesi", "C) Toprak vermesi", "D) Monarşiye geçmesi"], "cevap": "A) Almanya ve Japonya'ya kağıt üzerinde savaş ilan etmesi"},
        {"soru": "1950 seçimlerini 'Yeter! Söz Milletindir' sloganıyla kazanarak 27 yıllık CHP iktidarını bitiren parti hangisidir?", "secenekler": ["A) Serbest Cumhuriyet Fırkası", "B) Terakkiperver Fırka", "C) Demokrat Parti", "D) Milli Nizam Partisi"], "cevap": "C) Demokrat Parti"},
        {"soru": "Atatürk'ün Geometri kitabı yazarak terimleri Türkçeleştirmesi onun hangi özelliğini gösterir?", "secenekler": ["A) Dış politikaya önem verdiğini", "B) Çok yönlülüğünü ve eğitime, bilime verdiği önemi", "C) Sanata düşkünlüğünü", "D) Sadece askerlere eğitim verdiğini"], "cevap": "B) Çok yönlülüğünü ve eğitime, bilime verdiği önemi"}
    ]
}

# --- OTURUM YÖNETİMİ ---
if 'ogrenci' not in st.session_state: st.session_state.ogrenci = None
if 'secilen_unite' not in st.session_state: st.session_state.secilen_unite = None
if 'sinav_bitti' not in st.session_state: st.session_state.sinav_bitti = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- YÖNETİCİ (ADMİN) ŞİFRE GİRİŞİ (SOL MENÜ) ---
with st.sidebar:
    st.header("⚙️ Öğretmen Girişi")
    sifre = st.text_input("Şifre", type="password")
    if sifre == "1923":
        st.session_state.is_admin = True
        st.success("Yönetici moduna geçildi.")
    else:
        st.session_state.is_admin = False
        if sifre != "":
            st.error("Hatalı Şifre!")

# =========================================================================
# 1. BÖLÜM: ÖĞRETMEN (ADMİN) PANELİ (Şifre girilince bura açılır)
# =========================================================================
if st.session_state.is_admin:
    st.title("📊 Yönetici ve Analiz Paneli")
    
    # Tüm verileri RowID (benzersiz kimlik) ile çekiyoruz ki silebilelim
    df = pd.read_sql_query("SELECT rowid, * FROM sonuclar ORDER BY tarih DESC", conn)
    
    tab1, tab2, tab3 = st.tabs(["📋 Tüm Sonuçlar", "📈 Ünite Analizi ve Rapor", "🗑️ Öğrenci Kaydı Sil"])
    
    # SEKME 1: TÜM SONUÇLAR
    with tab1:
        if not df.empty:
            st.metric("Sisteme Düşen Toplam Sınav Sayısı", len(df))
            st.dataframe(df.drop(columns=['rowid']))
            st.download_button("📥 Sonuçları Excel Olarak İndir", df.drop(columns=['rowid']).to_csv(index=False).encode('utf-8'), "lgs_sonuclari.csv", "text/csv")
        else:
            st.info("Henüz sisteme girip test çözen öğrenci yok.")
            
    # SEKME 2: YAPAY ZEKA TADINDA ANALİZ
    with tab2:
        st.subheader("Ünite Bazlı Sınıf Analizi")
        secili_unite_analiz = st.selectbox("Analiz Edilecek Üniteyi Seçin:", mufredat)
        df_unite = df[df['unite'] == secili_unite_analiz]
        
        if not df_unite.empty:
            kisi_sayisi = len(df_unite)
            ortalama = df_unite['puan'].mean()
            
            col1, col2 = st.columns(2)
            col1.metric("Bu Üniteyi Çözen Öğrenci Sayısı", kisi_sayisi)
            col2.metric("Sınıf Puan Ortalaması", f"{ortalama:.1f} / 100")
            
            st.markdown("---")
            st.markdown("#### ⚠️ En Çok Yanlış Yapılan Sorular (Konu Özeti)")
            
            # Detaylar sütununu parçalayıp hangi sorunun kaç kere yanlış yapıldığını sayıyoruz
            hata_sayilari = {i: 0 for i in range(1, 11)}
            for detay in df_unite['detaylar']:
                maddeler = detay.split(", ")
                for madde in maddeler:
                    if "Yanlış" in madde:
                        soru_no = int(madde.split(":")[0].replace("S", ""))
                        hata_sayilari[soru_no] += 1
                        
            # Hata oranına göre çoktan aza sırala
            sirali_hatalar = sorted(hata_sayilari.items(), key=lambda x: x[1], reverse=True)
            
            # Sadece hata yapılanları listele
            hata_bulundu = False
            for soru_no, hata_sayisi in sirali_hatalar:
                if hata_sayisi > 0:
                    hata_bulundu = True
                    hata_yuzdesi = (hata_sayisi / kisi_sayisi) * 100
                    st.error(f"**Soru {soru_no}:** Sınıfın **%{hata_yuzdesi:.0f}**'si bu soruyu yanlış yaptı! ({hata_sayisi} Öğrenci)")
                    # Hangi konuda olduklarını bilsin diye soru metnini basıyoruz
                    st.info(f"**Konu/Soru Metni:** {sorular_db[secili_unite_analiz][soru_no-1]['soru']}")
                    
            if not hata_bulundu:
                st.success("Harika! Bu ünitede öğrenciler hiç yanlış yapmamış.")
        else:
            st.warning("Bu üniteyi henüz çözen öğrenci bulunmuyor.")

    # SEKME 3: ÖĞRENCİ KAYDI SİLME
    with tab3:
        st.subheader("Öğrenci Sınav Kaydını Sistemden Sil")
        st.write("Aynı öğrenci iki kere girmek isterse veya yanlış şube girerse buradan kaydını silebilirsiniz.")
        
        if not df.empty:
            silinecek_liste = []
            for index, row in df.iterrows():
                silinecek_liste.append(f"ID: {row['rowid']} | {row['ad']} {row['soyad']} - {row['sube']} - {row['unite']} - Puan: {row['puan']}")
            
            secilen_sil = st.selectbox("Silinecek Kaydı Seçin:", ["Seçiniz"] + silinecek_liste)
            
            if secilen_sil != "Seçiniz":
                rowid_to_delete = secilen_sil.split(" | ")[0].replace("ID: ", "")
                if st.button("🗑️ Bu Kaydı Kalıcı Olarak Sil"):
                    c.execute("DELETE FROM sonuclar WHERE rowid=?", (rowid_to_delete,))
                    conn.commit()
                    st.success("Kayıt başarıyla silindi! Sistem güncelleniyor...")
                    st.rerun()
        else:
            st.info("Silinecek kayıt bulunamadı.")


# =========================================================================
# 2. BÖLÜM: ÖĞRENCİ SINAV EKRANI (Admin giriş yapmamışsa bura görünür)
# =========================================================================
else:
    if st.session_state.ogrenci is None:
        st.title("🎓 LGS İnkılap Tarihi Sınav Sistemi")
        st.markdown("Görevleri tamamla, 100 Puanı kap ve kilitleri aç!")
        with st.form("giris"):
            ad = st.text_input("Adınız", max_chars=30)
            soyad = st.text_input("Soyadınız", max_chars=30)
            sube = st.selectbox("Şube", ["Seçiniz", "8/A", "8/B", "8/C", "8/D", "8/E", "8/F"])
            if st.form_submit_button("Giriş Yap 🚀") and ad and soyad and sube != "Seçiniz":
                st.session_state.ogrenci = {'ad': ad.capitalize(), 'soyad': soyad.upper(), 'sube': sube}
                st.rerun()

    elif st.session_state.ogrenci and st.session_state.secilen_unite is None:
        ogr = st.session_state.ogrenci
        col1, col2 = st.columns([4, 1])
        col1.title(f"Hoş Geldin, {ogr['ad']} {ogr['soyad']} 👋")
        if col2.button("🚪 Çıkış Yap"):
            st.session_state.ogrenci = None
            st.rerun()
            
        # Öğrencinin çözdüğü üniteleri DB'den bul
        c.execute("SELECT unite FROM sonuclar WHERE ad=? AND soyad=? AND sube=?", (ogr['ad'], ogr['soyad'], ogr['sube']))
        cozulenler = [r[0] for r in c.fetchall()]
        
        st.markdown("---")
        # 7 Üniteyi Otomatik Döngüye Sok ve Kilitleri Kontrol Et
        for i, unite_adi in enumerate(mufredat):
            st.subheader(f"📚 {unite_adi}")
            
            if unite_adi in cozulenler:
                c.execute("SELECT puan FROM sonuclar WHERE ad=? AND soyad=? AND sube=? AND unite=?", (ogr['ad'], ogr['soyad'], ogr['sube'], unite_adi))
                puan_bilgisi = c.fetchone()[0]
                st.success(f"✅ Bu sınavı tamamladın. Aldığın Puan: **{puan_bilgisi} / 100**")
            else:
                if i > 0 and mufredat[i-1] not in cozulenler:
                    st.error("🔒 KİLİTLİ: Önceki üniteyi bitirmeden bu sınava giremezsin!")
                else:
                    st.info("🔓 Görev Açık!")
                    if st.button(f"▶️ {unite_adi} Sınavına Başla", key=f"btn_{i}"):
                        st.session_state.secilen_unite = unite_adi
                        st.rerun()
            st.markdown("---")

    elif st.session_state.secilen_unite and not st.session_state.sinav_bitti:
        st.title(st.session_state.secilen_unite)
        st.warning("⚠️ Her soru 10 puandır. Gönder butonuna bastıktan sonra cevapları değiştiremezsin.")
        
        sorular = sorular_db[st.session_state.secilen_unite]
        
        with st.form("sinav"):
            cevaplar = []
            for i, s in enumerate(sorular):
                st.markdown(f"**{i+1})** {s['soru']}")
                cevap = st.radio("Cevabınız:", s['secenekler'], key=f"s_{i}", index=None)
                cevaplar.append(cevap)
                st.write("---")
                
            if st.form_submit_button("Bitir ve Gönder 📤"):
                if None in cevaplar:
                    st.error("Lütfen boş soru bırakmayın!")
                else:
                    dogru_sayisi = 0
                    detay_listesi = []
                    
                    for i, c_cevap in enumerate(cevaplar):
                        dogru_cevap = sorular[i]['cevap']
                        if c_cevap == dogru_cevap:
                            dogru_sayisi += 1
                            detay_listesi.append(f"S{i+1}:Doğru")
                        else:
                            isaretlenen = str(c_cevap)[:2] if c_cevap else "Boş"
                            detay_listesi.append(f"S{i+1}:Yanlış({isaretlenen})")
                    
                    yanlis_sayisi = len(sorular) - dogru_sayisi
                    puan = dogru_sayisi * 10
                    detay_metni = ", ".join(detay_listesi)
                    tarih = datetime.now().strftime("%d.%m.%Y %H:%M")
                    ogr = st.session_state.ogrenci
                    
                    c.execute("INSERT INTO sonuclar (ad, soyad, sube, unite, puan, dogru, yanlis, detaylar, tarih) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (ogr['ad'], ogr['soyad'], ogr['sube'], st.session_state.secilen_unite, puan, dogru_sayisi, yanlis_sayisi, detay_metni, tarih))
                    conn.commit()
                    
                    st.session_state.sinav_bitti = True
                    st.session_state.sonuc = (puan, dogru_sayisi, yanlis_sayisi, detay_listesi)
                    st.rerun()

    elif st.session_state.sinav_bitti:
        puan, d, y, detaylar = st.session_state.sonuc
        st.success("🎉 Sınav kaydedildi!")
        st.title(f"🏆 Puanınız: {puan} / 100")
        st.info(f"✅ Doğru: {d} | ❌ Yanlış: {y}")
        
        st.subheader("Soru Analizin:")
        for detay in detaylar:
            if "Doğru" in detay:
                st.write(f"✅ {detay.split(':')[0]}. Soru: **Doğru**")
            else:
                st.write(f"❌ {detay.split(':')[0]}. Soru: **{detay.split(':')[1]}**")
                
        if st.button("🔙 Görevlere Dön (Sıradaki Kilit Açıldı)"):
            st.session_state.secilen_unite = None
            st.session_state.sinav_bitti = False
            st.rerun()
