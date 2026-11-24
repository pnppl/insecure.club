<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	if (strcasecmp($_POST['captcha'] ?? '', 'http') !== 0) {
		die('wrong answer to CAPTCHA');
	}

	// URLs should probably all be validated as URLs
	// client-side i only check the button URL cuz it's the only one I want the protocol for
	// should update everything to validate on both ends (also update placeholders) then strip the protocol in here
	// don't think i need to bother with rate limiting unless i get abuse because sending is capped at 10/hr in the host settings
	$url = htmlspecialchars($_POST['url'] ?? '');
	$url = str_replace(["\n", "\r"], '', $url);
	if (empty($url)) {
		die('Missing URL field');
	}
	if (mb_strlen($url, 'UTF-8') > 400) {
		die('URL too long');
	}

	$ssl = isset($_POST['ssl']) ? '1' : '0';

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

	$gopher = htmlspecialchars($_POST['gopher'] ?? '');
	$gopher = str_replace(["\n", "\r"], '', $gopher);
	if (mb_strlen($gopher, 'UTF-8') > 400) {
		die('Gopher URL too long');
	}

	$gemini = htmlspecialchars($_POST['gemini'] ?? '');
	$gemini = str_replace(["\n", "\r"], '', $gemini);
	if (mb_strlen($gemini, 'UTF-8') > 400) {
		die('Gemini URL too long');
	}

	$feed = htmlspecialchars($_POST['feed'] ?? '');
	$feed = str_replace(["\n", "\r"], '', $feed);
	if (mb_strlen($feed, 'UTF-8') > 400) {
		die('Feed URL too long');
	}

	$css = isset($_POST['css']) ? '1' : '0';

	$libre = isset($_POST['libre']) ? '1' : '0';

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

	$body = "url: $url\n";
	$body .= "ssl: $ssl\n";
	$body .= "cat: $cat\n";
	$cmd = <<<EOD

	recins --verbose -t site \\
		-f url -v $url \\
		-f ssl -v $ssl \\
		-f cat -v $cat \\

	EOD;
	if (!empty($desc)) {
		$body .= "desc: $desc\n";
		$cmd .= "\t-f desc -v $desc \\\n";
	}
	if (!empty($gopher)) {
		$body .= "gopher: $gopher\n";
		$cmd .= "\t-f gopher -v $gopher \\\n";
	}
	if (!empty($gemini)) {
		$body .= "gemini: $gemini\n";
		$cmd .= "\t-f gemini -v $gemini \\\n";
	}
	if (!empty($feed)) {
		$body .= "feed: $feed\n";
		$cmd .= "\t-f feed -v $feed \\\n";
	}
	$body .= "css: $css\n";
	$body .= "libre: $libre\n";
	$cmd .= <<<EOD
		-f css -v $css \\
		-f libre -v $libre \\

	EOD;
	if (!empty($button)) {
		$body .= "button: $button\n";
		$button_name = str_replace('.gif', '', end(explode('/', $button)));
		$cmd .= "\t-f button -v $button_name \\\n";
	}
	$date = date("Y-m-d");
	$cmd .= "\t-f added -v $date \\\n";
	if (!empty($message)) {
		$body .= "\nuser included the message:\n> $message\n";
	}
	$body .= $cmd . "\t~/insecure.club/sites.rec &&\n\trecfix --sort ~/insecure.club/sites.rec";

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
