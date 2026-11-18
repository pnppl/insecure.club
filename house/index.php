<?php

require __DIR__ . '/indieauth-client-php/vendor/autoload.php';

// Start a session for the library to be able to save state between requests.
session_start();
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

if (!isset($_SESSION['user'])) {
	$html .= <<<EOD
	<form action="." method="post">
		<input type="text" name="url">
		<input type="submit" name="mode" value="Log In">
	</form>
	EOD;
} else {
	$html .= "<p>Logged in as " . $_SESSION['user'] . '</p>';
	$html .= <<<EOD
	<form action="." method="post">
		<input type="submit" name="mode" value="Log Out">
	</form>
	EOD;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	switch ($_POST['mode']) {
		case 'Log In':
			if(!isset($_POST['url'])) {
				$html .= "<p>Error: Missing URL</p>";
			} else {
				$html .= login();
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
			header('Location: ' . 'http://insecure.club/house/');
			break;
		case 'Post':
			break;
		case 'Delete':
			break;
		default:
			// $html .= '<p>Error: missing mode</p>';
			list($response, $error) = IndieAuth\Client::complete($_GET);
			if($error) {
				$html .= "<p>Error: ".$error['error']."</p>";
				$html .= "<p>".$error['error_description']."</p>";
			} else {
				// save the user's URL in the session
				$_SESSION['user'] = $response['me'];
				header('Location: ' . 'http://insecure.club/house/');
			}
	}
}

function login() {
	// The client ID should be the home page of your app.
	IndieAuth\Client::$clientID = 'http://insecure.club/house/';

	// The redirect URL is where the user will be returned to after they approve the request.
	IndieAuth\Client::$redirectURL = 'http://insecure.club/house/';

	// Pass the user's URL and your requested scope to the client (scope omitted for simple auth)
	list($authorizationURL, $error) = IndieAuth\Client::begin($_POST['url']);

	// Check whether the library was able to discover the necessary endpoints
	if($error) {
		$html = "<p>Error: " . $error['error'] . "</p>";
		$html .= "<p>" . $error['error_description'] . "</p>";
		return $html;
	} else {
		// Redirect the user to their authorization endpoint
		header('Location: ' . $authorizationURL);
	}
}
$html .= <<<EOD
</body>
</html>
EOD;
echo $html;

exit();
?>
