<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$html = <<<EOD
<!DOCTYPE html>
<html>
<head>
	<title>HTTP test results</title>
	<style><!--
		html,
		body,
		center {
			width: 100%;
			padding: 0;
			margin: 0;
		}
		center {
			margin: 0.25em auto;
		}
	--></style>
</head>
<body>
EOD;
	$html .= "\n<center>";
	$url = filter_var($_POST['url'] ?? '', FILTER_VALIDATE_URL) ?: '';
	if (mb_strlen($url, 'UTF-8') > 400) {
		$html .= 'URL too long.';
	}
	elseif (empty($url)) {
		header('Location: ../');
		exit();
	}
	else {
		$url = preg_replace('/^https?:\/\//i', '', $url, 1);
		$curled = curl_init('http://' . $url);
		curl_setopt($curled, CURLOPT_NOBODY, true); // -I
		curl_setopt($curled, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($curled, CURLOPT_TIMEOUT, 30);
		curl_exec($curled);
		$result = curl_getinfo($curled, CURLINFO_HTTP_CODE);
		curl_close($curled);

		if ($result === 200) {
			$html .= "<span style=\"color:green\">$url supports HTTP!</span>";
		}
		else {
			$html .= "<span style=\"color:firebrick\">$url does <b>not</b> support HTTP (got $result).";
		}
	}

	$html .= <<<EOD
 <a href="../">Check another URL</a></center>
</body>
</html>
EOD;
	header('Content-Type: text/html');
	echo $html;
	exit();
}
header('Location: ../');
exit();
?>
