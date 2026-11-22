# Kör Nokta — bir bölüm nasıl üretilir

Bölüm 1–5 bu adımlarla üretildi. NN bölüm numarasıdır (06, 07 …). Paralel çalışan her üretici kendi kopyasında çalışır ve yalnızca adında `bNN` ya da `bolum-NN` geçen dosyalar üretir.

## Yalıtım
- Çalışma kopyası: `W=<scratchpad>/is-bNN`; `mkdir -p $W && cp -r /home/user/aivideo/kor-nokta $W/kor-nokta`, ardından `$W/kor-nokta/renders` ve `.hyperframes` silinir.
- Bütün `hyperframes` komutları, miks betiği ve `araclar/teslim.sh` `$W/kor-nokta` içinden çalışır (teslim.sh çıktıyı `$W/teslim` altına yazar). Depodaki `kor-nokta/index.html` dosyasına dokunulmaz, depoda hyperframes çalıştırılmaz.
- Ortak dosyalar değiştirilmez: `kn.css`, `kn.js`, `paylasim/sablon.html`, `paylasim/uret.cjs`, `araclar/teslim.sh`, eski bölüm dosyaları, `KADRO.md`, senaryo dosyaları.
- Git komutu çalıştırılmaz. Her ffmpeg çağrısında `-nostdin` kullanılır. Kullanım sinyali (`hyperframes events`) gönderilmez.

## 1. Sesler
- ElevenLabs akışı `1tGyQs6q8edbZ9oKjytI`, model `eleven_v4`, `generations_count: 1`, replik başına tek çağrı; ses kimlikleri senaryo dosyasındaki tabloda. Fısıltı satırlarının başına `[whispering] ` eklenir.
- En çok 3 yeni efekt (`creative_generate_in_flow`, `node_type: sfx`, model `eleven_text_to_sound_v3`). Var olanlar yeniden kullanılır: `assets/ses/` altında `fx-tik`, `fx-kagit`, `fx-pop`, `fx-vurus`, `fx-gicirti`, `fx-yagmur`, `fx-kapak`, `fx-cam`, `muzik-noir`, `b02/fx-tiktak`, `b02/fx-paket`, `v2/fx-kapi`, `b03/` (motor), `b05/` (siren, kapı, sürüyen adım).
- Dosyalar `assets/ses/bNN/` altına `r01-anlatici.mp3 … r13-anlatici.mp3` ve `fx-*.mp3` olarak iner (curl; `elevenlabsusercontent.com` izinli). Her dosyanın başlangıç, bitiş ve zirve değeri ölçülür.

