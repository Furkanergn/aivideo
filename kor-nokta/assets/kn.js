/* KÖR NOKTA — ortak sabitler ve yardımcılar. Sahneler sayı ve rengi buradan okur. */
(function () {
  const renk = { siyah: "#05070c", gece: "#0f1a2e", lacivert: "#1d3052", celik: "#3a5480", kemik: "#efe6d2", kehribar: "#f2a516", ten: "#e8b88a", sac: "#2b1b17" };
  window.REEL = {
    renk,
    // sahne başlangıçları (saniye) — index.html'deki data-start ile aynı
    sure: { saat: 0, sokak: 3, diyalog: 9.5, bardak: 15, kapak: 22, tavan: 27.5, tahta: 31, toplam: 35, gecis: 0.28 },
    egri: { giris: "power3.out", cikis: "power2.in", yay: "back.out(1.9)", sakin: "sine.inOut" },
  };
  // sabit tohumlu rastgele sayı üreteci: aynı kare her render'da aynı çıkar
  window.knTohum = function (a) {
    return function () { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  };
  const NS = "http://www.w3.org/2000/svg";
  window.knEl = function (ad, oz, ebeveyn) { const e = document.createElementNS(NS, ad); for (const k in oz) e.setAttribute(k, oz[k]); if (ebeveyn) ebeveyn.appendChild(e); return e; };
  // kadran çizgileri
  window.knKadran = function (g, cx, cy, ic, dis, kalin) {
    for (let i = 0; i < 12; i++) { const t = (i * Math.PI) / 6, a = i % 3 === 0 ? ic - (dis - ic) * 0.6 : ic; window.knEl("line", { x1: cx + Math.sin(t) * a, y1: cy - Math.cos(t) * a, x2: cx + Math.sin(t) * dis, y2: cy - Math.cos(t) * dis, stroke: renk.siyah, "stroke-width": i % 3 === 0 ? kalin * 1.5 : kalin, "stroke-linecap": "round" }, g); }
  };
  // sahne girişi: yeni sayfa, eskisinin üstüne sağdan kayar
  window.knSayfaGir = function (tl, secici) { tl.fromTo(secici, { xPercent: 100 }, { xPercent: 0, duration: window.REEL.sure.gecis, ease: window.REEL.egri.giris }, 0); };
  // konuşma balonu: yay eğrisiyle açılır
  window.knBalon = function (tl, secici, t) { tl.fromTo(secici, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.34, ease: window.REEL.egri.yay }, t); };
})();
