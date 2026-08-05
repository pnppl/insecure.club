for file in	index.html \
	{cat,new,has-feed,css-opt,libre,buttons}/index.html \
	sites.txt \
	feed/feed.atom
	echo -n '' > $file
end &&
python3 build.py
