// Figur „Drei Armtypen“ – die drei Arme einer Armzone, wie sie beim Abbau am 10.10.2026
// vermessen wurden. Jedes Maß kommt aus kern/angaben.json und nennt seine ID.
// Aufruf: node figuren/armtypen/build.mjs [--light] [--audit]
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "../../.claude/skills/anatomy/kit/iso-kit.mjs";
import * as A from "../../.claude/skills/anatomy/kit/audit.mjs";
import { kitScript } from "../../.claude/skills/anatomy/scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..", "..");
const THEME = process.argv.includes("--light") ? "light" : "dark";

// ---------------------------------------------------------------- Wahrheit aus dem Kern
const ANGABEN = JSON.parse(readFileSync(join(ROOT, "kern", "angaben.json"), "utf8")).angaben;
const an = (id) => {
  const a = ANGABEN.find((x) => x.id === id);
  if (!a) throw new Error(`Angabe ${id} fehlt im Kern`);
  return a;
};
const cm = (id) => {
  const a = an(id);
  return a.einheit === "m" ? a.wert * 100 : a.wert; // Skizzenmaße ohne Einheit sind cm
};
const zahl = (v) => (Math.round(v * 10) / 10).toLocaleString("de-DE");
const spanne = (id) => {
  const a = an(id);
  const f = a.einheit === "m" ? 100 : 1;
  const t = a.toleranz;
  if (t && t.art === "bereich") return `${zahl(t.von * f)}–${zahl(t.bis * f)} cm`;
  if (t && t.art === "ungefaehr") return `ca. ${zahl(a.wert * f)} cm`;
  return `${zahl(a.wert * f)} cm`;
};

const [QS_H, QS_W] = an("TH-20261009-27").wert.map((v) => v * 100); // 14 × 6,5 cm
const KERB_T = cm("AN-20261012-11"); // Kerbtiefe
const KERB_L = cm("AN-20261012-12"); // Kerblänge in Armmitte
const HALS = cm("AN-20261012-15"); // Halsbreite Mittelarm
const KROEPF = cm("AN-20261012-05"); // Versatz der Kröpfung (Skizze)
const ZONE = cm("AN-20261012-04"); // Länge der Kröpfungszone (Skizze)
const BOHR = cm("AN-20261012-17"); // Querbohrung
const WINKEL = 180 / an("CLAIM-0008").wert; // drei Armrichtungen → 60°
const COT = 1 / Math.tan((WINKEL * Math.PI) / 180);

// ---------------------------------------------------------------- Szene (1 Einheit = 1 cm)
const W = 680;
const H = 400;
const END = 62; // Arme gekürzt: ±62 cm um die Kerbe
const BASE = 10; // Oberkante der Unterleger
const HW = QS_W / 2;
const ARME = [
  { id: "A", y: -27, name: "Außenarm, nach oben gekröpft", j: KROEPF, kerbe: "oben", schraeg: 1 },
  { id: "B", y: 0, name: "Außenarm, nach unten gekröpft", j: -KROEPF, kerbe: "oben", schraeg: -1 },
  { id: "M", y: 27, name: "Mittelarm mit Hals", j: 0, kerbe: "hals", schraeg: 0 },
];
const FLOOR = { x: -84, y: -44, w: 168, d: 88, r: 2 };
const FLOOR_H = 3.2;
const LEGER = [-44, 44].map((x) => ({ x: x - 5, y: -40, w: 10, d: 80, r: 0.8 }));

