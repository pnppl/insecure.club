def write_head(page, out):
	path = ''
	title = "Insecure Club"
	if page != 'index':
		path = '../'
		title = f"""{page} | {title}"""
	else:
		page = ''
	print(f"""\
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<meta name="referrer" content="no-referrer">
		<meta name="color-scheme" content="light dark">
		<!--
		<meta name="theme-color" content="">
		<link rel="icon" href="">
		-->
		<link rel="license" href="{path}LICENSE.md">
		<link rel="alternate" href="{path}feed/feed.atom" title="Insecure Club URL feed" type="application/atom+xml">
		<link rel="alternate" href="{path}sites.yaml" title="YAML source" type="application/yaml">
		<meta property="og:site_name" content="Insecure Club">
		<meta property="og:title" content="{title}">
		<meta property="og:description" content="Directory of sites that support HTTP sans S">
		<!-- <meta property="og:image" content=""> -->
		<meta property="og:url" content="https://insecure.club/{page}">
		<meta property="og:type" content="website">
		<meta name="description" content="Directory of sites that support HTTP sans S">
		<link rel="stylesheet" href="{path}insecure.css">
		<title>{title}</title>
	</head>
	<body>
		<a id="skip-nav" href="#main">Skip to content</a>
		<center>
			<h1>The Insecure [HTTP] Club</h1>
			<p>A directory of websites that support HTTP <i>sans</i> S.</p>
			<p>Under construction. Maybe you'd like to <b><a href="{path}random">visit a random site</a></b> or <b><a href="{path}submit">submit a new one</a></b>?</p>
			<h2>{page}</h2>
		</center>""",
		file=out)

def write_nav(page, out):
	path = ''
	if len(page) > 0:
		path = '../'
	pages = [
		('', 'alpha'),
		('cat', 'categories'),
		('new', 'new'),
		('buttons', 'buttons'),
		('css-opt', 'CSS-optional'),
		('libre', 'free culture'),
		('has-feed', 'has feed')
	]
	out.write('\
		<center id="nav"><nav>[&nbsp;')
	for entry in pages:
		if entry[0] == page:
			out.write(f"""<span>{entry[1]}</span>""")
		else:
			out.write(f"""<a href="{path}{entry[0]}">{entry[1]}</a>""")
		if entry[0] == 'new':
			out.write(' | ')
		elif entry[0] == 'buttons':
			out.write(' | ')
		elif entry[0] != 'has-feed':
			out.write(' &#183; ')
	print("""&nbsp;]</nav></center>""", file=out)

def write_list(sites, page, out):
	path = ''
	if page != 'index':
		path = '../'
	print("""\
		<div id="main">
			<ul>""",
		file=out)
	old_cat = ''
	for site in sites:
		cat = site['cat']
		if old_cat != cat and page == 'cat':
			print(f"""\
			</ul>
			<h3 id="{cat}">{cat.capitalize()}</h3>
			<ul>""",
			file=out)
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

		print(f"""\
				<li>
					<img alt="{cat}:" class="icon invert" src="{path}img/cat/{cat}.gif" title="Category: {cat}" width="16" height="16"> {link}{protocols}""",
			file=out)

		additional = ''
		if 'libre' in site and site['libre'] and page != 'libre':
			additional += """<b class="libre">Free culture!</b> """
		if 'desc' in site and site['desc']:
			additional += f"""<i class="desc">{site['desc']}</i>"""
		if len(additional) > 0:
			print(f"""\
					<ul><li class="additional">{additional}</li></ul>""",
				file=out)

		print("""\
				</li>""",
			file=out)
	# /for
	print("""\
			</ul>""",
		file=out)
	if page != 'css-opt':
		print("""\
			<p><b>Bold</b> entries work well without CSS.</p>
		</div>""",
		file=out)

# /def

def write_close(page, out):
	path = ''
	if page != 'index':
		path = '../'
	print(f"""\
		<center>
			<p><a href="{path}LICENSE.md">AGPLv3</a> &#183; <a href="https://git.gay/pnppl/insecure.club">source</a> &#183; <a href="mailto:&#105;&#110;&#102;&#111;&#64;&#105;&#110;&#115;&#101;&#99;&#117;&#114;&#101;&#46;&#99;&#108;&#117;&#98;">&#105;&#110;&#102;&#111;&#64;&#105;&#110;&#115;&#101;&#99;&#117;&#114;&#101;&#46;&#99;&#108;&#117;&#98;</a> &#183; <a href="{path}feed/feed.atom">feed</a></p>
			<br>
			<p><i>It's okay to be a little insecure!</i></p>
		</center>
	</body>
</html>""",
		file=out)


