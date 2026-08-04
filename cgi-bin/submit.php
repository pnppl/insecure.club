<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$url = htmlspecialchars($_POST['your_name'] ?? '');
	$email = filter_var($_POST['your_email'] ?? '', FILTER_VALIDATE_EMAIL);
	$message = htmlspecialchars($_POST['message'] ?? '');

	// Validate
	if (!$url || !$message) {
		die('Missing fields');
	}

	$to = 'submission@insecure.club';
	$subject = "New submission: $url";

	$body = "$url";
	$body .= ":\r\n";
	$body .= "Message:\n$message";

	$headers = "From: <$to>\r\n";
	if ($email) {
		$headers .= "Reply-To: $email\r\n";
	}
	$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

	// Send email
	if (mail($to, $subject, $body, $headers)) {
		echo "Website submitted successfully!";
	} else {
		echo "Website submission failed.";
	}
}
?>
