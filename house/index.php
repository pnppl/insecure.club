<?php

require __DIR__ . '/indieauth-client-php/vendor/autoload.php';

session_start();

$loc = 'http://insecure.club/house/';
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
	$html .= "<p>Logged in as " . $_SESSION['user'] . '</p>';
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

				// Check whether the library was able to discover the necessary endpoints
				if($error) {
					$html .= "<p>Error: " . $error['error'] . "</p>";
					$html .= "<p>" . $error['error_description'] . "</p>";
				} else {
					// Redirect the user to their authorization endpoint
					header('Location: ' . $authorizationURL);
				}
			}
			break;
		case 'Log Out':
			$_SESSION = array();
			// If it's desired to kill the session, also delete the session cookie.
			// Note: This will destroy the session, and not just the session data!
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
	if($error) {
		$html .= "<p>Error: ".$error['error']."</p>";
		$html .= "<p>".$error['error_description']."</p>";
	} else {
		// save the user's URL in the session
		$_SESSION['user'] = $response['me'];
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
