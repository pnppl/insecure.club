<?php

require __DIR__ . '/indieauth-client-php/vendor/autoload.php';

$allowlist_path = '../sites.txt';
$loc = 'http://insecure.club/house/';
if (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] != 'off') {
	$loc = 'https://insecure.club/house/';
}

session_set_cookie_params([
	'lifetime' => 0,
	'path' => '/house',
	'secure' => false,
	'httponly' => true,
	'samesite' => 'Strict',
]);
session_start();

$html = <<<EOD
<!DOCTYPE html>
<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="color-scheme" content="light dark">
	<title>Clubhouse | insecure.club</title>
	<style><!--
	@media (prefers-color-scheme: dark) {
		body {
			background-color: black;
		}
	}
	--></style>
</head>
<body>
EOD;

if (isset($_SESSION['user'])) {
	$html .= <<<EOD

	<form action="." method="post"><fieldset>
		<label>
			Logged in as <a href="
EOD;
	$html .= $_SESSION['user'] . '">' . bare_url($_SESSION['user']);
	$html .= '</a> via <a href="' . $_SESSION['via'] . '">' . bare_url($_SESSION['via'] . '</a>');
	$html .= <<<EOD

			<input type="submit" name="mode" value="Log Out">
		</label>
	</fieldset></form>
	<center><h1>Clubhouse</h1></center>
	<form action="." method="post"><fieldset>
		<label>
			Message:
			<br>
			<textarea name="message" id="message"
			placeholder="Hello i am a very unfortunate nigerian prince who needs your help.
i will pay you 1 Million Dollars and a life time supply of boner pills if you wire me only 1000$"
			required></textarea>
		</label>
		<br>
		<label>
			Optional site to link your post to (your site's URL will always be shown):
			<br>
			<input type="url" name="link" id="link" placeholder="http://handthing.party/" title="Optional">
		</label>
		<br>
		<label><input type="checkbox" name="public" id="public"> Public</label>
		<input type="submit" name="mode" value="Post">
	</fieldset></form>

EOD;
} else {
	$html .= <<<EOD

	<form action="." method="post">
		<input type="text" name="url" placeholder="pnppl.cc">
		<input type="submit" name="mode" value="Log In">
	</form>
	<center><h1>Clubhouse</h1></center>
	<center><h2>These are only the public posts. <a href="../submit/">Join</a> to see the rest!</h2></center>

EOD;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	switch ($_POST['mode']) {
		case 'Log In':
			if (!isset($_POST['url']) || $_POST['url'] === '') {
				$html .= "<p>Error: Missing URL</p>";
			} else {
				$allowlist = file($allowlist_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
				if (in_array('http://' . bare_url($_POST['url']), $allowlist, true)) {
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
				} else {
					$html .= '<p>Only club members are allowed in the clubhouse. If your site is on the <a href="' . $allowlist_path . '">list</a> but you still can\'t log in, <a href="mailto:&#x68;&#x65;&#x6C;&#x70;&#x40;&#x69;&#x6E;&#x73;&#x65;&#x63;&#x75;&#x72;&#x65;&#x2E;&#x63;&#x6C;&#x75;&#x62;?subject=Clubhouse%20login%20issue">email me</a>.</p>';
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
			$msg = trim($_POST['message'] ?? '');
			if ($msg === '') {
				$html .= "<p>Got empty message.</p>";
			} elseif (isset($_SESSION['user'])) {
				$dir = 'posts/';
				if (isset($_POST['public'])) {
					$dir = 'public/';
				}
				$msg = htmlspecialchars($msg);
				$link = trim(filter_var($_POST['link'] ?? '', FILTER_VALIDATE_URL));
				if ($link !== '') {
					$msg = '<a href="' . $link . '">' . $msg . '</a>';
				}
				file_put_contents($dir . time() . ' ' . bare_url($_SESSION['user']), $msg);
				// $html .= '<p>Message posted! Refreshing in 5 seconds...</p>';
				// $html .= '<meta http-equiv="Refresh" content="5; url=\'.\'">';
				header('Location: ' . $loc);
			} else {
				$html .= "<p>You must be logged in to post.</p>";
			}
			break;
		case 'Delete':
			$victim = $_POST['victim'] ?? '';
			if ($victim !== '') {
				$filename = explode(" ", $victim);
				if (check_author($filename[1]) && preg_match('/^posts|public\//', $filename[0])) {
					unlink($victim);
					header('Location: ' . $loc);
				} else {
					$html .= "<p>You can only delete your own posts.</p>";
				}
			} else {
				$html .= "<p>Missing deletion target.</p>";
			}
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

// display the posts
$public = array_diff(scandir('public/', SCANDIR_SORT_DESCENDING), array('..', '.'));
$posts = array_fill_keys($public, 'public/');
if (isset($_SESSION['user'])) {
	$private = array_diff(scandir('posts/', SCANDIR_SORT_DESCENDING), array('..', '.'));
	$private = array_fill_keys($private, 'posts/');
	$posts = array_merge($posts, $private);
	krsort($posts);
}
foreach ($posts as $file => $dir) {
	$filename = explode(" ", $file);
	$post_time = date('Y-m-d (D.) @ H:i:s', $filename[0]);
	$post_author = $filename[1];
	$post_text = file_get_contents($dir . $file);
	$html .= "\n\t<blockquote>\n\t\t" . $post_text . "<br>\n\t\t<i>" . 'posted by <a href="http://' . $post_author . '">' . $post_author . '</a>, <time>' . $post_time . '</time></i>';
	if (check_author($post_author)) {
		$html .= <<<EOD

			<form action="." method="post">
				<input type="submit" name="mode" value="Delete">
	EOD;
		$html .= '<input type="hidden" name="victim" value="' . $dir . $file . '">' . "\n\t\t</form>";
	}
	$html .= "\n\t</blockquote>";
}

$html .= <<<EOD

</body>
</html>
EOD;
echo $html;

function bare_url($url) {
	$url_bare = preg_replace('/^https?:\/\//i', '', $url, 1);
	return preg_replace('/\/$/', '', $url_bare, 1);
}
function check_author($name) {
	if (isset($_SESSION['user']) && (bare_url($_SESSION['user']) === $name || bare_url($_SESSION['user']) === 'pnppl.cc')) {
		return true;
	}
	return false;
}

exit();
?>
