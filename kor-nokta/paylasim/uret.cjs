// Kullanım: node paylasim/uret.cjs paylasim/isler-b01.json   (kor-nokta klasöründen) — kapak ve hikaye görsellerini ../teslim/paylasim altına yazar
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const isler = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
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
