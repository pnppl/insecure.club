def write_head(page, out):
	path = ''
	title = "insecure.club"
	if page != 'index':
		path = '../'
		title = f"""{page} | {title}"""
	else:
		page = ''
	out.write(f"""\
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<meta name="referrer" content="no-referrer">
		<meta name="color-scheme" content="light dark">
		<meta name="theme-color" content="teal">
		<link rel="icon" href="{path}favicon.ico" sizes="16x16 32x32 48x48">
		<link rel="license" href="{path}LICENSE.md">
		<link rel="alternate" href="{path}feed/feed.atom" title="insecure.club URL feed" type="application/atom+xml">
		<link rel="alternate" href="{path}sites.yaml" title="YAML source" type="application/yaml">
		<meta property="og:site_name" content="insecure.club">
		<meta property="og:title" content="{title}">
		<meta property="og:description" content="Directory of sites that support HTTP sans S">
		<meta property="og:image" content="https://insecure.club/img/og.png">
		<meta property="og:url" content="https://insecure.club/{page}">
		<meta property="og:type" content="website">
		<meta name="description" content="Directory of sites that support HTTP sans S">
		<link rel="stylesheet" href="{path}insecure.css">
		<title>{title}</title>
""")

def write_nav(page, out):
	path = ''
	if len(page) > 0:
		path = '../'

	pages = [
		('', 'Sites'),
		('buttons', 'Buttons'),
		('fuq', 'FUQ'),
		('submit', 'Submit'),
		('random', 'Random'),
	]
	top_page = ''
	if any(page in tup for tup in pages):
		top_page = page

	out.write(f"""\
	</head>
	<body>
		<a id="skip-nav" href="#main">Skip to content</a>
		<center>
			<h1><a href="./{path}">insecure<img alt="." src="{path}img/dot.gif" width="20" height="20">club</a></h1>
			<p>A directory of websites that support HTTP <i>sans</i> S.</p>
		</center>
		<center><nav>
			<h2>[&nbsp;""")
	for entry in pages:
		if entry[0] == top_page:
			out.write(f"""<b>{entry[1]}</b>""")
		else:
			out.write(f"""<a href="{path}{entry[0]}">{entry[1]}</a>""")
		if entry[0] != 'random':
			out.write(' &#183; ')
	out.write("""&nbsp;]</h2>
""")

	lists_pages = [
		('', 'alpha'),
		('cat', 'categories'),
		('new', 'new'),
		('css-opt', 'CSS-optional'),
		('libre', 'free&nbsp;culture'),
		('has-feed', 'has&nbsp;feed')
	]
	if any(page in tup for tup in lists_pages):
		out.write("""\
			<p>[&nbsp;""")
		for entry in lists_pages:
			if entry[0] == page:
				out.write(f"""<b>{entry[1]}</b>""")
			else:
				out.write(f"""<a href="{path}{entry[0]}">{entry[1]}</a>""")
			if entry[0] == 'new':
				out.write(' | ')
			elif entry[0] != 'has-feed':
				out.write(' &#183; ')
		out.write("""&nbsp;]</p>
""")

	out.write("""\
		</nav></center>
""")

def write_filter(out, link=False):
	out.write("""\
		<center id="filters"><span class="hide">(Filters require CSS)</span>""")
	if link == False:
		for cat in all_categories:
			out.write(f""" <label><input type="checkbox" id="{cat}-filter" checked>&nbsp;{cat.capitalize()}</label> """)
	else:
		for cat in all_categories:
			out.write(f""" <span class="label"><input type="checkbox" id="{cat}-filter" checked>&nbsp;<a href="#{cat}">{cat.capitalize()}</a></span> """)
	out.write("""\
		</center>""")

