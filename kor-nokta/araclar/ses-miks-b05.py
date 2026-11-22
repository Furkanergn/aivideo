"""Bölüm 5 ses miksi. Kullanım: python3 araclar/ses-miks-b05.py (kor-nokta klasöründen).
Replik başlangıçları bolumler/bolum-05.html'deki R tablosuyla aynıdır."""
import subprocess
SES, SURE = "assets/ses", 69.5
ZIRVE = {"b05/r01-anlatici": -5.7, "b05/r02-mercan": -1.7, "b05/r03-sami": -2.7, "b05/r04-mercan": -1.7, "b05/r05-sami": -5.7,
         "b05/r06-poyraz": -3.6, "b05/r07-anlatici": -6.9, "b05/r08-mercan": -2.4, "b05/r09-sami": -4.5, "b05/r10-sami": -3.7,
         "b05/r11-anlatici": -7.5, "b05/r12-mercan": -1.7, "b05/r13-anlatici": -5.3,
         "b05/fx-adim": -20.9, "b05/fx-kiler": -15.2, "b05/fx-siren": -35.7,
         "fx-kagit": -17.3, "fx-pop": -3.4, "fx-vurus": -3.1}
REPLIK = [("b05/r01-anlatici", 0.8), ("b05/r02-mercan", 6.9), ("b05/r03-sami", 13.3), ("b05/r04-mercan", 18.1), ("b05/r05-sami", 20.9),
          ("b05/r06-poyraz", 27.2), ("b05/r07-anlatici", 32.4), ("b05/r08-mercan", 37.7), ("b05/r09-sami", 40.5), ("b05/r10-sami", 44.5),
          ("b05/r11-anlatici", 49.6), ("b05/r12-mercan", 56.2), ("b05/r13-anlatici", 59.8)]
FX = [("b05/fx-adim", 0.15, -8), ("b05/fx-adim", 4.6, -8), ("b05/fx-kiler", 25.3, -6), ("fx-vurus", 58.75, -4),
      ("fx-kagit", 11.65, -13), ("fx-kagit", 25.15, -14), ("fx-kagit", 39.15, -13), ("fx-kagit", 47.85, -13)] + \
     [("fx-pop", t - 0.17, -12) for t in (6.9, 13.3, 18.1, 20.9, 27.2, 37.7, 40.5, 44.5, 56.2)]
girdi, filtre, etiket = [], [], []
def ekle(dosya, f):
    i = len(girdi); girdi.append(dosya); filtre.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{f}[a{i}]"); etiket.append(f"[a{i}]")
for d, t in REPLIK: ekle(d, f"volume={-3 - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
for d, t, hedef in FX: ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
# siren: Poyraz'ın repliğinin sonunda yaklaşır, 7. ve 8. repliklerin altında sürer
ekle("b05/fx-siren", "volume=21dB,afade=t=in:st=0:d=1.2,afade=t=out:st=6.3:d=1.7,adelay=30700:all=1")
# üçüncü saat: 3/6 paneliyle işlemeye başlar, sona kadar sürer
ekle("b02/fx-tiktak", "volume=15dB,afade=t=in:st=0:d=0.4,adelay=52600:all=1")
ekle("b02/fx-tiktak", "volume=15dB,adelay=62100:all=1")
# müzik: 11. replikten önce susar
ekle("muzik-noir", "volume=0.26,afade=t=out:st=27.5:d=3,adelay=5000:all=1")
ekle("muzik-noir", "atrim=3:17.6,asetpts=PTS-STARTPTS,volume=0.26,afade=t=in:st=0:d=2.5,afade=t=out:st=12.2:d=2.4,adelay=33400:all=1")
ekle("fx-yagmur", "volume=0.3,afade=t=in:st=0:d=1,afade=t=out:st=27:d=3,adelay=0:all=1")
ekle("fx-yagmur", "volume=0.3,afade=t=in:st=0:d=3,afade=t=out:st=19:d=2.5,adelay=27000:all=1")
komut = ["ffmpeg", "-nostdin", "-y", "-v", "error"]
for g in girdi: komut += ["-i", f"{SES}/{g}.mp3"]
fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={len(girdi)}:normalize=0:duration=longest,alimiter=limit=0.84:level=0,apad,atrim=0:{SURE},afade=t=out:st={SURE-0.6}:d=0.6[o]"
subprocess.run(komut + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{SES}/bolum-05.wav"], check=True)
print("tamam")
