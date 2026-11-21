"""Bölüm 1 ses miksi. Kullanım: python3 araclar/ses-miks.py  (kor-nokta klasöründen)
Zamanlar saniye; her satır: dosya, başlangıç, hedef zirve (dBFS)."""
import subprocess, sys, os
SES = "assets/ses"
SURE = 35.0
ZIRVE = {"anlatici-1": -7.1, "anlatici-2": -2.8, "anlatici-3": -6.2, "anlatici-4": -6.8, "anlatici-5": -5.5,
         "mercan-1": -2.8, "mercan-2": -3.0, "poyraz-1": -14.5, "poyraz-2": -10.7,
         "fx-tik": -11.9, "fx-cam": -29.7, "fx-kagit": -17.3, "fx-pop": -3.4, "fx-kapak": -17.3,
         "fx-vurus": -3.1, "fx-gicirti": -14.4, "fx-blip": -1.3, "fx-sting": -4.6}
KONUSMA = [("anlatici-1", 0.45, -3), ("anlatici-2", 3.4, -3), ("poyraz-1", 9.9, -4), ("mercan-1", 12.0, -3),
           ("mercan-2", 15.6, -3), ("anlatici-3", 18.6, -3), ("anlatici-4", 23.0, -3), ("poyraz-2", 29.0, -5),
           ("anlatici-5", 31.5, -3)]
ORTAK = [("fx-tik", 0.0, -7), ("fx-tik", 0.95, -7), ("fx-cam", 2.3, -6), ("fx-kapak", 21.9, -6),
         ("fx-gicirti", 27.3, -4), ("fx-tik", 33.9, -9)]
SURUM = {
  "cizgi": {"muzik": "muzik-noir", "fx": [("fx-kagit", 8.95, -12), ("fx-kagit", 21.45, -12), ("fx-pop", 9.88, -11),
            ("fx-pop", 11.98, -11), ("fx-pop", 15.58, -11), ("fx-pop", 29.03, -11), ("fx-vurus", 25.15, -4), ("fx-vurus", 30.95, -4)]},
  "piksel": {"muzik": "muzik-piksel", "fx": [("fx-blip", 9.7, -13), ("fx-blip", 11.8, -13), ("fx-blip", 15.4, -13),
             ("fx-blip", 28.85, -13), ("fx-sting", 25.0, -6), ("fx-sting", 30.85, -6)]},
}
def kur(ad):
    s = SURUM[ad]; girdiler = []; filtre = []; etiket = []
    def ekle(dosya, f):
        i = len(girdiler); girdiler.append(dosya); filtre.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{f}[a{i}]"); etiket.append(f"[a{i}]")
    for d, t, hedef in KONUSMA + ORTAK + s["fx"]:
        ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
    # müzik: konuşmanın altında, tavan sahnesinde (27.3-31) neredeyse sessiz
    ekle(s["muzik"], "volume='if(between(t,27.3,31),0.04,if(lt(t,27.0),0.30,0.30))':eval=frame,afade=t=out:st=34.2:d=0.8")
    # yağmur: sokakta açık, içeride kısık
    ekle("fx-yagmur", "volume='if(lt(t,6.5),1.6,0.55)':eval=frame,afade=t=in:st=0:d=0.4,afade=t=out:st=27.2:d=0.6,adelay=3000:all=1")
    komut = ["ffmpeg", "-y", "-v", "error"]
    for g in girdiler: komut += ["-i", f"{SES}/{g}.mp3"]
    fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={len(girdiler)}:normalize=0:duration=longest,alimiter=limit=0.84:level=0,apad,atrim=0:{SURE},afade=t=out:st={SURE-0.5}:d=0.5[o]"
    cikti = f"{SES}/bolum-01-{ad}.wav"
    subprocess.run(komut + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", cikti], check=True)
    print(cikti)
for ad in (sys.argv[1:] or SURUM): kur(ad)