def write_list(sites, page, out):
	path = ''
	if page != 'index':
		path = '../'
	out.write("""\
		<div id="main" class="list">
			<ul>
""")
	old_cat = ''
	for site in sites:
		cat = site['cat']
		if old_cat != cat and page == 'cat':
			out.write(f"""\
			</ul>
			<h3 id="{cat}">{cat.capitalize()}</h3>
			<ul>
""")
		old_cat = cat

		link = f"""<a href="http://{site['url']}">{site['url']}</a>"""
		if 'css-opt' in site and site['css-opt'] and page != 'css-opt':
			link = f"""<b class="css-opt">{link}</b>"""

		protocols = ''
		if 'ssl' in site and site['ssl']:
			protocols += f""" <a href="https://{site['url']}"><img class="icon invert" src="{path}img/prot/https.gif" alt="[HTTPS]" width="16" height="16"></a>"""
		if 'gopher-url' in site and site['gopher-url']:
			protocols += f""" <a href="gopher://{site['gopher-url']}"><img class="icon" src="{path}img/prot/gopher.gif" alt="[Gopher]" width="16" height="16"></a>"""
		if 'gemini-url' in site and site['gemini-url']:
			protocols += f""" <a href="gemini://{site['gemini-url']}"><img class="icon invert" src="{path}img/prot/gemini.gif" alt="[Gemini]" width="16" height="16"></a>"""
		if 'feed-url' in site and site['feed-url']:
			protocols += f""" <a href="http://{site['feed-url']}"><img class="icon invert" src="{path}img/prot/feed.gif" alt="[feed]" width="16" height="16"></a>"""

		out.write(f"""\
				<li class="{cat}">
					<img alt="{cat}:" class="icon invert" src="{path}img/cat/{cat}.gif" title="Category: {cat}" width="16" height="16"> {link}{protocols}
""")

		additional = ''
		if 'libre' in site and site['libre'] and page != 'libre':
			additional += """<b class="libre">Free culture!</b> """
		if 'desc' in site and site['desc']:
			additional += f"""<i class="desc">{site['desc']}</i>"""
		if len(additional) > 0:
			out.write(f"""\
					<ul><li class="additional">{additional}</li></ul>
""")

		out.write("""\
				</li>
""")
	# /for
	out.write("""\
			</ul>
""")
	if page != 'css-opt':
		out.write("""\
			<p><b>Bold</b> entries work well without CSS.</p>
		</div>
""")

# /def

def write_close(page, out):
	path = ''
	if page != 'index':
		path = '../'
	if page == '2':
		path = '../../'
	out.write(f"""\
		<br>
		<center>
			<footer>
				<a href="{path}LICENSE.md">AGPLv3</a> &#183; <a href="https://git.gay/pnppl/insecure.club">source</a> &#183; <a href="mailto:&#104;&#105;&#64;&#105;&#110;&#115;&#101;&#99;&#117;&#114;&#101;&#46;&#99;&#108;&#117;&#98;">&#104;&#105;&#64;&#105;&#110;&#115;&#101;&#99;&#117;&#114;&#101;&#46;&#99;&#108;&#117;&#98;</a> &#183; <a href="{path}feed/feed.atom">feed</a>
				<p><a href="{path}buttons"><img id="footer-button" alt="animated CRT with nervous face: this site is a little insecure" src="{path}img/buttons/crt.gif"></a></p>
			</footer>
		</center>
	</body>
</html>
""")


# main
import yaml, datetime, html

with open("sites.yaml", "r") as sites_yaml:
	sites = list(yaml.load_all(sites_yaml, Loader=yaml.SafeLoader))
sites.sort(key=lambda s: s['url'].removeprefix('www.'))
sites_by_cat = list(sorted(sites, key=lambda s: s['cat']))
all_categories = list(dict.fromkeys(site['cat'] for site in sites_by_cat))
sites_new = sorted(sites, key=lambda s: s['added'], reverse=True)
sites_has_feed = filter(lambda s: 'feed-url' in s and s['feed-url'], sites)
sites_css_opt = filter(lambda s: 'css-opt' in s and s['css-opt'], sites)
sites_libre = filter(lambda s: 'libre' in s and s['libre'], sites)
sites_button = list(filter(lambda s: 'button' in s and s['button'], sites))

with open("index.html", "w") as out:
	write_head('index', out)
	write_nav('', out)
	write_filter(out)
	write_list(sites, 'index', out)
	write_close('index', out)
with open("cat/index.html", "w") as out:
	write_head('Categories', out)
	write_nav('cat', out)
	write_filter(out, True)
	write_list(sites_by_cat, 'cat', out)
	write_close('', out)
with open("new/index.html", "w") as out:
	write_head('Recently Added', out)
	write_nav('new', out)
	write_filter(out)
	write_list(sites_new, 'new', out)
	write_close('', out)
