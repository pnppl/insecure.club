<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$to = 'submission@insecure.club';
	$subject = "test";
	$body = "testing";

	// Email headers (important!)
//	$headers = "From: $email\r\n";
//	$headers .= "Reply-To: $email\r\n";
	$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

	// Send email
	if (mail($to, $subject, $body, $headers)) {
		echo "Email sent successfully!";
	} else {
		echo "Failed to send email. Please try again.";
	}
}
?>
