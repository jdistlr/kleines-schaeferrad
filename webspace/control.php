<?php
/*
 * Control plane for schaeferrad.jdistlr.de (operator only, read-only).
 *
 * Shows every contribution (who, when, where, how, what) and the API request log
 * written by api.php (daten/log/YYYY-MM-DD.jsonl). Identifiers in English, all
 * visible text in German (AGENTS.md, naming rule).
 *
 *   control.php                 overview (password from konfig.php key "control_password")
 *   control.php?format=csv      contributions as CSV (semicolon, UTF-8 BOM, opens in Excel)
 *
 * Side files written by scripts/kern/baue_webspace.py:
 *   targets.json   titles for kern IDs and VORGEHEN
 *   build.json     published commit and build time
 */
declare(strict_types=1);

const MIN_PASSWORD_LENGTH = 12;
const LOG_FILES_SHOWN = 30;
const LOG_ROWS_SHOWN = 500;
const TIMEZONE = 'Europe/Berlin';

$DATA_DIR = __DIR__ . '/daten';
$CONFIG = is_file(__DIR__ . '/konfig.php') ? require __DIR__ . '/konfig.php' : [];
$PASSWORD = (string)($CONFIG['control_password'] ?? '');

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');
header("Content-Security-Policy: default-src 'self'; img-src 'self' data:; media-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; frame-ancestors 'none'");

session_name('ks_control');
session_set_cookie_params(['lifetime' => 0, 'path' => dirname($_SERVER['SCRIPT_NAME'] ?? '/') ?: '/', 'secure' => !empty($_SERVER['HTTPS']), 'httponly' => true, 'samesite' => 'Strict']);
session_start();
if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(16));