with open("has-feed/index.html", "w") as out:
	write_head('Sites with Feeds', out)
	write_nav('has-feed', out)
	write_filter(out)
	write_list(sites_has_feed, 'feed', out)
	write_close('', out)
with open("css-opt/index.html", "w") as out:
	write_head('CSS-Optional', out)
	write_nav('css-opt', out)
	write_filter(out)
	write_list(sites_css_opt, 'css-opt', out)
	write_close('', out)
with open("libre/index.html", "w") as out:
	write_head('Free Culture', out)
	write_nav('libre', out)
	write_filter(out)
	write_list(sites_libre, 'libre', out)
	write_close('', out)
with open("buttons/index.html", "w") as out:
	write_head('Button Wall', out)
	out.write("""\
		<style><!--
		#main:not(:has(#anim:checked)) {
""")
	for site in sites_button:
		if site['button'].endswith("-anim"):
			out.write(f"""\
			img[src$="{site['button']}.gif"] {{ content: url("{site['button'][0:-5]}-static.gif") }}
""")
	out.write("""\
		}
		@media (prefers-reduced-motion: reduce) {
			/* reset the box */
			#anim {
				appearance: none;
				width: 1em;
				height: 1em;
				border: 1px solid currentColor;
				border-radius: 0.15em;
				margin: 0;
			}
			/* "uncheck" the box */
			#anim:checked:before {
				display: none;
			}
			/* "check" the box */
			#anim:before {
				content: '';
				background: currentColor;
				clip-path: polygon(14% 44%, 0 65%, 50% 100%, 100% 16%, 80% 0%, 43% 62%);
				display: block;
				width: 0.9em;
				height: 0.9em;
			}
			#main:has(#anim:checked) {
""")
	for site in sites_button:
		if site['button'].endswith("-anim"):
			out.write(f"""\
				img[src$="{site['button']}.gif"] {{ content: url("{site['button'][0:-5]}-static.gif") }}
""")
	out.write("""\
			}
			#main:not(:has(#anim:checked)) {
""")
	for site in sites_button:
		if site['button'].endswith("-anim"):
			out.write(f"""\
				img[src$="{site['button']}.gif"] {{ content: url("{site['button']}.gif") }}
""")
	out.write("""\
			}
		}
		--></style>
""")
	write_nav('buttons', out)
	out.write("""\
			<br>
""")
	write_filter(out)
	out.write("""\
		<center id="main">
			<h3>Button Wall</h3>
			<br>
			<label><input type="checkbox" id="anim" checked> Animate<span class="hide"> (toggle requires CSS)</span></label>
			<p>
""")
	for site in sites_button:
		out.write(f"""\
				<a href="http://{site['url']}"><img src="{site['button']}.gif" alt="{site['url']}" class="{site['cat']}" title="{site['url']}" width="88" height="31"></a>
""")
	out.write("""\
			</p>
			<br>
			<h3>Club/Member Buttons</h3>
			<p>
				<img alt="animated CRT with nervous face: this site is a little insecure" src="../img/buttons/crt.gif">
				<img alt="static CRT with nervous face: this site is a little insecure" src="../img/buttons/crt-static.gif">
				<img alt="! insecure.club" src="../img/buttons/warning.gif">
				<img alt="open lock with club name in edgy techno font" src="../img/buttons/unlocked.gif">
			</p>
		</center>
		<br>
""")
	write_close('', out)
