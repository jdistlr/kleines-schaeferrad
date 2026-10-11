// Figur „Wellenlager Landseite“ – Wellenende mit Dorn im offenen Schlitz des Lagerklotzes,
// abgelesen beim Abbau am 10.10.2026. Jedes Maß kommt aus kern/angaben.json und nennt seine ID.
// Aufruf: node figuren/wellenlager/build.mjs [--light] [--audit]
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "../../.claude/skills/anatomy/kit/iso-kit.mjs";
import * as G from "../../.claude/skills/anatomy/kit/lathe.mjs";
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
const cm = (id) => (an(id).einheit === "m" ? an(id).wert * 100 : an(id).wert);
const zahl = (v) => (Math.round(v * 10) / 10).toLocaleString("de-DE");
const spanne = (id) => {
  const a = an(id);
  const f = a.einheit === "m" ? 100 : 1;
  const t = a.toleranz;
  if (t && t.art === "bereich") return `${zahl(t.von * f)}–${zahl(t.bis * f)} cm`;
  return `ca. ${zahl(a.wert * f)} cm`;
};

const R_ECKE = cm("AN-20261011-11") / 2; // Zwölfeck, 37 über Ecken
const KLOTZ_OBEN = cm("AN-20261012-28"); // Oberkante Lagerklotz über Radstadt
const DORN_TIEF = cm("AN-20261012-27"); // Dornmitte unter Oberkante Klotz
const ACHSE = KLOTZ_OBEN - DORN_TIEF; // = AN-20261012-30
const DORN_R = cm("AN-20261012-22") / 2;
const DORN_L = cm("AN-20261012-21");
const SCHLITZ_AB = cm("AN-20261012-29"); // linkes Klotzende bis Schlitzkante
const SCHELLE_INNEN = cm("AN-20261012-24");

// Annahmen (in der Bildunterschrift genannt)
const KLOTZ_LANG = 64; // grob aus dem Foto
const KLOTZ_DICK = 14;
const SPALT = 3; // Stirnfläche bis Klotz
const SCHLITZ_B = 2 * DORN_R + 1;
const BALKEN_H = cm("AN-20261012-35");
const BALKEN_B = 30;
const WELLE_ZEIGEN = 78; // gekürzt
const BAND_AUSSEN = 7;
const BAND_INNEN = 4.5;

