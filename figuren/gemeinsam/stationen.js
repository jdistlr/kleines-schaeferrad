// Gemeinsame Laufzeit für Figuren mit Messstellen: blendet den Zollstock der gewählten Stelle ein.
const D = __DATA__;
const stage = document.querySelector(".iso-stage");
const readout = document.querySelector("[data-readout]");
const still = matchMedia("(prefers-reduced-motion: reduce)");
const nodes = Object.fromEntries(D.stationen.map((s) => [s.id, stage.querySelector('[data-station="' + s.id + '"]')]));
const op = Object.fromEntries(D.stationen.map((s, i) => [s.id, i === 0 ? 1 : 0]));
let current = 0, touring = !still.matches, clock = 0, last = 0, frame = 0, visible = false, idle = 0;
const say = () => {
  const s = D.stationen[current];
  const text = s.titel + " · " + s.wert + " · " + s.ids;
  if (readout.textContent !== text) readout.textContent = text;
  stage.setAttribute("aria-valuenow", String(current + 1));
  stage.setAttribute("aria-valuetext", text);
};
function tick(now) {
  const dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
  last = now;
  if (touring) { clock += dt; const next = Math.floor(clock / 3.2) % D.stationen.length; if (next !== current) { current = next; say(); } }
  let moving = false;
  D.stationen.forEach((s, i) => {
    const goal = i === current ? 1 : 0;
    const v = still.matches ? goal : op[s.id] + (goal - op[s.id]) * (1 - Math.exp(-dt / 0.18));
    op[s.id] = Math.abs(goal - v) < 0.004 ? goal : v;
    if (op[s.id] !== goal) moving = true;
    nodes[s.id].style.opacity = op[s.id].toFixed(3);
  });
  frame = visible && (touring || moving) ? requestAnimationFrame(tick) : 0;
}
const run = () => { if (!frame && visible) { last = 0; frame = requestAnimationFrame(tick); } };
const go = (i) => {
  touring = false;
  current = (i + D.stationen.length) % D.stationen.length;
  say();
  clearTimeout(idle);
  idle = setTimeout(() => { touring = !still.matches; clock = current * 3.2; run(); }, 5000);
  run();
};
new IntersectionObserver((e) => { visible = e[e.length - 1].isIntersecting; if (visible) run(); }, { rootMargin: "120px 0px" }).observe(stage);
stage.addEventListener("pointermove", (event) => {
  const box = stage.getBoundingClientRect();
  const share = Math.min(0.999, Math.max(0, (event.clientX - box.left) / box.width));
  const i = Math.floor(share * D.stationen.length);
  if (i !== current || touring) go(i);
});
stage.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight" || event.key === "ArrowUp") { event.preventDefault(); go(current + 1); }
  if (event.key === "ArrowLeft" || event.key === "ArrowDown") { event.preventDefault(); go(current - 1); }
});
say();
