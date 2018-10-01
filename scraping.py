import csv, time, requests
import pyprind
from bs4 import BeautifulSoup

url_zenhan = "https://filmarks.com/"
page = "?page="
contents = []

#各年代の映画について
#最初のページから、詳細ページのリンクを集める
def urlget(url_toshi):
    r_moto = requests.get(url_toshi)
    soup_moto = BeautifulSoup(r_moto.content, "lxml")
    urls = [ p_movie_cassette__readmore.get('href') \
        for p_movie_cassette__readmore \
        in soup_moto.select(".p-movie-cassette__people__readmore \
        .p-movie-cassette__readmore")]
    return urls

pbar = pyprind.ProgBar(500)

urls = urlget("https://filmarks.com/list/year/1990s/1993")

for url_kohan in urls:
    for i in range(2,27):
        time.sleep(1)
        pbar.update()
        r = requests.get(url_zenhan + url_kohan + page + str(i))
        soup = BeautifulSoup(r.content, "lxml")
        contents += \
            [(p_mark__review.text.encode('cp932', 'ignore').decode('cp932'), \
            c_rating__score.string) \
            for p_mark__review, c_rating__score in \
            zip(soup.select(".p-mark__review"), \
            soup.select(".c-media__content .c-rating__score"))]

with open('data1993', 'wt') as fout:
    csvout = csv.writer(fout)
    csvout.writerows(contents)
