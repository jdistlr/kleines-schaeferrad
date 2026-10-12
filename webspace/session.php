<?php
/*
 * Shared sign-in session for control.php and api.php.
 *
 * Signing in happens only in control.php (GitHub OAuth). api.php reads the same session to know
 * whether Johannes or Thorsten is at the keyboard; their confirmations then count as decisions.
 * Everybody else never gets a cookie: api.php starts a session only when one already exists.
 */
declare(strict_types=1);

const SESSION_NAME = 'ks_session';

function startSession(bool $onlyIfPresent = false): bool {
    if (session_status() === PHP_SESSION_ACTIVE) return true;
    if ($onlyIfPresent && empty($_COOKIE[SESSION_NAME])) return false;
    session_name(SESSION_NAME);
    session_set_cookie_params([
        'lifetime' => 60 * 60 * 24 * 60, // stay signed in on one's own device for 60 days
        'path' => '/',
        'secure' => !empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off',
        'httponly' => true,
        'samesite' => 'Lax', // Lax: the session must survive the redirect back from github.com
    ]);
    ini_set('session.gc_maxlifetime', (string)(60 * 60 * 24 * 60));
    session_start();
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(16));
    return true;
}

/** Signed-in person allowed to decide, or null. The allowlist is re-checked on every request. */
function currentAuthority(array $config): ?array {
    $user = $_SESSION['user'] ?? null;
    if (!is_array($user)) return null;
    $id = (int)($user['id'] ?? 0);
    $allowed = array_map('intval', (array)($config['allowed_github_ids'] ?? []));
    if (!in_array($id, $allowed, true)) return null;
    $people = (array)($config['github_people'] ?? []);
    return [
        'id' => $id,
        'login' => (string)($user['login'] ?? ''),
        'name' => (string)($user['name'] ?? ''),
        'person' => (string)($people[(string)$id] ?? ''),
    ];
}

/** Same-origin relative path to return to after sign-in, or null. */
function safeReturnPath($value): ?string {
    $v = is_string($value) ? $value : '';
    if ($v === '' || strlen($v) > 300 || str_starts_with($v, '//') || preg_match('/[\r\n\\\\]/', $v)) return null;
    return (str_starts_with($v, './') || str_starts_with($v, '/') || str_starts_with($v, '#')) ? $v : null;
}
