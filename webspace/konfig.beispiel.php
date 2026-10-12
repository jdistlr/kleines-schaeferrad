<?php
// Vorlage. Die echte konfig.php schreibt die Veröffentlichung aus dem GitHub-Secret KS_EXPORT_SCHLUESSEL.
// Nie mit echtem Schlüssel ins Repository legen.
return [
    'export_schluessel' => 'hier-eine-lange-zufallszeichenfolge',
    // GitHub-Anmeldung für control.php (OAuth-App von jdistlr, Secrets KS_GITHUB_CLIENT_ID/_SECRET).
    'github_client_id' => 'Ov23li…',
    'github_client_secret' => '…',
    'allowed_github_ids' => [1959022, 72215618], // jdistlr, ThorstenHalsch
];
