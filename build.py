import yaml

with open(".sites.yaml", "r") as yam:
	sites = yaml.load(yam, Loader=yaml.SafeLoader)

print("""\
	</head>
	<body>
		<ul>""")

for site in sites:
	cat = '?'
	if 'cat' in sites[site]:
		cat = sites[site]['cat']

	protocols = ''
	if 'ssl' in sites[site] and sites[site]['ssl']:
		protocols += f""" <a href="https://{site}"><img class="icon invert" src="img/https.gif" alt="[HTTPS]"></a>"""
	if 'gopher' in sites[site]:
		protocols += f""" <a href="gopher://{sites[site]['gopher']}"><img class="icon" src="img/gopher.gif" alt="[Gopher]"></a>"""
	if 'gemini' in sites[site]:
		protocols += f""" <a href="gemini://{sites[site]['gemini']}"><img class="icon invert" src="img/gemini.gif" alt="[Gemini]"></a>"""

	print(f"""\
			<li>
				<img alt="{cat}:" class="icon invert" src="img/{cat}.gif" title="Category: {cat}"> <a href="http://{site}">{site}</a>{protocols}""")

	additional = ''
	if 'css-opt' in sites[site] and sites[site]['css-opt']:
		additional += """<b class="css-opt">CSS optional.</b> """
	if 'libre' in sites[site] and sites[site]['libre']:
		additional += """<b class="libre">Free culture!</b> """
	if 'desc' in sites[site] and len(sites[site]['desc']) > 0:
		additional += f"""<i>{sites[site]['desc']}</i>"""
	if len(additional) > 0:
		print(f"""\
				<ul><li>{additional}</li></ul>""")

	print("""\
			</li>""")
print("""\
		</ul>""")
