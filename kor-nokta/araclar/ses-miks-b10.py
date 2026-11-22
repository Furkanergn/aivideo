"""Bölüm 10 ses miksi. Kullanım: python3 araclar/ses-miks-b10.py (kor-nokta klasöründen).
Replik başlangıçları bolumler/bolum-10.html'deki R tablosuyla aynıdır."""
import subprocess
SES, SURE = "assets/ses", 66.0
ZIRVE = {"b10/r01-anlatici": -7.1, "b10/r02-poyraz": -7.1, "b10/r03-defne": -6.9, "b10/r04-tarik": -4.1, "b10/r05-defne": -5.1,
         "b10/r06-mercan": -1.2, "b10/r07-defne": -2.4, "b10/r08-anlatici": -4.7, "b10/r09-tarik": -1.1, "b10/r10-mercan": -1.6,
         "b10/r11-anlatici": -6.2, "b10/r12-mercan": -1.6, "b10/r13-anlatici": -5.9,
         "b05/fx-adim": -20.9, "fx-kagit": -16.9, "fx-pop": -2.9, "fx-vurus": -2.7, "fx-kapak": -8.6}
REPLIK = [("b10/r01-anlatici", 0.8), ("b10/r02-poyraz", 6.6), ("b10/r03-defne", 11.1), ("b10/r04-tarik", 15.7), ("b10/r05-defne", 18.2),
          ("b10/r06-mercan", 23.4), ("b10/r07-defne", 26.2), ("b10/r08-anlatici", 32.2), ("b10/r09-tarik", 37.2), ("b10/r10-mercan", 43.2),
          ("b10/r11-anlatici", 48.2), ("b10/r12-mercan", 54.2), ("b10/r13-anlatici", 57.4)]
# sayfa çevirme (kâğıt), telefon bildirimi (pop), kapağın açılması (kapak), kapanış vuruşu
FX = [("b05/fx-adim", 0.15, -10), ("fx-kagit", 5.75, -13), ("fx-kagit", 14.95, -13), ("fx-kagit", 22.75, -13), ("fx-kagit", 36.75, -13),
      ("fx-kagit", 42.55, -13), ("fx-pop", 19.75, -7), ("fx-kapak", 47.05, -5), ("fx-vurus", 56.6, -5)] + \
     [("fx-pop", t - 0.17, -12) for t in (6.6, 11.1, 15.7, 18.2, 23.4, 26.2, 37.2, 43.2, 54.2)]
girdi, filtre, etiket = [], [], []
def ekle(dosya, f):
    i = len(girdi); girdi.append(dosya); filtre.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{f}[a{i}]"); etiket.append(f"[a{i}]")
for d, t in REPLIK: ekle(d, f"volume={-3 - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
for d, t, hedef in FX: ekle(d, f"volume={hedef - ZIRVE[d]:.1f}dB,adelay={int(t*1000)}:all=1")
# dördüncü saat: kapak açılınca işlemeye başlar, sona kadar sürer
ekle("b02/fx-tiktak", "volume=15dB,afade=t=in:st=0:d=0.4,adelay=47400:all=1")
ekle("b02/fx-tiktak", "volume=15dB,adelay=56900:all=1")
# müzik: 7. replikten sonra susar (arşiv binası sessizliği), Tarık'la döner, kapak açılmadan önce yine susar
ekle("muzik-noir", "volume=0.26,afade=t=out:st=28.3:d=2.6,adelay=2000:all=1")
ekle("muzik-noir", "atrim=3:13.2,asetpts=PTS-STARTPTS,volume=0.24,afade=t=in:st=0:d=2.0,afade=t=out:st=7.8:d=2.4,adelay=36400:all=1")
ekle("fx-yagmur", "volume=0.16,afade=t=in:st=0:d=1,afade=t=out:st=27:d=3,adelay=0:all=1")
ekle("fx-yagmur", "volume=0.16,afade=t=in:st=0:d=3,afade=t=out:st=17:d=3,adelay=27000:all=1")
komut = ["ffmpeg", "-nostdin", "-y", "-v", "error"]
for g in girdi: komut += ["-i", f"{SES}/{g}.mp3"]
fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={len(girdi)}:normalize=0:duration=longest,alimiter=limit=0.84:level=0,apad,atrim=0:{SURE},afade=t=out:st={SURE-0.6}:d=0.6[o]"
subprocess.run(komut + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{SES}/bolum-10.wav"], check=True)
print("tamam")
