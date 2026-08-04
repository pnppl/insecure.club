<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$url = htmlspecialchars($_POST['url'] ?? '');
	if (!$url) {
		die('Missing URL field');
	}
	$ssl = $_POST['ssl'] ?? 'no';
	$cat = $_POST['cat'] ?? '';
	if (!$cat) {
		die('Missing category selection');
	}
	$desc = htmlspecialchars($_POST['desc'] ?? '');
	$gopher_url = htmlspecialchars($_POST['gopher-url'] ?? '');
	$gemini_url = htmlspecialchars($_POST['gemini-url'] ?? '');
	$feed_url = htmlspecialchars($_POST['feed-url'] ?? '');
	$css_opt = $_POST['css-opt'] ?? 'no';
	$libre = $_POST['libre'] ?? 'no';
	$button = htmlspecialchars($_POST['button'] ?? '');
	$email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);
	$message = htmlspecialchars($_POST['message'] ?? '');

	$to = 'submission@insecure.club';
	$subject = "New submission: $url";

	$body = "---\n";
	$body .= "url: $url\n";
	$body .= "ssl: $ssl\n";
	$body .= "cat: $cat\n";
	if (!empty($desc)) {
		$body .= "desc: $desc\n";
	}
	if (!empty($gopher_url)) {
		$body .= "gopher-url: $gopher_url\n";
	}
	if (!empty($gemini_url)) {
		$body .= "gemini-url: $gemini_url\n";
	}
	if (!empty($feed_url)) {
		$body .= "feed-url: $feed_url\n";
	}
	$body .= "css-opt: $css_opt\n";
	$body .= "libre: $libre\n";
	if (!empty($button)) {
		$body .= "button: $button\n";
	}
	$body .= "added: " . date("Y-m-d") . "\n";
	$body .= "\nuser included the message: $message";

	$headers = "From: <$to>\n";
	if ($email) {
		$headers .= "Reply-To: <$email>\n";
	}
	$headers .= "Content-Type: text/plain; charset=UTF-8\n";

	// Send email
	if (mail($to, $subject, $body, $headers)) {
		echo "Website submitted successfully!";
	} else {
		echo "Website submission failed.";
	}
}
?>
