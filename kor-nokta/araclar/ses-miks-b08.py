"""Bölüm 8 ses miksi. Kullanım: python3 araclar/ses-miks-b08.py (kor-nokta klasöründen).
Replik başlangıçları bolumler/bolum-08.html'deki R tablosuyla aynıdır."""
import subprocess
SES, SURE = "assets/ses", 70.0
ZIRVE = {"b08/r01-anlatici": -4.0, "b08/r02-mercan": -0.5, "b08/r03-rifat": -6.5, "b08/r04-poyraz": -8.4, "b08/r05-rifat": -6.8,
         "b08/r06-mercan": -1.6, "b08/r07-anlatici": -7.3, "b08/r08-cayci": -13.4, "b08/r09-rifat": -6.7, "b08/r10-mercan": -2.9,
         "b08/r11-anlatici": -6.1, "b08/r12-mercan": -1.3, "b08/r13-anlatici": -6.2,
         "b08/fx-bardak": -0.7, "b08/fx-vapur": -18.8,
         "fx-kagit": -17.3, "fx-pop": -3.4, "fx-vurus": -3.1, "fx-tik": -11.9}
REPLIK = [("b08/r01-anlatici", 0.8), ("b08/r02-mercan", 7.3), ("b08/r03-rifat", 14.4), ("b08/r04-poyraz", 22.0), ("b08/r05-rifat", 25.5),
          ("b08/r06-mercan", 30.3), ("b08/r07-anlatici", 37.5), ("b08/r08-cayci", 42.2), ("b08/r09-rifat", 47.0), ("b08/r10-mercan", 50.1),
          ("b08/r11-anlatici", 53.0), ("b08/r12-mercan", 58.7), ("b08/r13-anlatici", 64.2)]
# bardak masaya konur (tık), Mercan bardağa vurur (vuruş), bardak güvertede kırılır
FX = [("fx-tik", 41.75, -8), ("fx-vurus", 50.02, -5), ("b08/fx-bardak", 50.6, -3), ("fx-vurus", 63.35, -5),
      ("fx-kagit", 6.35, -13), ("fx-kagit", 13.55, -13), ("fx-kagit", 21.15, -13), ("fx-kagit", 24.75, -13), ("fx-kagit", 29.35, -13),
      ("fx-kagit", 36.75, -13), ("fx-kagit", 46.15, -13), ("fx-kagit", 57.85, -13)] + \
     [("fx-pop", t - 0.17, -12) for t in (7.3, 14.4, 22.0, 25.5, 30.3, 42.2, 47.0, 58.7)]
girdi, filtre, etiket = [], [], []
def ekle(dosya, f):
    i = len(girdi); girdi.append(dosya); filtre.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{f}[a{i}]"); etiket.append(f"[a{i}]")
for d, t in REPLIK: ekle(d, f"volume={-3 - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
for d, t, hedef in FX: ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
# vapurun makine uğultusu: baştan sona, üç parça üst üste bindirilir
ekle("b08/fx-vapur", "volume=6dB,afade=t=in:st=0:d=0.8,afade=t=out:st=26.5:d=3,adelay=0:all=1")
ekle("b08/fx-vapur", "volume=6dB,afade=t=in:st=0:d=3,afade=t=out:st=20.5:d=3,adelay=26500:all=1")
ekle("b08/fx-vapur", "volume=6dB,afade=t=in:st=0:d=3,afade=t=out:st=21:d=2,adelay=47000:all=1")
# müzik "İçmeyin!" anında (50.0) kesilir
ekle("muzik-noir", "volume=0.26,afade=t=in:st=0:d=1.5,afade=t=out:st=24.5:d=3,adelay=6000:all=1")
ekle("muzik-noir", "atrim=3:23.05,asetpts=PTS-STARTPTS,volume=0.26,afade=t=in:st=0:d=2.5,afade=t=out:st=19.8:d=0.25,adelay=29950:all=1")
komut = ["ffmpeg", "-nostdin", "-y", "-v", "error"]
for g in girdi: komut += ["-i", f"{SES}/{g}.mp3"]
fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={len(girdi)}:normalize=0:duration=longest,alimiter=limit=0.84:level=0,apad,atrim=0:{SURE},afade=t=out:st={SURE-0.6}:d=0.6[o]"
subprocess.run(komut + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{SES}/bolum-08.wav"], check=True)
print("tamam")
