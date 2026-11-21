"""Bölüm 2 ses miksi. Kullanım: python3 araclar/ses-miks-b02.py (kor-nokta klasöründen).
Replik başlangıçları bolumler/bolum-02.html'deki R tablosuyla aynıdır."""
import subprocess
SES, SURE = "assets/ses", 65.0
ZIRVE = {"b02/r01-anlatici": -9.0, "b02/r02-emre": -5.9, "b02/r03-mercan": -1.4, "b02/r04-emre": -16.9, "b02/r05-emre": -16.3,
         "b02/r06-mercan": -1.3, "b02/r07-emre": -16.0, "b02/r08-mercan": -2.0, "b02/r09-poyraz": -3.8, "b02/r10-mercan": -2.2,
         "b02/r11-poyraz": -10.9, "b02/r12-mercan": -1.4, "b02/r13-anlatici": -6.5,
         "b02/fx-tornavida": -3.5, "b02/fx-paket": -16.5, "b02/fx-tiktak": -33.7,
         "fx-kagit": -17.3, "fx-pop": -3.4, "fx-vurus": -3.1, "fx-gicirti": -14.4}
REPLIK = [("b02/r01-anlatici", 0.7), ("b02/r02-emre", 8.6), ("b02/r03-mercan", 12.7), ("b02/r04-emre", 19.3), ("b02/r05-emre", 24.0),
          ("b02/r06-mercan", 29.5), ("b02/r07-emre", 31.5), ("b02/r08-mercan", 36.9), ("b02/r09-poyraz", 40.1), ("b02/r10-mercan", 48.2),
          ("b02/r11-poyraz", 50.4), ("b02/r12-mercan", 52.6), ("b02/r13-anlatici", 59.0)]
FX = [("fx-gicirti", 5.8, -5), ("fx-vurus", 7.85, -5), ("b02/fx-tornavida", 17.2, -6), ("b02/fx-paket", 45.5, -5), ("fx-vurus", 58.25, -4),
      ("fx-kagit", 11.45, -13), ("fx-kagit", 22.85, -13), ("fx-kagit", 35.45, -13), ("fx-kagit", 51.35, -13)] + \
     [("fx-pop", t - 0.17, -12) for t in (8.6, 12.7, 19.3, 29.5, 31.5, 36.9, 40.1, 48.2, 50.4, 52.6)]
girdi, filtre, etiket = [], [], []
def ekle(dosya, f):
    i = len(girdi); girdi.append(dosya); filtre.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{f}[a{i}]"); etiket.append(f"[a{i}]")
for d, t in REPLIK: ekle(d, f"volume={-3 - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
for d, t, hedef in FX: ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
# aşağıdaki dükkânın saatleri: Emre "saatler sustu" derken kesilir (28.0)
ekle("b02/fx-tiktak", "atrim=0:5,volume=9dB,afade=t=in:st=0:d=0.6,afade=t=out:st=4.2:d=0.1,adelay=23400:all=1")
# 2/6 saati: paketten çıkınca işlemeye başlar, sona kadar sürer
ekle("b02/fx-tiktak", "volume=15dB,afade=t=in:st=0:d=0.4,adelay=46700:all=1")
ekle("b02/fx-tiktak", "volume=15dB,adelay=56200:all=1")
ekle("muzik-noir", "volume=0.26,afade=t=out:st=27.5:d=3,adelay=6000:all=1")
ekle("muzik-noir", "atrim=3:27,asetpts=PTS-STARTPTS,volume=0.26,afade=t=in:st=0:d=2.5,afade=t=out:st=11:d=2,adelay=33700:all=1")
ekle("fx-yagmur", "volume=0.4,afade=t=in:st=0:d=1,afade=t=out:st=27:d=3,adelay=0:all=1")
ekle("fx-yagmur", "volume=0.4,afade=t=in:st=0:d=3,afade=t=out:st=17:d=2.5,adelay=27000:all=1")
komut = ["ffmpeg", "-nostdin", "-y", "-v", "error"]
for g in girdi: komut += ["-i", f"{SES}/{g}.mp3"]
fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={len(girdi)}:normalize=0:duration=longest,alimiter=limit=0.84:level=0,apad,atrim=0:{SURE},afade=t=out:st={SURE-0.6}:d=0.6[o]"
subprocess.run(komut + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{SES}/bolum-02.wav"], check=True)
print("tamam")
