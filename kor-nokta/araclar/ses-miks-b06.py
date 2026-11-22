"""Bölüm 6 ses miksi. Kullanım: python3 araclar/ses-miks-b06.py (kor-nokta klasöründen).
Replik başlangıçları bolumler/bolum-06.html'deki R tablosuyla aynıdır."""
import subprocess
SES, SURE = "assets/ses", 66.5
ZIRVE = {"b06/r01-anlatici": -8.5, "b06/r02-tarik": -2.0, "b06/r03-mercan": -1.3, "b06/r04-anlatici": -5.9, "b06/r05-poyraz": -8.2,
         "b06/r06-feride": -1.4, "b06/r07-mercan": -1.8, "b06/r08-feride": -1.0, "b06/r09-mercan": -0.7, "b06/r10-poyraz": -5.5,
         "b06/r11-tarik": -1.8, "b06/r12-mercan": -1.4, "b06/r13-anlatici": -4.2,
         "b06/fx-jeton": -4.3, "b06/fx-vapur": -30.0, "fx-kagit": -17.3, "fx-pop": -3.4}
REPLIK = [("b06/r01-anlatici", 0.8), ("b06/r02-tarik", 8.6), ("b06/r03-mercan", 12.6), ("b06/r04-anlatici", 18.4), ("b06/r05-poyraz", 23.0),
          ("b06/r06-feride", 27.0), ("b06/r07-mercan", 32.0), ("b06/r08-feride", 34.4), ("b06/r09-mercan", 40.3), ("b06/r10-poyraz", 44.8),
          ("b06/r11-tarik", 49.6), ("b06/r12-mercan", 52.5), ("b06/r13-anlatici", 57.8)]
FX = [("b06/fx-jeton", 17.6, -5), ("b06/fx-vapur", 48.2, -9), ("b06/fx-vapur", 54.5, -17),
      ("fx-kagit", 4.25, -13), ("fx-kagit", 16.65, -13), ("fx-kagit", 39.45, -13), ("fx-kagit", 47.85, -14)] + \
     [("fx-pop", t - 0.17, -12) for t in (8.6, 12.6, 23.0, 27.0, 32.0, 34.4, 40.3, 44.8, 49.6, 52.5)]
girdi, filtre, etiket = [], [], []
def ekle(dosya, f):
    i = len(girdi); girdi.append(dosya); filtre.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{f}[a{i}]"); etiket.append(f"[a{i}]")
for d, t in REPLIK: ekle(d, f"volume={-3 - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
for d, t, hedef in FX: ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
# üçüncü saat: açılışta avuçta işler, kapanış kartında sona kadar sürer
ekle("b02/fx-tiktak", "atrim=0:3.9,volume=15dB,afade=t=in:st=0:d=0.3,afade=t=out:st=3.4:d=0.5,adelay=4400:all=1")
ekle("b02/fx-tiktak", "volume=15dB,afade=t=in:st=0:d=0.4,adelay=57400:all=1")
# müzik: Poyraz'ın 10. repliğinden sonra susar, vapur düdüğü sessizlikte duyulur
ekle("muzik-noir", "volume=0.26,afade=t=in:st=0:d=1.5,afade=t=out:st=27.5:d=3,adelay=3000:all=1")
ekle("muzik-noir", "atrim=3:17.6,asetpts=PTS-STARTPTS,volume=0.26,afade=t=in:st=0:d=2.5,afade=t=out:st=12.0:d=2.6,adelay=32600:all=1")
komut = ["ffmpeg", "-nostdin", "-y", "-v", "error"]
for g in girdi: komut += ["-i", f"{SES}/{g}.mp3"]
fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={len(girdi)}:normalize=0:duration=longest,alimiter=limit=0.84:level=0,apad,atrim=0:{SURE},afade=t=out:st={SURE-0.6}:d=0.6[o]"
subprocess.run(komut + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{SES}/bolum-06.wav"], check=True)
print("tamam")
