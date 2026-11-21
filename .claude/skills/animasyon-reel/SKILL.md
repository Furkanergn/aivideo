---
name: animasyon-reel
description: Tek bir fikirden 9:16 dikey animasyonlu reel kurar ve MP4 olarak render eder - piksel sanat, kara tahta çizimi, çizgi roman, tuğla oyuncak dünyası, sinematik 3D sahne ya da serbest tarz. Görüntü video yapay zekasıyla değil kodla üretilir, video kredisi harcanmaz. Kullanıcı animasyonlu reel, kısa video, motion grafik, Instagram/TikTok/Shorts videosu ya da "şu tarzda bir reel" istediğinde kullan.
---

# Animasyon Reel

15-35 saniyelik dikey reel kurarsın. Görüntü tamamen koddur: HTML + CSS + JavaScript animasyon zaman çizelgesi (gerekirse canvas ya da Three.js), sonunda MP4. Video üreten bir yapay zeka kullanmazsın; her kare kodla çizilir, bu yüzden aynı sahneyi istediğin kadar düzeltip yeniden render edebilirsin. Hedef "şablon gibi" değil "bir animatörün elinden çıkmış gibi" görünmek: seçilen tarz baştan sona tutarlı, her hareketin bir nedeni, her olayın bir sesi var.

## 0. Önce kısa bir brief al

Kullanıcının zaten verdiğini tekrar sorma. Sorman gerekenler (köşeli parantez varsayılan):

1. **Fikir ve tek mesaj:** Reel ne anlatsın, izleyici sonunda ne yapsın? Bir reel, bir fikir. (Örnek: "Kahve dükkanım için sabah açılışını anlatan bir reel, sonunda menüye gelsinler.")
2. **Araç:** Hangi araçla render alalım? [HyperFrames; alternatif Remotion]. HyperFrames düz HTML ile çalışır, sıfırdan başlayan için daha kolaydır; Remotion React projesi kullananlar için uygundur. Cevabı bu dosyanın sonundaki "Kayıtlı tercihler" bölümüne yaz, sonraki reel'lerde tekrar sorma. Aracın kendi skill'i ya da belgesi varsa önce onu oku; teknik konularda (render, ses dosyası, zaman çizelgesi) aracın kuralı bu dosyadan önce gelir.
3. **Tarz:** piksel sanat, kara tahta çizimi, çizgi roman, tuğla oyuncak dünyası, sinematik 3D sahne ya da serbest. Kullanıcı kararsızsa fikre göre öner (bkz. 3. bölüm) ve nedenini tek cümleyle söyle.
4. **Marka:** kullanıcı adı, 2-4 renk, varsa logo ya da maskot dosyası. Maskot ya da logo verilmişse dosyayı olduğu gibi kullan, yeniden çizme.
5. **Ses:** konuşma var mı (kendi kaydı, metin) yoksa yalnız müzik ve efekt mi? Müzik/efekt kütüphanesi varsa yolunu iste.
6. **Süre ve kapanış:** [20-30 sn]. Kapanış çağrısı [yorumlara bir anahtar kelime yazdırmak].

Sonra koda geçmeden **sahne tablosu** yaz: her satırda başlangıç-bitiş saniyesi, ekranda görünenler, hareket, ekran yazısı, ses. Kullanıcıya göster ve onay bekle. Kontrolde bir sahneyi uzatman gerekirse toplam süre ±2 sn kayabilir; fazlası için sor. Tablodan saparsan tabloyu da güncelle.

## 1. Kurulum

