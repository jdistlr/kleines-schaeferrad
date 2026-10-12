<?php
// Vorlage. Die echte konfig.php schreibt die Veröffentlichung aus dem GitHub-Secret KS_EXPORT_SCHLUESSEL.
// Nie mit echtem Schlüssel ins Repository legen.
return [
    'export_schluessel' => 'hier-eine-lange-zufallszeichenfolge',
    // Passwort für control.php aus dem GitHub-Secret KS_CONTROL_PASSWORD (mindestens 12 Zeichen).
    'control_password' => 'hier-ein-passwort',
];
