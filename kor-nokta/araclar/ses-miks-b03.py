"""Bölüm 3 ses miksi. Kullanım: python3 araclar/ses-miks-b03.py (kor-nokta klasöründen).
Replik başlangıçları bolumler/bolum-03.html'deki R tablosuyla aynıdır."""
import subprocess
SES, SURE = "assets/ses", 65.0
ZIRVE = {"b03/r01-anlatici": -5.4, "b03/r02-mercan": -1.1, "b03/r03-poyraz": -6.8, "b03/r04-emre": -14.5, "b03/r05-anlatici": -5.5,
         "b03/r06-emre": -15.9, "b03/r07-mercan": -1.3, "b03/r08-poyraz": -6.5, "b03/r09-mercan": -2.1, "b03/r10-anlatici": -7.0,
         "b03/r11-poyraz": -12.1, "b03/r12-mercan": -1.2, "b03/r13-anlatici": -6.6, "b03/fx-motor": -12.5,
         "fx-kagit": -17.3, "fx-pop": -3.4, "fx-vurus": -3.1, "fx-kapak": -17.3}
REPLIK = [("b03/r01-anlatici", 0.7), ("b03/r02-mercan", 7.3), ("b03/r03-poyraz", 10.9), ("b03/r04-emre", 14.9), ("b03/r05-anlatici", 19.9),
          ("b03/r06-emre", 26.2), ("b03/r07-mercan", 30.5), ("b03/r08-poyraz", 35.0), ("b03/r09-mercan", 39.3), ("b03/r10-anlatici", 47.0),
          ("b03/r11-poyraz", 51.5), ("b03/r12-mercan", 55.8), ("b03/r13-anlatici", 59.2)]
FX = [("fx-kapak", 5.2, -6), ("fx-kagit", 9.35, -10), ("fx-vurus", 33.9, -6), ("b03/fx-motor", 43.6, -5), ("fx-vurus", 58.35, -4),
      ("fx-kagit", 13.45, -13), ("fx-kagit", 29.15, -13), ("fx-kagit", 42.95, -13)] + \
     [("fx-pop", t - 0.17, -12) for t in (7.3, 10.9, 14.9, 26.2, 30.5, 35.0, 39.3, 51.5, 55.8)]
girdi, filtre, etiket = [], [], []
def ekle(dosya, f):
    i = len(girdi); girdi.append(dosya); filtre.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{f}[a{i}]"); etiket.append(f"[a{i}]")
for d, t in REPLIK:
    hedef = -6 if "r11" in d else -3
    ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
for d, t, hedef in FX: ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
# 2/6 saati: açılışta işler, Mercan saati çevirince geri plana düşer; kapanış kartında yeniden duyulur
ekle("b02/fx-tiktak", "atrim=0:6.6,volume=15dB,afade=t=in:st=0:d=0.3,afade=t=out:st=5.6:d=1.0,adelay=0:all=1")
ekle("b02/fx-tiktak", "atrim=0:6.4,volume=14dB,afade=t=in:st=0:d=0.5,adelay=58600:all=1")
ekle("muzik-noir", "volume=0.26,afade=t=out:st=27.5:d=3,adelay=5000:all=1")
ekle("muzik-noir", "atrim=3:30,asetpts=PTS-STARTPTS,volume=0.26,afade=t=in:st=0:d=2.5,afade=t=out:st=22.5:d=2.5,adelay=32700:all=1")
# yağmur: tavan arasında kısık, dışarıda (43.5 sn'den sonra) açık
ekle("fx-yagmur", "volume=0.35,afade=t=in:st=0:d=1,afade=t=out:st=27:d=3,adelay=0:all=1")
ekle("fx-yagmur", "volume='if(lt(t,16.5),0.35,0.9)':eval=frame,afade=t=in:st=0:d=3,adelay=27000:all=1")
ekle("fx-yagmur", "atrim=0:10,volume=0.9,afade=t=in:st=0:d=2,afade=t=out:st=3:d=3,adelay=55000:all=1")
komut = ["ffmpeg", "-nostdin", "-y", "-v", "error"]
for g in girdi: komut += ["-i", f"{SES}/{g}.mp3"]
fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={len(girdi)}:normalize=0:duration=longest,alimiter=limit=0.84:level=0,apad,atrim=0:{SURE},afade=t=out:st={SURE-0.6}:d=0.6[o]"
subprocess.run(komut + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{SES}/bolum-03.wav"], check=True)
print("tamam")