- Tuval 1080x1920, 30 fps. Her sahne ayrı bir dosya ya da bileşen; ana dosya yalnız sıralar.
- **Ortak sabitler:** renkler `:root` CSS değişkenlerinde, süreler ve eğriler tek bir global nesnede (`window.REEL = { renk:..., sure:..., egri:... }`). Sahneler kendi sayı ve rengini yazmaz, buradan okur.
- **Belirlenimli animasyon:** her şey zaman çizelgesine bağlı ve geri sarılabilir olsun; aynı saniyeyi iki kez render edince aynı kare çıkmalı. `Math.random()` kullanma, sabit tohumlu bir rastgele sayı üreteci kullan. Canvas ve Three.js sahneleri kendi saatiyle değil, aracın verdiği zamanla (seek) çizilsin.
- **Fontlar:** her fontta `ı İ ş Ş ğ Ğ ü Ü ö Ö ç Ç` harflerinin olduğunu doğrula (fontTools ile karakter tablosuna bak ya da bu harfleri içeren bir kareyi render edip yakından incele). Tarz fontlarının çoğunda Türkçe harf eksiktir; eksikse tam karakter setli (latin-ext) bir alternatif seç. Fontları projeye yerel koy, render'dan önce yüklenmelerini bekle.
- **Güvenli alan:** önemli yazı, yüz ve ürün y=180 ile y=1670 arasında kalsın; üstte ve altta Instagram arayüzü var. Kullanıcı adı köşe etiketi y ≥ 180, sol kenardan ~60 px içeride, küçük ve sade.

## 2. Bütün tarzlarda geçerli kurgu kuralları

- **İlk kare kapaktır:** 0. karede ekran boş olmasın; ana görsel ve ilk yazı daha 0. karede okunur olsun. Bu kare Instagram'ın kapak görüntüsü olur.
- **İlk 2 saniye kanca:** en ilginç görüntü ya da soru en başta. Logo ya da tanıtım ile açma.
- **Yazı birden belirmez:** kelimeler taşması gizli bir kutudan kayarak, tarzın kendi diliyle gelir (piksel tarzda harf harf, kara tahtada çizilerek, çizgi romanda balonla). Kutuya üstten ve alttan yazı boyunun ~%15'i kadar pay ver ki ğ, ş, ç ve İ kesilmesin.
- **Okuma süresi:** okunacak yazı en az 1,5 sn tam okunur kalsın; 5 kelimeden uzunsa `0,5 + 0,3 × kelime sayısı` sn. Ekranda en fazla iki satır, satır başına ~14 karakter; sığmıyorsa satırı böl, fontu küçültme.
- **Konuşma varsa:** görüntü konuşmaya zamanlanır. Kelime zamanlarını transkriptten çıkar (Whisper gibi bir araçla); her sahne değişimi bir cümle ya da vurgu kelimesiyle aynı karede olsun. Anlatılan liste ekranda madde madde, söylendiği anda açılsın.
- **Geçişler üst üste biner:** yeni sahne eskisi tamamen gitmeden başlamış olsun; hiçbir karede yalnız boş zemin kalmasın.
- **Tek eğri ailesi:** girişte hızlı başlayıp yavaş oturan, çıkışta yavaş başlayıp hızlanan bir eğri çifti seç ve hep onu kullan. Fiziksel hareketler (zıplama, düşme, sallanma) için tek bir yay eğrisi.
- **Marka adı ve logo:** başka şirketlerin logosunu, karakterini ya da ürün tasarımını çizme. "Tuğla oyuncak" gibi tarzlarda genel bir görünüm kur, markalı parça kullanma.

## 3. Tarz tarifleri

Her tarz için önce tek bir "stil kartı" kur (renk paleti, font, doku, hareket ritmi) ve kullanıcıya bir test karesiyle göster. Kart onaylanınca bütün sahneler ondan okur.

### 3a. Piksel sanat

- **Ne zaman:** bir karakteri oynatmak, siparişi ya da süreci küçük bir oyun gibi göstermek, kısa döngüler.
- Düşük çözünürlüklü bir tuval kur (ör. 180x320), her şeyi orada çiz ve 6 katına büyüt: canvas'ta `imageSmoothingEnabled = false`, CSS'te `image-rendering: pixelated`. Konumları tam piksele yuvarla; yarım pikselde titreme olur.
- Palet 8-16 renk, gölgeler ayrı renk tonuyla (gradyan yok). Kenar yumuşatma yok.
- Karakter animasyonu 8-12 fps kare kare (yürüme döngüsü 4-6 kare), kamera ve arka plan 30 fps akabilir. CSS'te `steps()` kullan.
- Yazı: piksel font, Türkçe harfleri olmalı; yoksa okunaklı bir mono font + kalın gölge.
- Ses: 8-bit tarzı kısa bip, para, zıplama efektleri; müzik varsa chiptune havasında.

