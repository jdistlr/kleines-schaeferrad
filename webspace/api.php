<?php
/*
 * Antworten-Schnittstelle des Cockpits auf schaeferrad.jdistlr.de
 *
 * Keine Datenbank: eine JSON-Datei je Antwort unter daten/antworten/JJJJ/MM/, nur anhängen.
 * Beschreibung: docs/ordnung/ANTWORTEN-SCHNITTSTELLE.md im Repository jdistlr/kleines-schaeferrad.
 *
 *   GET  api.php?aktion=liste            alle Antworten (öffentlich, wie im Cockpit sichtbar)
 *   GET  api.php?aktion=namen            Namensvorschläge (Vorname, bei Gleichheit mit Nachnamensergänzung)
 *   POST api.php?aktion=speichern        neue Antwort (multipart/form-data oder JSON)
 *   GET  api.php?aktion=datei&id=…       angehängtes Foto oder Sprachnachricht
 *   GET  api.php?aktion=export&schluessel=…   alles für die Übernahme ins Repository
 *
 * Speichern und Export schreiben je Aufruf eine Zeile nach daten/log/YYYY-MM-DD.jsonl
 * (Ansicht: control.php). Neuer Code nutzt englische Bezeichner (AGENTS.md).
 */
declare(strict_types=1);

const MAX_TEXT = 6000;
const MAX_BILD = 15 * 1024 * 1024;
const MAX_TON = 25 * 1024 * 1024;
const MAX_DATEIEN = 6;
const BILD_KANTE = 2000;
const PRO_MINUTE = 8;
const TYPEN = ['stimmt', 'stimmt_nicht', 'genauer', 'ergaenzung', 'korrektur', 'hinweis'];
// Anker: Kern-IDs (Fragen, Bauteile, Quellen, Angaben, Beziehungen) oder der feste Anker VORGEHEN.
const ANKER = '/^(VORGEHEN|[A-Z][A-Z0-9]*(?:-[A-Za-z0-9_]+)+)$/';

$DATEN = __DIR__ . '/daten';
$KONFIG = is_file(__DIR__ . '/konfig.php') ? require __DIR__ . '/konfig.php' : [];
const LOG_KEEP_DAYS = 180;
$REQUEST_LOG = ['started' => microtime(true)];

