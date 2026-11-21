"""Bölüm 1 (çizimli sürüm) ses miksi. Kullanım: python3 araclar/ses-miks-v2.py (kor-nokta klasöründen).
Her satır: dosya, başlangıç saniyesi, hedef zirve (dBFS). Replik başlangıçları index.html'deki R tablosuyla aynıdır."""
import subprocess
SES, SURE = "assets/ses", 73.5
ZIRVE = {"v2/r01-anlatici": -4.6, "v2/r02-anlatici": -5.5, "v2/r03-poyraz": -8.0, "v2/r04-poyraz": -7.1, "v2/r05-mercan": -1.8,
         "v2/r06-mercan": -2.0, "v2/r07-anlatici": -5.3, "v2/r08-mercan": -1.7, "v2/r09-poyraz": -8.0, "v2/r10-mercan": -1.0,
         "v2/r11-poyraz": -14.3, "v2/r12-anlatici": -8.2, "v2/r13-anlatici": -6.2, "v2/fx-kapi": -8.1,
         "fx-tik": -11.9, "fx-cam": -29.7, "fx-kagit": -17.3, "fx-pop": -3.4, "fx-kapak": -17.3, "fx-vurus": -3.1, "fx-gicirti": -14.4}
REPLIK = [("v2/r01-anlatici", 0.6), ("v2/r02-anlatici", 7.4), ("v2/r03-poyraz", 16.6), ("v2/r04-poyraz", 22.1), ("v2/r05-mercan", 27.9),
          ("v2/r06-mercan", 32.3), ("v2/r07-anlatici", 38.1), ("v2/r08-mercan", 45.2), ("v2/r09-poyraz", 51.2), ("v2/r10-mercan", 53.7),
          ("v2/r11-poyraz", 58.0), ("v2/r12-anlatici", 62.9), ("v2/r13-anlatici", 68.2)]
FX = [("fx-tik", t, -8) for t in (0.0, 1.0, 2.0, 3.0, 4.0)] + [("fx-cam", 5.5, -7), ("v2/fx-kapi", 14.2, -6), ("fx-kapak", 44.3, -7),
      ("fx-vurus", 51.1, -5), ("fx-gicirti", 65.6, -4), ("fx-vurus", 67.5, -4), ("fx-tik", 72.4, -9),
      ("fx-kagit", 6.25, -13), ("fx-kagit", 21.05, -13), ("fx-kagit", 36.75, -13), ("fx-kagit", 44.25, -13)] + \
     [("fx-pop", t - 0.17, -12) for t in (16.6, 22.1, 27.9, 32.3, 45.2, 51.2, 53.7, 58.0)]
girdi, filtre, etiket = [], [], []
def ekle(dosya, f):
    i = len(girdi); girdi.append(dosya); filtre.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{f}[a{i}]"); etiket.append(f"[a{i}]")
for d, t in REPLIK:
    hedef = -6 if "r11" in d else -3
    ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
for d, t, hedef in FX: ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
# müzik: 35 sn'lik tema iki kez, üst üste bindirilerek; fısıltı sahnesinden itibaren susar
ekle("muzik-noir", "volume=0.26,afade=t=out:st=27.5:d=3,adelay=6800:all=1")
ekle("muzik-noir", "atrim=3:30,asetpts=PTS-STARTPTS,volume=0.26,afade=t=in:st=0:d=2.5,afade=t=out:st=20.5:d=1.5,adelay=34500:all=1")
# yağmur: sokakta açık, içeride kısık
ekle("fx-yagmur", "volume='if(lt(t,4.6),1.7,0.5)':eval=frame,afade=t=in:st=0:d=0.5,afade=t=out:st=27:d=3,adelay=6800:all=1")
ekle("fx-yagmur", "volume=0.5,afade=t=in:st=0:d=3,afade=t=out:st=20.5:d=1.5,adelay=33800:all=1")
komut = ["ffmpeg", "-y", "-v", "error"]
for g in girdi: komut += ["-i", f"{SES}/{g}.mp3"]
fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={len(girdi)}:normalize=0:duration=longest,alimiter=limit=0.84:level=0,apad,atrim=0:{SURE},afade=t=out:st={SURE-0.6}:d=0.6[o]"
subprocess.run(komut + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{SES}/bolum-01-v2.wav"], check=True)
print("tamam")
