<?php
// include this in html with SSI so we can stick most recent public post into static pages
$public = scandir('public/', SCANDIR_SORT_DESCENDING);
$filename = explode(" ", $public[0]);
$post_time = date('Y-m-d (D.) @ H:i:s', $filename[0]);
$post_author = $filename[1];
$post_text = file_get_contents('public/' . $public[0]);
echo "<blockquote>\n\t\t\t" . $post_text . "\n\t\t</blockquote>\n\t\t<cite>" . 'posted by <a href="http://' . $post_author . '">' . $post_author . '</a>, <time>' . $post_time . "</time></cite>";
?>
