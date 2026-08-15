<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$url = htmlspecialchars($_POST['url'] ?? '');
	$url = str_replace(["\n", "\r"], '', $url);
	if (empty($url)) {
		die('Missing URL field');
	}
	if (mb_strlen($url, 'UTF-8') > 400) {
		die('URL too long');
	}

	$ssl = isset($_POST['ssl']) ? 'yes' : 'no';

	$cat = $_POST['cat'] ?? '';
	$cat = str_replace(["\n", "\r"], '', $cat);
	if (empty($cat)) {
		die('Missing category selection');
	}
	if (mb_strlen($cat, 'UTF-8') > 20) {
		die('Bad category');
	}

	$desc = htmlspecialchars($_POST['desc'] ?? '');
	$desc = str_replace(["\n", "\r"], '', $desc);
	if (mb_strlen($desc, 'UTF-8') > 80) {
		$desc = mb_substr($desc, 0, 77, 'UTF-8') . "...";
	}

	$gopher_url = htmlspecialchars($_POST['gopher-url'] ?? '');
	$gopher_url = str_replace(["\n", "\r"], '', $gopher_url);
	if (mb_strlen($gopher_url, 'UTF-8') > 400) {
		die('Gopher URL too long');
	}

	$gemini_url = htmlspecialchars($_POST['gemini-url'] ?? '');
	$gemini_url = str_replace(["\n", "\r"], '', $gemini_url);
	if (mb_strlen($gemini_url, 'UTF-8') > 400) {
		die('Gemini URL too long');
	}

	$feed_url = htmlspecialchars($_POST['feed-url'] ?? '');
	$feed_url = str_replace(["\n", "\r"], '', $feed_url);
	if (mb_strlen($feed_url, 'UTF-8') > 400) {
		die('Feed URL too long');
	}

	$css_opt = isset($_POST['css-opt']) ? 'yes' : 'no';

	$libre = isset($_POST['libre']) ? 'yes' : 'no';

	$button = htmlspecialchars($_POST['button'] ?? '');
	$button = str_replace(["\n", "\r"], '', $button);
	if (mb_strlen($button, 'UTF-8') > 400) {
		die('Button URL too long');
	}

	$email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);

	$message = htmlspecialchars($_POST['message'] ?? '');
	$message = str_replace(["\n", "\r"], '(NEWLINE)', $message);
	if (mb_strlen($message, 'UTF-8') > 5000) {
		die('Message too long');
	}

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
	if (!empty($message)) {
		$body .= "\nuser included the message:\n> $message";
	}

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
