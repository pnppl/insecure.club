<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$url = htmlspecialchars($_POST['url'] ?? '');
	if (!$url) {
		die('Missing URL field');
	}
	$ssl = $_POST['ssl'];
	$cat = $_POST['cat'];
	if (!$cat) {
		die('Missing category selection');
	}
	$desc = htmlspecialchars($_POST['desc'] ?? '');
	$gopher_url = htmlspecialchars($_POST['gopher-url'] ?? '');
	$gemini_url = htmlspecialchars($_POST['gemini-url'] ?? '');
	$feed_url = htmlspecialchars($_POST['feed-url'] ?? '');
	$css_opt = $_POST['css-opt'];
	$libre = $_POST['libre'];
	$email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);
	$message = htmlspecialchars($_POST['message'] ?? '');

	$to = 'submission@insecure.club';
	$subject = "New submission: $url";

	$body = "---\n";
	$body .= "url: $url\n";
	$body .= "ssl: $ssl\n";
	$body .= "cat: $cat\n";
	$body .= "desc: $desc\n";
	$body .= "gopher-url: $gopher_url\n";
	$body .= "gemini-url: $gemini_url\n";
	$body .= "feed-url: $feed_url\n";
	$body .= "css-opt: $css_opt\n";
	$body .= "libre: $libre\n";
	$body .= "added: ";
	$body .= date("Y-m-d");
	$body .= "\n\n$message";

	$headers = "From: <$to>\n";
	if ($email) {
		$headers .= "Reply-To: $email\n";
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
