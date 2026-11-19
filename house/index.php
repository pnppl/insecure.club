<?php

require __DIR__ . '/indieauth-client-php/vendor/autoload.php';

session_start();

$loc = 'https://insecure.club/house/';
$html = <<<EOD
<!DOCTYPE html>
<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="color-scheme" content="light dark">
	<title>clubhouse | insecure.club</title>
</head>
<body>
EOD;

if (isset($_SESSION['user'])) {
	$html .= "<p>Logged in as " . $_SESSION['user'] . ' via ' . $_SESSION['via'] . '</p>';
	$html .= <<<EOD
	<form action="." method="post">
		<input type="submit" name="mode" value="Log Out">
	</form>
	EOD;
} else {
	$html .= <<<EOD
	<form action="." method="post">
		<input type="text" name="url">
		<input type="submit" name="mode" value="Log In">
	</form>
	EOD;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	switch ($_POST['mode']) {
		case 'Log In':
			if(!isset($_POST['url'])) {
				$html .= "<p>Error: Missing URL</p>";
			} else {
				IndieAuth\Client::$clientID = $loc;
				IndieAuth\Client::$redirectURL = $loc;

				// Pass the user's URL and your requested scope to the client (scope omitted for simple auth)
				list($authorizationURL, $error) = IndieAuth\Client::begin($_POST['url']);

				// indielogin fallback (for rel=me etc)
				// seems to be working, ish, but you have to type the URL exactly or you get an error about the auth endpoints not matching
				// kind of seems like these begin/complete wrappers just don't really work well with indielogin despite it being specifically mentioned
				if ($error) {
					$error = false;
					list($authorizationURL, $error) = IndieAuth\Client::begin(
						$_POST['url'],
						authorizationEndpoint: 'https://indielogin.com/auth', // the docs all say /authorize, but chatbot insisted on /auth which i tried, and surprisingly i stopped getting 405s...
					);
				}

				if ($error) {
					$html .= "<p>Error: " . $error['error'] . "</p>";
					$html .= "<p>" . $error['error_description'] . "</p>";
				} else {
					// Redirect the user to their authorization endpoint
					header('Location: ' . $authorizationURL);
				}
			}
			break;
		case 'Log Out':
			// clear session
			$_SESSION = array();
			// clear cookies
			if (ini_get("session.use_cookies")) {
			    $params = session_get_cookie_params();
			    setcookie(session_name(), '', time() - 42000,
			        $params["path"], $params["domain"],
			        $params["secure"], $params["httponly"]
			    );
			}
			header('Location: ' . $loc);
			break;
		case 'Post':
			break;
		case 'Delete':
			break;
	}
}

// assume login redirect and attempt to handle it
if ($_SERVER['REQUEST_METHOD'] === 'GET' && !empty($_GET)) {
	IndieAuth\Client::$clientID = $loc;
	IndieAuth\Client::$redirectURL = $loc;
	list($response, $error) = IndieAuth\Client::complete($_GET);

	if ($error) {
		$html .= "<p>Error: ".$error['error']."</p>";
		$html .= "<p>".$error['error_description']."</p>";
		if ($error['error'] === 'invalid_authorization_endpoint') {
			$html .= "<p>Make sure you enter your URL exactly, including trailing slash if applicable.</p>";
		}
	} else {
		// login complete - save the user's URL and auth endpoint in the session
		$_SESSION['user'] = $response['me'];
		$_SESSION['via'] = $response['response_details']['url'];
		header('Location: ' . $loc);
	}
}

$html .= <<<EOD
</body>
</html>
EOD;
echo $html;

exit();
?>