with open("fuq/index.html", "w") as out:
	write_head('Fully Unasked Questions', out)
	out.write("""\
		<style><!--
		h3 {
			margin-top: 1em;
			margin-bottom: 0;
		}
		#main p,
		#main summary {
			margin-left: 1em;
		}
		#main p,
		#main details {
			margin-bottom: 1em;
		}
		#main details ul {
			margin-left: 2em;
		}
		@media screen and (max-width: 500px) {
			#main p,
			#main summary {
				margin-left: 0;
			}
			#main ol {
				padding-left: 1em;
			}
			#main details ul {
				margin-left: 1em;
			}
		}
		--></style>
""")
	write_nav('fuq', out)
	out.write("""\
		<br>
		<div id="main">
			<h3>Why does this exist?</h3>
			<ol>
				<li>To make it easier to find cool sites that can be viewed in old browsers.</li>
				<li>To raise awareness of the value of HTTP and encourage webmasters to <b>disable automatic redirects</b>.</li>
			</ol>

			<h3>What sites are eligible?</h3>
			<p>See <a href="../submit/#rules">the rules section of the submit page.</a> The TL;DR is it needs to be a real website accessible over HTTP.</p>

			<h3>Why should websites support insecure HTTP?</h3>
			<p>HTTP<b><i>S</i></b> is a massive barrier between old browsers and the web --- particularly the small and independent web, which is not so gung-ho about JavaScript. Many websites have solid HTML and would work just fine in truly ancient browsers, but the HTTP<b><i>S</i></b> requirement immediately cuts them off.</p>
			<p>Mandatory HTTP<b><i>S</i></b> is a form of forced obsolescence. Devices that are still perfectly functional are made artificially incompatible with the web, thus adding to ever-growing mountains of e-waste and discriminating against people who can't afford the latest computer/fondleslab.</p>
			<p>Plus, using old computers is <i>fun</i>.</p>

			<h3>What about privacy?</h3>
			<p>Which is worse: the risk of being spied on when you visit a website, or <i>not being able to visit it at all?</i></p>
			<p>Users should be allowed to decide for themselves if they accept that risk --- particularly since browsers make it very difficult to access insecure websites. Anyone who uses HTTP has probably either jumped through several hoops to voluntarily circumvent their browser safeguards or is entirely unable to use HTTP<b><i>S</i></b>.</p>
			<p>Sites often support broken HTTP<b><i>S</i></b> cipher suites for compatibility. Instead, they should drop the old ciphers and add HTTP --- that way compatibility is maximized and users are informed when their connection isn't truly secure.</p>

			<h3>I want to renounce industry best practices, but I don't want to self-host, and also I'm a cheapskate. What do?</h3>
			<p>I've started a <a href="http://pnppl.cc/2026-05-01_http/">list of free webhosts that support HTTP.</a></p>

			<h3>Got any other hot tips for serving HTTP?</h3>
			<p>For maximum insecurity, you should steer clear of top-level domains on the <a href="https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security#Solutions_with_preload_list">HSTS preload list.</a> These are hardcoded in browsers to <i>only</i> support HTTP<b><i>S</i></b>. You might think that's fine because browsers old enough to need HTTP won't have the preload list, but that's not entirely true.</p>
			<p>Browsers with the preload list can still be incompatible due to outdated cipher suites. Many browsers support HTTP<b><i>S</i></b> but not <i>modern</i> HTTP<b><i>S</i></b> --- an ever-moving target. Plus, it's more difficult to tell during development if insecure HTTP is working (if you mostly use a modern browser, which you probably should).</p>
			<details>
				<summary>TLDs to avoid</summary>
				<ul>
					<li>.app</li>
					<li>.bank</li>
					<li>.boo</li>
					<li>.channel</li>
					<li>.dad</li>
					<li>.day</li>
					<li>.dev</li>
					<li>.eat</li>
					<li>.esq</li>
					<li>.fire</li>
					<li>.fly</li>
					<li>.foo</li>
					<li>.hangout</li>
					<li>.ing</li>
					<li>.insurance</li>
					<li>.meme</li>
					<li>.mov</li>
					<li>.new</li>
					<li>.nexus</li>
					<li>.office</li>
					<li>.page</li>
					<li>.phd</li>
					<li>.play</li>
					<li>.prof</li>
					<li>.rsvp</li>
					<li>.search</li>
					<li>.zip</li>
					<li>.xn--cckwcxetd (.アマゾン)</li>
					<li>.xn--jlq480n2rg (.亚马逊)</li>
				</ul>
				<p><i>Note that some of these may be reserved for evil corporations or otherwise unavailable for registration. <a href="https://serverfault.com/a/1067232">The preload list is controlled by Google and changes over time.</a></i></p>
			</details>

			<h3>You're using the word "insecure" wrong.</h3>
			<p>You are encouraged to submit websites that lack self-confidence (and also support HTTP).</p>

		</div>
""")
	write_close('', out)
