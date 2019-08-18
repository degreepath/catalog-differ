import pathlib
import requests
import glob
import urllib.parse as urlparse
from bs4 import BeautifulSoup


def fetch_all():
    root = "http://catalog.stolaf.edu"
    prefix = "academic-programs"

    for catalog in range(2015, 2020):
        catalog = f"{catalog}-{str(catalog + 1)}"

        folder = pathlib.Path('./') / catalog
        folder.mkdir(exist_ok=True)

        url = root
        if catalog == '2019-2020':
            url = '/'.join([url, prefix])
        else:
            url = '/'.join([url, 'archive', catalog, prefix])

        print(url)

        body = requests.get(url).text
        soup = BeautifulSoup(body, features="html5lib")

        hrefs = set(
            urlparse.urljoin(url, a['href'])
            for a in soup.select('a[href]')
            if '/academic-programs' in a['href']
        )

        for href in hrefs:
            print(href)

            r = requests.get(href)
            name = href.split('/')[-2]

            with (folder / f"{name}.html").open('w', encoding='utf-8') as outfile:
                outfile.write(r.text)


def extract_requirements():
    for filename in glob.iglob('./*-*/*.html'):
        print(filename)

        with open(filename, 'r', encoding='utf-8') as infile:
            data = infile.read()

        soup = BeautifulSoup(data, features='html5lib')

        el = soup.select('#requirementstextcontainer')

        if not el:
            continue

        el = el[0]

        output = el.prettify()

        with open(filename.replace('.html', '.req.html'), 'w', encoding='utf-8') as outfile:
            outfile.write(output)


if __name__ == '__main__':
    # fetch_all()
    extract_requirements()