function h($value): string { return htmlspecialchars((string)$value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

function readJson(string $path): array {
    if (!is_file($path)) return [];
    $data = json_decode((string)file_get_contents($path), true);
    return is_array($data) ? $data : [];
}

function formatLocalTime(?string $iso, string $format = 'd.m.Y H:i'): string {
    if (!$iso) return '';
    try { return (new DateTimeImmutable($iso))->setTimezone(new DateTimeZone(TIMEZONE))->format($format); }
    catch (Exception $e) { return $iso; }
}

/** Short, readable device description from a user agent. */
function deviceLabel(string $agent): string {
    if ($agent === '') return '';
    $os = match (true) {
        str_contains($agent, 'iPhone') => 'iPhone', str_contains($agent, 'iPad') => 'iPad',
        str_contains($agent, 'Android') => 'Android', str_contains($agent, 'Windows') => 'Windows',
        str_contains($agent, 'Mac OS X') => 'Mac', str_contains($agent, 'Linux') => 'Linux', default => '',
    };
    $browser = match (true) {
        str_contains($agent, 'Edg/') => 'Edge', str_contains($agent, 'Firefox') || str_contains($agent, 'FxiOS') => 'Firefox',
        str_contains($agent, 'Chrome') || str_contains($agent, 'CriOS') => 'Chrome', str_contains($agent, 'Safari') => 'Safari',
        str_contains($agent, 'curl') => 'curl', str_contains($agent, 'python') => 'Skript', default => '',
    };
    $label = trim($browser . ($os ? ' auf ' . $os : ''));
    return $label !== '' ? $label : mb_substr($agent, 0, 40);
}

function loadContributions(string $dir): array {
    $list = [];
    foreach (glob($dir . '/antworten/*/*/*.json') ?: [] as $file) {
        $item = readJson($file);
        if (!empty($item['id'])) $list[] = $item;
    }
    usort($list, fn($a, $b) => strcmp($b['am'] ?? '', $a['am'] ?? ''));
    return $list;
}

function loadLog(string $dir): array {
    $files = glob($dir . '/log/*.jsonl') ?: [];
    rsort($files);
    $rows = [];
    foreach (array_slice($files, 0, LOG_FILES_SHOWN) as $file) {
        $lines = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: [];
        foreach (array_reverse($lines) as $line) {
            $row = json_decode($line, true);
            if (is_array($row)) $rows[] = $row;
            if (count($rows) >= LOG_ROWS_SHOWN) break 2;
        }
    }
    return $rows;
}

const KIND_LABELS = [
    'stimmt' => 'Stimmt so', 'stimmt_nicht' => 'Stimmt nicht', 'genauer' => 'Weiß es genauer',
    'ergaenzung' => 'Ergänzung', 'korrektur' => 'Korrektur', 'hinweis' => 'Hinweis',
];
const OUTCOME_LABELS = ['saved' => 'gespeichert', 'exported' => 'abgeholt', 'honeypot' => 'Bot abgefangen'];
const ACTION_LABELS = ['speichern' => 'Antwort', 'export' => 'Abholung'];

function targetTitle(array $targets, string $id): string {
    if ($id === 'VORGEHEN') return 'Wie wir vorgehen';
    return (string)($targets[$id]['title'] ?? '');
}
function targetLink(string $id): string { return './#' . ($id === 'VORGEHEN' ? 'vorgehen' : rawurlencode($id)); }

// ---------- login / logout ----------

$loginError = '';
if (($_POST['do'] ?? '') === 'login') {
    if (strlen($PASSWORD) >= MIN_PASSWORD_LENGTH && hash_equals($PASSWORD, (string)($_POST['password'] ?? ''))) {
        session_regenerate_id(true);
        $_SESSION['signed_in'] = true;
        header('Location: ' . strtok($_SERVER['REQUEST_URI'] ?? 'control.php', '?'), true, 303);
        exit;
    }
    sleep(2);
    $loginError = 'Das Passwort stimmt nicht.';
}
if (($_POST['do'] ?? '') === 'logout' && hash_equals($_SESSION['csrf'], (string)($_POST['csrf'] ?? ''))) {
    $_SESSION = [];
    session_destroy();
    header('Location: ' . strtok($_SERVER['REQUEST_URI'] ?? 'control.php', '?'), true, 303);
    exit;
}
$signedIn = !empty($_SESSION['signed_in']);

// ---------- data ----------

if ($signedIn) {
    $targets = readJson(__DIR__ . '/targets.json');
    $build = readJson(__DIR__ . '/build.json');
    $contributions = loadContributions($DATA_DIR);
    $log = loadLog($DATA_DIR);

    if (($_GET['format'] ?? '') === 'csv') {
        header('Content-Type: text/csv; charset=utf-8');
        header('Content-Disposition: attachment; filename="beitraege-' . date('Y-m-d') . '.csv"');
        $out = fopen('php://output', 'w');
        fwrite($out, "\xEF\xBB\xBF");
        fputcsv($out, ['Zeit', 'Name', 'Ziel', 'Titel', 'Art', 'Wert', 'Text', 'Antwort auf', 'Betrifft auch', 'Anhänge', 'Ansicht', 'Gerät', 'Im Kern', 'ID'], ';');
        foreach (array_reverse($contributions) as $c) {
            fputcsv($out, [
                formatLocalTime($c['am'] ?? null), $c['name'] ?? '', $c['ziel'] ?? '', targetTitle($targets, (string)($c['ziel'] ?? '')),
                KIND_LABELS[$c['typ'] ?? ''] ?? ($c['typ'] ?? ''), $c['wert'] ?? '', $c['text'] ?? '', $c['antwort_auf'] ?? '',
                implode(' ', $c['betrifft_auch'] ?? []), implode(' ', array_map(fn($f) => $f['id'] ?? '', $c['dateien'] ?? [])),
                $c['ansicht'] ?? '', deviceLabel((string)($c['geraet'] ?? '')), !empty($c['uebernommen']) ? 'ja' : 'nein', $c['id'],
            ], ';');
        }
        exit;
    }

    $today = (new DateTimeImmutable('now', new DateTimeZone(TIMEZONE)))->format('Y-m-d');
    $people = [];
    foreach ($contributions as $c) {
        $name = trim((string)($c['name'] ?? '')) ?: 'ohne Namen';
        $people[$name] = ($people[$name] ?? 0) + 1;
    }
    arsort($people);
    $stats = [
        'total' => count($contributions),
        'today' => count(array_filter($contributions, fn($c) => formatLocalTime($c['am'] ?? null, 'Y-m-d') === $today)),
        'people' => count(array_filter(array_keys($people), fn($n) => $n !== 'ohne Namen')),
        'photos' => count(array_filter($contributions, fn($c) => array_filter($c['dateien'] ?? [], fn($f) => ($f['art'] ?? '') === 'bild'))),
        'voice' => count(array_filter($contributions, fn($c) => array_filter($c['dateien'] ?? [], fn($f) => ($f['art'] ?? '') === 'ton'))),
        'open' => count(array_filter($contributions, fn($c) => empty($c['uebernommen']))),
        'rejected' => count(array_filter($log, fn($r) => ($r['status'] ?? 200) >= 400 || ($r['outcome'] ?? '') === 'honeypot')),
    ];
    $lastExport = null;
    foreach ($log as $r) if (($r['action'] ?? '') === 'export' && ($r['status'] ?? 0) === 200) { $lastExport = $r['time']; break; }
}
?><!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Überblick – Kleines Schäferrad</title>
<style>
:root {
  --papier: #edf1ec; --flaeche: #f6f8f5; --tinte: #1c2726; --leise: #5f6d6a; --linie: #c9d1cc;
  --wasser: #2b6a76; --wasser-hauch: #d6e6e8; --roetel: #a5412a; --roetel-hauch: #f3e2dc; --eiche: #4f6f2a; --holz: #e2d8c6;
  --serif: "Alegreya", "Iowan Old Style", Georgia, serif;
  --sans: "Alegreya Sans", "Gill Sans", "Segoe UI", system-ui, sans-serif;
  --m1: .8125rem; --m2: .9375rem; --m3: 1.0625rem; --m4: 1.3125rem; --m5: 1.75rem;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --papier: #121817; --flaeche: #1a2120; --tinte: #dfe6e2; --leise: #9aa8a4; --linie: #33403d;
  --wasser: #86bec7; --wasser-hauch: #20393d; --roetel: #e48c71; --roetel-hauch: #3a2520; --eiche: #a9c77a; --holz: #3a352b; color-scheme: dark; } }
:root[data-theme="dark"] {
  --papier: #121817; --flaeche: #1a2120; --tinte: #dfe6e2; --leise: #9aa8a4; --linie: #33403d;
  --wasser: #86bec7; --wasser-hauch: #20393d; --roetel: #e48c71; --roetel-hauch: #3a2520; --eiche: #a9c77a; --holz: #3a352b; color-scheme: dark; }
* { box-sizing: border-box; }
[hidden] { display: none !important; }
body { margin: 0; background: var(--papier); color: var(--tinte); font: 400 var(--m3)/1.5 var(--sans); }
button, input, select { font: inherit; color: inherit; }
a { color: var(--wasser); text-underline-offset: 3px; }
:focus-visible { outline: 2px solid var(--wasser); outline-offset: 2px; border-radius: 3px; }
.zahl { font-variant-numeric: tabular-nums; }
.leise { color: var(--leise); }
main { max-width: 1440px; margin: 0 auto; padding: 0 clamp(16px, 3vw, 32px) 64px; }
.leiste { display: flex; align-items: baseline; gap: 8px 24px; flex-wrap: wrap; padding: 16px 0 14px; border-bottom: 1px solid var(--linie); }
.leiste h1 { font: 700 var(--m4)/1.1 var(--serif); margin: 0; }
.leiste nav { margin-left: auto; display: flex; gap: 16px; align-items: baseline; font-size: var(--m2); }
.leiste form { margin: 0; }
.knopf-leise { background: none; border: 0; padding: 0; color: var(--wasser); cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }
h2 { font: 700 var(--m4)/1.2 var(--serif); margin: 36px 0 4px; }
h2 + p { margin: 0 0 14px; color: var(--leise); font-size: var(--m2); }

.kennzahlen { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 1px; background: var(--linie); border: 1px solid var(--linie); border-radius: 8px; overflow: hidden; margin-top: 20px; }
.kennzahlen div { background: var(--flaeche); padding: 12px 14px; }
.kennzahlen b { display: block; font: 700 var(--m5)/1.1 var(--serif); font-variant-numeric: tabular-nums; }
.kennzahlen span { display: block; margin-top: 4px; font-size: var(--m1); line-height: 1.3; color: var(--leise); }
.kennzahlen .klein b { font: 600 var(--m3)/1.6 var(--sans); }

.filter { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 0 0 12px; }
.filter input[type=search], .filter select { padding: 7px 11px; border: 1px solid var(--linie); border-radius: 6px; background: var(--flaeche); }
.filter input[type=search] { flex: 1 1 240px; max-width: 380px; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 12px; }
.chip { border: 1px solid var(--linie); background: var(--flaeche); border-radius: 999px; padding: 3px 11px; font-size: var(--m2); cursor: pointer; }
.chip[aria-pressed="true"] { background: var(--wasser); border-color: var(--wasser); color: var(--papier); }
.chip small { opacity: .7; margin-left: 4px; font-variant-numeric: tabular-nums; }

.tabelle-rahmen { overflow-x: auto; border: 1px solid var(--linie); border-radius: 8px; background: var(--flaeche); }
table { border-collapse: collapse; width: 100%; font-size: var(--m2); }
th { text-align: left; font-weight: 600; font-size: var(--m1); color: var(--leise); padding: 9px 12px; border-bottom: 1px solid var(--linie); white-space: nowrap; position: sticky; top: 0; background: var(--flaeche); }
td { padding: 10px 12px; border-bottom: 1px solid var(--linie); vertical-align: top; }
tr:last-child td { border-bottom: 0; }
td.wann { white-space: nowrap; }
td.was { min-width: 260px; max-width: 520px; }
td.was p { margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; }
td.was .wert { font-weight: 700; }
.ziel-id { font: 600 var(--m1)/1.4 ui-monospace, "SF Mono", Menlo, monospace; }
.marke { display: inline-block; font-size: var(--m1); line-height: 1.5; padding: 0 8px; border-radius: 999px; background: var(--wasser-hauch); white-space: nowrap; }
.marke.nein, .marke.fehler { background: var(--roetel-hauch); color: var(--roetel); }
.marke.kern { background: var(--holz); }
.anhaenge { display: flex; gap: 6px; flex-wrap: wrap; }
.anhaenge img { width: 56px; height: 56px; object-fit: cover; border-radius: 4px; border: 1px solid var(--linie); display: block; }
.anhaenge audio { width: 200px; height: 32px; }
.leer { padding: 28px; text-align: center; color: var(--leise); }

.anmeldung { max-width: 380px; margin: 14vh auto 0; background: var(--flaeche); border: 1px solid var(--linie); border-radius: 10px; padding: 28px; }
.anmeldung h1 { font: 700 var(--m5)/1.1 var(--serif); margin: 0 0 6px; }
.anmeldung p { margin: 0 0 18px; color: var(--leise); font-size: var(--m2); }
.anmeldung input { width: 100%; padding: 9px 12px; border: 1px solid var(--linie); border-radius: 6px; background: var(--papier); margin-bottom: 12px; }
.anmeldung button { width: 100%; padding: 9px; border: 0; border-radius: 6px; background: var(--wasser); color: var(--papier); font-weight: 600; cursor: pointer; }
.fehlertext { color: var(--roetel); font-size: var(--m2); margin: 0 0 12px; }
@media (max-width: 720px) {
  .leiste nav { margin-left: 0; }
  .tabelle-rahmen { overflow: visible; border: 0; background: none; }
  table, tbody, tr, td { display: block; width: 100%; }
  thead { display: none; }
  tr { background: var(--flaeche); border: 1px solid var(--linie); border-radius: 8px; padding: 6px 0; margin-bottom: 10px; }
  td { border: 0; padding: 4px 14px 4px 108px; position: relative; min-height: 28px; }
  td::before { content: attr(data-label); position: absolute; left: 14px; top: 6px; width: 84px; font: 400 var(--m1)/1.4 var(--sans); color: var(--leise); }
  td:empty, td.ohne { display: none; }
  td.was { min-width: 0; max-width: none; }
}
</style>
</head>
<body>
<?php if (!$signedIn): ?>
<main>
  <form class="anmeldung" method="post">
    <h1>Überblick</h1>
    <?php if (strlen($PASSWORD) < MIN_PASSWORD_LENGTH): ?>
      <p>Diese Seite ist noch nicht eingerichtet. Es fehlt das Passwort (GitHub-Secret <code>KS_CONTROL_PASSWORD</code>, mindestens 12 Zeichen). Danach einmal neu veröffentlichen.</p>
    <?php else: ?>
      <p>Wer hat was wann eingebracht – und was hat die Schnittstelle gemeldet. Nur für Johannes.</p>
      <?php if ($loginError): ?><p class="fehlertext"><?= h($loginError) ?></p><?php endif; ?>
      <input type="hidden" name="do" value="login">
      <label class="leise" for="pw" style="font-size:var(--m1)">Passwort</label>
      <input id="pw" type="password" name="password" autocomplete="current-password" autofocus required>
      <button type="submit">Anmelden</button>
    <?php endif; ?>
    <p style="margin:18px 0 0"><a href="./">Zum Cockpit</a></p>
  </form>
</main>
<?php else: ?>
<main>
  <header class="leiste">
    <h1>Überblick der Beiträge</h1>
    <span class="leise" style="font-size:var(--m2)">schaeferrad.jdistlr.de</span>
    <nav>
      <a href="./">Cockpit</a>
      <a href="?format=csv">Als Tabelle herunterladen</a>
      <form method="post"><input type="hidden" name="do" value="logout"><input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>"><button class="knopf-leise" type="submit">Abmelden</button></form>
    </nav>
  </header>

  <section class="kennzahlen" aria-label="Kennzahlen">
    <div><b><?= $stats['total'] ?></b><span>Beiträge insgesamt</span></div>
    <div><b><?= $stats['today'] ?></b><span>davon heute</span></div>
    <div><b><?= $stats['people'] ?></b><span>Personen mit Namen</span></div>
    <div><b><?= $stats['open'] ?></b><span>noch nicht im Wissenskern</span></div>
    <div><b><?= $stats['photos'] ?></b><span>mit Foto</span></div>
    <div><b><?= $stats['voice'] ?></b><span>mit Sprachnachricht</span></div>
    <div><b><?= $stats['rejected'] ?></b><span>abgewiesen (im Protokoll)</span></div>
    <div class="klein"><b><?= $lastExport ? h(formatLocalTime($lastExport)) : '–' ?></b><span>zuletzt nach GitHub abgeholt</span></div>
    <div class="klein"><b><?= !empty($build['commit']) ? h(substr((string)$build['commit'], 0, 7)) : '–' ?></b><span>veröffentlicht <?= !empty($build['built_at']) ? h(formatLocalTime($build['built_at'])) : '' ?></span></div>
  </section>

  <h2 id="beitraege">Beiträge</h2>
  <p>Neueste zuerst. Ein Klick auf das Ziel öffnet die Stelle im Cockpit.</p>
  <div class="chips" role="group" aria-label="Nach Person filtern">
    <button class="chip" type="button" data-person="" aria-pressed="true">Alle<small><?= $stats['total'] ?></small></button>
    <?php foreach ($people as $name => $count): ?>
      <button class="chip" type="button" data-person="<?= h($name) ?>" aria-pressed="false"><?= h($name) ?><small><?= $count ?></small></button>
    <?php endforeach; ?>
  </div>
  <div class="filter">
    <input type="search" id="search" placeholder="Suchen in Text, Ziel, Name …" aria-label="Beiträge durchsuchen">
    <select id="kind" aria-label="Nach Art filtern">
      <option value="">Jede Art</option>
      <?php foreach (KIND_LABELS as $key => $label): ?><option value="<?= h($key) ?>"><?= h($label) ?></option><?php endforeach; ?>
    </select>
    <select id="state" aria-label="Nach Stand filtern">
      <option value="">Jeder Stand</option>
      <option value="open">noch nicht im Kern</option>
      <option value="done">im Kern</option>
    </select>
    <span class="leise zahl" id="count" style="font-size:var(--m2)"></span>
  </div>
  <div class="tabelle-rahmen">
  <?php if (!$contributions): ?>
    <div class="leer">Noch keine Beiträge. Sobald jemand im Cockpit antwortet, steht es hier.</div>
  <?php else: ?>
    <table id="contributions">
      <thead><tr><th>Wann</th><th>Wer</th><th>Wo</th><th>Wie</th><th>Was</th><th>Anhänge</th><th>Stand</th></tr></thead>
      <tbody>
      <?php foreach ($contributions as $c):
          $target = (string)($c['ziel'] ?? '');
          $title = targetTitle($targets, $target);
          $name = trim((string)($c['name'] ?? '')) ?: 'ohne Namen';
          $kind = (string)($c['typ'] ?? '');
          $searchText = mb_strtolower(implode(' ', [$name, $target, $title, $c['text'] ?? '', $c['wert'] ?? '', $c['id'] ?? '', implode(' ', $c['betrifft_auch'] ?? [])]));
      ?>
        <tr data-person="<?= h($name) ?>" data-kind="<?= h($kind) ?>" data-state="<?= !empty($c['uebernommen']) ? 'done' : 'open' ?>" data-search="<?= h($searchText) ?>">
          <td class="wann zahl" data-label="Wann"><?= h(formatLocalTime($c['am'] ?? null)) ?></td>
          <td data-label="Wer"><?= $name === 'ohne Namen' ? '<span class="leise">ohne Namen</span>' : h($name) ?></td>
          <td data-label="Wo">
            <a class="ziel-id" href="<?= h(targetLink($target)) ?>"><?= h($target) ?></a>
            <?php if ($title): ?><div class="leise" style="font-size:var(--m1);max-width:260px"><?= h(mb_strimwidth($title, 0, 110, ' …')) ?></div><?php endif; ?>
            <?php if (!empty($c['betrifft_auch'])): ?><div class="leise" style="font-size:var(--m1)">auch: <?= h(implode(', ', $c['betrifft_auch'])) ?></div><?php endif; ?>
          </td>
          <td data-label="Wie">
            <span class="marke<?= $kind === 'stimmt_nicht' ? ' nein' : '' ?>"><?= h(KIND_LABELS[$kind] ?? $kind) ?></span>
            <div class="leise" style="font-size:var(--m1)"><?= h(deviceLabel((string)($c['geraet'] ?? ''))) ?></div>
            <?php if (!empty($c['ansicht'])): ?><div class="leise" style="font-size:var(--m1)">aus Ansicht „<?= h($c['ansicht']) ?>“</div><?php endif; ?>
          </td>
          <td class="was" data-label="Was">
            <?php if (!empty($c['antwort_auf'])): ?><div class="leise" style="font-size:var(--m1)">Antwort auf <?= h($c['antwort_auf']) ?></div><?php endif; ?>
            <?php if (($c['wert'] ?? '') !== ''): ?><p class="wert"><?= h($c['wert']) ?></p><?php endif; ?>
            <?php if (($c['text'] ?? '') !== ''): ?><p><?= h($c['text']) ?></p><?php endif; ?>
            <div class="leise ziel-id" style="font-weight:400;margin-top:4px"><?= h($c['id']) ?></div>
          </td>
          <td data-label="Anhänge"<?= empty($c['dateien']) ? ' class="ohne"' : '' ?>>
            <div class="anhaenge">
            <?php foreach ($c['dateien'] ?? [] as $file):
                $url = 'api.php?aktion=datei&id=' . rawurlencode((string)($file['id'] ?? '')); ?>
              <?php if (($file['art'] ?? '') === 'bild'): ?>
                <a href="<?= h($url) ?>" target="_blank" rel="noopener" title="<?= h($file['name'] ?? '') ?>"><img src="<?= h($url) ?>" alt="Foto <?= h($file['name'] ?? '') ?>" loading="lazy"></a>
              <?php else: ?>
                <audio controls preload="none" src="<?= h($url) ?>" title="<?= h($file['name'] ?? '') ?>"></audio>
              <?php endif; ?>
            <?php endforeach; ?>
            </div>
          </td>
          <td data-label="Stand"><?= !empty($c['uebernommen']) ? '<span class="marke kern">im Kern</span>' : '<span class="leise" style="font-size:var(--m1)">offen</span>' ?></td>
        </tr>
      <?php endforeach; ?>
      </tbody>
    </table>
  <?php endif; ?>
  </div>

  <h2 id="protokoll">Meldungen der Schnittstelle</h2>
  <p>Jeder Speicherversuch und jede Abholung durch GitHub, neueste zuerst (höchstens <?= LOG_ROWS_SHOWN ?> Zeilen, 180 Tage aufbewahrt). Statt der IP-Adresse steht ein Kürzel, das täglich wechselt.</p>
  <div class="tabelle-rahmen">
  <?php if (!$log): ?>
    <div class="leer">Noch keine Meldungen. Das Protokoll beginnt mit dem ersten Speichern nach dieser Veröffentlichung.</div>
  <?php else: ?>
    <table>
      <thead><tr><th>Wann</th><th>Vorgang</th><th>Ergebnis</th><th>Ziel</th><th>Name</th><th>Anhänge</th><th>Größe</th><th>Dauer</th><th>Gerät</th><th>Kürzel</th></tr></thead>
      <tbody>
      <?php foreach ($log as $r):
          $status = (int)($r['status'] ?? 0);
          $outcome = (string)($r['outcome'] ?? '');
          $bad = $status >= 400 || $outcome === 'honeypot'; ?>
        <tr>
          <td class="wann zahl" data-label="Wann"><?= h(formatLocalTime($r['time'] ?? null, 'd.m.Y H:i:s')) ?></td>
          <td data-label="Vorgang"><?= h(ACTION_LABELS[$r['action'] ?? ''] ?? ($r['action'] ?? '')) ?></td>
          <td data-label="Ergebnis"><span class="marke<?= $bad ? ' fehler' : '' ?>"><?= h(OUTCOME_LABELS[$outcome] ?? $outcome) ?></span> <span class="leise zahl" style="font-size:var(--m1)"><?= $status ?></span></td>
          <td data-label="Ziel"><?= !empty($r['target']) ? '<a class="ziel-id" href="' . h(targetLink((string)$r['target'])) . '">' . h($r['target']) . '</a>' : '' ?><?= !empty($r['answer_id']) ? '<div class="leise ziel-id" style="font-weight:400">' . h($r['answer_id']) . '</div>' : '' ?></td>
          <td data-label="Name"><?= h($r['name'] ?? '') ?></td>
          <td class="zahl" data-label="Anhänge"><?= (int)($r['files'] ?? 0) ?: '' ?></td>
          <td class="zahl" data-label="Größe"><?= !empty($r['request_bytes']) ? h(number_format(max(1, round($r['request_bytes'] / 1024)), 0, ',', '.')) . ' KB' : '' ?></td>
          <td class="zahl" data-label="Dauer"><?= isset($r['duration_ms']) ? (int)$r['duration_ms'] . ' ms' : '' ?></td>
          <td data-label="Gerät"><?= h(deviceLabel((string)($r['user_agent'] ?? ''))) ?></td>
          <td class="ziel-id" style="font-weight:400" data-label="Kürzel"><?= h($r['client'] ?? '') ?></td>
        </tr>
      <?php endforeach; ?>
      </tbody>
    </table>
  <?php endif; ?>
  </div>
</main>
<script>
(() => {
  const rows = [...document.querySelectorAll('#contributions tbody tr')];
  const search = document.getElementById('search'), kind = document.getElementById('kind'), state = document.getElementById('state');
  const count = document.getElementById('count');
  let person = '';
  function apply() {
    const q = (search?.value || '').trim().toLowerCase();
    let shown = 0;
    for (const r of rows) {
      const ok = (!person || r.dataset.person === person) && (!kind.value || r.dataset.kind === kind.value)
        && (!state.value || r.dataset.state === state.value) && (!q || r.dataset.search.includes(q));
      r.hidden = !ok; if (ok) shown++;
    }
    if (count) count.textContent = rows.length ? `${shown} von ${rows.length}` : '';
  }
  document.querySelectorAll('.chip').forEach(b => b.addEventListener('click', () => {
    person = b.dataset.person;
    document.querySelectorAll('.chip').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    apply();
  }));
  [search, kind, state].forEach(el => el && el.addEventListener('input', apply));
  apply();
})();
</script>
<?php endif; ?>
</body>
</html>