with open("submit/index.html", "w") as out:
	write_head('Submit a Site', out)
	out.write("""\
		<style><!--
			fieldset {
				border: 1px dashed hotpink;
			}
			legend {
				margin: 1em;
				margin-left: 0;
				font-family: sans-serif;
				padding: 0.5em;
				color: white;
				background: purple;
				border: 1px solid purple;
			}
			h3 {
				font-weight: normal;
				padding-top: 0.5em;
			}
			#rules h3:first-of-type {
				margin-top: 0;
				padding-top: 0;
			}
			#rules h3:last-of-type {
				margin-top: 2em;
			}
			#rules > ul {
				margin: 0 1em;
			}
			#rules > ul > li {
				margin-left: 1em;
			}
			#rules h3,
			#rules p {
				padding: 0 1.5em;
			}
			#rules p {
				margin-top: 2em;
			}
			#friendly {
				font-size: 0.9em;
				padding-top: 1em;
			}
			#checker-wrap {
				margin: 0 1.5em;
			}
			iframe {
				width: 100%;
				height: 2em;
			}
			fieldset > ul {
				list-style: none;
				padding: 0;
				margin: 0.25em;
			}
			fieldset > ul > li {
				padding: 0 1em;
			}
			fieldset > ul > li {
				margin-bottom: 0.5em;
			}
			input[name=desc] {
				width: 100%;
			}
			#category {
				list-style: none;
			}
			details,
			summary {
				display: inline;
			}
			#bonus label {
				display: flex;
				gap: 0.5em;
			}
			#bonus input {
				flex: 1;
			}
			#bonus span {
				flex-basis: 40%;
			}
			textarea {
				width: 100%;
			}
			#main input[type=submit] {
				display: block;
				margin-left: auto;
				padding: 0.5em 1em;
				font-size: 1.1em;
				font-weight: bold;
			}
			@media (prefers-color-scheme: dark) {
				#category,
				#category label {
					filter: invert();
				}
				fieldset {
					border-color: purple;
				}
				legend {
					color: black;
					background: hotpink;
					border-color: hotpink;
				}
			}
			@media (max-width: 500px) {
				#bonus label {
					display: inline;
				}
				#main {
					max-width: 100%;
				}
				fieldset {
					padding-left: 0.1em;
					padding-right: 0.1em;
				}
				input[type=text],
				input[type=email],
				input[type=url] {
					width: 100%;
				}
				#main ul,
				#main li,
				input {
					padding: 0;
				}
				#main li {
					margin-left: 1em;
					margin-right: 1em;
				}
				legend {
					margin-left: 0.5em;
				}
			}
		--></style>
""")
	write_nav('submit', out)
	out.write("""\
		<br>
		<form method="post" action="submit.php" id="main">
			<fieldset>
				<legend><span>Rules</span></legend>
				<div id="rules">
					<h3><i>Member sites <b>must:</b></i></h3>
					<ul>
						<li>support plain old unsecured, unencrypted HTTP.</li>
						<li>contain stuff made by a human, at least partially in English, that is
							<details>
								<summary title="click to expand">substantive.</summary>
								<ul>
									<li>A site can be silly and small, but it needs to be a real thing that a real person put real time into.</li>
									<li>As a rule of thumb, blog-style sites should contain at least three entries.</li>
									<li>Sites that consist solely of a r&#233;sum&#233; or list of ways to contact the owner are not eligible.</li>
									<li><a href="https://singleservingsites.cool/">Single-serving sites</a> are generally eligible.</li>
								</ul>
							</details>
						</li>
						<li>be <tt>curl</tt>-able.</li>
					</ul>
					<h3><i>Member sites <b>must <u>not:</u></b></i></h3>
					<ul>
						<li>require JavaScript for basic functionality (<i>eg</i> displaying text), including forcing the visitor to complete a JS-based CAPTCHA or PoW (<i>eg</i> Anubis, Cloudflare).</li>
						<li>discriminate against old user agents.</li>
						<li>espouse fascism, racism, sexism, homophobia, transphobia, or any other form of bigotry or right-wing ideology.</li>
					</ul>
					<h3><i>Site checker:</i></h3>
					<div id="checker-wrap">
						<iframe src="checker/" title="Site HTTP checker" width="300" height="50">Your browser doesn't support iframes. <a href="checker/">Click here to visit the site checker.</a></iframe>
					</div>
					<p id="friendly"><i>If you aren't sure if your site is eligible, that's okay! As long as it passes the <a href="checker/">checker</a>, just submit it.</i></p>
				</div>
			</fieldset>
			<br>
			<fieldset>
				<legend><span>Basics</span></legend>
				<ul id="basics">
					<li><label>URL: &nbsp; <input type="text" name="url" placeholder="insecure.club" required></label></li>
					<li><label>Description (optional): &nbsp; <input type="text" name="desc" maxlength="80" placeholder="A directory of sites that support HTTP sans S"></label></li>
					<li>Category (when in doubt, pick the one further down the list):
						<ul id="category">
							<li style="list-style-image:url('../img/cat/misc.gif')"><label><input type="radio" name="cat" value="misc"> <b>Misc:</b> the categorization system has failed</label></li>
							<li style="list-style-image:url('../img/cat/personal.gif')"><label><input type="radio" name="cat" value="personal" checked> <b>Personal:</b> a homepage, blog, digital garden, or other multi-topic site run by a single person</label></li>
							<li style="list-style-image:url('../img/cat/creative.gif')"><label><input type="radio" name="cat" value="creative"> <b>Creative:</b> a novel, zine, multi-user blog, or other predominantly textual creative work (not necessarily fictional)</label></li>
							<li style="list-style-image:url('../img/cat/informative.gif')"><label><input type="radio" name="cat" value="informative"> <b>Informative:</b> a wiki or other site collecting news or information about a nonfiction subject</label></li>
							<li style="list-style-image:url('../img/cat/technical.gif')"><label><input type="radio" name="cat" value="technical"> <b>Technical:</b> a site predominantly about programming, engineering, hacking, science, etc.</label></li>
							<li style="list-style-image:url('../img/cat/useful.gif')"><label><input type="radio" name="cat" value="useful"> <b>Useful:</b> a service like checking the weather, the homepage of an application, a directory of sites, or another helpful resource</label></li>
							<li style="list-style-image:url('../img/cat/audiovisual.gif')"><label><input type="radio" name="cat" value="audiovisual"> <b>Audiovisual:</b> a site predominantly consisting of photos, videos, or audio</label></li>
							<li style="list-style-image:url('../img/cat/interactive.gif')"><label><input type="radio" name="cat" value="interactive"> <b>Interactive:</b> a site predominantly consisting of games, toys, or experimental art projects that require the user to do something</label></li>
							<li style="list-style-image:url('../img/cat/social.gif')"><label><input type="radio" name="cat" value="social"> <b>Social:</b> a forum, pubnix, imageboard, or other digital community</label></li>
							<li style="list-style-image:url('../img/cat/sexual.gif')"><label><input type="radio" name="cat" value="sexual"> <b>Sexual:</b> a site predominantly consisting of pornography, erotica, or smut</label></li>
							<li style="list-style-image:url('../img/cat/historical.gif')"><label><input type="radio" name="cat" value="historical"> <b>Historical:</b> a site that has been abandoned for a long time</label></li>
						</ul>
					</li>
				</ul>
			</fieldset>
			<br>
			<fieldset>
				<legend><span>Features</span></legend>
				<ul>
					<li><label><input type="checkbox" name="https" checked> Also supports HTTP<b><u>S</u></b></label></li>
					<li><label><input type="checkbox" name="css-opt"> Works well without CSS</label></li>
					<li><label><input type="checkbox" name="libre"> Content is predominantly 
						<details>
							<summary title="click to expand">free culture</summary>
							<ul>
								<li>Public domain: <a href="https://en.wikipedia.org/wiki/Public-domain-equivalent_license">CC0, WTFPL, Unlicense,</a> "dedicated to the public domain", "anti-copyright", etc.</li>
								<li>Creative Commons licenses <b>without</b> NonCommercial (NC) or NoDerivatives (ND) clauses: CC0, CC BY, CC BY-SA</li>
								<li>Anything the FSF considers <a href="http://www.gnu.org/licenses/license-list.html">free</a>:
									<ul>
										<li>GNU FDL and other <a href="http://www.gnu.org/licenses/license-list.html#FreeDocumentationLicenses">free documentation licenses</a></li>
										<li>GPL, AGPL, MIT, and other <a href="http://www.gnu.org/licenses/license-list.html#GPLCompatibleLicenses">free software licenses</a> (GPL compatibility <a href="http://www.gnu.org/licenses/license-list.html#GPLIncompatibleLicenses">not required</a>)</li>
									</ul>
								</li>
							</ul>
						</details>
					</label></li>
				</ul>
			</fieldset>
			<br>
			<fieldset>
				<legend><span>Bonus URLs (optional)</span></legend>
				<ul id="bonus">
					<li><label><span><img alt="Feed URL" src="../img/prot/feed.gif" class="icon invert"> Feed URL: &nbsp; </span><input type="text" name="feed-url" placeholder="insecure.club/feed"></label></li>
					<li><label><span><img alt="Gopher URL" src="../img/prot/gopher.gif" class="icon"> Gopher URL: &nbsp; </span><input type="text" name="gopher-url" placeholder="goph.insecure.club"></label></li>
					<li><label><span><img alt="Gemini URL" src="../img/prot/gemini.gif" class="icon invert"> Gemini URL: &nbsp; </span><input type="text" name="gemini-url" placeholder="gem.insecure.club"></label></li>
					<li>
						<label><span><a href="../buttons/">Button</a> image URL: &nbsp; </span><input type="url" name="button" placeholder="http://insecure.club/buttons/insecure.club.gif"></label>
						<ul><li><details>
							<summary title="click to expand">requirements</summary>
							<ul>
								<li>Format: GIF</li>
								<li>Width: &lt;= 88px</li>
								<li>Height: &lt;= 31px</li>
							</ul>
						</details></li></ul>
					</li>
				</ul>
			</fieldset>
			<br>
			<fieldset>
				<legend><span>Finish</span></legend>
				<ul>
					<li><label>Your email address (optional; for follow-up): &nbsp; <input type="email" name="email" placeholder="submit@insecure.club"></label></li>
					<li>
						<label for="message">Anything else I should know about your submission? Protocols I'm missing? Feedback? (optional)</label>
						<br>
						<textarea name="message" id="message" placeholder="i couldn't select the right option cuz your web design is hot garbage. also my site is on telnet. luv u, bye"></textarea>
					</li>
				</ul>
				<br>
				<input type="submit" value="Submit Site">
			</fieldset>
		</form>
	""")
	write_close('', out)