const P = k.fitProjection(
  [...k.boxCorners(FLOOR, -FLOOR_H, 0), [-END, -30, BASE + QS_H + KROEPF + 22], [END, 30, BASE + QS_H + 22]],
  W,
  H,
  { pad: 18, azimuth: 62, elevation: 40 },
);
const at = (p) => k.iso(p, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (pts, style) => k.dotsSvg(pts, style);
const { sinA, cosA } = k.cameraOf(P);

const R = A.recorder(P);
const put = (name, centre, svg, shapes, extra = {}) => R.put({ piece: "figur", name: R.nameFor(name), at: centre, svg, move: [0, 0, 0], shapes: shapes.map((s) => R.solid(s)), ...extra });
const prism = (name, ring, z, h, style, inner = "") => {
  const paths = k.extrude(ring, z, h, P, { bevel: style.bevel ?? 0, convex: style.convex ?? true });
  const cx = ring.reduce((s, p) => s + p[0], 0) / ring.length;
  const cy = ring.reduce((s, p) => s + p[1], 0) / ring.length;
  put(name, [cx, cy, z + h / 2], S(paths, { tone: style.tone ?? "hi", crease: style.crease ?? "faint", lit: style.lit, inner }), [A.extruded(ring, z, h, { name })]);
};
const FLICKEN = [];
const STUFEN = [];
const rect = (x0, x1, y0, y1) => [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];

// Schattierung der Vorderseite (Normale +y), damit Flicken über Scheinfugen die Fläche treffen.
const shadeOf = (nx, ny) => Math.min(3, Math.max(0, Math.floor(((nx * -sinA + ny * cosA + 1) / 2) * 4)));
// unten/oben: [von, bis, Art] einer Kante, die der Flicken anschneidet und die neu gezogen wird.
const flicken = (s, y, z0, z1, unten, oben) => {
  const d = [[s - 0.45, y, z0], [s + 0.45, y, z0], [s + 0.45, y, z1], [s - 0.45, y, z1]].map(at);
  let out = `<path class="iso-shade" data-shade="${shadeOf(0, 1)}" d="M${d.map((p) => p.map((v) => v.toFixed(1)).join(" ")).join("L")}Z"/>`;
  for (const [kante, z] of [[unten, z0], [oben, z1]]) {
    if (!kante) continue;
    const [a, b, art] = kante;
    const seg = k.segment([s + a, y, z], [s + b, y, z], P);
    out += art === "kante" ? `<path class="iso-line iso-edge" data-tone="hi" d="${seg}"/>` : `<path class="iso-line iso-crease" data-tone="faint" d="${seg}"/>`;
  }
  return out;
};

// ---------------------------------------------------------------- Boden und Unterleger
function boden() {
  const out = [`<path class="iso-halo" d="${k.haloOf(FLOOR, -FLOOR_H, FLOOR_H, P)}"/>`];
  const bohlen = 6;
  const bw = (FLOOR.d - (bohlen - 1) * 0.6) / bohlen;
  for (let i = 0; i < bohlen; i++) {
    const y0 = FLOOR.y + i * (bw + 0.6);
    const plan = { x: FLOOR.x, y: y0, w: FLOOR.w, d: bw, r: 0.6 };
    const nails = [FLOOR.x + 4, FLOOR.x + FLOOR.w - 4].flatMap((x) => [at([x, y0 + 3, 0]), at([x, y0 + bw - 3, 0])]);
    const fasern = [0.3, 0.62].map((t) => k.lineOnTop([FLOOR.x, y0 + bw * t], [FLOOR.x + FLOOR.w, y0 + bw * t], 0, P)).join("");
    put(`stand.bohle${i}`, [0, y0 + bw / 2, -FLOOR_H / 2], S(k.slabOf(plan, -FLOOR_H, FLOOR_H, P, 2, 0.4), { tone: "lo" }) + L(fasern, { tone: "faint" }) + D(nails, { size: 0.42, tone: "lo" }), [A.slab(plan, -FLOOR_H, FLOOR_H, { name: `stand.bohle${i}` }, 2)]);
  }
  LEGER.forEach((plan, i) => {
    const ring = k.ringOf(plan, 2);
    const kanten = [plan.y + 2.5, plan.y + plan.d - 2.5].map((y) => k.lineOnTop([plan.x, y], [plan.x + plan.w, y], BASE, P)).join("");
    put(`stand.leger${i}`, [plan.x + 5, 0, BASE / 2], `<path class="iso-halo" d="${k.haloOf(plan, 0, 0.1, P)}" style="filter:blur(3px)"/>` + S(k.extrude(ring, 0, BASE, P, { bevel: 0.5 }), { tone: "mid" }) + L(kanten, { tone: "faint" }), [A.extruded(ring, 0, BASE, { name: `stand.leger${i}` })]);
  });
}

// ---------------------------------------------------------------- Ein Arm
// Querschnitt hochkant: 6,5 cm in y, 14 cm in z. Die Kerbenden stehen schräg im Kreuzungswinkel.
function arm(cfg) {
  const { id, y, j, schraeg } = cfg;
  const y0 = y - HW;
  const y1 = y + HW;
  const zU = BASE; // Unterkante außerhalb der Kröpfungszone
  const zZ = BASE + j; // Unterkante in der Zone
  const half = ZONE / 2;
  const kl = KERB_L / 2;
  // x der Kerbgrenze an der Stelle yy (links: -1, rechts: +1)
  const grenze = (seite, yy) => {
    if (schraeg) return seite * kl + schraeg * (yy - y) * COT;
    return seite * (kl + Math.abs(yy - y) * COT); // Mittelarm: zwei Kreuzungen → Kehle
  };
  const tone = { tone: "hi", bevel: 0.35 };
  const flick = [];
  if (j !== 0) {
    // Endstücke außerhalb der Zone, Zone versetzt (Kröpfung laut Skizze)
    prism(`arm${id}.ende-l`, rect(-END, -half, y0, y1), zU, QS_H, tone, maserung(-END, -half, y0, y1, zU + QS_H) + seite(-END, -half, y1, zU) + bewuchs(-END, -half, y0, y1, zU + QS_H, zU) + hirnholz(-END, y0, y1, zU));
    prism(`arm${id}.ende-r`, rect(half, END, y0, y1), zU, QS_H, tone, maserung(half, END, y0, y1, zU + QS_H) + seite(half, END, y1, zU, -Infinity, Infinity, { ende: -Infinity }) + bewuchs(half, END, y0, y1, zU + QS_H, zU) + hirnholz(END, y0, y1, zU));
    const zl = [[-half, y0], [grenze(-1, y0), y0], [grenze(-1, y1), y1], [-half, y1]];
    const zr = [[grenze(1, y0), y0], [half, y0], [half, y1], [grenze(1, y1), y1]];
    const lo = Math.max(zU, zZ);
    const hi = Math.min(zU, zZ) + QS_H;
    prism(`arm${id}.zone-l`, zl, zZ, QS_H, tone, maserung(-half, grenze(-1, y), y0, y1, zZ + QS_H, zl) + seite(-half, grenze(-1, y1), y1, zZ, -Infinity, Infinity, { ende: zZ + QS_H - KERB_T }));
    prism(`arm${id}.zone-r`, zr, zZ, QS_H, tone, maserung(grenze(1, y), half, y0, y1, zZ + QS_H, zr) + seite(grenze(1, y1), half, y1, zZ, -Infinity, Infinity, { anfang: zZ + QS_H - KERB_T }));
    // A (Zone höher): unten setzt die Zonenunterkante an, oben endet die Kante des Endstücks; B umgekehrt.
    const auf = j > 0;
    const sx = auf ? -half : half;
    const sz = auf ? zU + QS_H : zZ + QS_H;
    STUFEN.push({ svg: `<path class="iso-line iso-edge" data-tone="hi" d="${k.segment([sx, y0, sz], [sx, y1, sz], P)}"/>`, nachbarn: [`arm${id}.${auf ? "ende-l" : "ende-r"}`, `arm${id}.${auf ? "zone-l" : "zone-r"}`] });
    flick.push(
      [-half, lo, hi, "ende-l", "zone-l", auf ? [0, 0.7, "kante"] : [-0.7, 0, "kante"], auf ? [-0.7, 0, "falz"] : [0, 0.7, "falz"]],
      [half, lo, hi, "ende-r", "zone-r", auf ? [-0.7, 0, "kante"] : [0, 0.7, "kante"], auf ? [0, 0.7, "falz"] : [-0.7, 0, "falz"]],
    );
    const boden = zZ + QS_H - KERB_T;
    const kerbe = [[grenze(-1, y0), y0], [grenze(1, y0), y0], [grenze(1, y1), y1], [grenze(-1, y1), y1]];
    prism(`arm${id}.kerbe`, kerbe, zZ, QS_H - KERB_T, tone, seite(grenze(-1, y1), grenze(1, y1), y1, zZ, zZ, boden) + bohrung(0, y, boden));
    flick.push(
      [grenze(-1, y1), zZ, boden, "zone-l", "kerbe", [-0.7, 0.7, "kante"], [0, 0.7, "falz"]],
      [grenze(1, y1), zZ, boden, "zone-r", "kerbe", [-0.7, 0.7, "kante"], [-0.7, 0, "falz"]],
    );
  } else {
    // Mittelarm: gerade, beidseitig ausgeklinkt
    const lpoly = [[-END, y0], [grenze(-1, y0), y0], [-kl, y], [grenze(-1, y1), y1], [-END, y1]];
    const rpoly = [[grenze(1, y0), y0], [END, y0], [END, y1], [grenze(1, y1), y1], [kl, y]];
    prism(`arm${id}.links`, lpoly, zU, QS_H, tone, maserung(-END, -kl - 2, y0, y1, zU + QS_H, lpoly) + seite(-END, grenze(-1, y1), y1, zU, -Infinity, Infinity, { ende: zU + (QS_H + HALS) / 2 }) + bewuchs(-END, -kl, y0, y1, zU + QS_H, zU) + hirnholz(-END, y0, y1, zU));
    prism(`arm${id}.rechts`, rpoly, zU, QS_H, tone, maserung(kl + 2, END, y0, y1, zU + QS_H, rpoly) + seite(grenze(1, y1), END, y1, zU, -Infinity, Infinity, { anfang: zU + (QS_H + HALS) / 2, ende: -Infinity }) + bewuchs(kl, END, y0, y1, zU + QS_H, zU) + hirnholz(END, y0, y1, zU) + zeichen(y));
    const zh = zU + (QS_H - HALS) / 2;
    // Hals in zwei konvexe Hälften geteilt (sonst verschränkt er sich mit den Nachbarn), die Fuge auf
    // dem Kerbgrund wird überdeckt, darauf die Bohrung.
    prism(`arm${id}.hals-h`, [[grenze(-1, y0), y0], [grenze(1, y0), y0], [kl, y], [-kl, y]], zh, HALS, tone);
    prism(`arm${id}.hals-v`, [[-kl, y], [kl, y], [grenze(1, y1), y1], [grenze(-1, y1), y1]], zh, HALS, tone, seite(grenze(-1, y1), grenze(1, y1), y1, zU, zh, zh + HALS));
    const zt = zh + HALS;
    const band = [[-kl + 0.3, y - 0.45], [kl - 0.3, y - 0.45], [kl - 0.3, y + 0.45], [-kl + 0.3, y + 0.45]].map(([px, py]) => at([px, py, zt]));
    FLICKEN.push({ svg: `<path class="iso-top" d="M${band.map((q) => q.map((v) => v.toFixed(1)).join(" ")).join("L")}Z"/>` + bohrung(0, y, zt), nachbarn: [`arm${id}.hals-h`, `arm${id}.hals-v`] });
    flick.push([grenze(-1, y1), zh, zh + HALS, "links", "hals-v", [0, 0.7, "kante"], [0, 0.7, "falz"]], [grenze(1, y1), zh, zh + HALS, "rechts", "hals-v", [-0.7, 0, "kante"], [-0.7, 0, "falz"]]);
  }
  for (const [s, z0, z1, a, b, unten, oben] of flick) if (z1 > z0) FLICKEN.push({ svg: flicken(s, y1, z0, z1, unten, oben), nachbarn: [`arm${id}.${a}`, `arm${id}.${b}`] });
}


// Maserung auf der Vorderseite (y = yv) zwischen x0 und x1, Unterkante zb
function seite(x0, x1, yv, zb, zmin = -Infinity, zmax = Infinity, { anfang = Infinity, ende = Infinity } = {}) {
  // Linien über der Höhe `anfang` bzw. `ende` laufen an diesem Ende aus (dort ist keine gezeichnete Kante).
  const out = [];
  const plain = [];
  [0.34, 0.71].forEach((t, i) => {
    const zl = zb + QS_H * t;
    if (zl < zmin + 0.6 || zl > zmax - 0.6) return;
    const pts = [];
    for (let n = 0; n <= 10; n++) {
      const x = x0 + ((x1 - x0) * n) / 10;
      const z = zl + (n > 0 && n < 10 ? 0.35 * Math.sin(n * 1.3 + i * 2) : 0);
      pts.push(at([x, yv, z]));
    }
    const fade = [zl > anfang ? 14 : 0, zl > ende ? 14 : 0];
    if (fade[0] || fade[1]) out.push(k.fadeLineSvg(pts, { fade, tone: "faint" }));
    else plain.push(`M${pts.map((q) => q.map((v) => v.toFixed(1)).join(" ")).join("L")}`);
  });
  return L(plain.join(""), { tone: "faint" }) + out.join("");
}

// Bewuchs: außen bemoost, zur Kerbzone hin sauber (AN-20261012-18). Punkte blenden nach innen aus.
let saat = 7;
const zufall = () => ((saat = (saat * 16807) % 2147483647) / 2147483647);
function bewuchs(x0, x1, y0, y1, zt, zb) {
  const pts = [];
  const von = 36;
  for (let n = 0; n < 90; n++) {
    const x = x0 + (x1 - x0) * zufall();
    const a = Math.min(0.55, Math.max(0, (Math.abs(x) - von) / (END - von)) * 0.55);
    if (a < 0.03) continue;
    if (n % 2) pts.push([...at([x, y0 + 0.4 + (y1 - y0 - 0.8) * zufall(), zt]), a]);
    else pts.push([...at([x, y1, zb + 0.5 + (QS_H - 1) * zufall()]), a]);
  }
  return D(pts, { size: 0.32, tone: "lo" });
}

// Maserung auf der Oberseite: Linien längs, von Kante zu Kante (bzw. bis zur Kerbgrenze)
function maserung(x0, x1, y0, y1, z, poly) {
  const lines = [];
  [0.28, 0.55, 0.8].forEach((t, i) => {
    const yy = y0 + (y1 - y0) * t;
    let a = x0;
    let b = x1;
    if (poly) {
      const xs = schnitt(poly, yy);
      if (xs.length < 2) return;
      a = xs[0];
      b = xs[xs.length - 1];
    }
    const wobble = i === 1 ? 0.25 : -0.2;
    const pts = [];
    for (let n = 0; n <= 8; n++) {
      const x = a + ((b - a) * n) / 8;
      pts.push([x, yy + (n > 0 && n < 8 ? wobble * Math.sin(n * 1.7 + i) : 0)]);
    }
    lines.push(k.onTop(pts, z, P));
  });
  return L(lines.join(""), { tone: "faint" });
}
function schnitt(poly, yy) {
  const xs = [];
  for (let i = 0; i < poly.length; i++) {
    const [ax, ay] = poly[i];
    const [bx, by] = poly[(i + 1) % poly.length];
    if ((ay <= yy && by > yy) || (by <= yy && ay > yy)) xs.push(ax + ((yy - ay) / (by - ay)) * (bx - ax));
  }
  return xs.sort((p, q) => p - q);
}

// Hirnholz an der Schnittstelle (nur sichtbar am rechten Ende): Jahresringe als Bögen,
// die auf den Kanten der Stirnfläche enden. Mark liegt außerhalb des Querschnitts.
function hirnholz(x, y0, y1, z0) {
  if (x < 0) return "";
  const mark = [y0 - 3, z0 + QS_H + 4]; // Mark oben außen: Ringe laufen von der Ober- zur Hinterkante
  const out = [];
  const zt = z0 + QS_H;
  for (const r of [6, 7.3, 8.6, 9.9]) {
    // Schnittwinkel des Kreises mit den vier Kanten, dann die Bögen dazwischen, die innen liegen
    const winkel = [];
    for (const yy of [y0, y1]) { const c = (yy - mark[0]) / r; if (Math.abs(c) <= 1) { const t = Math.acos(c); winkel.push(t, -t); } }
    for (const zz of [z0, zt]) { const c = (zz - mark[1]) / r; if (Math.abs(c) <= 1) { const t = Math.asin(c); winkel.push(t, Math.PI - t); } }
    const ws = [...new Set(winkel.map((w) => ((w % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI)))].sort((a, b) => a - b);
    for (let i = 0; i < ws.length; i++) {
      const a = ws[i];
      const b = i + 1 < ws.length ? ws[i + 1] : ws[0] + 2 * Math.PI;
      const m = (a + b) / 2;
      const ym = mark[0] + r * Math.cos(m);
      const zm = mark[1] + r * Math.sin(m);
      if (ym < y0 || ym > y1 || zm < z0 || zm > zt) continue;
      const pts = [];
      for (let n = 0; n <= 24; n++) {
        const t = a + ((b - a) * n) / 24;
        pts.push(at([x, Math.min(y1, Math.max(y0, mark[0] + r * Math.cos(t))), Math.min(zt, Math.max(z0, mark[1] + r * Math.sin(t)))]));
      }
      out.push(`M${pts.map((q) => q.map((v) => v.toFixed(1)).join(" ")).join("L")}`);
    }
  }
  const riss = [[x, y0 + 1.2, z0 + QS_H], [x, y0 + 2.1, z0 + QS_H - 3.4]];
  return L(out.join(""), { tone: "lo" }) + L(k.segment(riss[0], riss[1], P), { tone: "lo", free: "end" });
}

// Querbohrung im Kerbgrund (AN-20261012-17)
function bohrung(x, y, z) {
  const r = BOHR / 2;
  const ring = k.circleRing(x, y, r, 18);
  const d = `M${ring.map(([px, py]) => at([px, py, z]).map((v) => v.toFixed(1)).join(" ")).join("L")}Z`;
  return `<path class="iso-line" data-tone="mid" d="${d}" style="fill:var(--anatomy-halo)"/>`;
}

// Eingeschlagene Ziffer am Mittelarm (CLAIM-0014: Mittelarm trägt 1 und 4)
function zeichen(y) {
  return k.faceTextSvg(k.topMatrix([44, y - 1.2], BASE + QS_H, P, "x"), "1", { size: 3.4, tone: "lo", anchor: "middle" });
}

// ---------------------------------------------------------------- Zollstock
// Zwei aufgeklappte Glieder (je 20 cm, 1,6 breit, 0,3 dick), an jeder Messstelle einzeln gebaut.
const GLIED = 20;
function zollstock(name, origin, dir, quer, n = 2) {
  // origin: Nullpunkt; dir: Richtung entlang des Stocks; quer: Richtung der Breite
  const len = GLIED * n;
  const add = (p, v, s) => [p[0] + v[0] * s, p[1] + v[1] * s, p[2] + v[2] * s];
  const t = 0.3;
  const vertikal = dir[2] !== 0;
  const items = [];
  if (!vertikal) {
    // liegend: als Platte auf z = origin[2]
    const a = origin;
    const b = add(a, dir, len);
    const c = add(b, quer, 1.6);
    const d = add(a, quer, 1.6);
    const ring = [a, b, c, d].map((p) => [p[0], p[1]]);
    const paths = k.extrude(ring, origin[2], t, P, { bevel: 0 });
    const ticks = [];
    for (let cmv = 1; cmv < len; cmv++) {
      const lang = cmv % 10 === 0 ? 0.9 : cmv % 5 === 0 ? 0.65 : 0.38;
      const p0 = add(origin, dir, cmv);
      ticks.push(k.lineOnTop([p0[0], p0[1]], [p0[0] + quer[0] * lang, p0[1] + quer[1] * lang], origin[2] + t, P));
    }
    const fuge = add(add(origin, dir, GLIED), quer, 0.8);
    items.push(S(paths, { tone: "hi", lit: true, inner: L(ticks.join(""), { tone: "lo" }) }) + D([at([fuge[0], fuge[1], origin[2] + t])], { size: 0.55, tone: "hi" }));
    put(name, add(add(origin, dir, len / 2), quer, 0.8), items.join(""), [A.extruded(ring, origin[2], t, { name })], { station: name });
  } else {
    // stehend: schmale Säule, Breite entlang quer, Dicke t
    const ring = [[origin[0], origin[1]], [origin[0] + quer[0] * 1.6, origin[1] + quer[1] * 1.6], [origin[0] + quer[0] * 1.6 - quer[1] * t, origin[1] + quer[1] * 1.6 + quer[0] * t], [origin[0] - quer[1] * t, origin[1] + quer[0] * t]];
    const paths = k.extrude(ring, origin[2], len, P, { bevel: 0 });
    const ticks = [];
    const front = [origin[0] - quer[1] * t, origin[1] + quer[0] * t];
    for (let cmv = 1; cmv < len; cmv++) {
      const lang = cmv % 10 === 0 ? 0.9 : cmv % 5 === 0 ? 0.65 : 0.38;
      const z = origin[2] + cmv;
      ticks.push(k.segment([front[0], front[1], z], [front[0] + quer[0] * lang, front[1] + quer[1] * lang, z], P));
    }
    const fz = origin[2] + GLIED;
    items.push(S(paths, { tone: "hi", lit: true, inner: L(ticks.join(""), { tone: "lo" }) }) + D([at([front[0] + quer[0] * 0.8, front[1] + quer[1] * 0.8, fz])], { size: 0.55, tone: "hi" }));
    put(name, [origin[0], origin[1], origin[2] + len / 2], items.join(""), [A.extruded(ring, origin[2], len, { name })], { station: name });
  }
}

// ---------------------------------------------------------------- Aufbau
boden();
ARME.forEach(arm);

const armA = ARME[0];
const armB = ARME[1];
const armM = ARME[2];
const topA = BASE + armA.j + QS_H;
const STATIONEN = [
  { id: "kerbtiefe", titel: "Kerbtiefe", wert: spanne("AN-20261012-11"), ids: "AN-20261012-11" },
  { id: "kerblaenge", titel: "Kerblänge", wert: spanne("AN-20261012-12"), ids: "AN-20261012-12" },
  { id: "kroepfung", titel: "Kröpfung", wert: `${zahl(KROEPF)} (Skizze)`, ids: "AN-20261012-05" },
  { id: "hals", titel: "Halsbreite", wert: spanne("AN-20261012-15"), ids: "AN-20261012-15" },
  { id: "breite", titel: "Armbreite", wert: spanne("AN-20261012-09"), ids: "AN-20261012-09" },
  { id: "dicke", titel: "Armdicke", wert: spanne("AN-20261012-10"), ids: "AN-20261012-10" },
];
// Kerbtiefe: stehend im Kerbgrund von A, an der Vorderkante
zollstock("station.kerbtiefe", [-0.8 + armA.y * 0 + 0.0, armA.y + HW - 1.9, topA - KERB_T], [0, 0, 1], [1, 0, 0], 1);
// Kerblänge: liegend über der Kerbe von A, Null an der linken Kerbgrenze
zollstock("station.kerblaenge", [-KERB_L / 2 - (HW - 0.2) * COT, armA.y + HW - 1.8, topA], [1, 0, 0], [0, 1, 0], 1);
// Kröpfung: stehend auf dem linken Endstück von A, an der Stufe
zollstock("station.kroepfung", [-ZONE / 2 - 1.9, armA.y - 0.8, BASE + QS_H], [0, 0, 1], [1, 0, 0], 1);
// Halsbreite: stehend vor dem Hals des Mittelarms, auf dem Boden
zollstock("station.hals", [-0.8, armM.y + HW + 0.05, 0], [0, 0, 1], [1, 0, 0], 2);
// Armbreite: stehend auf dem Unterleger vor dem Mittelarm
zollstock("station.breite", [30, armM.y + HW + 0.05, BASE], [0, 0, 1], [1, 0, 0], 1);
// Armdicke: liegend quer über den Mittelarm
zollstock("station.dicke", [-30, armM.y - HW - 4, BASE + QS_H], [0, 1, 0], [-1, 0, 0], 1);

A.settle(R, P);
// Flicken direkt über die Fuge, die sie verdecken: nach dem höchsten Nachbarn zeichnen
for (const f of [...FLICKEN, ...STUFEN]) {
  const later = R.items.filter((it) => f.nachbarn.includes(it.name)).sort((a, b) => b.key - a.key)[0];
  later.svg += f.svg;
}
R.items.sort((a, b) => a.key - b.key);

const groups = R.items.map((item) => (item.station ? `<g data-station="${item.station.replace("station.", "")}"${item.station === "station.kerbtiefe" ? "" : ' style="opacity:0"'}>${item.svg}</g>` : item.svg));

const LABEL =
  "Drei Arme des Kleinen Schäferrads hochkant auf zwei Unterlegern: vorn der gerade Mittelarm mit beidseitig ausgeklinktem Hals, dahinter zwei Außenarme mit einseitiger Kerbe, der eine nach oben, der andere nach unten gekröpft. Ein Zollstock zeigt nacheinander die gemessenen Maße.";
const svg = k.figureSvg({ width: W, height: H, label: LABEL, body: groups });

const DATA = { stationen: STATIONEN };
const LIVE = readFileSync(join(HERE, "..", "gemeinsam", "stationen.js"), "utf8").replace("__DATA__", JSON.stringify(DATA));

const body = k.plateHtml({
  fig: "Fig 1",
  title: "Drei Armtypen",
  hint: "Zeigen oder Pfeiltasten: Messstelle wählen",
  readout: `${STATIONEN[0].titel} · ${STATIONEN[0].wert} · ${STATIONEN[0].ids}`,
  keys: [
    { mark: "lit", label: "Zollstock an der gerade gezeigten Messstelle" },
    { mark: "raised", label: "Die drei Arme, gezeichnet nach den Maßen im Kern" },
  ],
  caption:
    `Die drei Armtypen einer Armzone, vermessen beim Abbau am 10.10.2026, hochkant auf zwei Unterlegern. Vorn der gerade Mittelarm mit beidseitig ausgeklinktem Hals (${spanne("AN-20261012-15")}, AN-20261012-15), dahinter die zwei Außenarme mit einseitiger Kerbe (Tiefe ${spanne("AN-20261012-11")}, Länge ${spanne("AN-20261012-12")}), gegensinnig gekröpft (AN-20261011-12, Skizze: ${zahl(KROEPF)} auf ${zahl(ZONE)}). ` +
    `Querschnitt ${zahl(QS_H)} × ${zahl(QS_W)} cm (TH-20261009-27). Im Kerbgrund sitzt eine Querbohrung von ${spanne("AN-20261012-17")}. Die Arme sind gekürzt gezeichnet: je ${END} cm um die Kerbe, ganz sind sie 4,55 m lang, und die Kerbe liegt in der Armmitte (AN-20261012-19). ` +
    `Angenommen sind der Kreuzungswinkel von ${zahl(WINKEL)}° (drei Armrichtungen, CLAIM-0008), die Lage der Kröpfungsstufen am Rand der Zone und die Kröpfung bei beiden Außenarmen. Alle Maße sind offen, bis Thorsten sie bestätigt. Wie die drei Arme in der Welle ineinandergreifen, zeigt diese Figur nicht: Das sind die Fragen F-005 und F-034.`,
  body: `<div class="iso-stage" tabindex="0" role="slider" aria-label="Drei Armtypen: Pfeiltasten wechseln die Messstelle" aria-valuemin="1" aria-valuemax="${STATIONEN.length}" aria-valuenow="1">${svg}</div>`,
});

const page = k.pageHtml({ title: "Drei Armtypen", theme: THEME, body, script: kitScript() + LIVE, width: 720 }).replace('<html lang="en">', '<html lang="de">');
const out = THEME === "light" ? "armtypen-hell.html" : "armtypen.html";
writeFileSync(join(HERE, out), page);
console.log("geschrieben:", out, `${(page.length / 1024).toFixed(0)} KB`, `${R.items.length} Teile`);
A.auditOrExit(R, P);