// ---------------------------------------------------------------- Szene (1 Einheit = 1 cm)
// x: Wellenachse (Klotz bei x = 0 … KLOTZ_DICK, Welle nach −x), y: quer, z: oben, Radstadt-Oberkante z = 0.
const W = 680;
const H = 420;
const SY = -KLOTZ_LANG / 2 + SCHLITZ_AB + SCHLITZ_B / 2; // y der Schlitzmitte = y der Achse
const XS = -SPALT; // Stirnfläche der Welle
const P = k.fitProjection(
  [
    ...k.boxCorners({ x: -6, y: -KLOTZ_LANG / 2 - 8, w: KLOTZ_DICK + 14, d: KLOTZ_LANG + 16, r: 0 }, -BALKEN_H, KLOTZ_OBEN + 3),
    [-WELLE_ZEIGEN, SY - R_ECKE - 4, ACHSE + R_ECKE + 4],
    [-WELLE_ZEIGEN, SY + R_ECKE + 4, ACHSE - R_ECKE],
  ],
  W,
  H,
  { pad: 34, azimuth: 28, elevation: 28 },
);
const at = (p) => k.iso(p, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (pts, style) => k.dotsSvg(pts, style);

const R = A.recorder(P);
const put = (name, centre, svg, shapes, extra = {}) =>
  R.put({ piece: "figur", name: R.nameFor(name), at: centre, svg, move: [0, 0, 0], shapes: shapes.map((s) => R.solid(s)), ...extra });
const box = (name, x0, x1, y0, y1, z0, z1, style = {}, inner = "") => {
  const ring = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
  put(name, [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2], S(k.extrude(ring, z0, z1 - z0, P, { bevel: style.bevel ?? 0.4 }), { tone: style.tone ?? "mid", lit: style.lit, inner }), [A.extruded(ring, z0, z1 - z0, { name })]);
};

// ---------------------------------------------------------------- Radstadt-Balken
const BX0 = -WELLE_ZEIGEN + 6;
const BX1 = KLOTZ_DICK + 8;
{
  const plan = { x: BX0, y: -BALKEN_B / 2 - 6, w: BX1 - BX0, d: BALKEN_B + 12, r: 1.5 };
  // Der Balken liegt quer zur Welle (uferparallel); hier nur ein Stück, längs y.
  const ring = [[-6, -KLOTZ_LANG / 2 - 8], [KLOTZ_DICK + 8, -KLOTZ_LANG / 2 - 8], [KLOTZ_DICK + 8, KLOTZ_LANG / 2 + 8], [-6, KLOTZ_LANG / 2 + 8]];
  const fasern = [0.25, 0.5, 0.75].map((t) => {
    const x = -6 + (KLOTZ_DICK + 14) * t;
    return k.lineOnTop([x, -KLOTZ_LANG / 2 - 8], [x, KLOTZ_LANG / 2 + 8], 0, P);
  }).join("");
  put("stand.balken", [KLOTZ_DICK / 2, 0, -BALKEN_H / 2], `<path class="iso-halo" d="${k.haloOf({ x: -6, y: -KLOTZ_LANG / 2 - 8, w: KLOTZ_DICK + 14, d: KLOTZ_LANG + 16, r: 1 }, -BALKEN_H, BALKEN_H, P)}"/>` + S(k.extrude(ring, -BALKEN_H, BALKEN_H, P, { bevel: 0.6 }), { tone: "lo", inner: L(fasern, { tone: "faint" }) }), [A.extruded(ring, -BALKEN_H, BALKEN_H, { name: "stand.balken" })]);
  void plan;
}

// ---------------------------------------------------------------- Lagerklotz mit offenem Schlitz
const Y0 = -KLOTZ_LANG / 2;
const Y1 = KLOTZ_LANG / 2;
const SL0 = SY - SCHLITZ_B / 2;
const SL1 = SY + SCHLITZ_B / 2;
const SBODEN = ACHSE - DORN_R; // Dorn liegt im Schlitzgrund
// Maserung auf der Stirn: läuft an der Außenkante auf die Kante, zum Schlitz hin aus.
const maserKlotz = (y0, y1, z0, z1, schlitzAmAnfang) => {
  const out = [];
  for (const t of [0.3, 0.62]) {
    const z = z0 + (z1 - z0) * t;
    const pts = Array.from({ length: 9 }, (_, i) => at([KLOTZ_DICK, y0 + ((y1 - y0) * i) / 8, z]));
    // Am sichtbaren Seitenende (y1 = Y1) läuft die Linie um die Ecke bis zur Hinterkante.
    if (schlitzAmAnfang) for (let i = 1; i <= 4; i++) pts.push(at([KLOTZ_DICK * (1 - i / 4), y1, z]));
    out.push(k.fadeLineSvg(pts, { fade: schlitzAmAnfang ? [12, 0] : [0, 12], tone: "faint" }));
  }
  return out.join("");
};
box("klotz.links", 0, KLOTZ_DICK, Y0, SL0, 0, KLOTZ_OBEN, { tone: "mid" }, maserKlotz(Y0, SL0, 0, KLOTZ_OBEN, false));
box("klotz.rechts", 0, KLOTZ_DICK, SL1, Y1, 0, KLOTZ_OBEN, { tone: "mid" }, maserKlotz(SL1, Y1, 0, KLOTZ_OBEN, true) + zeichenL());
box("klotz.unten", 0, KLOTZ_DICK, SL0, SL1, 0, SBODEN, { tone: "mid" });
// Deckbrett oben, über dem Schlitz
box("klotz.deckbrett", -1, KLOTZ_DICK + 1, Y0 + 2, Y1 - 2, KLOTZ_OBEN, KLOTZ_OBEN + 2.4, { tone: "mid", bevel: 0.3 },
  D([[-1 + 3, Y0 + 6], [-1 + 3, Y1 - 6], [KLOTZ_DICK - 2, Y0 + 6], [KLOTZ_DICK - 2, Y1 - 6]].map(([x, y]) => at([x, y, KLOTZ_OBEN + 2.4])), { size: 0.45, tone: "mid" }));

// Eingeschnittenes „L“ an der Stirn (Landseite) – zwei Kerben, die auf Kanten enden
function zeichenL() {
  const yL = SL1 + 7;
  const z0 = 10;
  const a = k.segment([KLOTZ_DICK, yL, z0 + 12], [KLOTZ_DICK, yL, z0], P);
  const b = k.segment([KLOTZ_DICK, yL, z0], [KLOTZ_DICK, yL + 6, z0], P);
  return L(a + b, { tone: "lo", free: true });
}

// ---------------------------------------------------------------- Welle (Zwölfeck) mit Schellen
const FW = G.frameOf([XS, SY, ACHSE], [-1, 0, 0], [0, 1, 0], [0, 0, 1]); // s läuft von der Stirnfläche nach hinten
const zwoelf = Array.from({ length: 12 }, (_, i) => {
  const t = (i / 12) * Math.PI * 2 + Math.PI / 12;
  return [R_ECKE * Math.cos(t), R_ECKE * Math.sin(t)];
});
const stuecke = [
  [0, BAND_AUSSEN],
  [BAND_AUSSEN, SCHELLE_INNEN - BAND_INNEN / 2],
  [SCHELLE_INNEN - BAND_INNEN / 2, SCHELLE_INNEN + BAND_INNEN / 2],
  [SCHELLE_INNEN + BAND_INNEN / 2, WELLE_ZEIGEN],
];
stuecke.forEach(([s0, s1], i) => {
  if (i % 2 === 0) return; // unter den Schellen verdeckt; die Schelle ist dort der Körper
  const name = `welle.${i}`;
  put(name, G.pointOf(FW, (s0 + s1) / 2, 0, 0), S(G.prismOf(FW, zwoelf, s0, s1, P), { tone: "hi" }), [A.prism(FW, zwoelf, s0, s1, { name })]);
});
// Schellen: Bänder um das Zwölfeck, je zwei Laschen mit Schraube
const BAND_R = R_ECKE + 0.7;
for (const [name, s0, s1] of [["schelle.aussen", -0.2, BAND_AUSSEN], ["schelle.innen", SCHELLE_INNEN - BAND_INNEN / 2, SCHELLE_INNEN + BAND_INNEN / 2]]) {
  put(name, G.pointOf(FW, (s0 + s1) / 2, 0, 0), S(G.disc(s0, s1, BAND_R, FW, P), { tone: "mid" }), [A.disc(FW, s0, s1, BAND_R, { name })]);
  for (const seite of [1, -1]) {
    const lname = `${name}.lasche${seite > 0 ? "o" : "u"}`;
    const lasche = [[-1.2, 0], [1.2, 0], [1.2, 3.2], [-1.2, 3.2]].map(([u, v]) => [u, seite * (BAND_R + v)]);
    const conv = seite > 0 ? lasche : lasche.reverse();
    put(lname, G.pointOf(FW, (s0 + s1) / 2, BAND_R + 1.6, (seite > 0 ? 1 : -1) * Math.PI / 2), S(G.prismOf(FW, conv, s0 + 0.4, s1 - 0.4, P), { tone: "mid" }) +
      D([at(G.pointOf(FW, (s0 + s1) / 2, BAND_R + 1.8, (seite > 0 ? 1 : -1) * Math.PI / 2))], { size: 0.8, tone: "hi" }), [A.prism(FW, conv, s0 + 0.4, s1 - 0.4, { name: lname })]);
  }
}

// ---------------------------------------------------------------- Dorn (Stahlzapfen) mit Laufrillen
const FD = G.frameOf([XS, SY, ACHSE], [1, 0, 0], [0, 1, 0], [0, 0, 1]);
{
  const s0 = 0;
  const s1 = DORN_L;
  const paths = G.disc(s0, s1, DORN_R, FD, P);
  const rillen = [];
  for (let s = 1.2; s < s1 - 0.6; s += 0.9) rillen.push(G.arcOf(FD, s, DORN_R, P));
  const innen = L(rillen.join(""), { tone: "lo" });
  put("dorn", G.pointOf(FD, (s0 + s1) / 2, 0, 0), S(paths, { tone: "hi", lit: true, inner: innen }), [A.disc(FD, s0, s1, DORN_R, { name: "dorn" })]);
}

// ---------------------------------------------------------------- Zollstock (je Messstelle)
const STATIONEN = [];
function zollstock(id, titel, wertText, ids, origin, dir, quer, len) {
  STATIONEN.push({ id, titel, wert: wertText, ids });
  const t = 0.3;
  const add = (p, v, s) => [p[0] + v[0] * s, p[1] + v[1] * s, p[2] + v[2] * s];
  const ticks = [];
  let svg;
  let shape;
  if (dir[2] === 0) {
    const a = origin;
    const b = add(a, dir, len);
    const ring = [a, b, add(b, quer, 1.6), add(a, quer, 1.6)].map((p) => [p[0], p[1]]);
    for (let c = 1; c < len; c++) {
      const l = c % 10 === 0 ? 0.9 : c % 5 === 0 ? 0.65 : 0.38;
      const p0 = add(origin, dir, c);
      ticks.push(k.lineOnTop([p0[0], p0[1]], [p0[0] + quer[0] * l, p0[1] + quer[1] * l], origin[2] + t, P));
    }
    svg = S(k.extrude(ring, origin[2], t, P, {}), { tone: "hi", lit: true, inner: L(ticks.join(""), { tone: "lo" }) });
    shape = A.extruded(ring, origin[2], t, { name: `station.${id}` });
  } else {
    const ring = [[origin[0], origin[1]], [origin[0] + quer[0] * 1.6, origin[1] + quer[1] * 1.6], [origin[0] + quer[0] * 1.6 + t, origin[1] + quer[1] * 1.6], [origin[0] + t, origin[1]]];
    const front = [origin[0] + t, origin[1]];
    for (let c = 1; c < len; c++) {
      const l = c % 10 === 0 ? 0.9 : c % 5 === 0 ? 0.65 : 0.38;
      ticks.push(k.segment([front[0], front[1], origin[2] + c], [front[0], front[1] + quer[1] * l, origin[2] + c], P));
    }
    svg = S(k.extrude(ring, origin[2], len, P, {}), { tone: "hi", lit: true, inner: L(ticks.join(""), { tone: "lo" }) });
    shape = A.extruded(ring, origin[2], len, { name: `station.${id}` });
  }
  put(`station.${id}`, add(origin, dir, len / 2), svg, [shape], { station: id });
}
// 1. Oberkante Klotz über Radstadt: stehend auf dem Balken vor dem linken Klotzteil
zollstock("klotz", "Klotz über Radstadt", spanne("AN-20261012-28"), "AN-20261012-28", [KLOTZ_DICK + 0.1, Y0 + 5, 0], [0, 0, 1], [0, 1, 0], Math.round(KLOTZ_OBEN));
// 2. Dornmitte unter Oberkante: stehend vor dem Schlitz, vom Dornscheitel bis Oberkante
zollstock("tiefe", "Dorn unter Oberkante", spanne("AN-20261012-27"), "AN-20261012-27", [KLOTZ_DICK + 0.1, SL1 + 0.4, ACHSE], [0, 0, 1], [0, 1, 0], Math.round(DORN_TIEF));
// 3. Achshöhe (abgeleitet): stehend auf dem Balken neben dem Schlitz
zollstock("achse", "Achshöhe (abgeleitet)", spanne("AN-20261012-30"), "AN-20261012-30", [KLOTZ_DICK + 0.1, SL0 - 2.2, 0], [0, 0, 1], [0, 1, 0], Math.round(ACHSE));
// 4. Dornüberstand: liegend auf dem Dorn
zollstock("dorn", "Dornüberstand", spanne("AN-20261012-21"), "AN-20261012-21", [XS, SY - 0.8, ACHSE + DORN_R + 0.05], [1, 0, 0], [0, 1, 0], Math.round(DORN_L));
// 5. Innere Schelle: liegend auf der Welle ab Stirnfläche
zollstock("schelle", "Innere Schelle", spanne("AN-20261012-24"), "AN-20261012-24", [XS, SY - 0.8, ACHSE + BAND_R + 0.02], [-1, 0, 0], [0, 1, 0], Math.round(SCHELLE_INNEN));

A.settle(R, P);
R.items.sort((a, b) => a.key - b.key);
const groups = R.items.map((it) => (it.station ? `<g data-station="${it.station}"${it.station === "klotz" ? "" : ' style="opacity:0"'}>${it.svg}</g>` : it.svg));

const LABEL = "Landseitiges Wellenlager des Kleinen Schäferrads: ein Lagerklotz mit offenem senkrechten Schlitz steht auf dem Radstadt-Balken; im Schlitzgrund liegt der stählerne Dorn, der aus der Stirnfläche der zwölfeckigen Welle ragt. Zwei Eisenschellen umfassen das Wellenende. Ein Zollstock zeigt nacheinander die Maße.";
const svg = k.figureSvg({ width: W, height: H, label: LABEL, body: groups });
const LIVE = readFileSync(join(HERE, "..", "gemeinsam", "stationen.js"), "utf8").replace("__DATA__", JSON.stringify({ stationen: STATIONEN }));
const body = k.plateHtml({
  fig: "Fig 2",
  title: "Wellenlager Landseite",
  hint: "Zeigen oder Pfeiltasten: Messstelle wählen",
  readout: `${STATIONEN[0].titel} · ${STATIONEN[0].wert} · ${STATIONEN[0].ids}`,
  keys: [
    { mark: "lit", label: "Dorn und Zollstock an der gezeigten Messstelle" },
    { mark: "raised", label: "Welle, Lagerklotz und Radstadt-Balken nach den Maßen im Kern" },
  ],
  caption:
    `Das landseitige Wellenlager, vermessen beim Abbau am 10.10.2026. Der Lagerklotz steht auf dem Radstadt-Balken, seine Oberkante liegt ${spanne("AN-20261012-28")} darüber (AN-20261012-28). Der Dorn (${spanne("AN-20261012-22")} stark, ${spanne("AN-20261012-21")} überstehend, AN-20261012-21/22) liegt im Grund eines offenen Schlitzes, ${spanne("AN-20261012-27")} unter der Oberkante (AN-20261012-27). Der Schlitz sitzt nicht mittig (AN-20261012-29). ` +
    `Daraus folgt eine Wellenmitte von ${spanne("AN-20261012-30")} über der Radstadt (AN-20261012-30, abgeleitet) – der erste Messwert zu F-003. Die Welle ist ein Zwölfeck von ${zahl(R_ECKE * 2)} cm über Ecken (AN-20261011-11), die innere Schelle sitzt ${spanne("AN-20261012-24")} vom Holzende. ` +
    `Angenommen sind Klotzlänge ${KLOTZ_LANG} cm und -dicke ${KLOTZ_DICK} cm, ein Spalt von ${SPALT} cm zwischen Welle und Klotz, die Schellenbreiten und die Balkenbreite. Alle Maße sind offen, bis Thorsten sie bestätigt.`,
  body: `<div class="iso-stage" tabindex="0" role="slider" aria-label="Wellenlager: Pfeiltasten wechseln die Messstelle" aria-valuemin="1" aria-valuemax="${STATIONEN.length}" aria-valuenow="1">${svg}</div>`,
});
const page = k.pageHtml({ title: "Wellenlager Landseite", theme: THEME, body, script: kitScript() + LIVE, width: 720 }).replace('<html lang="en">', '<html lang="de">');
const out = THEME === "light" ? "wellenlager-hell.html" : "wellenlager.html";
writeFileSync(join(HERE, out), page);
console.log("geschrieben:", out, `${(page.length / 1024).toFixed(0)} KB`, `${R.items.length} Teile`);
A.auditOrExit(R, P);
