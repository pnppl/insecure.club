<?php
$sites_path = "../sites.txt";

$sites_file = fopen($sites_path, "r") or die("Can't read sites list");
$sites_str = fread($sites_file, filesize($sites_path));
fclose($sites_file);

$sites = explode("\n", $sites_str);
$site = $sites[array_rand($sites)];
header('Location: ' . $site);
?>
