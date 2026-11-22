"""Bölüm 7 ses miksi. Kullanım: python3 araclar/ses-miks-b07.py (kor-nokta klasöründen).
Replik başlangıçları bolumler/bolum-07.html'deki R tablosuyla aynıdır."""
import subprocess
SES, SURE = "assets/ses", 68.0
ZIRVE = {"b07/r01-anlatici": -5.3, "b07/r02-poyraz": -7.7, "b07/r03-mercan": -1.6, "b07/r04-anlatici": -7.7, "b07/r05-mercan": -1.1,
         "b07/r06-rifat": -7.6, "b07/r07-mercan": -1.3, "b07/r08-rifat": -6.2, "b07/r09-poyraz": -9.8, "b07/r10-rifat": -6.2,
         "b07/r11-mercan": -2.2, "b07/r12-rifat": -10.0, "b07/r13-anlatici": -6.3,
         "b07/fx-vapur": -1.0, "fx-kagit": -17.3, "fx-pop": -3.4, "fx-vurus": -3.1}
REPLIK = [("b07/r01-anlatici", 0.8), ("b07/r02-poyraz", 8.0), ("b07/r03-mercan", 11.4), ("b07/r04-anlatici", 17.5), ("b07/r05-mercan", 24.6),
          ("b07/r06-rifat", 28.3), ("b07/r07-mercan", 32.2), ("b07/r08-rifat", 37.5), ("b07/r09-poyraz", 42.9), ("b07/r10-rifat", 45.5),
          ("b07/r11-mercan", 52.4), ("b07/r12-rifat", 56.6), ("b07/r13-anlatici", 61.5)]
FX = [("fx-vurus", 60.65, -4),
      ("fx-kagit", 7.15, -13), ("fx-kagit", 16.85, -14), ("fx-kagit", 23.75, -13), ("fx-kagit", 27.65, -14), ("fx-kagit", 31.35, -13),
      ("fx-kagit", 36.65, -14), ("fx-kagit", 42.15, -13), ("fx-kagit", 44.75, -14), ("fx-kagit", 51.55, -13)] + \
     [("fx-pop", t - 0.17, -12) for t in (8.0, 11.4, 24.6, 28.3, 32.2, 37.5, 42.9, 45.5, 52.4, 56.6)]
girdi, filtre, etiket = [], [], []
def ekle(dosya, f):
    i = len(girdi); girdi.append(dosya); filtre.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{f}[a{i}]"); etiket.append(f"[a{i}]")
for d, t in REPLIK: ekle(d, f"volume={-3 - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
for d, t, hedef in FX: ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
# vapur düdüğü ve martılar: 1. replikten sonraki este; Poyraz girerken kısılır
ekle("b07/fx-vapur", "volume=-6dB,afade=t=out:st=2.7:d=2.2,adelay=5000:all=1")
# üçüncü saat: 3/6 paneliyle işler; Rıfat saate bakarken yeniden duyulur ve sona kadar sürer
ekle("b02/fx-tiktak", "volume=15dB,afade=t=in:st=0:d=0.4,afade=t=out:st=4.6:d=0.8,adelay=31400:all=1")
ekle("b02/fx-tiktak", "volume=15dB,afade=t=in:st=0:d=0.3,adelay=53900:all=1")
ekle("b02/fx-tiktak", "volume=15dB,adelay=61000:all=1")
# müzik: 11. replikten sonra, Rıfat saate bakarken susar
ekle("muzik-noir", "volume=0.26,afade=t=out:st=27.5:d=3,adelay=7000:all=1")
ekle("muzik-noir", "atrim=3:22,asetpts=PTS-STARTPTS,volume=0.26,afade=t=in:st=0:d=2.5,afade=t=out:st=16.4:d=2.6,adelay=35400:all=1")
komut = ["ffmpeg", "-nostdin", "-y", "-v", "error"]
for g in girdi: komut += ["-i", f"{SES}/{g}.mp3"]
fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={len(girdi)}:normalize=0:duration=longest,alimiter=limit=0.84:level=0,apad,atrim=0:{SURE},afade=t=out:st={SURE-0.6}:d=0.6[o]"
subprocess.run(komut + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{SES}/bolum-07.wav"], check=True)
print("tamam")
