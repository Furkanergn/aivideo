"""Bölüm 9 ses miksi. Kullanım: python3 araclar/ses-miks-b09.py (kor-nokta klasöründen).
Replik başlangıçları bolumler/bolum-09.html'deki R tablosuyla aynıdır."""
import subprocess
SES, SURE = "assets/ses", 62.5
ZIRVE = {"b09/r01-anlatici": -7.2, "b09/r02-poyraz": -4.2, "b09/r03-cayci": -16.9, "b09/r04-poyraz": -9.3, "b09/r05-anlatici": -8.2,
         "b09/r06-poyraz": -1.1, "b09/r07-mercan": -1.4, "b09/r08-anlatici": -3.4, "b09/r09-poyraz": -3.4, "b09/r10-anlatici": -5.7,
         "b09/r11-poyraz": -6.4, "b09/r12-defne": -5.9, "b09/r13-anlatici": -5.5,
         "b09/fx-kosu": -2.2, "b09/fx-paketdus": -1.0,
         "fx-kagit": -17.3, "fx-pop": -3.4, "fx-vurus": -3.1}
REPLIK = [("b09/r01-anlatici", 0.8), ("b09/r02-poyraz", 6.4), ("b09/r03-cayci", 9.9), ("b09/r04-poyraz", 15.6), ("b09/r05-anlatici", 18.2),
          ("b09/r06-poyraz", 24.65), ("b09/r07-mercan", 27.6), ("b09/r08-anlatici", 31.4), ("b09/r09-poyraz", 37.2), ("b09/r10-anlatici", 40.5),
          ("b09/r11-poyraz", 46.9), ("b09/r12-defne", 49.9), ("b09/r13-anlatici", 54.2)]
# koşu: 8. replikte uzaktan, 8–9 arasındaki este öne çıkar; paket 10. replikten hemen önce düşer
FX = [("b09/fx-kosu", 30.9, -17), ("b09/fx-kosu", 35.2, -7), ("b09/fx-paketdus", 39.4, -4), ("fx-vurus", 54.15, -6),
      ("fx-kagit", 5.15, -13), ("fx-kagit", 16.75, -13), ("fx-kagit", 23.45, -13), ("fx-kagit", 30.05, -13), ("fx-kagit", 48.25, -13), ("fx-kagit", 52.45, -13)] + \
     [("fx-pop", t - 0.17, -12) for t in (6.4, 9.9, 15.6, 24.65, 27.6, 37.2, 46.9, 49.9)]
girdi, filtre, etiket = [], [], []
def ekle(dosya, f):
    i = len(girdi); girdi.append(dosya); filtre.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{f}[a{i}]"); etiket.append(f"[a{i}]")
for d, t in REPLIK: ekle(d, f"volume={-3 - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
for d, t, hedef in FX: ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
# dördüncü saat: paketten çıkınca işlemeye başlar, sona kadar sürer
ekle("b02/fx-tiktak", "volume=15dB,afade=t=in:st=0:d=0.4,adelay=43900:all=1")
ekle("b02/fx-tiktak", "volume=15dB,adelay=53400:all=1")
ekle("muzik-noir", "volume=0.26,afade=t=out:st=27:d=3,adelay=4000:all=1")
ekle("muzik-noir", "atrim=3:30,asetpts=PTS-STARTPTS,volume=0.26,afade=t=in:st=0:d=2.5,afade=t=out:st=23.5:d=3.5,adelay=32500:all=1")
ekle("fx-yagmur", "volume=0.14,afade=t=in:st=0:d=1,afade=t=out:st=27:d=3,adelay=0:all=1")
ekle("fx-yagmur", "volume=0.14,afade=t=in:st=0:d=3,afade=t=out:st=27:d=3,adelay=27000:all=1")
ekle("fx-yagmur", "atrim=0:10,volume=0.14,afade=t=in:st=0:d=3,adelay=54000:all=1")
komut = ["ffmpeg", "-nostdin", "-y", "-v", "error"]
for g in girdi: komut += ["-i", f"{SES}/{g}.mp3"]
fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={len(girdi)}:normalize=0:duration=longest,alimiter=limit=0.84:level=0,apad,atrim=0:{SURE},afade=t=out:st={SURE-0.6}:d=0.6[o]"
subprocess.run(komut + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{SES}/bolum-09.wav"], check=True)
print("tamam")