## 2. Paneller
- Görsel akışı `dqozTQpGnJdHDkQP9me4`, model `gpt-image-2.5-sunburst`, parametreler `{"quality":"high","aspect_ratio":"9:16","resolution":"1K"}`, `generations_count: 1`; `creative_add_flow_node` sonra `creative_run_flow_nodes` (önce `estimate_only`).
- Stil cümlesi (referanssız panellerde aynen): "Comic book panel illustration, flat inked noir style, thick black outlines, cross-hatching and halftone dot shading, limited palette of deep navy, steel blue, bone white and a single amber accent. Vertical 9:16 composition." Sonunda: "No text, no speech bubbles, no logos, no watermark." Referanslı panellerde: "Same inked comic style, line weight and colour palette as the reference image." ve "the same <kişi> as in the reference image: <tarif>".
- Referans yalnız yüzün belirleyici olduğu panellerde kullanılır (`connect_from`); referanslı panel ~433, referanssız ~190 kredi. Düğüm kimlikleri senaryo dosyasında.
- Balon gelecek bölge için "The lower third of the frame is darker and calmer." yazılır.
- Kadranı görünen saatler İBRESİZ çizdirilir ("the dial has no hands at all"), ibreler kodla eklenir ve saniye ibresi tıklar (Bölüm 2 ve 5'teki gibi; kadran merkezi görüntüye bakılarak bulunur).
- Önceki bölümlerin panelleri uygun yerde yeniden kullanılır (`assets/paneller/`, `b02/` … `b05/`, `karakter/`).
- `content.png` indirilir, 1080×1920 JPEG'e çevrilir (lanczos, `-q:v 2`), `assets/paneller/bNN/` altına konur. Her panele bakılır; en çok bir kötü panel yeniden üretilir.

## 3. Miks
- `araclar/ses-miks-b02.py` kopyalanıp `ses-miks-bNN.py` yapılır. Konuşanlar arasında 0,7–1,7 sn es, her este ekranda bir hareket. `muzik-noir` iki kez üst üste bindirilir; senaryo sustuğunu söylediği yerde susar. Çıktı `assets/ses/bolum-NN.wav`, hedef 60–75 sn.
- Çok kısık üretilen replik (zirve −14 dB altı) mikste −3 dB'ye çekilir; rapora yazılır.

## 4. Kurgu
- `bolumler/bolum-05.html` kopyalanıp `bolum-NN.html` yapılır; motor, büyütülmüş balonlar, çerçeve, `@BFStudiosAI` ve `KÖR NOKTA · BN` etiketleri korunur. Sahneler, R/S tabloları, metinler ve zamanlar değişir.
- 0. kare kapaktır: `BÖLÜM N` kutusu ve büyük başlık. Kapanış kartı: logo, senaryodaki soru (iki satır, sığmazsa font küçültülür), "Tahminini yorumlara yaz", "DEVAMI YARIN" (vaka sonunda "YENİ VAKA YARIN").
- Balon başına en çok iki satır, satır başına ~22 harf; uzun replik ardışık balonlara bölünür. `kuyrukX: 110`.
- Sonra `$W/kor-nokta` içinde `cp bolumler/bolum-NN.html index.html`.

## 5. Denetim, render, teslim
- `npx -y hyperframes@0.9.78 check` 0 hata vermeli. 0. kareden, her sahneden ve her yazıdan kare alınır, kontrol sayfalarına bakılır; kesilen yazı, kapanan yüz, boş kare düzeltilir.
- `araclar/teslim.sh assets/ses/bolum-NN.wav kor-nokta-bolum-NN <süre>`; ffprobe ve ses seviyesi (≈ −14 LUFS, true peak ≤ −2 dBTP) doğrulanır. Bitmiş MP4'ten ~12 kare tek sayfada çıkarılıp bakılır.

## 6. Kapak, hikaye, içerik yazısı
- `paylasim/isler-bNN.json` (`isler-b05.json` biçiminde bir `kapak` ve bir `hikaye` işi; alt satırlar senaryo dosyasından). Kapakta en güçlü yüz ya da siluet, hikayede bir nesne. `y` öyle seçilir ki özne ortadaki 4:5 kırpmada (y 300–1620) kalsın ve başlık bloklarının (y 1010–1500) altında kalmasın.
- `node paylasim/uret.cjs paylasim/isler-bNN.json` (`$W/kor-nokta` içinden; çıktı `$W/teslim/paylasim`). İki görsele de bakılır.
- `bolum-NN-yazi.txt`: senaryo dosyasındaki kalıp, kanca ve soru ile.

## 7. Depoya kopyalama (yalnız bunlar)
- `bolumler/bolum-NN.html`, `araclar/ses-miks-bNN.py`, `paylasim/isler-bNN.json`, `assets/ses/bNN/`, `assets/ses/bolum-NN.wav`, `assets/paneller/bNN/` → `/home/user/aivideo/kor-nokta/`
- `kor-nokta-bolum-NN.mp4` → `/home/user/aivideo/teslim/`; `bolum-NN-kapak.jpg`, `bolum-NN-hikaye.jpg`, `bolum-NN-yazi.txt` → `/home/user/aivideo/teslim/paylasim/`

## Rapor
Son MP4 yolu, süre, ölçülen LUFS ve true peak, sahne listesi ve zamanları, harcanan kredi (ses, efekt, görsel ayrı), referanslı paneller, görülen kusurlar, doğrulanamayanlar (ses dinlenemez) ve bu belgeden sapmalar.