/** Appends one JSON line per logged request; never breaks the response. */
function logRequest(int $status, $payload): void {
    global $REQUEST_LOG, $DATEN, $KONFIG;
    $action = $_GET['aktion'] ?? '';
    if (!in_array($action, ['speichern', 'export'], true)) return;
    $outcome = $REQUEST_LOG['outcome'] ?? ($status < 300 ? ($action === 'export' ? 'exported' : 'saved') : (string)($payload['fehler'] ?? 'error'));
    $ip = $_SERVER['REMOTE_ADDR'] ?? '';
    $entry = [
        'time' => gmdate('Y-m-d\TH:i:s\Z'),
        'action' => $action,
        'method' => $_SERVER['REQUEST_METHOD'] ?? '',
        'status' => $status,
        'outcome' => $outcome,
        'answer_id' => is_array($payload) && isset($payload['id']) && $payload['id'] !== 'ok' ? $payload['id'] : null,
        'target' => $REQUEST_LOG['target'] ?? null,
        'name' => $REQUEST_LOG['name'] ?? null,
        'view' => $REQUEST_LOG['view'] ?? null,
        'files' => $REQUEST_LOG['files'] ?? 0,
        'request_bytes' => (int)($_SERVER['CONTENT_LENGTH'] ?? 0),
        'duration_ms' => (int)round((microtime(true) - $REQUEST_LOG['started']) * 1000),
        'user_agent' => mb_substr((string)($_SERVER['HTTP_USER_AGENT'] ?? ''), 0, 200),
        // Short daily pseudonym instead of the IP address: groups requests of one day, not reversible.
        'client' => $ip === '' ? null : substr(hash('sha256', $ip . gmdate('Ymd') . ($KONFIG['export_schluessel'] ?? '')), 0, 8),
    ];
    $dir = $DATEN . '/log';
    if (!is_dir($dir)) @mkdir($dir, 0775, true);
    @file_put_contents($dir . '/' . gmdate('Y-m-d') . '.jsonl', json_encode($entry, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n", FILE_APPEND | LOCK_EX);
    if (random_int(0, 100) === 0) foreach (glob($dir . '/*.jsonl') ?: [] as $old) if (filemtime($old) < time() - LOG_KEEP_DAYS * 86400) @unlink($old);
}

function antwort(int $status, $daten): void {
    logRequest($status, $daten);
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($daten, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
function fehler(int $status, string $text): void { antwort($status, ['fehler' => $text]); }

function einzeilig($v, int $max): string {
    $v = is_string($v) ? $v : '';
    $v = preg_replace('/[\x00-\x09\x0B-\x1F\x7F]/u', '', $v) ?? '';
    return mb_substr(trim($v), 0, $max);
}
function mehrzeilig($v, int $max): string {
    $v = is_string($v) ? str_replace("\r\n", "\n", $v) : '';
    $v = preg_replace('/[\x00-\x08\x0B-\x1F\x7F]/u', '', $v) ?? '';
    return mb_substr(trim($v), 0, $max);
}

/** Schreibt atomar: erst Zwischendatei, dann umbenennen. */
function schreibe(string $pfad, string $inhalt): void {
    if (!is_dir(dirname($pfad)) && !mkdir(dirname($pfad), 0775, true) && !is_dir(dirname($pfad))) fehler(500, 'Ablage nicht beschreibbar');
    $tmp = $pfad . '.' . bin2hex(random_bytes(4)) . '.tmp';
    if (file_put_contents($tmp, $inhalt, LOCK_EX) === false || !rename($tmp, $pfad)) { @unlink($tmp); fehler(500, 'Speichern fehlgeschlagen'); }
}

/** Liest alle Antworten; ein Zwischenspeicher wird bei jeder neuen Antwort verworfen. */
function alle(string $DATEN): array {
    $cache = $DATEN . '/cache-liste.json';
    if (is_file($cache)) { $c = json_decode((string)file_get_contents($cache), true); if (is_array($c)) return $c; }
    $liste = [];
    foreach (glob($DATEN . '/antworten/*/*/*.json') ?: [] as $f) {
        $a = json_decode((string)file_get_contents($f), true);
        if (is_array($a) && !empty($a['id'])) $liste[] = $a;
    }
    usort($liste, fn($x, $y) => strcmp($x['am'] ?? '', $y['am'] ?? ''));
    schreibe($cache, json_encode($liste, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    return $liste;
}

function oeffentlich(array $a): array {
    unset($a['ip'], $a['geraet']);
    return $a;
}

/** Vorname, bei mehreren verschiedenen Personen gleichen Vornamens mit Nachnamensergänzung. */
function namensvorschlaege(array $liste): array {
    $voll = [];
    foreach ($liste as $a) { $n = trim(preg_replace('/\s+/u', ' ', $a['name'] ?? '') ?? ''); if ($n !== '') $voll[mb_strtolower($n)] = $n; }
    $nachVorname = [];
    foreach ($voll as $n) { $teile = explode(' ', $n); $nachVorname[mb_strtolower($teile[0])][] = $teile; }
    $vorschlaege = [];
    foreach ($nachVorname as $gruppe) {
        $nachnamen = array_values(array_unique(array_map(fn($t) => implode(' ', array_slice($t, 1)), $gruppe)));
        $mitNachname = array_values(array_filter($nachnamen, fn($x) => $x !== ''));
        if (count($mitNachname) <= 1) { $vorschlaege[] = $gruppe[0][0]; if (count($nachnamen) > 1 && count($mitNachname) === 1) continue; continue; }
        foreach ($mitNachname as $nn) {
            for ($l = 1; $l <= mb_strlen($nn); $l++) {
                $k = mb_substr($nn, 0, $l);
                $gleich = array_filter($mitNachname, fn($x) => mb_strtolower(mb_substr($x, 0, $l)) === mb_strtolower($k));
                if (count($gleich) === 1) { $vorschlaege[] = $gruppe[0][0] . ' ' . $k . ($l < mb_strlen($nn) ? '.' : ''); break; }
            }
        }
    }
    sort($vorschlaege, SORT_LOCALE_STRING);
    return array_values(array_unique($vorschlaege));
}

function bremse(string $DATEN): void {
    $id = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . date('YmdHi'));
    $f = $DATEN . '/bremse/' . $id;
    $n = is_file($f) ? (int)file_get_contents($f) : 0;
    if ($n >= PRO_MINUTE) fehler(429, 'Zu viele Antworten in kurzer Zeit. Bitte gleich noch einmal versuchen.');
    schreibe($f, (string)($n + 1));
    if (random_int(0, 50) === 0) foreach (glob($DATEN . '/bremse/*') ?: [] as $alt) if (filemtime($alt) < time() - 300) @unlink($alt);
}

function datei_speichern(string $DATEN, array $f): ?array {
    if (($f['error'] ?? UPLOAD_ERR_NO_FILE) === UPLOAD_ERR_NO_FILE) return null;
    if ($f['error'] !== UPLOAD_ERR_OK || !is_uploaded_file($f['tmp_name'])) fehler(400, 'Datei konnte nicht hochgeladen werden');
    $mime = (new finfo(FILEINFO_MIME_TYPE))->file($f['tmp_name']) ?: '';
    $id = date('Ymd-His') . '-' . bin2hex(random_bytes(5));
    $ziel = $DATEN . '/dateien/';
    if (!is_dir($ziel)) mkdir($ziel, 0775, true);
    if (str_starts_with($mime, 'image/')) {
        if ($f['size'] > MAX_BILD) fehler(413, 'Foto zu groß (höchstens 15 MB)');
        $bild = verkleinern($f['tmp_name'], $mime);
        if ($bild !== null) { schreibe($ziel . $id . '.jpg', $bild); return ['id' => $id . '.jpg', 'art' => 'bild', 'name' => einzeilig($f['name'], 120)]; }
        $endung = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp', 'image/heic' => 'heic', 'image/heif' => 'heic', 'image/gif' => 'gif'][$mime] ?? null;
        if (!$endung) fehler(415, 'Bildformat wird nicht unterstützt');
        move_uploaded_file($f['tmp_name'], $ziel . $id . '.' . $endung);
        return ['id' => $id . '.' . $endung, 'art' => 'bild', 'name' => einzeilig($f['name'], 120)];
    }
    if (str_starts_with($mime, 'audio/') || $mime === 'video/webm' || $mime === 'video/mp4') {
        if ($f['size'] > MAX_TON) fehler(413, 'Sprachnachricht zu groß (höchstens 25 MB)');
        $endung = ['audio/webm' => 'webm', 'video/webm' => 'webm', 'audio/ogg' => 'ogg', 'audio/mpeg' => 'mp3', 'audio/mp4' => 'm4a', 'audio/x-m4a' => 'm4a', 'video/mp4' => 'm4a', 'audio/aac' => 'aac', 'audio/wav' => 'wav', 'audio/x-wav' => 'wav'][$mime] ?? null;
        if (!$endung) fehler(415, 'Tonformat wird nicht unterstützt');
        move_uploaded_file($f['tmp_name'], $ziel . $id . '.' . $endung);
        return ['id' => $id . '.' . $endung, 'art' => 'ton', 'name' => einzeilig($f['name'], 120)];
    }
    fehler(415, 'Nur Fotos und Sprachnachrichten können angehängt werden');
    return null;
}

/** Verkleinert auf höchstens BILD_KANTE, dreht nach EXIF, speichert JPEG. Ohne GD: null. */
function verkleinern(string $pfad, string $mime): ?string {
    if (!function_exists('imagecreatefromstring')) return null;
    $roh = @imagecreatefromstring((string)file_get_contents($pfad));
    if (!$roh) return null;
    if ($mime === 'image/jpeg' && function_exists('exif_read_data')) {
        $o = @exif_read_data($pfad)['Orientation'] ?? 1;
        $winkel = [3 => 180, 6 => -90, 8 => 90][$o] ?? 0;
        if ($winkel) { $g = imagerotate($roh, $winkel, 0); if ($g) { imagedestroy($roh); $roh = $g; } }
    }
    $b = imagesx($roh); $h = imagesy($roh); $s = min(1, BILD_KANTE / max($b, $h));
    $neu = imagecreatetruecolor(max(1, (int)round($b * $s)), max(1, (int)round($h * $s)));
    imagefill($neu, 0, 0, imagecolorallocate($neu, 255, 255, 255));
    imagecopyresampled($neu, $roh, 0, 0, 0, 0, imagesx($neu), imagesy($neu), $b, $h);
    ob_start(); imagejpeg($neu, null, 84); $jpg = (string)ob_get_clean();
    imagedestroy($roh); imagedestroy($neu);
    return $jpg;
}

$aktion = $_GET['aktion'] ?? '';
$methode = $_SERVER['REQUEST_METHOD'] ?? 'GET';

if ($aktion === 'liste' && $methode === 'GET') antwort(200, array_map('oeffentlich', alle($DATEN)));
if ($aktion === 'namen' && $methode === 'GET') antwort(200, namensvorschlaege(alle($DATEN)));

if ($aktion === 'datei' && $methode === 'GET') {
    $id = basename((string)($_GET['id'] ?? ''));
    if (!preg_match('/^\d{8}-\d{6}-[0-9a-f]{10}\.(jpg|png|webp|heic|gif|webm|ogg|mp3|m4a|aac|wav)$/', $id)) fehler(404, 'Nicht gefunden');
    $f = $DATEN . '/dateien/' . $id;
    if (!is_file($f)) fehler(404, 'Nicht gefunden');
    header('Content-Type: ' . ((new finfo(FILEINFO_MIME_TYPE))->file($f) ?: 'application/octet-stream'));
    header('Content-Length: ' . filesize($f));
    header('Cache-Control: public, max-age=31536000, immutable');
    header('X-Content-Type-Options: nosniff');
    readfile($f);
    exit;
}

if ($aktion === 'export' && $methode === 'GET') {
    $soll = (string)($KONFIG['export_schluessel'] ?? '');
    if (strlen($soll) < 16 || !hash_equals($soll, (string)($_GET['schluessel'] ?? ''))) fehler(403, 'Kein Zugriff');
    antwort(200, ['erzeugt' => gmdate('c'), 'antworten' => alle($DATEN)]);
}

if ($aktion === 'speichern' && $methode === 'POST') {
    $json = str_starts_with($_SERVER['CONTENT_TYPE'] ?? '', 'application/json');
    $e = $json ? (json_decode((string)file_get_contents('php://input'), true) ?: []) : $_POST;
    $REQUEST_LOG['target'] = einzeilig($e['ziel'] ?? '', 80);
    $REQUEST_LOG['name'] = einzeilig($e['name'] ?? '', 80);
    $REQUEST_LOG['view'] = einzeilig($e['ansicht'] ?? '', 120);
    $REQUEST_LOG['files'] = (!$json && !empty($_FILES['dateien']['name'])) ? count(array_filter((array)$_FILES['dateien']['name'], fn($n) => $n !== '')) : 0;
    if (!empty($e['webseite'])) { $REQUEST_LOG['outcome'] = 'honeypot'; antwort(201, ['id' => 'ok']); } // Fangfeld: Bots bekommen „ok“, nichts wird gespeichert
    $ziel = einzeilig($e['ziel'] ?? '', 80);
    if (!preg_match(ANKER, $ziel)) fehler(400, 'Unbekanntes Ziel');
    $typ = einzeilig($e['typ'] ?? '', 20);
    if (!in_array($typ, TYPEN, true)) $typ = 'hinweis';
    $text = mehrzeilig($e['text'] ?? '', MAX_TEXT);
    $wert = einzeilig($e['wert'] ?? '', 120);
    $betrifft = array_values(array_filter(array_map(fn($x) => einzeilig($x, 80), is_array($e['betrifft_auch'] ?? null) ? $e['betrifft_auch'] : preg_split('/[\s,]+/', (string)($e['betrifft_auch'] ?? ''))), fn($x) => preg_match(ANKER, $x)));
    $auf = einzeilig($e['antwort_auf'] ?? '', 60);
    if ($auf !== '' && !preg_match('/^A-\d{8}-\d{6}-[0-9a-f]{8}$/', $auf)) $auf = '';
    bremse($DATEN);
    $dateien = [];
    if (!$json && !empty($_FILES['dateien'])) {
        $F = $_FILES['dateien'];
        $n = is_array($F['name']) ? count($F['name']) : 1;
        if ($n > MAX_DATEIEN) fehler(413, 'Höchstens ' . MAX_DATEIEN . ' Dateien je Antwort');
        for ($i = 0; $i < $n; $i++) {
            $eine = is_array($F['name']) ? ['name' => $F['name'][$i], 'type' => $F['type'][$i], 'tmp_name' => $F['tmp_name'][$i], 'error' => $F['error'][$i], 'size' => $F['size'][$i]] : $F;
            if ($d = datei_speichern($DATEN, $eine)) $dateien[] = $d;
        }
    }
    if ($text === '' && $wert === '' && !$dateien && !in_array($typ, ['stimmt', 'stimmt_nicht'], true)) fehler(400, 'Die Antwort ist leer');
    $jetzt = new DateTimeImmutable('now', new DateTimeZone('UTC'));
    $id = 'A-' . $jetzt->format('Ymd-His') . '-' . bin2hex(random_bytes(4));
    $a = [
        'id' => $id, 'ziel' => $ziel, 'typ' => $typ, 'text' => $text, 'wert' => $wert,
        'name' => einzeilig($e['name'] ?? '', 80), 'am' => $jetzt->format('Y-m-d\TH:i:s\Z'),
        'antwort_auf' => $auf ?: null, 'betrifft_auch' => $betrifft,
        'frage_wortlaut' => mehrzeilig($e['frage_wortlaut'] ?? '', 600), 'ansicht' => einzeilig($e['ansicht'] ?? '', 120),
        'dateien' => $dateien, 'uebernommen' => false, 'quelle' => 'webspace',
        'geraet' => einzeilig($_SERVER['HTTP_USER_AGENT'] ?? '', 200),
    ];
    schreibe($DATEN . '/antworten/' . $jetzt->format('Y/m') . '/' . $id . '.json', json_encode($a, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT));
    @unlink($DATEN . '/cache-liste.json');
    antwort(201, oeffentlich($a));
}

fehler(404, 'Unbekannte Aktion');