# main
import yaml, datetime, html

sites_yaml = open("sites.yaml", "r")
sites = list(yaml.load_all(sites_yaml, Loader=yaml.SafeLoader))
sites.sort(key=lambda s: s['url'].removeprefix('www.'))
sites_by_cat = sorted(sites, key=lambda s: s['cat'])
sites_new = sorted(sites, key=lambda s: s['added'], reverse=True)
sites_has_feed = filter(lambda s: 'feed-url' in s and s['feed-url'], sites)
sites_css_opt = filter(lambda s: 'css-opt' in s and s['css-opt'], sites)
sites_libre = filter(lambda s: 'libre' in s and s['libre'], sites)
sites_button = filter(lambda s: 'button' in s and s['button'], sites)

with open("index.html", "a") as out:
	write_head('index', out)
	write_nav('', out)
	write_list(sites, 'index', out)
	write_close('index', out)
with open("cat/index.html", "a") as out:
	write_head('Categories', out)
	write_nav('cat', out)
	write_list(sites_by_cat, 'cat', out)
	write_close('', out)
with open("new/index.html", "a") as out:
	write_head('Recently Added', out)
	write_nav('new', out)
	write_list(sites_new, 'new', out)
	write_close('', out)
with open("has-feed/index.html", "a") as out:
	write_head('Sites with Feeds', out)
	write_nav('has-feed', out)
	write_list(sites_has_feed, 'feed', out)
	write_close('', out)
with open("css-opt/index.html", "a") as out:
	write_head('CSS-Optional', out)
	write_nav('css-opt', out)
	write_list(sites_css_opt, 'css-opt', out)
	write_close('', out)
with open("libre/index.html", "a") as out:
	write_head('Free Culture', out)
	write_nav('libre', out)
	write_list(sites_libre, 'libre', out)
	write_close('', out)
with open("buttons/index.html", "a") as out:
	write_head('Button Wall', out)
	write_nav('buttons', out)
	print("""\
		<br>
		<center>
			<p>""",
		file=out)
	for site in sites_button:
		print(f"""\
				<a href="http://{site['url']}"><img src="{site['button']}.gif" alt="{site['url']}" title="{site['url']}" width="88" height="31"></a>""",
			file=out)
	print("""\
			</p>
			<br>
			<h3>Clubmember Buttons</h3>
			<p>
				<img alt="animated CRT with nervous face: this site is a little insecure" src="../img/buttons/crt.gif">
				<img alt="static CRT with nervous face: this site is a little insecure" src="../img/buttons/crt-static.gif">
			</p>
		</center>
		<br>""",
		file=out)
	write_close('', out)
with open("sites.txt", "a") as out:
	for site in sites:
		print(f"http://{site['url']}", file=out)
with open("feed/feed.atom", "a") as out:
	print(f"""\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
	<title>Insecure Club</title>
	<id>http://insecure.club/</id>
	<link rel="alternate" href="http://insecure.club/"/>
	<link rel="self" href="http://insecure.club/feed/atom.xml"/>
	<updated>{datetime.datetime.now(datetime.timezone.utc).isoformat()}</updated>
	<author>
		<name>pnppl</name>
	</author>""",
	file=out)
	for site in sites_new:
		out.write(f"""\
	<entry>
		<title>{site['url']}</title>
		<link rel="alternate" type="text/html" href="http://{site['url']}/"/>
		<id>http://{site['url']}/</id>
		<published>{site['added']}T00:00:00Z</published>
		<updated>{site['added']}T00:00:00Z</updated>
		<summary>{site['cat']}""")
		if 'css-opt' in site and site['css-opt']:
			out.write("; CSS optional")
		if 'libre' in site and site['libre']:
			out.write("; free culture")
		if 'desc' in site:
			out.write(f""": {html.escape(f"<i>{site['desc']}</i>", True)}""")
		print("""</summary>
	</entry>""",
		file=out)
	out.write("""\
</feed>""")

sites_yaml.close()
