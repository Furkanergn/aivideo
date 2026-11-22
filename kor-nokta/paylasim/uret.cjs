// Kullanım: node paylasim/uret.cjs   (kor-nokta klasöründen) — kapak ve hikaye görsellerini ../teslim/paylasim altına yazar
const { chromium } = require('playwright');
const path = require('path');
const isler = [
  ['bolum-01-kapak', 'kapak', 1920, { bolum: 1, resim: 'p06-mercan.jpg', alt: 'Saat üçe on kala durdu. Katil durmadı.' }],
  ['bolum-01-hikaye', 'hikaye', 1920, { bolum: 1, resim: 'p01-saat.jpg', y: -300, ibre: '534,939,85,300,180,290', alt: 'Bir saat durdu. Kapağında bir sayı: 1/6.' }],
  ['bolum-02-kapak', 'kapak', 1920, { bolum: 2, resim: 'b02/q02-emre.jpg', alt: 'Üst katta biri saklanıyordu. Ve bir saat hâlâ işliyor.' }],
  ['bolum-02-hikaye', 'hikaye', 1920, { bolum: 2, resim: 'b02/q10-saat.jpg', y: -150, ibre: '555,822,140,240,36,190', alt: 'Paketten bir saat çıktı. Hâlâ işliyor.' }],
];
(async () => {
  const b = await chromium.launch();
  for (const [ad, tur, yuk, p] of isler) {
    const s = await b.newPage({ viewport: { width: 1080, height: yuk }, deviceScaleFactor: 1 });
    const q = new URLSearchParams({ tur, ...p }).toString();
    await s.goto('file://' + path.resolve('paylasim/sablon.html') + '?' + q);
    await s.evaluate(() => document.fonts.ready); await s.waitForTimeout(400);
    await s.screenshot({ path: path.resolve('../teslim/paylasim', ad + '.jpg'), type: 'jpeg', quality: 93 });
    await s.close(); console.log(ad);
  }
  await b.close();
})();
