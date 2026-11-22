"""Bölüm 4 ses miksi. Kullanım: python3 araclar/ses-miks-b04.py (kor-nokta klasöründen).
Replik başlangıçları bolumler/bolum-04.html'deki R tablosuyla aynıdır."""
import subprocess
SES, SURE = "assets/ses", 60.5
ZIRVE = {"b04/r01-anlatici": -6.8, "b04/r02-mercan": -1.7, "b04/r03-anlatici": -5.7, "b04/r04-poyraz": -6.5, "b04/r05-mercan": -2.0,
         "b04/r06-poyraz": -9.8, "b04/r07-anlatici": -8.8, "b04/r08-sami": -4.6, "b04/r09-mercan": -1.3, "b04/r10-sami": -2.2,
         "b04/r11-mercan": -2.0, "b04/r12-sami": -2.4, "b04/r13-anlatici": -6.3, "b04/fx-adim": -32.6,
         "v2/fx-kapi": -8.1, "fx-kagit": -17.3, "fx-pop": -3.4, "fx-vurus": -3.1}
REPLIK = [("b04/r01-anlatici", 0.7), ("b04/r02-mercan", 7.7), ("b04/r03-anlatici", 12.1), ("b04/r04-poyraz", 17.0), ("b04/r05-mercan", 21.9),
          ("b04/r06-poyraz", 26.0), ("b04/r07-anlatici", 30.9), ("b04/r08-sami", 36.6), ("b04/r09-mercan", 40.9), ("b04/r10-sami", 42.9),
          ("b04/r11-mercan", 47.5), ("b04/r12-sami", 49.9), ("b04/r13-anlatici", 53.2)]
FX = [("v2/fx-kapi", 5.5, -8), ("b04/fx-adim", 28.9, -8), ("b04/fx-adim", 34.2, -11), ("fx-vurus", 35.0, -5), ("fx-vurus", 52.35, -4),
      ("fx-kagit", 10.85, -13), ("fx-kagit", 20.65, -13), ("fx-kagit", 41.65, -13)] + \
     [("fx-pop", t - 0.17, -12) for t in (7.7, 17.0, 21.9, 26.0, 36.6, 40.9, 42.9, 47.5, 49.9)]
girdi, filtre, etiket = [], [], []
def ekle(dosya, f):
    i = len(girdi); girdi.append(dosya); filtre.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{f}[a{i}]"); etiket.append(f"[a{i}]")
for d, t in REPLIK: ekle(d, f"volume={-3 - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
for d, t, hedef in FX: ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
# müzik: 7. replikten önce (28.4) susar; sonrası sessizlik ve cepteki saatin tıkırtısı
ekle("muzik-noir", "volume=0.26,afade=t=out:st=26.6:d=1.8,adelay=0:all=1")
# Mercan'ın cebindeki 2/6 saati: müzik susunca duyulur, kapanışta biraz öne çıkar
for t in (28.2, 38.0, 47.8):
    ekle("b02/fx-tiktak", f"volume=8dB,afade=t=in:st=0:d=0.8,adelay={int(t*1000)}:all=1")
ekle("b02/fx-tiktak", "atrim=0:8,volume=13dB,afade=t=in:st=0:d=0.5,adelay=52400:all=1")
ekle("fx-yagmur", "volume=0.38,afade=t=in:st=0:d=1,afade=t=out:st=27:d=3,adelay=0:all=1")
ekle("fx-yagmur", "volume=0.3,afade=t=in:st=0:d=3,afade=t=out:st=27:d=3,adelay=27000:all=1")
komut = ["ffmpeg", "-nostdin", "-y", "-v", "error"]
for g in girdi: komut += ["-i", f"{SES}/{g}.mp3"]
fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={len(girdi)}:normalize=0:duration=longest,alimiter=limit=0.84:level=0,apad,atrim=0:{SURE},afade=t=out:st={SURE-0.6}:d=0.6[o]"
subprocess.run(komut + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{SES}/bolum-04.wav"], check=True)
print("tamam")