### 3b. Kara tahta çizimi

- **Ne zaman:** tarif, menü, adım adım anlatım, "nasıl çalışır" açıklaması.
- Zemin koyu yeşil-siyah (ör. #1E2A24) ve hafif silinmiş tebeşir dokusu: düşük opaklıkta gürültü + birkaç soluk eski çizgi.
- Çizgiler SVG yolu olarak `stroke-dasharray` / `stroke-dashoffset` ile çizilerek gelsin; tebeşir pürüzü için `feTurbulence` + `feDisplacementMap` filtresi (değerleri sabit, karede değişmesin). Çizgi kalınlığı biraz düzensiz, uçları yuvarlak.
- Yazı el yazısı fontuyla (Türkçe harf kontrolü şart), çizim hızıyla aynı ritimde soldan sağa açılsın.
- Ara sıra tebeşir tozu parçacıkları (sabit tohumlu), silme sahnelerinde silgi izi.
- Ses: tebeşir gıcırtısı yazı çizilirken, silgi hışırtısı sahne değişirken; çok sık kullanma, rahatsız eder.

### 3c. Çizgi roman

- **Ne zaman:** karşılıklı konuşma, komik tepki, önce/sonra, panellerle ilerleyen kısa olay.
- Sayfa kalın siyah çerçeveli panellere bölünür; kamera paneller arasında kayar ya da paneller sırayla açılır.
- Doku: noktalı tram (halftone) için `radial-gradient` deseni, düz ve doygun renkler, kalın siyah dış çizgi.
- Konuşma balonları kuyruğuyla konuşana bağlı, yay eğrisiyle açılır; balondaki metin kısa. Vurgu anlarında ses yansıması yazısı (BAM, ZIP gibi) eğik ve büyük, kısa sarsıntıyla.
- Hız çizgileri ve panel dışına taşan tek bir öğe hareket hissi verir.
- Ses: balon açılışında pop, vurgu yazısında sert vuruş, sayfa çevirmede kağıt sesi.

### 3d. Tuğla oyuncak dünyası

- **Ne zaman:** bir tezgahın, vitrinin, ürünün ya da sistemin parça parça kurulduğunu göstermek.
- Üstünde yuvarlak çıkıntıları olan genel oyuncak tuğlalar; parlak plastik renkler, yumuşak gölge. Markalı figür, logo ya da birebir ürün tasarımı kullanma.
- Basit sahnede CSS 3D (`transform-style: preserve-3d`) yeter; kamera dönecekse Three.js kullan (3e'deki kurallar geçerli).
- Tuğlalar yukarıdan düşer, yay eğrisiyle oturur ve hafifçe ezilir; her oturmada tık sesi. Kurulum aşağıdan yukarı, ritmik (her tuğla ~0,15-0,25 sn arayla).
- Kapanışta bitmiş yapı yavaşça döner ya da kamera geri çekilir.

### 3e. Sinematik 3D hikaye sahnesi

- **Ne zaman:** mekan, ışık ve kamera hareketiyle küçük bir hikaye anlatmak (ör. yağmurlu bir gecede ışığı yanan kahve dükkanı).
- Three.js ile kur. Render'ı aracın zamanına bağla: her karede sahneyi o saniyeye göre kur ve `renderer.render()` çağır; kendi `requestAnimationFrame` döngüsünü çalıştırma. HyperFrames kullanılıyorsa onun Three.js skill'ini oku.
- Sahne az ve güçlü öğeyle kurulsun: basit geometri (kutu, silindir, düzlem), sıcak bir ana ışık, soğuk bir dolgu ışığı, sis (`scene.fog`), gerekirse yağmur ya da toz parçacıkları (sabit tohumlu).
- Kamera tek bir anlamlı hareket yapsın: yavaş yaklaşma, yanal kayma ya da yukarıdan iniş. Hareket yumuşak başlasın ve yumuşak dursun; sarsıntı ve hızlı dönüş yok.
- Poligon ve ışık sayısını düşük tut; gölge haritası 1024 yeter. Render süresi bunlarla hızla artar.
- Yazı 3D sahnenin içine değil, üstüne düz bir katman olarak konsun ki okunaklı kalsın.

### 3f. Serbest tarz

Kullanıcı başka bir tarz isterse (kağıt kesme, kil animasyonu, neon, retro TV gibi) önce o tarzın 3-4 tanımlayıcı özelliğini yaz (renk, doku, hareket ritmi, ses), bunları bir test karesiyle onaylat, sonra yukarıdaki yapıyla kur.

## 4. Ses

- **Başkasının reel'inden ses ya da müzik kopyalama.** Telifli şarkı kullanma.
- **Kaynak sırası:**
  1. Kullanıcının verdiği müzik ve efekt kütüphanesi.
  2. Video aracının kendi telifsiz ses kaynakları.
  3. Telifsiz/CC0 ses arşivleri. Lisansını kontrol et, her dosyanın kaynağını not et.
  4. Hiçbiri yoksa müzik koyma, yalnız efektlerle kur ve bunu kullanıcıya söyle.
- Kullanmadan önce her ses dosyasının gerçek süresine ve zirvesinin nerede olduğuna bak; dosya adı yanıltıcı olabilir.
- **Eşleştirme:** her görsel olayın tarzına uygun bir sesi olsun (3. bölümdeki önerilere bak). Efektin zirvesi görsel olaydan 1 kare sonra. Her kesime efekt koyma; konuşma varsa efektler onun altında kalsın.
- **Son seviye:** render'dan sonra sesi iki geçişli loudnorm ile **-14 LUFS**'a getir, videoyu yeniden kodlama (`-c:v copy`); true peak hedefi **-2 dBTP**. Sonda 0,5 sn sesi kıs. Ölçtüğün değerleri teslimde yaz.

## 5. Render'dan önce kontrol

1. 0. kareden, her sahne sınırından, her geçişin ortasından ve her yazının tam okunur olduğu andan birer kare çıkar; hepsini tek bir kontrol sayfasında yan yana koy ve bak.
2. Şunları ara:
   - kesilmiş ya da kutusundan taşan yazı (özellikle ğ, ş, ç ve İ), yanlış fonta düşen Türkçe harf,
   - tarzın bozulduğu kare (piksel tarzda bulanık kenar, kara tahtada düz dijital çizgi, 3D'de titreyen gölge),
   - ana öğenin yazının üstüne binmesi, güvenli alan dışında kalan yazı,
   - boş ya da yalnız zeminin göründüğü kare, zamanından önce görünen öğe,
   - konuşma varsa sahne değişiminin cümleden kayması.
3. Aracın kendi kontrol komutu varsa (ör. HyperFrames `check`) onu da çalıştır.
4. Düzelt, tekrar bak, sonra tam render al. Uzun sürecekse önce tahmini süreyi söyle.

## 6. Dışa aktarma

- 1080x1920, 30 fps, H.264 video + AAC ses, `yuv420p`, `faststart`.
- ffprobe ile codec, çözünürlük, fps, süre ve boyutu doğrula.
- Revizyonda eski render'ı sil, klasörde tek güncel dosya kalsın.

## 7. Teslim

Önce MP4'ün yolunu ver, sonra tek satırlık sahne listesini, ölçülen ses seviyesini ve kullanılan her ses dosyasının kaynağı ile lisansını (atıf isteyenleri ayrıca belirt). Sonra şunları teklif et: bir sahnenin hızını ya da süresini değiştirmek, yazıları değiştirmek, aynı fikri başka bir tarzda yeniden kurmak. Sesi dinlemediysen bunu söyle.

## Kayıtlı tercihler

Kullanıcı seçtikçe buraya yaz ve sonraki reel'lerde bunları kullan:

- Render aracı: HyperFrames
- Marka renkleri: "Kör Nokta" dizisi için siyah #05070C, gece laciverti #0F1A2E, lacivert #1D3052, çelik mavi #3A5480, kemik #EFE6D2, vurgu kehribar #F2A516 (kor-nokta/assets/kn.css)
- Kullanıcı adı: @BFStudiosAI
- Ses kütüphanesi yolu: yok; anlatım, müzik ve efektler ElevenLabs bağlantısıyla üretilir (kullanıcı onayladı)
