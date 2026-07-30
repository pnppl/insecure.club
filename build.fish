cat sites/* > .sites.yaml &&
cat head.html > index.html &&
python3 build.py >> index.html
