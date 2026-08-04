def write_head(page, out):
	path = ''
	title = "Insecure Website Club"
	if page != 'index':
		path = '../'
		title = f"""{page} | {title}"""
	print(f"""\
<!DOCTYPE html>
<html>
	<head>
		<meta name="color-scheme" content="light dark">
		<link rel="stylesheet" href="{path}insecure.css">
		<title>{title}</title>
	</head>""",
		file=out)


def write_list(sites, page, out):
	path = ''
	if page != 'index':
		path = '../'
	print("""\
	<body>
		<ul>""",
		file=out)
	old_cat = ''
	for site in sites:
		cat = site['cat']
		if old_cat != cat and page == 'by-cat':
			print(f"""\
		<h3 id="{cat}">{cat}</h3>""",
			file=out)
		old_cat = cat

		link = f"""<a href="http://{site['url']}">{site['url']}</a>"""
		if 'css-opt' in site and site['css-opt'] and page != 'css-opt':
			link = f"""<b class="css-opt">{link}</b>"""

		protocols = ''
		if 'ssl' in site and site['ssl']:
			protocols += f""" <a href="https://{site['url']}"><img class="icon invert" src="{path}img/prot/https.gif" alt="[HTTPS]"></a>"""
		if 'gopher_url' in site and site['gopher_url']:
			protocols += f""" <a href="gopher://{site['gopher_url']}"><img class="icon" src="{path}img/prot/gopher.gif" alt="[Gopher]"></a>"""
		if 'gemini_url' in site and site['gemini_url']:
			protocols += f""" <a href="gemini://{site['gemini_url']}"><img class="icon invert" src="{path}img/prot/gemini.gif" alt="[Gemini]"></a>"""

		print(f"""\
			<li>
				<img alt="{cat}:" class="icon invert" src="{path}img/cat/{cat}.gif" title="Category: {cat}"> {link}{protocols}""",
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
# /def

def write_close(out):
	print("""\
	</body>
</html>""",
		file=out)

import yaml

sites_yaml = open("sites.yaml", "r")
sites = list(yaml.load_all(sites_yaml, Loader=yaml.SafeLoader))
sites.sort(key=lambda s: s['url'])
sites_by_cat = sorted(sites, key=lambda s: s['cat'])
sites_css_opt = filter(lambda s: 'css-opt' in s and s['css-opt'], sites)
sites_libre = filter(lambda s: 'libre' in s and s['libre'], sites)
sites_button = filter(lambda s: 'button' in s and s['button'], sites)

with open("index.html", "a") as out:
	write_head('index', out)
	write_list(sites, 'index', out)
	write_close(out)
with open("by-cat/index.html", "a") as out:
	write_head('Categories', out)
	write_list(sites_by_cat, 'by-cat', out)
	write_close(out)
with open("css-opt/index.html", "a") as out:
	write_head('CSS-Optional', out)
	write_list(sites_css_opt, 'css-opt', out)
	write_close(out)
with open("libre/index.html", "a") as out:
	write_head('Free Culture', out)
	write_list(sites_libre, 'libre', out)
	write_close(out)
with open("buttons/index.html", "a") as out:
	write_head('Button Wall', out)
	print("""\
	<body>""", file=out)
	for site in sites_button:
		print(f"""\
		<a href="http://{site['url']}"><img src="{site['button']}.gif" alt="{site['url']}" title="{site['url']}"></a>""",
			file=out)
	write_close(out)

sites_yaml.close()
