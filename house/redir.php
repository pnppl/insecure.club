<?php

require __DIR__ . '/indieauth-client-php/vendor/autoload.php';

session_start();
IndieAuth\Client::$clientID = 'http://insecure.club/house/';
IndieAuth\Client::$redirectURL = 'http://insecure.club/house/redir.php';

list($response, $error) = IndieAuth\Client::complete($_GET);

header('Content-Type: text/html; charset=utf-8');
$html = <<<EOD
<!DOCTYPE html>
<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="color-scheme" content="light dark">
EOD;

if($error) {
	$html .= <<<EOD
		<title>Login failed</title>
	</head>
	<body>
	EOD;
} else {
	// Login succeeded!
	// The library will return the user's profile URL in the property "me"
	// It will also return the full response from the authorization or token endpoint, as well as debug info
	/*
	echo "URL: ".$response['me']."<br>";
	if(isset($response['response']['access_token'])) {
		echo "Access Token: ".$response['response']['access_token']."<br>";
		echo "Scope: ".$response['response']['scope']."<br>";
	}
	*/

	// The full parsed response from the endpoint will be available as:
	// $response['response']

	// The raw response:
	// $response['raw_response']

	// The HTTP response code:
	// $response['response_code']

	// save the user's URL in the session
	$_SESSION['user'] = $response['me'];
	$html .= <<<EOD
		<meta http-equiv="Refresh" content="0; url='/house'">
		<title>Redirecting...</title>
	</head>
	<body>
		<p>Logged in successfully! Redirecting to <a href="/house">the clubhouse</a>...</p>
	EOD;
}

$html .= <<<EOD
	</body>
	</html>
	EOD;
echo $html;

exit();
?>