with open("submit/checker/index.html", "w") as out:
	write_head('Check a site for HTTP support', out)
	out.write("""\
		<style><!--
			html,
			body,
			center,
			form {
				width: 100%;
				margin: 0;
				padding: 0;
			}
			form {
				margin: 0.25em auto;
				max-width: 95%;
				display: flex;
				gap: 0.5em;
				justify-content: space-around;
			}
			#url,
			#sub {
				flex: 1;
			}
			#url {
				flex-basis: 75%;
			}
		--></style>
	</head>
	<body>
		<center>
			<form method="post" action="curl/">
				<input id="url" name="url" type="url" placeholder="http://insecure.club/">
				<input id="sub" type="submit" value="Check">
			</form>
		</center>
	</body>
	</html>
""")
with open("sites.txt", "w") as out:
	for site in sites:
		out.write(f"""http://{site['url']}
""")
with open("feed/feed.atom", "w") as out:
	out.write(f"""\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
	<title>insecure.club</title>
	<id>http://insecure.club/</id>
	<link rel="alternate" href="http://insecure.club/"/>
	<link rel="self" href="http://insecure.club/feed/feed.atom"/>
	<updated>{datetime.datetime.now(datetime.timezone.utc).isoformat()}</updated>
	<author>
		<name>pnppl</name>
	</author>
""")
	for site in sites_new:
		out.write(f"""\
	<entry>
		<title>{site['url']}</title>
		<link rel="alternate" type="text/html" href="http://{site['url']}/"/>
		<id>http://{site['url']}/</id>
		<published>{site['added']}T16:00:00Z</published>
		<updated>{site['added']}T16:00:00Z</updated>
		<summary type="html">{site['cat']}""")
		if 'css-opt' in site and site['css-opt']:
			out.write("; CSS optional")
		if 'libre' in site and site['libre']:
			out.write("; free culture")
		if 'desc' in site:
			out.write(f""": {html.escape(f"<i>{site['desc']}</i>", True)}""")
		out.write("""</summary>
	</entry>
""")
	out.write("""\
</feed>""")


