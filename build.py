def write_head(page, out):
	path = ''
	title = "Insecure Website Club"
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
		<link rel="license" href="">
		<link rel="alternate" href="" title="" type="application/rss+xml">
		-->
		<link rel="alternate" href="{path}sites.yaml" title="YAML source" type="application/yaml">
		<meta property="og:site_name" content="Insecure Website Club">
		<meta property="og:title" content="{title}">
		<meta property="og:description" content="Directory of sites that support HTTP sans S">
		<meta property="og:image" content="">
		<meta property="og:url" content="https://insecure.club/{page}">
		<meta property="og:type" content="website">
		<meta name="description" content="Directory of sites that support HTTP sans S">
		<link rel="stylesheet" href="{path}insecure.css">
		<title>{title}</title>
	</head>
	<body>
		<a id="skip-nav" href="#main">Skip to content</a>
		<center>
			<h1>Insecure Website Club</h1>
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
	print("""&nbsp;]</nav></center>
		<br>""", file=out)

def write_list(sites, page, out):
	path = ''
	if page != 'index':
		path = '../'
	print("""\
		<ul id="main">""",
		file=out)
	old_cat = ''
	for site in sites:
		cat = site['cat']
		if old_cat != cat and page == 'cat':
			print(f"""\
		<h3 id="{cat}">{cat.capitalize()}</h3>""",
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
		<p><i><b>Bold</b> entries work well without CSS.</i></p>""",
		file=out)

# /def

def write_close(out):
	print("""\
	</body>
</html>""",
		file=out)

import yaml

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
	write_close(out)
with open("cat/index.html", "a") as out:
	write_head('Categories', out)
	write_nav('cat', out)
	write_list(sites_by_cat, 'cat', out)
	write_close(out)
with open("new/index.html", "a") as out:
	write_head('Recently Added', out)
	write_nav('new', out)
	write_list(sites_new, 'new', out)
	write_close(out)
with open("has-feed/index.html", "a") as out:
	write_head('Sites with Feeds', out)
	write_nav('has-feed', out)
	write_list(sites_has_feed, 'feed', out)
	write_close(out)
with open("css-opt/index.html", "a") as out:
	write_head('CSS-Optional', out)
	write_nav('css-opt', out)
	write_list(sites_css_opt, 'css-opt', out)
	write_close(out)
with open("libre/index.html", "a") as out:
	write_head('Free Culture', out)
	write_nav('libre', out)
	write_list(sites_libre, 'libre', out)
	write_close(out)
with open("buttons/index.html", "a") as out:
	write_head('Button Wall', out)
	write_nav('buttons', out)
	print('\
		<center>',
		file=out)
	for site in sites_button:
		print(f"""\
		<a href="http://{site['url']}"><img src="{site['button']}.gif" alt="{site['url']}" title="{site['url']}" width="88" height="31"></a>""",
			file=out)
	print('\
		</center>',
		file=out)
	write_close(out)

sites_yaml.close()
